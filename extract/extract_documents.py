import fitz  # PyMuPDF
import re
import json


def extract_text(pdf_path: str) -> str:
    """Đọc toàn bộ text từ PDF"""

    doc = fitz.open(pdf_path)

    pages = []

    for page in doc:
        text = page.get_text("text")
        pages.append(text)

    doc.close()

    return "\n".join(pages)


def clean_text(text: str) -> str:
    """Làm sạch cơ bản"""

    # xuống dòng kiểu Windows
    text = text.replace("\r", "")

    # bỏ khoảng trắng cuối dòng
    text = re.sub(r"[ \t]+\n", "\n", text)

    # nhiều dòng trống -> 1 dòng trống
    text = re.sub(r"\n{2,}", "\n\n", text)

    return text.strip()


def split_articles(text: str):
    """
    Tách theo:
        Điều 1.
        Điều 2.
        Điều 35.
    """

    pattern = r"(?=Điều\s+\d+\.)"

    articles = re.split(pattern, text)

    # bỏ phần mở đầu (Chương, tiêu đề...)
    articles = [a.strip() for a in articles if a.strip().startswith("Điều")]

    return articles


def build_documents(articles):
    """Sinh document JSON"""

    documents = []

    for idx, article in enumerate(articles, start=1):

        documents.append({
            "id": idx,
            "content": article
        })

    return documents


def pdf_to_documents(pdf_path):

    text = extract_text(pdf_path)

    text = clean_text(text)

    articles = split_articles(text)

    documents = build_documents(articles)

    return documents


if __name__ == "__main__":

    docs = pdf_to_documents("data/sample.pdf")

    print(f"Total documents: {len(docs)}")

    print(json.dumps(docs[0], ensure_ascii=False, indent=None))
    
    with open("data_processed/documents.jsonl", "w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False))
            f.write("\n")
