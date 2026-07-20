import json
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

CSV_PATH = "data/crawl.csv"
OUTPUT_DIR = "qdrant/embeddings"

MODEL_NAME = "AITeamVN/Vietnamese_Embedding"
BATCH_SIZE = 64

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column names to snake_case.
    Example:
        Issue ID -> issue_id
        Created Time -> created_time
    """
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

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    print("Loading CSV...")

    df = pd.read_csv(CSV_PATH)

    # Chuẩn hóa tên cột
    df = normalize_columns(df)

    # Thay NaN bằng chuỗi rỗng
    df = df.fillna("")

    print(f"Loaded {len(df)} rows")

    print("Building text...")

    df["text"] = df.apply(build_text, axis=1)

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings...")

    embeddings = model.encode(
        df["text"].tolist(),
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    print(f"Embedding shape: {embeddings.shape}")


    np.save(output_dir / "embeddings.npy", embeddings)


    metadata_columns = [
        "issue_id",
        "issue_code",
        "title",
        "content",
        "answers",
        "department",
        "status",
        "sender_type",
        "created_time",
        "last_update_time",
        "rating",
    ]

    df[metadata_columns].to_csv(
        output_dir / "metadata.csv",
        index=False,
        encoding="utf-8-sig",
    )

    info = {
        "model": MODEL_NAME,
        "dimension": embeddings.shape[1],
        "num_vectors": embeddings.shape[0],
        "normalized": True,
    }

    with open(output_dir / "info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)

    print("\nDone!")
    print(f"Embeddings : {output_dir / 'embeddings.npy'}")
    print(f"Metadata   : {output_dir / 'metadata.csv'}")
    print(f"Info       : {output_dir / 'info.json'}")


if __name__ == "__main__":
    main()