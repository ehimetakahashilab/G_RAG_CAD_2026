from __future__ import annotations
import os, json, re, hashlib, datetime, sys, subprocess, locale
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import shutil
import glob
import hashlib  # _sha12_from_file で使用
from pathlib import Path
import config


from langchain_google_genai import ChatGoogleGenerativeAI

from dataclasses import dataclass, field

ENV_PATH = Path(__file__).with_name("Neo4.env")
load_dotenv(dotenv_path=ENV_PATH, override=True, encoding="utf-8")

#命令分割用のデータクラス
@dataclass
class GenerationStep:
    instruction: str    #1ステップの命令
    expected_count: Optional[int] = None

@dataclass
class GenerationPlan:
    mode: str                                                       #動作モード
    original_instruction: str                                       #もともとの命令
    steps: List[GenerationStep] = field(default_factory=list)       #分割後の命令
    chunk_size: int = 5                                             #1ステップあたりの変更数
    max_iterations: int = 20                                        #ステップ数
    stop_reason: Optional[str] = None                               

@dataclass
class StepResult:
    ok: bool
    output_py: Optional[str] = None
    output_stl: Optional[str] = None
    explanation: str = ""
    stderr: str = ""
    stl_changed: Optional[bool] = None




plane_path=r"data\plane_code.py"
# --- 出力の文字化け対策（Windows cp932 向け） ---
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")



#gemini対応用の追記
def get_llm_provider() -> str:
    """
    gpt / gemini を返す。
    GUI から差し込みやすいように関数化。
    """
    return os.getenv("LLM_PROVIDER", "gpt").strip().lower()

def create_langchain_llm(provider: Optional[str] = None):
    provider = (provider or get_llm_provider()).lower()

    if provider == "gpt":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY が未設定です。")
        return ChatOpenAI(
            model="gpt-5.4",
            temperature=0,
            openai_api_key=api_key,
        )

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY が未設定です。")
        return ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            api_key=api_key,
            temperature=0,
        )

    raise ValueError(f"Unknown provider: {provider}")


# =========================
# デフォルト getter（GUI なしでも動く）
# GUI 側から必要なら上書きする
# =========================
def get_instruction_text() -> str:
    return ""


def get_input_py_path() -> Optional[str]:
    return None


def get_use_previous_base() -> bool:
    return False


def get_mode_hint() -> Optional[str]:
 
 
    return None


def get_minimal_template_path() -> str:
    """
    添付なし生成時に使う最小構成テンプレート
    """
    return "minimal_base.py"


def is_qa_request(instruction: str) -> bool:
    text = (instruction or "").strip().lower()

    qa_keywords = [
        "とは", "何ですか", "使い方", "説明", "help", "ヘルプ",
        "how to", "what is", "what's", "usage", "manual"
    ]
    return any(k in text for k in qa_keywords)


def looks_like_qa_by_rule(instruction: str) -> bool:
    text = (instruction or "").strip().lower()
    qa_keywords = [
        "とは", "何ですか", "使い方", "説明", "教えて",
        "help", "ヘルプ", "usage", "manual"
    ]
    return any(k in text for k in qa_keywords)


def decide_mode(instruction: str, mode_hint=None, llm=None) -> str:
    if mode_hint in {"qa", "generate"}:
        return mode_hint

    # 明確なQAはルールで即決
    if looks_like_qa_by_rule(instruction):
        return "qa"

    # LLM が使えるなら曖昧ケースを分類
    if llm is not None:
        return classify_mode_with_llm(instruction, llm)

    return "generate"


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
_ZEN2HAN_TABLE = str.maketrans({
    "０":"0","１":"1","２":"2","３":"3","４":"4",
    "５":"5","６":"6","７":"7","８":"8","９":"9",
    "（":"(","）":")","［":"[","］":"]","｛":"{","｝":"}",
    "：":":","；":";","、":",","。":".","　":" "
})

def get_enable_stl_compare() -> bool:
    """
    STL 比較を行うかどうか。
    必要なら GUI 側から差し替え可能。
    """
    return False

def normalize_instruction(text: str) -> str:
    """
    - 全角→半角（数字・記号）/ 連続空白畳み
    - 典型的な曖昧語を軽く具体化（最小限）
    """
    t = (text or "").strip()
    t = t.translate(_ZEN2HAN_TABLE)
    t = re.sub(r"\s+", " ", t)

    # 軽い具体化
    t = re.sub(r"四隅", "四隅（各角）", t)
    t = re.sub(r"大きめ|小さめ", "適切なサイズ（必要ならパラメータ化）", t)
    t = re.sub(r"適当に|いい感じに", "明示的な数値や規則に基づいて", t)
    return t

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def _decide_base_in_path() -> Optional[str]:
    """元コード選択ロジックを元の仕様のまま再現"""
    in_path = get_input_py_path()
    if not in_path:
        if get_use_previous_base():
            if os.path.exists("out.py"):
                in_path = "out.py"
        else:
            if os.path.exists("data/sample1.py"):
                in_path = "data/sample1.py"
    return in_path

def _decode_bytes(b: bytes) -> str:
    for enc in ("utf-8", "cp932", locale.getpreferredencoding(False), "mbcs", "latin-1"):
        try:
            return b.decode(enc)
        except Exception:
            pass
    # 最後の保険
    return b.decode("utf-8", errors="replace")

# === 追加: out.pyの退避 ===
def _rotate_out_py_before_write(output_path: str, versions_dir: str = "out_versions") -> Optional[str]:
    if not os.path.exists(output_path):
        return None
    os.makedirs(versions_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    sha = _sha12_from_file(output_path)
    archived = os.path.join(versions_dir, f"out_{ts}_{sha}.py")
    shutil.move(output_path, archived)
    return archived

def _retention_cleanup(versions_dir: str = "out_versions", keep: int = 20):
    files = sorted(
        glob.glob(os.path.join(versions_dir, "out_*.py")),
        key=lambda p: os.path.getmtime(p),
        reverse=True
    )
    for old in files[keep:]:
        try:
            os.remove(old)
        except Exception:
            pass

def _sha12_from_file(py_path: str) -> str:
    with open(py_path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:12]

def _extract_explanation_from_query_stdout(stdout_text: str) -> str:
    """
    実行ログから「スクリプトの説明」だけを抜き出す。
    - "--- Script Explanation ---" 行を起点に、それ以降の本文を次の区切りまで取得
    - 区切り候補: 次の '---' ライン, 次の Markdown 見出し, 'Wrote out.py' など
    - 代替: "### スクリプトの説明" セクション
    """
    if not stdout_text:
        return ""
    # 改行を正規化（Windowsの\r\nを\nへ）
    s = stdout_text.replace("\r\n", "\n").replace("\r", "\n")
    print("log:\n"+s)
    # 1) 英語版ヘッダ（行単位マッチ）
    m = re.search(r"(?im)^[ \t]*---\s*Script\s+Explanation\s*---[ \t]*$", s)
    if m:
        tail = s[m.end():].lstrip()

        # 次の区切り候補を探す
        end_candidates = []
        # 次の '--- something ---' ライン
        m2 = re.search(r"(?im)^[ \t]*---.*?---[ \t]*$", tail)
        if m2: end_candidates.append(m2.start())
        # 次の Markdown 見出し
        m3 = re.search(r"(?m)^\s*#{1,6}\s+", tail)
        if m3: end_candidates.append(m3.start())
        # ランタイム末尾によく出る行
        m4 = re.search(r"(?m)^\s*Wrote\s+out\.py.*$", tail)
        if m4: end_candidates.append(m4.start())

        end = min(end_candidates) if end_candidates else len(tail)
        return tail[:end].strip()

    # 2) 日本語Markdownセクション "### スクリプトの説明"
    m = re.search(r"(?im)^###\s*スクリプトの説明\s*$", s)
    if m:
        tail = s[m.end():].lstrip()
        # 次の見出しまで
        mnext = re.search(r"(?m)^\s*#{1,6}\s+", tail)
        end = mnext.start() if mnext else len(tail)
        return tail[:end].strip()

    # 3) 最後の保険：'Script Explanation' の行を起点に、それ以降を全部
    m = re.search(r"(?im)Script\s+Explanation\s*", s)
    if m:
        return s[m.end():].strip()

    # 4) さらなる保険：'Answer' の行を起点に、それ以降を全部
    m = re.search(r"(?im)Answer\s*", s)
    if m:
        return s[m.end():].strip()

    return ""


def _read_doc_or_header_comment(py_path: str) -> str:
    """
    out.py からモジュールドックストリング or 先頭コメント群を要約として拾う
    """
    import ast
    try:
        with open(py_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        try:
            mod = ast.parse(text)
            doc = ast.get_docstring(mod)
            if doc:
                return doc.strip()
        except Exception:
            pass
        # 先頭コメント
        header_lines = []
        for line in text.splitlines():
            if line.lstrip().startswith("#"):
                header_lines.append(line.lstrip("# ").rstrip())
            elif line.strip() == "":
                if header_lines:
                    header_lines.append("")
            else:
                break
        return "\n".join(header_lines).strip()
    except Exception:
        return ""

def _format_gui_summary(instruction: str, base_for_query: str | None, script_expl: str, output_path: str) -> str:
    mode = "編集" if (base_for_query and os.path.exists(base_for_query)) else "新規"
    base_name = os.path.basename(base_for_query) if (base_for_query and os.path.exists(base_for_query)) else "-"
    parts = [
        "【命令】",
        instruction or "(空)",
        "",
        "【動作形態】",
        f"{mode}" + (f"（基底: {base_name}）" if mode == "編集" else ""),
        "",
        "【スクリプトの説明】",
        script_expl.strip() or "(説明なし)",
    ]
    return "\n".join(parts)

def llm_response_to_text(response) -> str:
    content = getattr(response, "content", response)

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if "text" in item and isinstance(item["text"], str):
                    parts.append(item["text"])
                elif item.get("type") == "text" and isinstance(item.get("text"), str):
                    parts.append(item["text"])
                else:
                    parts.append(str(item))
            else:
                text = getattr(item, "text", None)
                if isinstance(text, str):
                    parts.append(text)
                else:
                    parts.append(str(item))
        return "\n".join(p for p in parts if p).strip()

    return str(content).strip()

"""実装予定-受け取ったコードからstlファイルの生成を行う部分"""
def export_python_to_stl(src_py: str, out_stl: str, work_py: str) -> Dict[str, Any]:
    """
    Python CAD スクリプトに STL export を追記して実行する
    """

    result = {
        "ok": False,
        "src_py": src_py,
        "work_py": work_py,
        "stl_path": None,
        "stdout": "",
        "stderr": "",
        "returncode": None,
        "message": ""
    }

    if not os.path.exists(src_py):
        result["message"] = "source python not found"
        return result

    with open(src_py, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()

    if "Create3DDocument()" not in code:
        result["message"] = "Create3DDocument() not found"
        return result

    snippet = f"""
# ===== Auto STL export =====
try:
    p0pt = doc.CreateSTLOption()
    FileName = r"{os.path.abspath(out_stl)}"
    doc.ExporAsSTL(FileName, p0pt)
    print("[STL_EXPORT] success:", FileName)
except Exception as e:
    print("[STL_EXPORT] failed:", repr(e))
    raise
"""

    merged = code + "\n" + snippet

    os.makedirs(os.path.dirname(work_py), exist_ok=True)
    os.makedirs(os.path.dirname(out_stl), exist_ok=True)

    with open(work_py, "w", encoding="utf-8") as f:
        f.write(merged)

    proc = subprocess.run(
        [sys.executable, work_py],
        capture_output=True,
        text=True
    )

    result["stdout"] = proc.stdout
    result["stderr"] = proc.stderr
    result["returncode"] = proc.returncode

    if proc.returncode != 0:
        result["message"] = "python execution failed"
        return result

    if not os.path.exists(out_stl):
        result["message"] = "stl file not created"
        return result

    result["ok"] = True
    result["stl_path"] = out_stl
    result["message"] = "stl export success"

    return result

#比較w呼び出す部分
def compare_stl(a_stl: str, b_stl: str, out_json: str) -> Dict[str, Any]:

    cmd = [
        sys.executable,
        "compare_stl.py",
        "--a", a_stl,
        "--b", b_stl,
        "--out", out_json
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        return {
            "ok": False,
            "stderr": proc.stderr
        }

    if not os.path.exists(out_json):
        return {"ok": False}

    with open(out_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "ok": True,
        "data": data
    }

#モードの切り替え
def decide_mode(instruction: str, mode_hint: Optional[str] = None) -> str:
    if mode_hint in {"generate", "qa"}:
        return mode_hint

    if is_qa_request(instruction):
        return "qa"

    return "generate"


#曖昧表現の調整
def classify_mode_with_llm(instruction: str, llm) -> str:
    prompt = f"""
次のユーザ要求を次の3つのどれかに分類してください。
- edit: 既存モデル修正
- generate: 新規モデル生成
- qa: 機能説明・質問応答

要求:
{instruction}

カテゴリ名だけ返してください。
"""
    result = llm_response_to_text(llm.invoke(prompt)).lower()

    if result not in {"qa", "generate"}:
        if "qa" in result:
            return "qa"
        return "generate"
    return result


def run_help_qa(question: str, provider: Optional[str] = None) -> str:
    provider = (provider or get_llm_provider()).lower()

    this_dir = os.path.dirname(os.path.abspath(__file__))
    cand = [
        os.path.join(this_dir, "help_qa.py"),
        os.path.join(this_dir, "graphrag-gpt-main", "help_qa.py"),
    ]
    help_script = next((p for p in cand if os.path.exists(p)), None)
    if not help_script:
        raise FileNotFoundError("help_qa.py が見つかりません。")

    cmd = [sys.executable, help_script, question, "--model", provider]
    print("[run_pipeline] exec:", " ".join(repr(x) for x in cmd))

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    proc = subprocess.run(cmd, capture_output=True, text=False, env=env)

    stdout_text = _decode_bytes(proc.stdout).strip()
    stderr_text = _decode_bytes(proc.stderr).strip()

    if proc.returncode != 0:
        raise RuntimeError(stderr_text or stdout_text or "help_qa.py failed")

    return stdout_text or "(回答なし)"

def is_bracket_task_simple(instruction: str) -> bool:
    text = (instruction or "").lower()
    keywords = [
        "bracket",
        "ブラケット",
        "補強金具",
        "l字金具",
        "取付金具",
    ]
    return any(k in text for k in keywords)


def save_session_log(instruction: str, explanation: str, output_path: Optional[str], out_exists: bool):
    log_dir = get_log_dir()
    ensure_dir(log_dir)
    session_file = os.path.join(log_dir, f"session_{datetime.date.today().isoformat()}.jsonl")

    now = datetime.datetime.now().isoformat(timespec="seconds")
    out_hash = "-"
    if output_path and out_exists and os.path.exists(output_path):
        out_hash = sha1(open(output_path, "r", encoding="utf-8").read())

    def save_chatlog(session_path: str, record: Dict[str, Any]):
        with open(session_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    save_chatlog(session_file, {"ts": now, "role": "user", "content": instruction})
    save_chatlog(session_file, {
        "ts": now,
        "role": "assistant",
        "content": explanation,
        "out_file": output_path if (output_path and out_exists) else None,
        "out_hash": out_hash
    })

def decide_pipeline_mode(instruction: str, use_graph: bool = True) -> str:
    """
    query.py の --pipeline-mode を決める
    three/two は専用プロンプト系、one は汎用
    """
    if is_bracket_task_simple(instruction):
        return "three" if use_graph else "two"
    return "off"

def classify_mode_with_llm(instruction: str, llm) -> str:
    prompt = f"""
次のユーザ要求を、以下のどちらか1つに分類してください。

- qa:
  関数説明、機能説明、使い方、仕様質問、概念説明を求めている。
  実際のモデル生成コードや出力ファイルを要求していない。

- generate:
  モデル生成やモデル編集の実行を求めている。
  Pythonコードや出力ファイルを作ることが目的。

例:
- 「ブラケットの生成に関する関数を教えてください」 -> qa
- 「プレートの取り付け方法を教えてください」 -> qa
- 「直方体の生成を行ってください」 -> generate
- 「ブラケットの追加を行ってください」 -> generate

ユーザ要求:
{instruction}

出力は qa か generate のどちらか1語のみ。
"""
    result = llm.invoke(prompt).content.strip().lower()

    if result not in {"qa", "generate"}:
        if "qa" in result:
            return "qa"
        return "generate"
    return result

def run_qa_mode(instruction: str) -> str:
    provider = get_llm_provider()
    explanation = run_help_qa(instruction, provider=provider)
    explanation = f"[QAモード:{provider}]\n\n{explanation}"
    save_session_log(
        instruction=instruction,
        explanation=explanation,
        output_path=None,
        out_exists=False,
    )
    return explanation

def run_generation_mode(instruction: str, output_path: str = "out.py") -> str:
    in_path = _decide_base_in_path() or ""
    enable_stl_compare = get_enable_stl_compare()

    plan = build_generation_plan(
        instruction=instruction,
        chunk_size=5,
        max_iterations=20,
    )

    result = execute_generation_plan(
        plan=plan,
        initial_base_path=in_path,
        output_path=output_path,
        query_retry=5,
        keep_compare=enable_stl_compare,
        
    )

    save_session_log(
        instruction=instruction,
        explanation=result.explanation if result.explanation else result.stderr,
        output_path=output_path,
        out_exists=result.ok and bool(result.output_py and os.path.exists(result.output_py)),
    )

    if result.ok:
        return result.explanation

    return (result.explanation + "\n\n" + result.stderr).strip()

#超簡易的なstl比較
def is_stl_changed(prev_stl: Optional[str], new_stl: Optional[str]) -> bool:

    if not prev_stl or not new_stl:
        return True
    if not (os.path.exists(prev_stl) and os.path.exists(new_stl)):
        return True

    try:
        if os.path.getsize(prev_stl) != os.path.getsize(new_stl):
            return True

        with open(prev_stl, "rb") as f1, open(new_stl, "rb") as f2:
            return f1.read() != f2.read()

    except OSError:
        # 判定不能なら安全側で「変化あり」
        return True

#ルールベースによる命令分析
def parse_requested_count(instruction: str) -> Optional[int]:
    """
    命令から 'N個・N回' のような個数を抽出する。
    """
    m = re.search(r'(\d+)\s*個', instruction)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            return None
    return None

def is_until_fail_request(instruction: str) -> bool:
    """
    'できる限り' 系の命令を検出する
    """
    keywords = [
        "できる限り",
        "可能な限り",
        "最大限",
        "なるべく多く",
    ]
    return any(k in instruction for k in keywords)

def replace_count_instruction(instruction: str, new_count: int) -> str:
    return re.sub(
        r'(\d+)\s*(個|本|枚|つ|箇所)',
        lambda m: f"{new_count}{m.group(2)}",
        instruction,
        count=1
    )


def normalize_unbounded_instruction(instruction: str, chunk_size: int) -> str:
    """
    'できる限り穴を追加してください'
      -> '穴を5個追加してください'

    すでに count 表現がある場合は、その count 部分だけを置換する。
    """
    text = instruction
    for k in ["できる限り", "可能な限り", "最大限", "なるべく多く"]:
        text = text.replace(k, "")

    text = text.strip()

    count_token = extract_count_token(text)
    if count_token:
        return replace_specific_count_text(
            text,
            count_token["text"],
            chunk_size
        )

    if "追加" in text:
        return text.replace("追加", f"{chunk_size}個追加", 1)

    return text



def build_generation_plan(
    instruction: str,
    chunk_size: int = 5,
    max_iterations: int = 20
) -> GenerationPlan:
    """
    命令文から GenerationPlan を作る。
    現段階では rule_analyze_instruction() の結果だけを使う。
    """
    plan = GenerationPlan(
        mode="single",
        original_instruction=instruction,
        chunk_size=chunk_size,
        max_iterations=max_iterations
    )

    # 1. できる限り系
    if is_until_fail_request(instruction):
        step_instruction = normalize_unbounded_instruction(instruction, chunk_size)
        plan.mode = "until_fail"

        for _ in range(max_iterations):
            plan.steps.append(
                GenerationStep(instruction=step_instruction)
            )

        return plan

    # 2. ルール解析
    analysis = rule_analyze_instruction(instruction)

    # 3. 追加個数が明確な場合のみ chunk 分割
    if analysis["chunkable"]:
        count = analysis["quantity_value"]
        replace_target_text = analysis["replace_target_text"]

        if (
            count is not None and
            replace_target_text is not None and
            count > chunk_size
        ):
            plan.mode = "chunked"

            full = count // chunk_size
            rem = count % chunk_size

            for _ in range(full):
                plan.steps.append(
                    GenerationStep(
                        instruction=replace_specific_count_text(
                            instruction,
                            replace_target_text,
                            chunk_size
                        ),
                        expected_count=chunk_size
                    )
                )

            if rem > 0:
                plan.steps.append(
                    GenerationStep(
                        instruction=replace_specific_count_text(
                            instruction,
                            replace_target_text,
                            rem
                        ),
                        expected_count=rem
                    )
                )

            return plan

    # 4. それ以外は単発
    plan.steps.append(
        GenerationStep(instruction=instruction)
    )
    return plan



#生成プランの実行
def execute_generation_plan(
    plan: GenerationPlan,
    initial_base_path: Optional[str],
    output_path: str,
    query_retry: int = 5,
    keep_compare: bool = True,
    provider: Optional[str] = None,
) -> StepResult:
    """
    plan.steps を順に実行する。
    - 各 step の成功結果を次 step の基底にする
    - STL 出力失敗で停止
    - STL が変わらなければ停止
    - 失敗時は直前成功版を採用
    """
    if not plan.steps:
        return StepResult(
            ok=False,
            explanation="",
            stderr="GenerationPlan.steps が空です。"
        )

    current_base = initial_base_path
    last_success: Optional[StepResult] = None
    prev_stl: Optional[str] = None
    steps = plan.steps if plan.mode != "until_fail" else [plan.steps[0]] * plan.max_iterations
    provider = (provider or get_llm_provider()).lower()
    for idx, step in enumerate(steps, start=1):
        print(f"[PLAN] step={idx}, instruction={step.instruction}")
        print(f"[PLAN] current_base={current_base}")
        print(f"[PLAN] current_base_exists={os.path.exists(current_base) if current_base else False}")
        result = run_single_generation_step(
            instruction=step.instruction,
            base_in_path=current_base,
            output_path=output_path,
            query_retry=query_retry,
            provider=provider,
            keep_compare=keep_compare,
        )
        print(f"[PLAN] result.output_py={result.output_py}")
        print(f"[PLAN] result.output_stl={result.output_stl}")

        # 失敗 → 直前成功があればそれを採用して終了
        if not result.ok:
            if last_success is not None:
                stop_msg = (
                    f"\n\n[execute_generation_plan] "
                    f"step {idx} で失敗したため、直前の成功結果を採用しました。"
                )
                last_success.explanation += stop_msg
                return last_success

            return StepResult(
                ok=False,
                explanation=result.explanation,
                stderr=result.stderr or f"step {idx} failed"
            )

        # STL 不変なら停止
        if keep_compare:
            changed = is_stl_changed(prev_stl, result.output_stl)
            result.stl_changed = changed

            if last_success is not None and not changed:
                last_success.explanation += (
                    f"\n\n[execute_generation_plan] step {idx} で STL が変化しなかったため停止しました。"
                )
                return last_success
        else:
            result.stl_changed = None

        # 成功結果を保存
        last_success = result
        current_base = result.output_py
        prev_stl = result.output_stl

    return last_success if last_success is not None else StepResult(
        ok=False,
        explanation="",
        stderr="No successful step."
    )

COUNT_PATTERN = re.compile(r'(\d+)\s*(個|本|枚|つ|箇所)')


def extract_count_token(instruction: str) -> Optional[Dict[str, Any]]:
    """
    命令文から、分割対象となる count 表現を1つ抽出する。
    例:
      '直径100mmの穴を10個追加してください'
      -> {"value": 10, "unit": "個", "text": "10個", "span": (.., ..)}

    現段階では最初に見つかった count 表現のみ対象とする。
    """
    m = COUNT_PATTERN.search(instruction)
    if not m:
        return None

    return {
        "value": int(m.group(1)),
        "unit": m.group(2),
        "text": m.group(0),
        "span": m.span(),
    }


def replace_specific_count_text(
    instruction: str,
    target_text: str,
    new_count: int
) -> str:
    """
    target_text で指定された count 表現だけを new_count に置換する。
    例:
      instruction='直径100mmの穴を10個追加してください'
      target_text='10個'
      new_count=5
      -> '直径100mmの穴を5個追加してください'
    """
    m = re.fullmatch(r'(\d+)\s*(個|本|枚|つ|箇所)', target_text)
    if not m:
        return instruction

    unit = m.group(2)
    new_text = f"{new_count}{unit}"
    return instruction.replace(target_text, new_text, 1)


def rule_analyze_instruction(instruction: str) -> Dict[str, Any]:
    """
    命令文をルールベースで解析する。
    現段階では:
      - 追加系かどうか
      - count 表現があるか
      - 分割候補か
    を見る。
    """
    text = instruction.strip()

    result = {
        "operation_type": "unknown",   # add / modify / delete / replace / unknown
        "quantity_kind": "unknown",    # count / dimension / id / parameter / unknown
        "quantity_value": None,
        "count_unit": None,
        "replace_target_text": None,
        "chunkable": False,
        "target": None,
        "is_confident": False,
    }

    # 1. 操作種別
    if any(k in text for k in ["追加", "配置", "設置", "挿入", "取り付け", "増や"]):
        result["operation_type"] = "add"
    elif any(k in text for k in ["削除", "消", "除去"]):
        result["operation_type"] = "delete"
    elif any(k in text for k in ["置換", "入れ替え", "差し替え"]):
        result["operation_type"] = "replace"
    elif any(k in text for k in ["変更", "修正", "調整"]):
        result["operation_type"] = "modify"

    # 2. count 表現を最優先で見る
    count_token = extract_count_token(text)
    if count_token is not None:
        result["quantity_kind"] = "count"
        result["quantity_value"] = count_token["value"]
        result["count_unit"] = count_token["unit"]
        result["replace_target_text"] = count_token["text"]

    # 3. count がない場合だけ、他の数値っぽい意味をざっくり判定
    if result["quantity_kind"] == "unknown":
        if any(k in text for k in ["長さ", "幅", "高さ", "半径", "直径", "厚さ", "mm", "cm"]):
            result["quantity_kind"] = "dimension"
        elif any(k in text for k in ["部品番号", "パーツ番号", "面番号", "ID"]):
            result["quantity_kind"] = "id"
        elif re.search(r"(部品|パーツ|面)\s*\d+", text):
            result["quantity_kind"] = "id"
        elif any(k in text for k in ["角度", "座標", "オフセット", "x=", "y=", "z="]):
            result["quantity_kind"] = "parameter"

    # 4. 分割可能か
    if result["operation_type"] == "add" and result["quantity_kind"] == "count":
        result["chunkable"] = True
        result["is_confident"] = True

    return result


#llmによる分割判定の曖昧削除
def llm_analyze_instruction(instruction: str, llm) -> dict:
    prompt = f"""
次の CAD 編集命令を、生成計画用に解析してください。

命令:
{instruction}

目的:
- 分割してよいのは「追加個数(count)」だけです
- 寸法(dimension)、識別番号(id)、その他パラメータ(parameter)は分割してはいけません
- 数値が複数ある場合、どれが count かを特定してください

出力ルール:
JSONのみを返してください。
キーは次のものだけを含めてください:

{{
  "operation_type": "add|modify|delete|replace|unknown",
  "chunkable": true,
  "count_value": 10,
  "count_unit": "個",
  "replace_target_text": "10個",
  "numbers": [
    {{"text": "100mm", "value": 100, "kind": "dimension"}},
    {{"text": "10個", "value": 10, "kind": "count"}}
  ],
  "confidence": 0.95
}}

注意:
- 数値ごとに kind を付ける
- kind は count / dimension / id / parameter / unknown のいずれか
- 分割可能なのは operation_type=add かつ count が特定できた場合のみ
- 不明な場合は count_value を null にしてください
"""
    raw = llm.invoke(prompt)

    text = raw.content if hasattr(raw, "content") else str(raw)
    text = text.strip()

    # ```json ... ``` を除去
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        data = json.loads(text)
    except Exception:
        return {
            "operation_type": "unknown",
            "chunkable": False,
            "count_value": None,
            "count_unit": None,
            "replace_target_text": None,
            "numbers": [],
            "confidence": 0.0,
        }

    return data

def analyze_instruction_for_planning(instruction: str, llm=None) -> dict:
    rule_result = rule_analyze_instruction(instruction)

    # ルールで十分明確ならそのまま使う
    if rule_result.get("is_confident"):
        return rule_result

    # LLM がなければ安全側でそのまま返す
    if llm is None:
        return rule_result

    llm_result = llm_analyze_instruction(instruction, llm)

    # 最低限の妥当性チェック
    if (
        llm_result.get("operation_type") == "add" and
        llm_result.get("count_value") is not None and
        llm_result.get("replace_target_text")
    ):
        return llm_result

    return rule_result




#1step生成部
def run_single_generation_step(
    instruction: str,
    base_in_path: Optional[str],
    output_path: str,
    keep_compare: bool = True,
    query_retry: int = 20,
    provider: Optional[str] = None,
) -> StepResult:
    provider = (provider or get_llm_provider()).lower()
    print(base_in_path,output_path)
    new_out_tmp = "success_"+output_path
    base_for_query = base_in_path or ""
    using_out_as_base = (
        base_for_query and os.path.exists(output_path) and
        os.path.abspath(base_for_query) == os.path.abspath(output_path)
    )

    if using_out_as_base:
        tmp_base = output_path + "_base.py"
        shutil.copy2(output_path, tmp_base)
        base_for_query = tmp_base
    else:
        tmp_base = None

    try:
        if not (base_for_query and os.path.exists(base_for_query)):
            base_for_query = plane_path

        this_dir = os.path.dirname(os.path.abspath(__file__))
        cand = [os.path.join(this_dir, "graphrag-gpt-main", "query.py")]
        query_script = next((p for p in cand if os.path.exists(p)), None)
        if not query_script:
            print("query.py_error")
            return StepResult(ok=False, stderr="query.py が見つかりません。")

        cmd = [sys.executable, query_script]
        cmd += [base_for_query, instruction]
        cmd += ["-o", new_out_tmp]

        use_graph = True
        pipeline_mode = decide_pipeline_mode(instruction, use_graph=use_graph)

        cmd += ["--model", provider]
        cmd += ["--max-retries", str(max(1, query_retry))]
        cmd += ["--pipeline-mode", pipeline_mode]
        if use_graph:
            cmd += ["--use-graph"]

        print("[run_pipeline] exec:", " ".join(repr(x) for x in cmd))

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        print(f"[STEP] instruction={instruction}")
        print(f"[STEP] base_in_path(raw)={base_in_path}")
        print(f"[STEP] output_path={output_path}")
        print(f"[STEP] base_for_query(final)={base_for_query}")
        print(f"[STEP] using_out_as_base={using_out_as_base}")
        print(f"[STEP] base_for_query_exists={os.path.exists(base_for_query) if base_for_query else False}")
        proc = subprocess.run(cmd, capture_output=True, text=False, env=env)

        explanation = _decode_bytes(proc.stdout).strip()
        stderr_text = _decode_bytes(proc.stderr).strip()

        # query.py が返した filename を優先
        filename_from_query = None
        m = re.search(r"^__QUERY_RESULT__=(.+)$", explanation, re.MULTILINE)
        if m:
            try:
                query_meta = json.loads(m.group(1))
                filename_from_query = query_meta.get("filename")
            except json.JSONDecodeError:
                filename_from_query = None

        generated_file = filename_from_query if filename_from_query else new_out_tmp
        new_ready = bool(generated_file) and os.path.exists(generated_file)

        if (proc.returncode != 0) or (not new_ready):
            err_msg = []
            err_msg.append("[run_pipeline] query.py 実行に失敗しました。")
            err_msg.append(f"returncode={proc.returncode}")
            err_msg.append(f"generated_file={generated_file!r}")
            if explanation:
                err_msg.append("--- stdout (query.py) ---\n" + explanation)
            if stderr_text:
                err_msg.append("--- stderr (query.py) ---\n" + stderr_text)

            if generated_file and os.path.exists(generated_file):
                os.remove(generated_file)
            
            print("query.py_error2")
            return StepResult(
                ok=False,
                explanation=explanation,
                stderr="\n".join(err_msg)
            )

        # 成功時は output_path に反映
        if os.path.exists(output_path):
            _rotate_out_py_before_write(output_path)
        shutil.move(generated_file, output_path)
        _retention_cleanup("out_versions", keep=20)

        generated_stl = None
        compare_summary = ""

        if keep_compare and base_for_query and os.path.exists(base_for_query):
            reference_stl = "tmp/reference.stl"
            generated_stl = "tmp/generated.stl"

            ref_export = export_python_to_stl(
                src_py=base_for_query,
                out_stl=reference_stl,
                work_py="tmp/reference_export.py"
            )

            gen_export = export_python_to_stl(
                src_py=output_path,
                out_stl=generated_stl,
                work_py="tmp/generated_export.py"
            )

            if ref_export["ok"] and gen_export["ok"]:
                cmp_res = compare_stl(
                    reference_stl,
                    generated_stl,
                    "tmp/compare_result.json"
                )
                if cmp_res["ok"]:
                    d = cmp_res["data"]
                    summary = d.get("summary", {})
                    compare_summary = (
                        "\n\n【STL比較結果】\n"
                        f"common: {summary.get('common_count')}\n"
                        f"added: {summary.get('added_count')}\n"
                        f"removed: {summary.get('removed_count')}\n"
                    )
                else:
                    compare_summary = "\n\n[STL比較失敗]"
            else:
                compare_summary = "\n\n[STL生成失敗]"

        script_expl = _extract_explanation_from_query_stdout(explanation)
        if (not script_expl) and os.path.exists(output_path):
            script_expl = _read_doc_or_header_comment(output_path)

        final_explanation = _format_gui_summary(
            instruction=instruction,
            base_for_query=base_for_query if (base_for_query and os.path.exists(base_for_query)) else None,
            script_expl=script_expl,
            output_path=output_path
        )
        final_explanation += f"\n\n[pipeline_mode] {pipeline_mode}"
        final_explanation += compare_summary
        
        print("true")
        return StepResult(
            ok=True,
            output_py=output_path,
            output_stl=generated_stl,
            explanation=final_explanation,
            stderr=stderr_text,
        )

    finally:
        if tmp_base and os.path.exists(tmp_base):
            os.remove(tmp_base)


def main(output_path: str = "out.py") -> str:
    print("mode:",get_llm_provider())
    raw_instruction = get_instruction_text()
    instruction = normalize_instruction(raw_instruction)

    if not instruction.strip():
        raise ValueError("instruction is empty")

    mode_hint = get_mode_hint()
    mode = decide_mode(instruction, mode_hint=mode_hint)
    print("【動作】", mode)
    if mode == "qa":
        return run_qa_mode(instruction)

    return run_generation_mode(instruction, output_path=output_path)


if __name__ == "__main__":
    print("LLM_PROVIDER env =", os.getenv("LLM_PROVIDER"))
 
