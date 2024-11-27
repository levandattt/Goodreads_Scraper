from multiprocessing.connection import deliver_challenge
from uuid import uuid4

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField

from src.config import kafka_config
from confluent_kafka import Producer
from proto import event_pb2
from google.protobuf.message import Message  # Base class for Protobuf messages
from src.constants import kafka_topic
from src.models import Genre, Author
from src.schemas.index import genre_schema

def get_serializer(topic):
    schema_registry_client = SchemaRegistryClient(kafka_config.SCHEMA_REGISTRY_CONFIG)

    match topic:
        case kafka_topic.ADD_BOOK_TOPIC:
            return ProtobufSerializer(event_pb2.AddBookEvent, schema_registry_client, {'use.deprecated.format': False})
        case kafka_topic.ADD_AUTHOR_TOPIC:
            return ProtobufSerializer(event_pb2.Author, schema_registry_client, {'use.deprecated.format': False})
        case kafka_topic.ADD_GENRE_TOPIC:
            return ProtobufSerializer(event_pb2.Genre, schema_registry_client, {'use.deprecated.format': False})
        case _:
            # raise ValueError(f"No serializer found for topic: {topic}")
            print(f"No serializer found for topic: {topic}")


def send(topic , event):
    try:
        schema_registry_client = SchemaRegistryClient(kafka_config.SCHEMA_REGISTRY_CONFIG)
        protobuf_serializer = get_serializer(topic)

        producer = Producer(kafka_config.PRODUCER_CONFIG)
        # Serve on_delivery callbacks from previous calls to produce()
        producer.poll(0.0)

        try:
            string_serializer = StringSerializer('utf8')
            producer.produce(topic=topic, partition=0,
                             key=string_serializer(str(uuid4())),
                             value=protobuf_serializer(event, SerializationContext(topic, MessageField.VALUE)),
                             on_delivery=delivery_report)
        except ValueError:
            # raise ValueError
            print("Invalid input, discarding record...")
        producer.flush()
    except Exception as e:
        print(f"Error sending message to Kafka: {e}")
        # raise e

def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    # print('User record {} successfully produced to {} [{}] at offset {}'.format(
    #     msg.key(), msg.topic(), msg.partition(), msg.offset()))

if __name__ == '__main__':
    genre = Genre(id=1, uuid=str(uuid4()), name="Fantasy")
    genre_event = genre.to_event()
    send(kafka_topic.ADD_GENRE_TOPIC, genre_event)

    author = Author(id=1, uuid=str(uuid4()), name="J.K. Rowling")
    author_event = author.to_event()
    send(kafka_topic.ADD_AUTHOR_TOPIC, author_event)

