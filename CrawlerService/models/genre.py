from dataclasses import field

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from . import Base
import uuid
import json
from google.protobuf import wrappers_pb2
from proto import event_pb2

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    goodreads_id = Column(String(255), nullable=False, unique=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()), nullable=False, unique=True)

    books = relationship("Book", secondary="books_genres", back_populates="genres")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "goodreads_id": self.goodreads_id,
            "uuid": self.uuid
        }

    def to_event(self):
        fields = {
            "id": self.id,
            "uuid": self.uuid,
        }

        if self.name:
            fields["name"] = wrappers_pb2.StringValue(value=self.name)
        return event_pb2.Genre(**fields)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)