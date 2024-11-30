from sqlalchemy import Column, BigInteger, String, Text
from sqlalchemy.orm import relationship
from . import Base
import uuid
import json
from google.protobuf import wrappers_pb2
from proto import event_pb2
from utils import time_convert



class Author(Base):
    __tablename__ = 'authors'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    stage_name = Column(String(255), nullable=True)
    birth_date = Column(String(255), nullable=True)
    death_date = Column(String(255), nullable=True)
    birth_place = Column(String(255), nullable=True)
    nationality = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    image = Column(String(255), nullable=False)
    goodreads_id = Column(String(100), nullable=False, unique=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()), nullable=False, unique=True)

    books = relationship("Book", secondary="books_authors", back_populates="authors")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "stage_name": self.stage_name,
            "birth_date": self.birth_date,
            "death_date": self.death_date,
            "birth_place": self.birth_place,
            "nationality": self.nationality,
            "website": self.website,
            "description": self.description,
            "image": self.image,
            "goodreads_id": self.goodreads_id,
            "uuid": self.uuid
        }

    def to_event(self):
        fields = {
            "id": self.id,
            "uuid": self.uuid,
        }

        if self.name:
            fields["name"] = self.name
        if self.stage_name:
            fields["stage_name"] = wrappers_pb2.StringValue(value=self.stage_name)
        if self.birth_date:
            fields["birth_date"] = wrappers_pb2.StringValue(value=time_convert.bdy_to_ymd(self.birth_date))
        if self.death_date:
            fields["death_date"] = wrappers_pb2.StringValue(value=time_convert.bdy_to_ymd(self.death_date))
        if self.birth_place:
            fields["birth_place"] = wrappers_pb2.StringValue(value=self.birth_place)
        if self.nationality:
            fields["nationality"] = wrappers_pb2.StringValue(value=self.nationality)
        if self.website:
            fields["website"] = wrappers_pb2.StringValue(value=self.website)
        if self.description:
            # fields["description"] = wrappers_pb2.StringValue(value=self.description)
            fields["description"] = wrappers_pb2.StringValue(value=self.description)
        if self.image:
            fields["image"] = wrappers_pb2.StringValue(value=self.image)

        return event_pb2.Author(**fields)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)

