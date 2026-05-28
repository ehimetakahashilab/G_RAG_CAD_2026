# Chatbot_interface_test.py
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import threading
import queue
import os
import json
import glob
import datetime
import run_pipeline

# --- グローバル変数 ---
dropped_file_path = None
history = []
use_prev_var = None
result_q = queue.Queue()

OUTPUT_FILE = "out.py"
LOG_DIR = "chatlogs"
MAX_LINES = 800


# =========================
# 共通ユーティリティ
# =========================
def append_log(text: str, clear: bool = False):
    chat_log.config(state="normal")
    if clear:
        chat_log.delete("1.0", "end")
    chat_log.insert("end", text)
    chat_log.see("end")

    # 行数上限
    try:
        lines = int(chat_log.index("end-1c").split(".")[0])
        if lines > MAX_LINES:
            chat_log.delete("1.0", f"{lines - MAX_LINES}.0")
    except Exception:
        pass

    chat_log.config(state="disabled")


def set_selected_file(path: str | None):
    global dropped_file_path
    dropped_file_path = path
    if path:
        file_name = os.path.basename(path)
        selected_file_var.set(file_name)   # 表示はファイル名のみ
        status_label.config(text=f"ファイル受け取り: {file_name}")
    else:
        selected_file_var.set("(未選択)")
        status_label.config(text="準備完了")

def ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def list_session_files():
    ensure_log_dir()
    files = sorted(glob.glob(os.path.join(LOG_DIR, "session_*.jsonl")))
    return files


def load_session_file(path: str):
    global history
    if not os.path.exists(path):
        messagebox.showerror("エラー", f"セッションファイルが見つかりません:\n{path}")
        return

    loaded = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                loaded.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    history = []
    blocks = []
    for rec in loaded:
        role = rec.get("role", "?")
        content = rec.get("content", "")
        ts = rec.get("ts", "")
        if role in ("user", "assistant"):
            history.append({"role": role, "content": content})
            label = "要求" if role == "user" else "応答"
            blocks.append(f"【{label}】 {ts}\n{content}\n\n")

    append_log("".join(blocks) if blocks else "(セッションは空です)\n", clear=True)
    status_label.config(text=f"セッション読込: {os.path.basename(path)}")


def load_latest_session():
    files = list_session_files()
    if files:
        load_session_file(files[-1])


# =========================
# 入力ファイル処理
# =========================
def drop(event):
    path = event.data.strip("{}")
    if os.path.isfile(path) and (path.endswith(".txt") or path.endswith(".py")):
        set_selected_file(path)
    else:
        status_label.config(text="無効なファイル形式です（.txt または .py）")


def choose_file():
    path = filedialog.askopenfilename(
        title="入力ファイルを選択",
        filetypes=[
            ("Python / Text", "*.py *.txt"),
            ("Python", "*.py"),
            ("Text", "*.txt"),
            ("All files", "*.*"),
        ]
    )
    if path:
        set_selected_file(path)


# =========================
# 出力ファイル操作
# =========================
def open_output_file():
    if os.path.exists(OUTPUT_FILE):
        os.startfile(os.path.abspath(OUTPUT_FILE))
    else:
        messagebox.showinfo("確認", f"{OUTPUT_FILE} はまだ存在しません。")


def open_log_folder():
    ensure_log_dir()
    os.startfile(os.path.abspath(LOG_DIR))


def open_selected_session():
    path = filedialog.askopenfilename(
        title="セッションファイルを開く",
        initialdir=os.path.abspath(LOG_DIR),
        filetypes=[("JSONL session", "*.jsonl"), ("All files", "*.*")]
    )
    if path:
        load_session_file(path)


# =========================
# 初期化
# =========================
def reset_function():
    global history
    history = []
    set_selected_file(None)
    entry.delete("1.0", "end")
    append_log("", clear=True)
    status_label.config(text="準備完了")
    
    selected_file_var.set("(未選択)")


# =========================
# 実行
# =========================
def run_function():
    global dropped_file_path 
    instruction_text = entry.get("1.0", "end-1c").strip()
    if not instruction_text:
        status_label.config(text="命令が空です")
        return

    continuous_edit = bool(use_prev_var.get())

    status_label.config(text="実行中…")
    button.config(state="disabled")

    if not continuous_edit:
        append_log("", clear=True)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    append_log(f"\n── 実行開始: {now} ───────────────────────\n")
    append_log(f"【要求】\n{instruction_text}\n\n")
    if dropped_file_path:
        append_log(f"【入力ファイル】\n{os.path.basename(dropped_file_path)}\n\n")

    t = threading.Thread(
        target=_worker_run_pipeline,
        args=(instruction_text, dropped_file_path, continuous_edit),
        daemon=True
    )
    
    dropped_file_path=None
    
    selected_file_var.set("(未選択)")
    t.start()


def _worker_run_pipeline(instruction_text: str, dropped_file_path_local: str | None, use_prev: bool):
    try:
        result_q.put(("progress", "run_pipeline 設定中..."))

        run_pipeline.get_input_py_path = lambda: (
            dropped_file_path_local if (dropped_file_path_local and dropped_file_path_local.endswith(".py")) else None
        )
        run_pipeline.get_instruction_text = lambda: instruction_text
        run_pipeline.get_history = lambda: history[:]   # 空ではなく現在履歴を渡す
        run_pipeline.get_log_dir = lambda: LOG_DIR
        run_pipeline.get_use_previous_base = lambda: bool(use_prev)

        result_q.put(("progress", "生成パイプライン実行中..."))
        summary = run_pipeline.main(output_path=OUTPUT_FILE)

        result_q.put(("progress", "実行結果を整理中..."))
        result_q.put(("ok", summary))

    except Exception as e:
        result_q.put(("err", str(e)))


def _poll_queue():
    global history
    try:
        while True:
            kind, payload = result_q.get_nowait()

            if kind == "progress":
                append_log(f"[進捗] {payload}\n")
                status_label.config(text=payload)

            elif kind == "ok":
                text_to_add = payload or "(説明なし)"
                append_log(f"【応答】\n{text_to_add}\n\n")

                # GUI側の会話履歴にも保持
                last_instruction = entry.get("1.0", "end-1c").strip()
                if last_instruction:
                    history.append({"role": "user", "content": last_instruction})
                history.append({"role": "assistant", "content": text_to_add})

                status_label.config(text="完了")
                button.config(state="normal")

            elif kind == "err":
                append_log(f"[エラー]\n{payload}\n\n")
                status_label.config(text="失敗")
                button.config(state="normal")

    except queue.Empty:
        pass

    root.after(50, _poll_queue)


# =========================
# GUIセットアップ
# =========================
root = TkinterDnD.Tk()
root.title("LLM_スクリプト生成インターフェース")
root.geometry("900x760")

# 命令入力
entry_label = tk.Label(root, text="命令テキスト")
entry_label.pack()
entry = tk.Text(root, width=100, height=8)
entry.pack(pady=5)

# ファイル選択部
file_frame = tk.Frame(root)
file_frame.pack(pady=4)

tk.Button(file_frame, text="ファイル参照", command=choose_file).grid(row=0, column=0, padx=4)
selected_file_var = tk.StringVar(value="(未選択)")
selected_file_label = tk.Label(file_frame, textvariable=selected_file_var, anchor="w", width=80)
selected_file_label.grid(row=0, column=1, padx=4)

# ドロップエリア
drop_area = tk.Label(
    root,
    text="スクリプト生成用 .py/.txt 投入口（ドラッグ＆ドロップ）",
    relief="ridge",
    width=80,
    height=4
)
drop_area.pack(pady=8)
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind("<<Drop>>", drop)

# モード
mode_frame = tk.Frame(root)
mode_frame.pack(pady=3)
use_prev_var = tk.IntVar(value=0)
chk = tk.Checkbutton(
    mode_frame,
    text="継続編集モード（直近の out.py を基底にする）",
    variable=use_prev_var
)
chk.pack()

# 実行・リセット
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

button = tk.Button(btn_frame, text="実行", command=run_function)
button.grid(row=0, column=0, padx=5)

reset = tk.Button(btn_frame, text="リセット", command=reset_function)
reset.grid(row=0, column=1, padx=5)

open_out_btn = tk.Button(btn_frame, text="生成コードを開く", command=open_output_file)
open_out_btn.grid(row=0, column=2, padx=5)

open_logs_btn = tk.Button(btn_frame, text="ログフォルダを開く", command=open_log_folder)
open_logs_btn.grid(row=0, column=3, padx=5)

load_session_btn = tk.Button(btn_frame, text="セッションを開く", command=open_selected_session)
load_session_btn.grid(row=0, column=4, padx=5)

# ステータス
status_label = tk.Label(root, text="準備完了")
status_label.pack(pady=5)

# ログ表示
log_label = tk.Label(root, text="対話ログ")
log_label.pack()
chat_log = tk.Text(root, width=100, height=28)
chat_log.pack(pady=5)
chat_log.config(state="disabled")

# 起動時に最新セッション読込
#load_latest_session()

root.after(50, _poll_queue)
root.mainloop()