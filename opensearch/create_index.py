from opensearch_client import client

mapping = {
    "mappings": {
        "properties": {
            "content": {
                "type": "text"
            }
        }
    }
}

if not client.indices.exists(index="laws"):
    client.indices.create(index="laws", body=mapping)
    print("Index created.")
else:
    print("Index already exists.")
