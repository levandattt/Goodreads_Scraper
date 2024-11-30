import os

SCHEMA_REGISTRY_CONFIG = {
    'url': os.getenv('SCHEMA_REGISTRY_URL', 'http://localhost:9091'),
}

PRODUCER_CONFIG = {
    'bootstrap.servers': os.getenv('KAFKA_SERVER', 'localhost:9092'),
}