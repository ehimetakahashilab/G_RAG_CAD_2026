from __future__ import annotations
import os, json, re, hashlib, datetime, sys, subprocess, locale
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import shutil
import glob
import hashlib  # _sha12_from_file で使用
from pathlib import Path

import os
import sys
import subprocess
from typing import Optional


from dataclasses import dataclass, field

#命令分割用のデータクラス
@dataclass
class GenerationStep:
    instruction: str
    expected_count: Optional[int] = None

@dataclass
class GenerationPlan:
    mode: str
    original_instruction: str
    steps: List[GenerationStep] = field(default_factory=list)
    chunk_size: int = 5
    max_iterations: int = 20
    stop_reason: Optional[str] = None

@dataclass
class StepResult:
    ok: bool
    output_py: Optional[str] = None
    output_stl: Optional[str] = None
    explanation: str = ""
    stderr: str = ""
    stl_changed: Optional[bool] = None




plane_path="data\plane_code.py"
# --- 出力の文字化け対策（Windows cp932 向け） ---
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")




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
    return llm.invoke(prompt).content.strip()


def run_help_qa(question: str) -> str:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    cand = [
        os.path.join(this_dir, "help_qa.py"),
        os.path.join(this_dir, "graphrag-gpt-main", "help_qa.py"),
    ]
    help_script = next((p for p in cand if os.path.exists(p)), None)
    if not help_script:
        raise FileNotFoundError("help_qa.py が見つかりません。")

    cmd = [sys.executable, help_script, question]
    print("[run_pipeline] exec:", " ".join(repr(x) for x in cmd))

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    proc = subprocess.run(cmd, capture_output=True, text=False, env=env)

    stdout_text = _decode_bytes(proc.stdout).strip()
    stderr_text = _decode_bytes(proc.stderr).strip()

    if proc.returncode != 0:
        err_msg = []
        err_msg.append("[run_pipeline] help_qa.py 実行に失敗しました。")
        err_msg.append(f"returncode={proc.returncode}")
        if stdout_text:
            err_msg.append("--- stdout (help_qa.py) ---\n" + stdout_text)
        if stderr_text:
            err_msg.append("--- stderr (help_qa.py) ---\n" + stderr_text)
        raise RuntimeError("\n".join(err_msg))

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
    explanation = run_help_qa(instruction)
    explanation = f"[QAモード]\n\n{explanation}"
    save_session_log(
        instruction=instruction,
        explanation=explanation,
        output_path=None,
        out_exists=False,
    )
    return explanation


def run_generation_mode(instruction: str, output_path: str = "out") -> str:
    """
    生成部本体:
      前処理済み instruction を受けて query.py を実行し、
      out.py 更新、STL生成/比較、ログ保存を行う
    """
    # 元コードパスの決定（未指定時は従来ロジック）
    in_path = _decide_base_in_path() or ""
    new_out_tmp = output_path + "_tmp.py"

    # もし out.py を参照元として使うなら、一時的にコピーを作ってそれを渡す
    base_for_query = in_path
    using_out_as_base = (
        in_path and os.path.exists(output_path) and
        os.path.abspath(in_path) == os.path.abspath(output_path)
    )
    if using_out_as_base:
        tmp_base = output_path + "_base.py"
        shutil.copy2(output_path, tmp_base)
        base_for_query = tmp_base
    else:
        tmp_base = None

    # query スクリプトの場所を自動検出
    this_dir = os.path.dirname(os.path.abspath(__file__))
    cand = [
        os.path.join(this_dir, "graphrag-gpt-main", "query.py")
    ]
    query_script = next((p for p in cand if os.path.exists(p)), None)
    if not query_script:
        raise FileNotFoundError(
            "graphrag-gpt-main/query.py が見つかりません。run_pipeline.py と同じディレクトリに置いてください。"
        )

    cmd = [sys.executable, query_script]

    # 添付なしの場合は最小構成モデルを使う
    if not (base_for_query and os.path.exists(base_for_query)):
        base_for_query = plane_path

    cmd += [base_for_query, instruction]
    cmd += ["-o", new_out_tmp]

    use_graph = True

    pipeline_mode = decide_pipeline_mode(instruction, use_graph=use_graph)

    cmd += ["--max-retries", "5"]
    cmd += ["--pipeline-mode", pipeline_mode]
    if use_graph:
        cmd += ["--use-graph"]

    print("[run_pipeline] exec:", " ".join(repr(x) for x in cmd))

    # 子プロセス側の標準出力文字化けを抑制
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # バイナリで取得して手動デコード（混在対策）
    proc = subprocess.run(cmd, capture_output=True, text=False, env=env)

    explanation = _decode_bytes(proc.stdout).strip()
    stderr_text = _decode_bytes(proc.stderr).strip()

    # ===== query.py から filename を抽出 =====
    filename_from_query = None
    query_meta = None

    m = re.search(r"^__QUERY_RESULT__=(.+)$", explanation, re.MULTILINE)
    if m:
        try:
            query_meta = json.loads(m.group(1))
            filename_from_query = query_meta.get("filename")
        except json.JSONDecodeError:
            filename_from_query = None
    print("#",explanation)

    print("$",stderr_text)
    # query.py が返した filename を優先、無ければ従来の new_out_tmp を使う
    generated_file = filename_from_query if filename_from_query else new_out_tmp
    print("------------------\n")
    print(f"[run_pipeline] filename_from_query = {filename_from_query!r}")
    print(f"[run_pipeline] generated_file = {generated_file!r}")
    print("------------------\n")

    new_ready = bool(generated_file) and os.path.exists(generated_file)
    compare_summary = ""

    if (proc.returncode != 0) or (not new_ready):
        # 失敗：何も壊さない（out.py はそのまま）
        err_msg = []
        err_msg.append("[run_pipeline] query.py 実行に失敗しました。")
        err_msg.append(f"returncode={proc.returncode}")
        err_msg.append(f"generated_file={generated_file!r}")
        if explanation:
            err_msg.append("--- stdout (query.py) ---\n" + explanation)
        if stderr_text:
            err_msg.append("--- stderr (query.py) ---\n" + stderr_text)
        msg = "\n".join(err_msg)
        print(msg)
        explanation = (explanation + ("\n\n" + msg if msg else "")).strip()

        if generated_file and os.path.exists(generated_file):
            os.remove(generated_file)
        if tmp_base and os.path.exists(tmp_base):
            os.remove(tmp_base)

        out_exists = os.path.exists(output_path)

    else:
        # 成功：旧 out.py をアーカイブ → 新規を out.py へ差し替え
        if os.path.exists(output_path):
            _rotate_out_py_before_write(output_path)
        shutil.move(generated_file, output_path)
        _retention_cleanup("out_versions", keep=20)
        out_exists = True

        # ===== STL生成 =====
        if base_for_query and os.path.exists(base_for_query):
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

        if tmp_base and os.path.exists(tmp_base):
            os.remove(tmp_base)

    # GUI向け説明整形
    explanation_raw = explanation
    script_expl = _extract_explanation_from_query_stdout(explanation_raw)
    if (not script_expl) and os.path.exists(output_path):
        script_expl = _read_doc_or_header_comment(output_path)

    explanation = _format_gui_summary(
        instruction=instruction,
        base_for_query=base_for_query if (base_for_query and os.path.exists(base_for_query)) else None,
        script_expl=script_expl,
        output_path=output_path
    )
    explanation += f"\n\n[pipeline_mode] {pipeline_mode}"
    explanation += compare_summary

    save_session_log(
        instruction=instruction,
        explanation=explanation,
        output_path=output_path,
        out_exists=out_exists,
    )

    if out_exists:
        print(f"Wrote {output_path}")
    return explanation


def main(output_path: str = "out.py") -> str:

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
    main()
