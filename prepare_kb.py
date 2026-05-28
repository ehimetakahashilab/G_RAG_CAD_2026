# prepare_kb.py
from __future__ import annotations
import json, os, math
from dataclasses import dataclass, asdict
from typing import List, Dict
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv

EMBED_MODEL = "text-embedding-3-small"  # コスパ良・一般用途向け
KB_PATH = "kb.json"

# .envファイルを読み込んで環境変数にセット
load_dotenv("API.env")

# 環境変数からAPIキーを取得
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)  # OPENAI_API_KEY を環境変数で


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def simple_chunk(text: str, max_chars: int = 1200) -> List[str]:
    # 手軽な文字数分割（必要なら tiktoken でトークン分割に変更）
    chunks, cur = [], []
    n = 0
    for line in text.splitlines(keepends=True):
        n += len(line); cur.append(line)
        if n >= max_chars:
            chunks.append("".join(cur)); cur=[]; n=0
    if cur: chunks.append("".join(cur))
    return chunks

#データの挿入
def embed_texts(texts: List[str]) -> List[List[float]]:
    # バッチで投げてもOK。ここは簡単に逐次で
    vecs = []
    for t in texts:
        resp = client.embeddings.create(model=EMBED_MODEL, input=t)
        vecs.append(resp.data[0].embedding)
    return vecs

@dataclass
class KBItem:
    id: str
    source: str   # "defs_A", "defs_B", "template"
    text: str
    embedding: List[float]

def build_kb(defs_a_path: str, defs_b_path: str, template_path: str, out_path: str = KB_PATH):
    items: List[KBItem] = []
    sources = {
        "defs_A": read_text(defs_a_path),
        "defs_B": read_text(defs_b_path),
        "template": read_text(template_path),
    }
    for source, full in sources.items():
        chunks = simple_chunk(full)
        vecs = embed_texts(chunks)
        for i, (chunk, vec) in enumerate(zip(chunks, vecs)):
            items.append(KBItem(id=f"{source}-{i:03d}", source=source, text=chunk, embedding=vec))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump([asdict(it) for it in items], f, ensure_ascii=False)
    print(f"Saved {len(items)} chunks to {out_path}")

if __name__ == "__main__":
    # ここは手持ちのパスに変更
    build_kb("data/api.txt", "data/api_arg_1.txt", "data/sample1.py")
