import json
from pathlib import Path

from elasticsearch.helpers import bulk

from elasticsearch_client import client

# actions = []

# for file in Path("data_processed").glob("*.jsonl"):
#     print(f"Loading {file.name}")

#     with open(file, "r", encoding="utf-8") as f:
#         for line in f:
#             doc = json.loads(line)

#             actions.append({
#                 "_index": "laws",
#                 "_id": doc["id"],
#                 "_source": doc
#             })

# success, failed = bulk(client, actions)

# print(f"Indexed: {success}")
# print(f"Failed: {len(failed)}")

import pandas as pd

INDEX_NAME = 'crawled_data'

mapping = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
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
            "created_time": {
                "type": "date",
                "format": "strict_date_optional_time||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd"
            },
            "last_update_time": {
                "type": "date",
                "format": "strict_date_optional_time||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd"
            },
            "status": {
                "type": "keyword"
            },
            "department": {
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
                "type": "date",
                "format": "strict_date_optional_time||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd"
            },
            "reply_feedback": {
                "type": "text"
            },
            "date_reply": {
                "type": "date",
                "format": "strict_date_optional_time||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd"
            },
            "answers": {
                "type": "text"
            },
            "process_log": {
                "type": "text"
            }
        }
    }
}

if client.indices.exists(index=INDEX_NAME):
    client.indices.delete(index=INDEX_NAME)

client.indices.create(
    index=INDEX_NAME,
    body=mapping
)

print("Index created.")


df = pd.read_csv("data/crawl.csv")      # hoặc pd.read_excel(...)

# Chuyển NaN -> None
import numpy as np

df = df.replace({np.nan: None})

actions = []

for _, row in df.iterrows():

    doc = {
        "_index": INDEX_NAME,
        "_id": row["Issue ID"],
        "_source": {
            "issue_id": row["Issue ID"],
            "issue_code": row["Issue Code"],
            "title": row["Title"],
            "content": row["Content"],
            "created_time": row["Created Time"],
            "last_update_time": row["Last Update Time"],
            "status": row["Status"],
            "department": row["Department"],
            "sender_type": row["Sender Type"],
            "full_name": row["Full Name"],
            "phone": row["Phone"],
            "email": row["Email"],
            "rating": row["Rating"],
            "feedback": row["Feedback"],
            "time_feedback": row["Time Feedback"],
            "reply_feedback": row["Reply Feedback"],
            "date_reply": row["Date Reply"],
            "answers": row["Answers"],
            "process_log": row["Process Log"],
        }
    }

    actions.append(doc)

success, failed = bulk(
    client,
    actions,
    stats_only=True,
)

print(f"Success: {success}")
print(f"Failed: {failed}")

print('=' * 80)
print(f"Indexed {len(actions)} documents.")
