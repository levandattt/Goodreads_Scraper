from sqlalchemy import Column, BigInteger, ForeignKey
from . import Base

class BookGenre(Base):
    __tablename__ = 'books_genres'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    book_id = Column(BigInteger, ForeignKey('books.id'), nullable=False)
    genre_id = Column(BigInteger, ForeignKey('genres.id'), nullable=False)
