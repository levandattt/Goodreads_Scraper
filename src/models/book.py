from sqlalchemy import Column, BigInteger, String, Integer, Text
from sqlalchemy.orm import relationship
from . import Base
import uuid
import json
from proto import event_pb2

class Book(Base):
    __tablename__ = 'books'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=True)
    total_pages = Column(Integer, nullable=True)
    published_at = Column(String(255), nullable=True)
    language = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)
    book_link = Column(String(255), nullable=True)
    goodreads_id = Column(String(255), nullable=False, unique=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()), nullable=False, unique=True)

    authors = relationship("Author", secondary="books_authors", back_populates="books",lazy='joined')
    genres = relationship("Genre", secondary="books_genres", back_populates="books", lazy='joined')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "publisher": self.publisher,
            "total_pages": self.total_pages,
            "published_at": self.published_at,
            "language": self.language,
            "description": self.description,
            "image": self.image,
            "book_link": self.book_link,
            "goodreads_id": self.goodreads_id,
            "uuid": self.uuid,
            "authors": self.authors,
            "genres": self.genres
        }

    def to_event(self):
        fields = {
            "id": self.id,
            "uuid": self.uuid,
        }

        if self.title:
            fields["title"] = self.title
        if self.publisher:
            fields["publisher"] = self.publisher
        if self.total_pages:
            fields["total_pages"] = self.total_pages
        if self.published_at:
            fields["published_at"] = self.published_at
        if self.language:
            fields["language"] = self.language
        if self.description:
            # fields["description"] = self.description
            fields["description"] = self.description
        if self.image:
            fields["image"] = self.image
        if self.book_link:
            fields["book_link"] = self.book_link
        if self.authors:
            fields["authors"] = [author.to_event() for author in self.authors]
        if self.genres:
            fields["genres"] = [genre.to_event() for genre in self.genres]
        return event_pb2.AddBookEvent(**fields)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)
