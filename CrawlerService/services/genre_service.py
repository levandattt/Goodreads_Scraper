from sqlalchemy.exc import SQLAlchemyError

from models.genre import Genre
from config.database import SessionLocal
from kafka import kafka_producer
from constants import kafka_topic

class GenreService:
    def __init__(self):
        self.session = SessionLocal()

    def add(self, genre_dict):
        try:
            genre = Genre(
                goodreads_id=genre_dict['id']
            )
            self.session.add(genre)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print("Error saving genre:", e)
        finally:
            self.session.close()

    def find_by_goodreads_id(self, goodreads_id):
        try:
            genre = self.session.query(Genre).filter(Genre.goodreads_id == goodreads_id).first()
            return genre
        except Exception as e:
            print("Error finding genre by goodreads_id:", e)
        finally:
            self.session.close()

    def find_by_ids(self, ids):
        try:
            genres = self.session.query(Genre).filter(Genre.goodreads_id.in_(ids)).all()
            return genres
        except Exception as e:
            print("Error finding genres by ids:", e)
        finally:
            self.session.close()


    def add_many(self, genres_list):
        new_genres = []
        try:
            genre_goodreads_id = [genre_dict.get('goodreads_id') for genre_dict in genres_list]
            existing_genres = self.find_by_ids(genre_goodreads_id)

            for genre_dict in genres_list:
                if(existing_genres):
                    if genre_dict['goodreads_id'] in [genre.goodreads_id for genre in existing_genres]:
                        continue
                new_genre = Genre(
                    goodreads_id=genre_dict.get('goodreads_id'),
                    name = genre_dict.get('name', None)
                )
                new_genres.append(new_genre)
            if new_genres:
                self.session.add_all(new_genres)
                self.session.commit()
                # print(f"Added {len(new_genres)} new genres.")
            # else:
                # print("No new genres to add.")
            # print("All genres added.")
            for genre in new_genres:
                self.session.refresh(genre)
                # genre_event = genre.to_event()
                # kafka_producer.send(kafka_topic.ADD_GENRE_TOPIC, genre_event)

            result = existing_genres + new_genres
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            print("Error adding multiple genres:", e)
        finally:
            self.session.close()


