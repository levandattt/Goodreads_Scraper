from bs4 import BeautifulSoup
import requests
import json
from src.services.author_service import AuthorService
from src.services.book_service import BookService
from src.services.genre_service import GenreService
from src.schemas.index import book_schema, genre_schema, author_schema
from src.kafka import kafka_producer
from src.constants import kafka_topic
from src.utils import save_to_file

def get_soup(bookURL):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.209.0 Safari/532.0'}
    status = None
    response = None
    while(status != 200):
        try:
            response = requests.get(bookURL, headers=headers)
            status = response.status_code
        except Exception as e:
            print(e)
            raise e
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

# Lấy thông tin book từ soup
def get_book_details(soup):
    book_dict = book_schema.copy()
    try:
        script_tag = soup.find('script', {'type': 'application/json'}).get_text()
        book_details_raw = json.loads(script_tag)
        apollo_state = book_details_raw.get('props', {}).get('pageProps', {}).get('apolloState', {})

        # get author details
        authors = []
        for key, value in apollo_state.items():
            if key.startswith("Contributor:kca://author/"):
                author = value
                author_url = author.get("webUrl", '')
                # check author url null
                if not author_url:
                    continue

                # check author exist
                author_service = AuthorService()
                existing_author = author_service.find_by_goodreads_id(author_url)

                author_detail = author_scraper(author_url)
                authors.append(author_detail)
        # save author to db
        author_service = AuthorService()
        authors_result = author_service.add_many(authors)
        book_dict['authors'] = authors_result
        for author in authors_result:
            author_event = author.to_event()
            kafka_producer.send(kafka_topic.ADD_AUTHOR_TOPIC, author_event)
        # END GET AUTHOR DETAILS ========================================

        # Get book details
        goodreads_book = None
        for key, value in apollo_state.items():
            if key.startswith("Book:kca://book/"):
                goodreads_book = value
                break

        #START GET GENRE DETAILS -------------------------------------------
        raw_genres = goodreads_book.get("bookGenres", [])
        genres = []
        for genre in raw_genres:
            name = genre.get('genre', {}).get('name')
            goodread_id = genre.get('genre', {}).get('webUrl')
            if(name):
                genre_dict = genre_schema.copy()
                genre_dict['name'] = name
                genre_dict['goodreads_id'] = goodread_id
                genres.append(genre_dict)

        genre_service = GenreService()
        genres_result = genre_service.add_many(genres)
        book_dict['genres'] = genres_result
        for genre in genres_result:
            genre_event = genre.to_event()
            kafka_producer.send(kafka_topic.ADD_GENRE_TOPIC, genre_event)

        #END GET GENRE DETAILS =============================================

        book_dict['link'] = goodreads_book.get("webUrl", '')

        book_dict['title'] = goodreads_book.get("title", '')

        book_dict['authors'] = authors_result

        book_dict['publisher'] = goodreads_book.get("details", {}).get("publisher", '')
        book_dict['totalPages'] = goodreads_book.get("details", {}).get("numPages", 0)
        book_dict['publishedAt'] = goodreads_book.get("details", {}).get("publicationTime", '')
        book_dict['language'] = goodreads_book.get("details", {}).get("language", {}).get("name", '')
        book_dict['description'] = goodreads_book.get("description", '')
        book_dict['image'] = goodreads_book.get("imageUrl", '')
        book_dict['goodreads_id'] = goodreads_book.get("webUrl", '')
        book_service = BookService()
        book_result = book_service.add(book_dict)
        return book_result
    except Exception as e:
        print(f"Error parsing book details: {e}")
        # raise e

def get_books_url_in_page(page_url, page_number):
    try:
        result = []
        rootURL = 'https://www.goodreads.com'
        pageURL = f'{page_url}?page={page_number}'

        page_soup = get_soup(pageURL)

        books = page_soup.find_all('a', {'class': 'bookTitle'})

        for book in books:
            book_url = rootURL + book.get('href','')
            result.append(book_url)
        return result

    except Exception as e:
        print("Error during scraping or saving:", e)
        # raise e

def book_scraper(bookURL):
    try:
        soup = get_soup(bookURL)
        book_details = get_book_details(soup)
        return book_details
    except Exception as e:
        print("Error during scraping or saving:", e)
        # raise e

def author_scraper(authorURL):
    try:
        soup = get_soup(authorURL)
        author_details = get_author_details(soup)
        return author_details
    except Exception as e:
        print("Error during scraping or saving:",   e)
        raise e

def get_author_details(soup):
    author_dict = author_schema.copy()
    try:
        author_dict['name'] = soup.find('h1', class_='authorName').get_text(strip=True)

        birth_date = soup.find('div', class_='dataItem', itemprop='birthDate')
        author_dict['birth_date'] = birth_date.get_text(strip=True) if birth_date else ''

        death_date = soup.find('div', class_='dataItem', itemprop='deathDate')
        author_dict['death_date'] = death_date.get_text(strip=True) if death_date else ''

        birth_place = soup.find('div', class_='dataTitle', string='Born')
        author_dict['birth_place'] = birth_place.next_sibling.get_text(strip=True) if birth_place else ''

        website = soup.find('link', rel='canonical')
        author_dict['website'] = website.get('href','') if website else ''
        author_dict['goodreads_id'] = website.get('href','') if website else ''

        description = soup.find("span", id=lambda value: value and value.startswith("freeTextContainerauthor"))
        author_dict['description'] = description.get_text(strip=True) if description else ''

        image = soup.find('div', class_='leftContainer authorLeftContainer').find('img')
        author_dict['image'] = image.get('src','') if image else ''

        return author_dict
    except Exception as e:
        print(f"Error parsing author details: {e}")
        # raise e
