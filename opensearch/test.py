import json
from opensearch_client import client

mapping = client.indices.get_mapping(index="crawled_data_vector")

print(json.dumps(mapping, indent=2))