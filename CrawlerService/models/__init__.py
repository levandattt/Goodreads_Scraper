from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .author import Author
from .book import Book
from .genre import Genre
from .book_author import BookAuthor
from .book_genre import BookGenre