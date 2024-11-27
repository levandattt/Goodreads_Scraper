from services.scraper_service import get_books_url_in_page, book_scraper, author_scraper
import time
from kafka import kafka_producer
from config.database import init_db
from constants import kafka_topic
from services.book_service import BookService


def run():
    try:
        #

        page = 0

        book_service = BookService()

        while page <=100:
            page += 1
            urls = get_books_url_in_page('https://www.goodreads.com/list/show/1.Best_Books_Ever', page)
            # crawl books in page
            for url in urls:
                existing_book =  book_service.find_by_goodreads_id(url)
                if existing_book:
                    continue

                start_time = time.time()

                print('Crawling book:', url)
                book_detail = book_scraper(url)
                print('Saved book:', url)

                book_event = book_detail.to_event()
                kafka_producer.send(kafka_topic.ADD_BOOK_TOPIC, book_event)

                end_time = time.time()
                print(f"Time elapsed: {end_time - start_time}")

    except Exception as e:
        print("Error:", e)
        raise e
if __name__ == '__main__':
    init_db()
    run()