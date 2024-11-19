from sqlalchemy.exc import SQLAlchemyError
from src.models.author import Author
from src.config.database import SessionLocal
from src.kafka import kafka_producer
from src.constants import kafka_topic

class AuthorService:
    def __init__(self):
        self.session = SessionLocal()

    def add(self, author_dict):
        try:
            author = Author(
                goodreads_id=author_dict['goodreads_id'],
            )
            self.session.add(author)
            self.session.commit()
            self.session.refresh(author)
            return author
        except Exception as e:
            self.session.rollback()
            print("Error saving author:", e)
            raise e
        finally:
            self.session.close()

    def find_by_goodreads_id(self, goodreads_id):
        try:
            author = self.session.query(Author).filter(Author.goodreads_id == goodreads_id).first()
            return author
        except Exception as e:
            print("Error finding author by goodreads_id:", e)
            raise e
        finally:
            self.session.close()

    def find_by_goodread_ids(self, ids):
        try:
            authors = self.session.query(Author).filter(Author.goodreads_id.in_(ids)).all()
            return authors
        except Exception as e:
            print("Error finding authors by ids:", e)
            raise e
        finally:
            self.session.close()

    def add_many(self, authors_list):
        new_authors = []
        try:
            author_goodreads_id = [author_dict.get('goodreads_id') for author_dict in authors_list]
            existing_authors = self.find_by_goodread_ids(author_goodreads_id)

            for author_dict in authors_list:
                if (existing_authors):
                    if author_dict['goodreads_id'] in [author.goodreads_id for author in existing_authors]:
                        continue
                new_author = Author(
                    goodreads_id=author_dict.get('goodreads_id',None),
                    name = author_dict.get('name',''),
                    stage_name = author_dict.get('stage_name',None),
                    birth_date = author_dict.get('birth_date',None),
                    death_date = author_dict.get('death_date',None),
                    birth_place = author_dict.get('birth_place',None),
                    nationality= author_dict.get('nationality',None),
                    website = author_dict.get('website',None),
                    description = author_dict.get('description',None),
                    image = author_dict.get('image',None),
                )
                new_authors.append(new_author)


            if new_authors:
                self.session.add_all(new_authors)
                self.session.commit()

            for author in new_authors:
                self.session.refresh(author)
                # author_event = author.to_event()
                # kafka_producer.send(kafka_topic.ADD_AUTHOR_TOPIC, author_event)

            result = existing_authors + new_authors
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            print("Error adding multiple authors:", e)
        finally:
            self.session.close()