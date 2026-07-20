from elasticsearch import Elasticsearch

client = Elasticsearch(
    "http://localhost:9200",
    request_timeout=30,
)

if not client.ping():
    raise RuntimeError("Cannot connect to Elasticsearch")

print("Connected to Elasticsearch")