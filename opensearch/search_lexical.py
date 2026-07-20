from opensearch_client import client

count = client.count(index="crawled_data")

print(count)

result = client.search(
    index="crawled_data",
    body={
        "size": 1,
        "query": {
            "match_all": {}
        }
    }
)

print(result["hits"]["hits"][0]["_source"])