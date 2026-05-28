# run_pipeline.py
from __future__ import annotations
import os, json, re, hashlib, datetime, sys
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# --- 出力の文字化け対策（Windows cp932 向け） ---
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ==== ここから：元ファイルの “設定値” は維持 ====
def sha1(text: str) -> str:
    import hashlib
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:12]

load_dotenv("API.env")

# --- GUI側で上書きされる想定のダミー取得関数 ---
def get_input_py_path() -> Optional[str]:
    return None

def get_instruction_text() -> str:
    return ""

def get_history() -> List[Dict[str, str]]:
    """形式: [{"role":"user","content":"..."},{"role":"assistant","content":"..."}]"""
    return []

def get_log_dir() -> str:
    return "chatlogs"

def get_use_previous_base() -> bool:
    """
    直近の out.py を基底にするかをGUIから注入。
    デフォルト False（= ドロップが無ければ新規作成）。
    """
    return False

# ==== 追加：曖昧表現の調整（前処理） ====
_ZEN2HAN_TABLE = str.maketrans(
    "０１２３４５６７８９（）［］｛｝：；、。　",
    "0123456789()[][]{}:;,. "
)

def normalize_instruction(text: str) -> str:
    """
    - 全角→半角（数字・記号）/ 連続空白畳み
    - 典型的な曖昧語を軽く具体化（最小限）
    """
    t = (text or "").strip()
    t = t.translate(_ZEN2HAN_TABLE)
    t = re.sub(r"\s+", " ", t)

    # 例: 「右側」→ 「+X方向（右側）」のような補足（必要なら増やせます）
    t = re.sub(r"四隅", "四隅（各角）", t)
    t = re.sub(r"大きめ|小さめ", "適切なサイズ（必要ならパラメータ化）", t)
    t = re.sub(r"適当に|いい感じに", "明示的な数値や規則に基づいて", t)
    return t

# ==== ここから query.py を呼ぶだけにする ====
from query import generate  # ← 検索+生成（当面はquery側で完結）

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def main(output_path: str = "out.py") -> str:
    """
    前処理（曖昧表現の調整）→ query.generate() 呼び出し → out.py 保存
    戻り値: explanation(str)
    """
    # 入力基底の決定
    in_path = get_input_py_path()

    if not in_path:
        if get_use_previous_base():
            if os.path.exists("out.py"):
                in_path = "out.py"
        else:
            if os.path.exists("data/sample1.py"):
                in_path = "data/sample1.py"

    # 指示テキスト（前処理）
    raw_instruction = get_instruction_text()
    instruction = normalize_instruction(raw_instruction)

    # 元コード読み出し
    py_code = None
    if in_path and os.path.exists(in_path):
        with open(in_path, "r", encoding="utf-8") as f:
            py_code = f.read()

    # 履歴（そのまま渡す）
    history_list = get_history() or []

    # === 検索＋生成（query.py 側で実施） ===
    result = generate(instruction=instruction, py_code=py_code, history_list=history_list)

    explanation, code = result["explanation"], result["code"]

    # out.py に保存
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)

    # セッションログ保存（元ファイルのロジックを維持）
    log_dir = get_log_dir()
    ensure_dir(log_dir)
    session_file = os.path.join(log_dir, f"session_{datetime.date.today().isoformat()}.jsonl")

    now = datetime.datetime.now().isoformat(timespec="seconds")
    out_hash = sha1(code)

    def save_chatlog(session_path: str, record: Dict[str, Any]):
        with open(session_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    save_chatlog(session_file, {"ts": now, "role": "user", "content": instruction})
    save_chatlog(session_file, {
        "ts": now, "role": "assistant", "content": explanation,
        "out_file": output_path, "out_hash": out_hash
    })

    print(f"Wrote {output_path}")
    return explanation

if __name__ == "__main__":
    main()
