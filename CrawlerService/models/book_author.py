from sqlalchemy import Column, BigInteger, ForeignKey
from . import Base

class BookAuthor(Base):
    __tablename__ = 'books_authors'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    book_id = Column(BigInteger, ForeignKey('books.id'), nullable=False)
    author_id = Column(BigInteger, ForeignKey('authors.id'), nullable=False)
