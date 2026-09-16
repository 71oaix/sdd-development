#!/usr/bin/env python3
"""Validate legacy and sdd-run/0.2 append-only SDD run logs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


EFFECTS = {"helped", "neutral", "hurt", "unknown", "not-needed", "not-used"}
OVERALLS = {"positive", "mixed", "negative", "unknown"}
CONFIDENCE = {"low", "medium", "high"}


def require(errors: list[str], record: dict[str, Any], keys: set[str], prefix: str) -> None:
    missing = sorted(keys - record.keys())
    if missing:
        errors.append(f"{prefix} 缺少字段: {', '.join(missing)}")


def validate_v2(record: Any, line_no: int) -> list[str]:
    errors: list[str] = []
    prefix = f"line {line_no}"
    if not isinstance(record, dict):
        return [f"{prefix}: 根对象必须是 JSON object"]
    require(
        errors,
        record,
        {"schema_version", "run_id", "ts_start", "ts_end", "task", "path", "mechanisms", "execution", "verification", "retrospective"},
        prefix,
    )
    if record.get("schema_version") != "sdd-run/0.2":
        errors.append(f"{prefix}: 不支持的 schema_version: {record.get('schema_version')!r}")
    for field in ("run_id", "ts_start", "ts_end"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            errors.append(f"{prefix}.{field}: 必须是非空字符串")
    task = record.get("task")
    if not isinstance(task, dict):
        errors.append(f"{prefix}.task: 必须是 object")
    else:
        require(errors, task, {"shape", "acceptance_count", "user_visible_scope"}, f"{prefix}.task")
        if not isinstance(task.get("acceptance_count"), int) or task.get("acceptance_count", -1) < 0:
            errors.append(f"{prefix}.task.acceptance_count: 必须是非负整数")
    path = record.get("path")
    if not isinstance(path, dict):
        errors.append(f"{prefix}.path: 必须是 object")
    else:
        require(errors, path, {"mode", "why"}, f"{prefix}.path")
    mechanisms = record.get("mechanisms")
    if not isinstance(mechanisms, dict):
        errors.append(f"{prefix}.mechanisms: 必须是 object")
    else:
        for name, mechanism in mechanisms.items():
            if not isinstance(mechanism, dict):
                errors.append(f"{prefix}.mechanisms.{name}: 必须是 object")
                continue
            require(errors, mechanism, {"used", "effect", "reason", "evidence_refs"}, f"{prefix}.mechanisms.{name}")
            if not isinstance(mechanism.get("used"), bool):
                errors.append(f"{prefix}.mechanisms.{name}.used: 必须是 boolean")
            if mechanism.get("effect") not in EFFECTS:
                errors.append(f"{prefix}.mechanisms.{name}.effect: 不支持的值 {mechanism.get('effect')!r}")
            if not isinstance(mechanism.get("evidence_refs"), list):
                errors.append(f"{prefix}.mechanisms.{name}.evidence_refs: 必须是数组")
    for field in ("execution", "verification", "retrospective"):
        if not isinstance(record.get(field), dict):
            errors.append(f"{prefix}.{field}: 必须是 object")
    retrospective = record.get("retrospective")
    if isinstance(retrospective, dict):
        require(errors, retrospective, {"overall", "keep", "trial_next_time", "simplify", "remove", "confidence", "reason"}, f"{prefix}.retrospective")
        if retrospective.get("overall") not in OVERALLS:
            errors.append(f"{prefix}.retrospective.overall: 不支持的值 {retrospective.get('overall')!r}")
        if retrospective.get("confidence") not in CONFIDENCE:
            errors.append(f"{prefix}.retrospective.confidence: 不支持的值 {retrospective.get('confidence')!r}")
    return errors


def validate(path: Path) -> tuple[list[str], int, int]:
    errors: list[str] = []
    legacy_count = 0
    v2_count = 0
    seen_run_ids: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return [f"文件不存在: {path}"], legacy_count, v2_count
    for line_no, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: JSON 无法解析: {exc}")
            continue
        if isinstance(record, dict) and "schema_version" not in record:
            if {"ts", "task", "success", "findings"} <= record.keys():
                legacy_count += 1
                continue
            errors.append(f"line {line_no}: 无 schema_version 且不符合 legacy 格式")
            continue
        if isinstance(record, dict) and record.get("schema_version") == "sdd-run/0.2":
            v2_count += 1
            run_id = record.get("run_id")
            if isinstance(run_id, str) and run_id in seen_run_ids:
                errors.append(f"line {line_no}: 重复 run_id: {run_id}")
            elif isinstance(run_id, str):
                seen_run_ids.add(run_id)
        errors.extend(validate_v2(record, line_no))
    if legacy_count + v2_count == 0:
        errors.append("日志没有可识别的记录")
    return errors, legacy_count, v2_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help=".run-log.jsonl 路径")
    args = parser.parse_args()
    errors, legacy_count, v2_count = validate(args.path)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"INFO: legacy={legacy_count}, sdd-run/0.2={v2_count}")
    if errors:
        return 1
    print("OK: run log 结构有效")
    return 0


if __name__ == "__main__":
    sys.exit(main())
