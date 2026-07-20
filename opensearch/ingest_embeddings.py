import json
from pathlib import Path

import numpy as np
import pandas as pd
from opensearchpy.helpers import bulk
from tqdm import tqdm

from opensearch_client import client


# ==========================
# Config
# ==========================

INDEX_NAME = "crawled_data_vector"

METADATA_FILE = Path("opensearch/embeddings/metadata.csv")
EMBEDDING_FILE = Path("opensearch/embeddings/embeddings.npy")
INFO_FILE = Path("opensearch/embeddings/info.json")

BATCH_SIZE = 500


# ==========================
# Helpers
# ==========================

def generate_actions(df, embeddings):
    """
    Generate OpenSearch bulk actions.
    """

    for i, row in df.iterrows():

        doc = row.to_dict()

        # Chuyển NaN thành None
        doc = {
            k: (None if pd.isna(v) else v)
            for k, v in doc.items()
        }

        # Thêm vector
        doc["embedding"] = embeddings[i].tolist()

        yield {
            "_index": INDEX_NAME,
            "_id": doc["issue_id"],      # hoặc id nếu dataset của bạn dùng cột id
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


# ==========================
# Main
# ==========================

def main():

    print("Loading metadata...")
    df = pd.read_csv(METADATA_FILE)

    print("Loading embeddings...")
    embeddings = np.load(EMBEDDING_FILE)

    with open(INFO_FILE, encoding="utf-8") as f:
        info = json.load(f)

    print(f"Model      : {info['model']}")
    print(f"Dimension  : {info['dimension']}")
    print(f"Documents  : {len(df)}")

    if len(df) != len(embeddings):
        raise ValueError(
            f"Metadata ({len(df)}) và Embedding ({len(embeddings)}) không khớp."
        )

    success = 0

    actions = generate_actions(df, embeddings)

    for batch in tqdm(
        batched(actions, BATCH_SIZE),
        desc="Indexing"
    ):

        ok, errors = bulk(
            client,
            batch,
            raise_on_error=False,
        )

        success += ok

        print(f"Success: {ok}")
        print(f"Errors : {len(errors)}")

        if errors:
            from pprint import pprint
            pprint(errors[0])
            break

    print(f"\nIndexed {success} documents.")


if __name__ == "__main__":
    main()