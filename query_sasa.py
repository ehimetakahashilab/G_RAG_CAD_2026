"""
使い方:
[モード1: 新規スクリプト生成]
    python query.py "<質問文>" vector     # ベクトル検索で新規作成
    python query.py "<質問文>" hybrid     # ベクトル + グラフ

[モード2: 既存スクリプト編集]
    python query.py <ファイルパス> "<編集指示>" vector
    python query.py <ファイルパス> "<編集指示>" graph
    python query.py ./board.py "板の四隅に直方体の柱を追加してください。" hybrid

[デフォルトの動作]
- ルートを省略した場合は 'graph' が採用されます。
    例: python query.py "<質問文>"
    例: python query.py <ファイルパス> "<編集指示>"
"""
import sys, os, re, json, textwrap, config


# LCEL / OpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# Vector store (community)
from langchain.vectorstores import Chroma

# Neo4j graph (community)
from neo4j import GraphDatabase

# ========= 共通 LLM =========
# ※ 安定モデル名に変更（必要なら環境に合わせて変更可）
llm = ChatOpenAI(
    model="gpt-5",
    temperature=0,
    # openai パッケージ 1.x は環境変数 OPENAI_API_KEY / OPENAI_BASE_URL も自動参照
    # ここで config.OPENAI_API_KEY を渡してもOK（どちらか片方で十分）
)

# ========= Vector QA (LCEL) =========
emb = OpenAIEmbeddings(model="text-embedding-3-small")
vectordb = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=emb,
)


# Neo4jGraph クラスを定義して接続
class Neo4jGraph:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def query(self, cypher):
        with self.driver.session() as session:
            result = session.run(cypher)
            return [record for record in result]

    def schema(self):
        # Neo4j スキーマの取得方法（スキーマ情報を適宜取得する方法を実装）
        return "スキーマ情報を取得するメソッド"


def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)




QA_TEMPLATE = """
あなたは、CADアプリケーション「EvoShip」をPythonで操作するエキスパートです。
あなたのタスクは、ユーザーの要求とナレッジグラフから取得した情報を基に、単一の完成された実行可能なPythonスクリプトと、そのスクリプトに関する説明を生成することです。

ユーザーの要求:
{question}

ナレッジグラフから取得した関連情報:
{context}

上記の情報を基に、以下の要件と出力形式に従って回答を生成してください。

## スクリプト生成の要件
- **ユーザーの要求に「元のスクリプト」が含まれる場合は、それを基に編集・修正を行ってください。**
- **「元のスクリプト」が含まれない場合は、ゼロから新しいスクリプトを作成してください。**
- 新規作成の場合は、常に `import win32com.client` から始めること。
- 新規作成の場合は、アプリケーションを起動する定型コード `evoship = win32com.client.DispatchEx("EvoShip.Application")` を含めること。
- 新規作成の場合は、ドキュメントとパートを作成するコード `doc = evoship.Create3DDocument()` と `part = doc.GetPart()` を含めること。
- メソッドの返り値は、後続のメソッドで利用するために変数に格納すること。
- 複数のAPI呼び出しがある場合、それらを論理的な順序で構成すること。
- 取得した情報から最も適切と考えられる単一のスクリプトを作成すること。
- ナレッジグラフからの情報にサンプルコードが含まれている場合は、それを最優先で参考にし、必要に応じて質問内容に合わせて修正してください。

## 出力形式
以下のマークダウン形式で回答してください。コードや説明以外の余計な文章は含めないでください。

## 生成されたスクリリプト
```python
# ここにPythonスクリプトを記述
````

### スクリプトの説明

ここに、生成したスクリプトが何をするものか、使用されている主要なAPIの目的、そしてユーザーが注意すべき点などを簡潔に解説してください。
"""
QA_PROMPT = PromptTemplate(
input_variables=["context", "question"], template=QA_TEMPLATE
)

vector_chain = (
{
"context": vectordb.as_retriever() | RunnableLambda(_format_docs),
"question": RunnablePassthrough(),
}
| QA_PROMPT
| llm
| StrOutputParser()
)

NEO4J_URI = getattr(config, "NEO4J_URI", None) or os.getenv("NEO4J_URI")
NEO4J_USERNAME = getattr(config, "NEO4J_USER", None) or os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = getattr(config, "NEO4J_PASSWORD", None) or os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = getattr(config, "NEO4J_DATABASE", None) or os.getenv("NEO4J_DATABASE") or "neo4j"

graph = Neo4jGraph(
url=NEO4J_URI,
username=NEO4J_USERNAME,
password=NEO4J_PASSWORD,
database=NEO4J_DATABASE,
)

CYPHER_GENERATION_TEMPLATE_JP = """
あなたは、CADアプリケーション「EvoShip」のAPIに関する知識グラフを熟知したエキスパートです。
次のスキーマに厳密に従って、質問に答えるための最適な Cypher クエリを1本だけ生成してください。
前置きや説明文は一切不要で、Cypher クエリのみを出力してください。

スキーマ

{schema}

ルール

スキーマに存在しないラベル/プロパティ/リレーションは使用禁止

文字列検索は toLower() + CONTAINS を活用

質問に答えるために必要な項目（名前、説明、引数、サンプルコード 等）を十分に含む RETURN を構成

質問: {question}
"""
CYPHER_PROMPT = PromptTemplate(
input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE_JP
)

def run_graph_qa(question: str) -> str:
    # 1) スキーマ取得
    schema_text = graph.schema


    # 2) Cypher 生成（出力はクエリ文字列のみを期待）
    cypher = (CYPHER_PROMPT | llm | StrOutputParser()).invoke(
        {"schema": schema_text, "question": question}
    )

    # 3) 実行
    try:
        records = graph.query(cypher)
    except Exception as e:
        # クエリが壊れている等の場合は、自己診断できるよう文脈にエラーを残す
        records = [{"error": str(e), "cypher": cypher}]

    context = json.dumps(records, ensure_ascii=False, indent=2)

    # 4) 最終回答（Vectorと同一テンプレートを再利用）
    answer = (QA_PROMPT | llm | StrOutputParser()).invoke(
        {"context": context, "question": question}
    )
    return answer

def run_hybrid_qa(question: str) -> str:
    docs = vectordb.as_retriever().get_relevant_documents(question)
    vector_ctx = _format_docs(docs) if docs else ""
    hybrid_question = (
    "以下の【ベクトル検索で得られた関連情報】を最優先で参考にして回答してください。\n"
    "【ベクトル検索で得られた関連情報】\n" + vector_ctx + "\n\n"
    "【元の質問】\n" + question
    )
    return run_graph_qa(hybrid_question)

def ask(question: str, route: str = "graph", original_code: str | None = None) -> str:
    route = route.lower()
    # 編集モードならプロンプトを合成
    if original_code:
        final_question = f"""
以下の【元のスクリプト】を【編集指示】に従って修正してください。

【元のスクリプト】
{original_code}


【編集指示】
{question}
""".strip()
    else:
        final_question = question
    if route == "graph":
        print("--- [Route: graph] Running Graph Search ---")
        return run_graph_qa(final_question)

    if route == "vector":
        print("--- [Route: vector] Running Vector Search ---")
        return vector_chain.invoke(final_question)

    if route == "hybrid":
        print("--- [Route: hybrid] Running Hybrid Search (Vector -> Graph) ---")
        return run_hybrid_qa(final_question)

    raise ValueError("route は 'vector', 'graph', 'hybrid' のみ指定できます。")


def main():
    import argparse
    parser = argparse.ArgumentParser(
    description="Generate or edit Python scripts for EvoShip based on user instructions.",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=textwrap.dedent(doc),
    )
    parser.add_argument("first_arg", help="質問文 もしくは 既存スクリプトのファイルパス")
    parser.add_argument("instruction", nargs="?", help="編集指示（編集モード時に必須）または route 指定")
    parser.add_argument("route", nargs="?", default="graph", choices=["vector", "graph", "hybrid"],
    help="検索ルート。未指定は 'graph'")
    parser.add_argument("-o", "--output", help="生成スクリプトを保存するファイルパス")
    args = parser.parse_args()
    original_code = None
    question = ""
    route = args.route

    # 既存ファイルなら編集モード
    if os.path.exists(args.first_arg):
        if not args.instruction:
            print("エラー: 編集モードでは <ファイルパス> と <編集指示> の両方が必要です。")
            parser.print_help()
            sys.exit(1)
        file_path = args.first_arg
        question = args.instruction
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_code = f.read()
            print(f"--- [Mode: Edit] Loading script from: {file_path} ---")
        except Exception as e:
            print(f"エラー: '{file_path}' の読み込みに失敗しました: {e}")
            sys.exit(1)

    else:
        # 新規生成モード
        question = args.first_arg
        # 2番目引数が route 指定のときに拾う（vector/graph/hybrid）
        if args.instruction in ("vector", "graph", "hybrid"):
            route = args.instruction
        print("--- [Mode: Create New] ---")

    try:
        answer = ask(question, route, original_code=original_code)

        # 保存オプション処理
        if args.output:
            # 最初の ```python ... ``` ブロックを抽出
            m = re.search(r"```python\n(.*?)```", answer, re.DOTALL)
            if m:
                code = m.group(1).strip()
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(code)
                print(f"\n--- Script saved to: {args.output} ---")

                # 説明部（見出しから後ろ）
                m2 = re.search(r"### スクリプトの説明\n\n(.*)", answer, re.DOTALL)
                if m2:
                    print("\n--- Script Explanation ---")
                    print(m2.group(1).strip())
                else:
                    print("\n--- Answer (no explicit explanation section) ---")
                    print(answer)
            else:
                print("\n--- Generated Answer (script block not found) ---")
                print(answer)
        else:
            print("\n--- Generated Answer ---")
            print(answer)

    except ValueError as e:
        print(f"\nエラー: {e}")
    except Exception as e:
        print(f"\n予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    main()

