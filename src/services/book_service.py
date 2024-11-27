from models import Author, Genre
from models.book import Book
from config.database import SessionLocal
class BookService:
    def __init__(self):
        self.session = SessionLocal()

    def add(self, book_dict):
        try:
            book = Book(
                title=book_dict['title'],
                publisher=book_dict['publisher'],
                total_pages=book_dict['total_pages'],
                published_at=book_dict['published_at'],
                language=book_dict['language'],
                description=book_dict['description'],
                image=book_dict['image'],
                book_link=book_dict['book_link'],
                goodreads_id = book_dict['goodreads_id'],
                genres = book_dict['genres'],
                authors = book_dict['authors'],
            )

            existing_book = self.session.query(Book).filter(Book.goodreads_id == book.goodreads_id)
            if existing_book.first() is None:
                self.session.add(book)
                self.session.commit()
                self.session.refresh(book)
            else:
                update_book = existing_book.first()
                author_ids = [author.id for author in book.authors]
                authors = self.session.query(Author).filter(Author.id.in_(author_ids)).all()
                genre_ids = [genre.id for genre in book.genres]
                genres = self.session.query(Genre).filter(Genre.id.in_(genre_ids)).all()
                update_book.genres = genres
                update_book.authors = authors
                self.session.commit()
                self.session.refresh(update_book)
                return update_book
            return book
        except Exception as e:
            self.session.rollback()
            print("Error saving book:", e)
            # raise e
        finally:
            self.session.close()

    def find_by_goodreads_id(self, goodreads_id):
        try:
            book = self.session.query(Book).filter(Book.goodreads_id == goodreads_id).first()
            return book
        except Exception as e:
            print("Error finding book by goodreads_id:", e)
        finally:
            self.session.close()