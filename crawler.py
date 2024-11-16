from proto import event_pb2


# Create an instance of AddBookEvent
new_event = event_pb2.AddBookEvent(
    id=1,
    title="The Great Gatsby",
    published_at=1925,
    publisher="Charles Scribner's Sons",
    total_pages=218,
    language="English",
    description="A classic novel by F. Scott Fitzgerald.",
    image="https://example.com/image.png",
    uuid="123e4567-e89b-12d3-a456-426614174000",
    old_title="Gatsby"
)

print(new_event)