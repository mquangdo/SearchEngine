import json
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

CSV_PATH = "data/crawl.csv"
OUTPUT_DIR = Path("opensearch/embeddings")

MODEL_NAME = "BAAI/bge-m3"
BATCH_SIZE = 64


def normalize_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df


def build_text(row):
    parts = []

    if row["title"]:
        parts.append(f"Tiêu đề:\n{row['title']}")

    if row["content"]:
        parts.append(f"Nội dung:\n{row['content']}")

    if row["answers"]:
        parts.append(f"Trả lời:\n{row['answers']}")

    return "\n\n".join(parts)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(CSV_PATH)
    df = normalize_columns(df)
    df = df.fillna("")

    df["text"] = df.apply(build_text, axis=1)

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        df["text"].tolist(),
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    np.save(OUTPUT_DIR / "embeddings.npy", embeddings)

    metadata = df.drop(columns=["text"])

    
    metadata.to_csv(
        OUTPUT_DIR / "metadata.csv",
        index=False,
        encoding="utf-8-sig",
    )

    info = {
        "model": MODEL_NAME,
        "dimension": embeddings.shape[1],
        "num_vectors": len(df),
    }

    with open(OUTPUT_DIR / "info.json", "w") as f:
        json.dump(info, f, indent=4)


if __name__ == "__main__":
    main()