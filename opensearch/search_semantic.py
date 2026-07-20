from sentence_transformers import SentenceTransformer

from opensearch_client import client

model = SentenceTransformer(
    "AITeamVN/Vietnamese_Embedding"
)

query = "Việc xác định đất vườn, ao gắn liền với đất ở theo điểm c khoản 2 Điều 10 Nghị quyết số 254/2025/QH15"

query_embedding = model.encode(
    query,
    normalize_embeddings=True
).tolist()


print('=' * 80)

response = client.search(
    index="crawled_data_vector",
    body={
        "size": 1,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_embedding,
                    "k": 1
                }
            }
        }
    }
)

print("Query:", query)
print("=" * 80)

for hit in response["hits"]["hits"]:
    print(f"Score: {hit['_score']:.4f}")
    print(hit["_source"]["content"])
    print("-" * 80)