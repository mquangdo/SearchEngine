import json
from pathlib import Path

from opensearchpy.helpers import bulk
from tqdm import tqdm

from opensearch_client import client

INPUT_FILE = Path("data_processed/documents_embedding.jsonl")
INDEX_NAME = "laws_vector"

BATCH_SIZE = 500


def generate_actions(file):
    for line in file:
        doc = json.loads(line)

        yield {
            "_index": INDEX_NAME,
            "_id": doc["id"],
            "_source": doc,
        }


def batched(iterator, batch_size):
    batch = []

    for item in iterator:
        batch.append(item)

        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch


def main():
    success = 0

    with INPUT_FILE.open("r", encoding="utf-8") as f:

        actions = generate_actions(f)

        for batch in tqdm(
            batched(actions, BATCH_SIZE),
            desc="Indexing",
        ):

            ok, _ = bulk(
                client,
                batch,
                raise_on_error=False,
            )

            success += ok

    print(f"\nIndexed {success} documents.")


if __name__ == "__main__":
    main()