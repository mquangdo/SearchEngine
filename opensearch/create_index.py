import json
from pathlib import Path

from opensearch_client import client

INDEX_NAME = "crawled_data_vector"

INFO_FILE = Path("opensearch/embeddings/info.json")


def main():

    with open(INFO_FILE, encoding="utf-8") as f:
        info = json.load(f)

    dimension = info["dimension"]

    print(f"Embedding dimension: {dimension}")

    # Xóa index cũ nếu tồn tại
    if client.indices.exists(index=INDEX_NAME):
        print(f"Delete existing index: {INDEX_NAME}")
        client.indices.delete(index=INDEX_NAME)

    mapping = {
        "settings": {
            "index": {
                "knn": True
            }
        },
        "mappings": {
            "properties": {

                "issue_id": {
                    "type": "keyword"
                },

                "issue_code": {
                    "type": "long"
                },

                "title": {
                    "type": "text"
                },

                "content": {
                    "type": "text"
                },

                "answers": {
                    "type": "text"
                },

                "department": {
                    "type": "keyword"
                },

                "status": {
                    "type": "keyword"
                },

                "sender_type": {
                    "type": "keyword"
                },

                "full_name": {
                    "type": "text"
                },

                "phone": {
                    "type": "keyword"
                },

                "email": {
                    "type": "keyword"
                },

                "rating": {
                    "type": "integer"
                },

                "feedback": {
                    "type": "text"
                },

                "time_feedback": {
                    "type": "date"
                },

                "reply_feedback": {
                    "type": "text"
                },

                "date_reply": {
                    "type": "date"
                },

                "created_time": {
                    "type": "date"
                },

                "last_update_time": {
                    "type": "date"
                },

                "process_log": {
                    "type": "text"
                },

                "embedding": {
                    "type": "knn_vector",
                    "dimension": dimension,
                    "method": {
                        "name": "hnsw",
                        "space_type": "cosinesimil",
                        "engine": "lucene"
                    }
                }
            }
        }
    }

    client.indices.create(
        index=INDEX_NAME,
        body=mapping,
    )

    print(f"\nCreated index: {INDEX_NAME}")


if __name__ == "__main__":
    main()