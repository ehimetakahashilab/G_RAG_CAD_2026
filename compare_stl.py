#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_stl_1218_structured_bp_v2_2.py

v2_1 パッチ版（重要修正）:
- classification は必ず added_objects を参照して生成し、ID対応ズレを原理的に防止する
- Code Interpreter が返すのは「差分の事実（summary / added_objects / removed_objects）」のみ
- bracket/plate 分類はローカルPython側で決定論に構築し、assertで bbox 対応を検証

Usage:
  python compare_stl_1218_structured_bp_v2_2.py --a nobracket.stl --b sample0_1119.stl --out stl_diff_bp.json --model gpt-4o
  python compare_stl_1218_structured_bp_v2_2.py --a nobra2_plate3.stl --b sample0_1119.stl --out stl_diff22_bp.json --model gpt-4o
  python compare_stl_1218_structured_bp_v2_2.py --a sample2-bra1.stl --b sample2.stl --out stl_diff3_bp.json --model gpt-4o

  python compare_stl_1218_structured_bp_v2_2.py --a nobracket.stl --b samplename2_bracket_23_1.stl --out stl_diff_bracket_23_1bp.json --model gpt-4o
  python compare_stl_1218_structured_bp_v2_2.py --a nobracket.stl --b samplename2_bracket_23_2.stl --out stl_diff_bracket_23_2bp.json --model gpt-4o

  python compare_stl_1218_structured_bp_v2_2.py --a nobracket.stl --b bracket_01.stl --out stl_diff_bracket_01bp.json --model gpt-4o
  python compare_stl_1218_structured_bp_v2_2.py --a nobracket.stl --b bracket_02.stl --out stl_diff_bracket_02bp.json --model gpt-4o
  python compare_stl_1218_structured_bp_v2_2.py --a nobracket.stl --b bracket_03.stl --out stl_diff_bracket_03bp.json --model gpt-4o
  python compare_stl_1218_structured_bp_v2_2.py --a nobracket.stl --b bracket_04.stl --out stl_diff_bracket_04bp.json --model gpt-4o

  python compare_stl_1218_structured_bp_v2_2_llm.py --a nobracket.stl --b bracket_01.stl --out stl_diff_bracket_01bp_llmsum.json --model gpt-4o --llm_summary
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

from openai import OpenAI

SCHEMA_VERSION = "stl_diff_bp_v2_2"
DEFAULT_MODEL = "gpt-4o-2024-08-06"

def llm_write_formal_summary_ja(client: OpenAI, model: str, *, added_total: int, removed_total: int, added_bracket: int, added_plate: int) -> str:
    """
    LLMに「指定テンプレート」形式で自然言語要約を書かせる。
    注意: 推測をさせないため、入力は数値のみ。出力は json_schema で1フィールドに固定。
    """
    payload = {
        "added_total": int(added_total),
        "removed_total": int(removed_total),
        "added_bracket": int(added_bracket),
        "added_plate": int(added_plate),
    }

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {"nl_summary_ja": {"type": "string"}},
        "required": ["nl_summary_ja"],
    }

    prompt = f"""
次の数値だけを使って、指定テンプレートに**完全に一致**する日本語要約を作成してください。
推測・補足・言い換えは禁止です。句読点もテンプレート通りにしてください。

テンプレート（この形に完全一致）:
「追加部材はブラケット{{added_bracket}}個、プレート{{added_plate}}個（合計{{added_total}}個）であった。削除部材は{{removed_total}}個であった。」

INPUT(JSON):
{json.dumps(payload, ensure_ascii=False)}
""".strip()

    resp = client.responses.create(
        model=model,
        input=[{"role": "user", "content": prompt}],
        text={
            "format": {
                "type": "json_schema",
                "name": "nl_summary_ja",
                "strict": True,
                "schema": schema,
            }
        },
    )
    txt = get_output_text(resp).strip()
    data = json.loads(txt)
    return str(data["nl_summary_ja"])



def get_output_text(resp) -> str:
    if getattr(resp, "output_text", None):
        return resp.output_text or ""
    out = ""
    for item in reversed(getattr(resp, "output", []) or []):
        if getattr(item, "type", None) == "message":
            for c in getattr(item, "content", []) or []:
                if getattr(c, "type", None) == "output_text":
                    out += c.text
    return out


def _safe_float(x) -> float:
    try:
        v = float(x)
        if math.isfinite(v):
            return v
    except Exception:
        pass
    return 0.0


def classify_from_bbox(bbox_size: List[float], long_thr: float, aspect_thr: float) -> Tuple[str, float, Dict[str, Any], str]:
    dims = sorted([abs(_safe_float(x)) for x in bbox_size])
    t, w, l = dims[0], dims[1], dims[2]
    aspect = (l / max(w, 1e-9))

    is_plate = (l >= long_thr) and (aspect >= aspect_thr)

    if is_plate:
        l_margin = (l - long_thr) / max(long_thr, 1e-9)
        a_margin = (aspect - aspect_thr) / max(aspect_thr, 1e-9)
        conf = 0.70 + 0.25 * min(1.0, max(0.0, min(l_margin, a_margin)))
        conf = float(min(0.95, max(0.60, conf)))
        part = "plate"
        notes = f"plate: l={l:.1f}>= {long_thr}, aspect={aspect:.2f}>= {aspect_thr}"
    else:
        near = max(l / max(long_thr, 1e-9), aspect / max(aspect_thr, 1e-9))
        conf = 0.92 - 0.25 * min(1.0, max(0.0, near))
        conf = float(min(0.95, max(0.60, conf)))
        part = "bracket"
        notes = f"bracket: plate条件不成立 (l={l:.1f}, aspect={aspect:.2f})"

    evidence = {
        "bbox_size": [float(_safe_float(x)) for x in bbox_size],
        "dims_sorted": [float(t), float(w), float(l)],
        "aspect_l_over_w": float(aspect),
        "rule_long_thr": float(long_thr),
        "rule_aspect_thr": float(aspect_thr),
    }
    return part, conf, evidence, notes


def build_classification(added_objects: List[Dict[str, Any]], long_thr: float, aspect_thr: float, max_items: int) -> Dict[str, Any]:
    objs = list(added_objects)
    objs.sort(key=lambda o: (-float(o.get("volume", 0.0)), int(o.get("id", 0))))

    id_to_type_list: List[Dict[str, Any]] = []
    per_added_object: List[Dict[str, Any]] = []
    needs_review: List[int] = []
    plate_like: List[int] = []
    confs: List[float] = []

    for o in objs:
        oid = int(o["id"])
        bbox = o["bbox_size"]
        part, conf, ev, notes = classify_from_bbox(bbox, long_thr, aspect_thr)

        dims = sorted([abs(_safe_float(x)) for x in bbox])
        t, w, l = dims[0], dims[1], dims[2]
        aspect = l / max(w, 1e-9)
        if (0.9 * long_thr <= l <= 1.1 * long_thr) or (0.9 * aspect_thr <= aspect <= 1.1 * aspect_thr):
            needs_review.append(oid)
        if part == "plate":
            plate_like.append(oid)

        id_to_type_list.append({"id": oid, "part_type": part})
        confs.append(conf)

    # truncate per_added_object but keep id_to_type_list full
    for item in id_to_type_list[:max_items]:
        oid = item["id"]
        o = next(x for x in objs if int(x["id"]) == oid)
        part, conf, ev, notes = classify_from_bbox(o["bbox_size"], long_thr, aspect_thr)
        per_added_object.append({
            "id": oid,
            "part_type": part,
            "confidence": float(round(conf, 3)),
            "rationale_ja": "added_objects の bbox_size から dims_sorted と aspect を計算し、固定閾値で二値分類（再現性のため決定論）。",
            "evidence": ev,
        })

    bracket_count = sum(1 for x in id_to_type_list if x["part_type"] == "bracket")
    plate_count = sum(1 for x in id_to_type_list if x["part_type"] == "plate")
    conf_overall = float(sum(confs) / len(confs)) if confs else 0.0

    summary = {
        "added_total": int(len(id_to_type_list)),
        "bracket_count": int(bracket_count),
        "plate_count": int(plate_count),
        "all_bracket": bool(plate_count == 0),
        "confidence_overall": float(round(conf_overall, 3)),
        "notes_ja": f"plate条件: l>= {long_thr} & (l/w)>= {aspect_thr}. 近傍は要確認。",
        "per_added_object_total": int(len(id_to_type_list)),
        "per_added_object_returned": int(len(per_added_object)),
        "per_added_object_truncated": bool(len(per_added_object) < len(id_to_type_list)),
    }

    return {
        "labels": ["bracket", "plate"],
        "summary": summary,
        "per_added_object": per_added_object,
        "id_to_type_list": id_to_type_list,
        "flags": {
            "needs_human_review_ids": needs_review,
            "plate_like_ids": plate_like,
        }
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--out", default="stl_diff_bp.json")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--summary_model", default=None, help="LLM要約に使用するモデル。未指定なら --model を使用")
    ap.add_argument("--llm_summary", action="store_true", help="LLMで形式要約 nl_summary_ja_llm を追加出力する")
    ap.add_argument("--max_list", type=int, default=200)
    ap.add_argument("--max_items", type=int, default=120)
    ap.add_argument("--retry", type=int, default=1)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--long_thr", type=float, default=1000.0)
    ap.add_argument("--aspect_thr", type=float, default=3.0)
    args = ap.parse_args()

    client = OpenAI()

    base_dir = Path(__file__).resolve().parent
    a_path = Path(args.a); b_path = Path(args.b); out_path = Path(args.out)
    if not a_path.is_absolute(): a_path = base_dir / a_path
    if not b_path.is_absolute(): b_path = base_dir / b_path
    if not out_path.is_absolute(): out_path = base_dir / out_path
    if not a_path.exists(): raise FileNotFoundError(a_path)
    if not b_path.exists(): raise FileNotFoundError(b_path)

    file_a = client.files.create(file=open(a_path, "rb"), purpose="user_data")
    file_b = client.files.create(file=open(b_path, "rb"), purpose="user_data")

    schema: Dict[str, Any] = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "schema_version": {"type": "string"},
            "units": {
                "type": "object",
                "additionalProperties": False,
                "properties": {"length": {"type": "string"}, "volume": {"type": "string"}},
                "required": ["length", "volume"],
            },
            "summary": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "common_count": {"type": "integer"},
                    "added_count": {"type": "integer"},
                    "removed_count": {"type": "integer"},
                    "added_returned": {"type": "integer"},
                    "removed_returned": {"type": "integer"},
                    "description": {"type": "string"},
                },
                "required": ["common_count", "added_count", "removed_count", "added_returned", "removed_returned", "description"],
            },
            "added_objects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "integer"},
                        "volume": {"type": "number"},
                        "centroid": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3},
                        "bbox_size": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3},
                    },
                    "required": ["id", "volume", "centroid", "bbox_size"],
                },
            },
            "removed_objects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "integer"},
                        "volume": {"type": "number"},
                        "centroid": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3},
                        "bbox_size": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3},
                    },
                    "required": ["id", "volume", "centroid", "bbox_size"],
                },
            },
        },
        "required": ["schema_version", "units", "summary", "added_objects", "removed_objects"],
    }

    prompt = f"""
あなたは Python(Code Interpreter)でSTL差分解析を行うエージェントです。

やること（厳守）:
1) file_a(before) と file_b(after) のSTLを読み、連結成分ごとに分割する
2) 各成分について volume（取れなければ0）, centroid, bbox_size(extents) を算出
3) beforeとafterを比較して common / added / removed を推定し、added_objects と removed_objects を作る
   - 出力は added/removed それぞれ最大 {args.max_list} 件（体積降順）
4) JSONは必ず schema に一致させる（説明文・Markdown禁止）

Files:
- file_a: {file_a.id}
- file_b: {file_b.id}
""".strip()

    last = ""
    for attempt in range(args.retry + 1):
        if not args.quiet:
            print("--- Code Interpreter 実行中 --- (attempt", attempt, ")")
        resp = client.responses.create(
            model=args.model,
            input=[{"role": "user", "content": prompt if attempt == 0 else "schema準拠のJSONのみ出力してください。"}],
            tools=[{
                "type": "code_interpreter",
                "container": {"type": "auto", "file_ids": [file_a.id, file_b.id]},
            }],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "stl_diff_fact",
                    "strict": True,
                    "schema": schema,
                }
            },
        )
        txt = get_output_text(resp).strip()
        last = txt
        try:
            fact = json.loads(txt)
            break
        except json.JSONDecodeError:
            if attempt >= args.retry:
                print("[ERROR] JSON parse failed head:\n", last[:1200])
                raise

    classification = build_classification(fact.get("added_objects", []), args.long_thr, args.aspect_thr, args.max_items)

    # Alignment assertions (critical)
    added_map = {int(o["id"]): o for o in fact.get("added_objects", [])}
    for p in classification["per_added_object"]:
        oid = int(p["id"])
        if oid not in added_map:
            raise RuntimeError(f"ID mismatch: per_added_object id {oid} not in added_objects")
        bbox_a = [float(_safe_float(x)) for x in added_map[oid]["bbox_size"]]
        bbox_p = [float(_safe_float(x)) for x in p["evidence"]["bbox_size"]]
        if bbox_a != bbox_p:
            raise RuntimeError(f"bbox mismatch for id {oid}: added={bbox_a} vs class={bbox_p}")

    out = {
        "schema_version": SCHEMA_VERSION,
        "units": fact["units"],
        "summary": fact["summary"],
        "added_objects": fact["added_objects"],
        "removed_objects": fact["removed_objects"],
        "classification": classification,
        "meta": {
            "model": args.model,
            "classification_rule": {"long_thr": args.long_thr, "aspect_thr": args.aspect_thr},
        }
    }

    # Deterministic formal summary (paper-friendly, reproducible)
    cs_det = out["classification"]["summary"]
    out["nl_summary_ja_det"] = (
        f"追加部材はブラケット{int(cs_det.get('bracket_count',0) or 0)}個、"
        f"プレート{int(cs_det.get('plate_count',0) or 0)}個（合計{int(out['summary'].get('added_count',0) or 0)}個）であった。"
        f"削除部材は{int(out['summary'].get('removed_count',0) or 0)}個であった。"
    )

    # Optional: LLM-written formal summary (same template, but produced by LLM)
    if args.llm_summary:
        smodel = args.summary_model or args.model
        try:
            out["nl_summary_ja_llm"] = llm_write_formal_summary_ja(
                client,
                smodel,
                added_total=int(out["summary"].get("added_count", 0) or 0),
                removed_total=int(out["summary"].get("removed_count", 0) or 0),
                added_bracket=int(cs_det.get("bracket_count", 0) or 0),
                added_plate=int(cs_det.get("plate_count", 0) or 0),
            )
        except Exception as e:
            out["nl_summary_ja_llm_error"] = str(e)
            # fallback to deterministic (keeps downstream stable)
            out["nl_summary_ja_llm"] = out["nl_summary_ja_det"]
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    # Print one-line summary to stdout (always)
    if "nl_summary_ja_llm" in out:
        print(out["nl_summary_ja_llm"])
    else:
        print(out.get("nl_summary_ja_det", ""))


    # FORCE_PRINT_LLM_SUMMARY: print formal summary even if --quiet is set
    if args.llm_summary and "nl_summary_ja_llm" in out:
        print(out["nl_summary_ja_llm"])

    if not args.quiet:
        s = out["summary"]
        cs = out["classification"]["summary"]
        print("\n[SUCCESS] wrote:", out_path)
        print(f"[Summary] common={s.get('common_count')} added={s.get('added_count')} removed={s.get('removed_count')}")
        print(f"[BP] bracket={cs.get('bracket_count')} plate={cs.get('plate_count')} all_bracket={cs.get('all_bracket')}")
        print(f"[per_added_object] returned={cs.get('per_added_object_returned')} truncated={cs.get('per_added_object_truncated')}")
        if "nl_summary_ja_llm" in out:
            print("[NL_LLM]", out["nl_summary_ja_llm"])

if __name__ == "__main__":
    main()
