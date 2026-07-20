from sentence_transformers import SentenceTransformer

from opensearch_client import client

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

query = "Chức năng của quốc hội là gì?"

query_embedding = model.encode(
    query,
    normalize_embeddings=True
).tolist()

response = client.search(
    index="laws_vector",
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

print("=" * 80)

print("Query:", query)

for hit in response["hits"]["hits"]:
    print(f"Score: {hit['_score']:.4f}")
    print(hit["_source"]["content"])
    print("-" * 80)