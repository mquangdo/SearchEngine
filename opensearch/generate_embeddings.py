import json

from opensearchpy.helpers import bulk

from opensearch_client import client

actions = []

with open("data_processed/documents_embedding.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        doc = json.loads(line)

        actions.append({
            "_index": "laws_vector",
            "_id": doc["id"],
            "_source": doc
        })

success, failed = bulk(client, actions)

print(f"Indexed: {success}")
print(f"Failed: {failed}")