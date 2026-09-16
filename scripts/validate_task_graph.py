#!/usr/bin/env python3
"""Deterministic checks for an SDD Task Graph JSON artifact."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {
    "draft",
    "ready",
    "in_progress",
    "implemented",
    "verified",
    "blocked",
    "cancelled",
}
REQUIRED_TICKET_FIELDS = {
    "id",
    "delivers",
    "traces_to",
    "blocked_by",
    "verification",
    "status",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def find_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        if node in visiting:
            start = stack.index(node)
            return stack[start:] + [node]
        if node in visited:
            return None
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, []):
            cycle = visit(dependency)
            if cycle:
                return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in graph:
        cycle = visit(node)
        if cycle:
            return cycle
    return None


def validate(payload: Any) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    if not isinstance(payload, dict):
        return ["根对象必须是 JSON object"], warnings, info
    graph_id = payload.get("graph_id")
    if not isinstance(graph_id, str) or not graph_id.strip():
        fail(errors, "graph_id 必须是非空字符串")

    tickets = payload.get("tickets")
    if not isinstance(tickets, list) or not tickets:
        return errors + ["tickets 必须是非空数组"], warnings, info

    by_id: dict[str, dict[str, Any]] = {}
    for index, ticket in enumerate(tickets, start=1):
        prefix = f"tickets[{index}]"
        if not isinstance(ticket, dict):
            fail(errors, f"{prefix} 必须是 object")
            continue
        missing = sorted(REQUIRED_TICKET_FIELDS - ticket.keys())
        if missing:
            fail(errors, f"{prefix} 缺少字段: {', '.join(missing)}")
        ticket_id = ticket.get("id")
        if not isinstance(ticket_id, str) or not ticket_id.strip():
            fail(errors, f"{prefix}.id 必须是非空字符串")
            continue
        if ticket_id in by_id:
            fail(errors, f"重复 ticket id: {ticket_id}")
        by_id[ticket_id] = ticket

        if not isinstance(ticket.get("delivers"), str) or not ticket["delivers"].strip():
            fail(errors, f"{ticket_id}.delivers 必须描述可观察能力")
        for field in ("traces_to", "blocked_by", "verification"):
            value = ticket.get(field)
            if not isinstance(value, list):
                fail(errors, f"{ticket_id}.{field} 必须是数组")
            elif field != "blocked_by" and not value:
                fail(errors, f"{ticket_id}.{field} 不能为空")
        status = ticket.get("status")
        if status not in ALLOWED_STATUSES:
            fail(errors, f"{ticket_id}.status 不支持: {status!r}")

    graph = {
        ticket_id: ticket.get("blocked_by", [])
        for ticket_id, ticket in by_id.items()
        if isinstance(ticket.get("blocked_by"), list)
    }
    for ticket_id, dependencies in graph.items():
        for dependency in dependencies:
            if not isinstance(dependency, str) or dependency not in by_id:
                fail(errors, f"{ticket_id}.blocked_by 引用了不存在的 ticket: {dependency!r}")
            elif dependency == ticket_id:
                fail(errors, f"{ticket_id} 不能阻塞自己")

    cycle = find_cycle(graph)
    if cycle:
        fail(errors, f"Task Graph 存在环: {' -> '.join(cycle)}")

    for ticket_id, ticket in by_id.items():
        status = ticket.get("status")
        dependencies = graph.get(ticket_id, [])
        unresolved = [
            dependency
            for dependency in dependencies
            if dependency in by_id and by_id[dependency].get("status") != "verified"
        ]
        if status in {"ready", "in_progress", "implemented", "verified"} and unresolved:
            fail(
                errors,
                f"{ticket_id} 状态为 {status}，但 blocker 尚未 verified: {', '.join(unresolved)}",
            )

    frontier = sorted(
        ticket_id
        for ticket_id, ticket in by_id.items()
        if ticket.get("status") == "ready"
        and all(
            dependency in by_id and by_id[dependency].get("status") == "verified"
            for dependency in graph.get(ticket_id, [])
        )
    )
    incomplete = [
        ticket_id
        for ticket_id, ticket in by_id.items()
        if ticket.get("status") not in {"verified", "cancelled"}
    ]
    if frontier:
        info.append(f"ready frontier: {', '.join(frontier)}")
    elif incomplete and not any(ticket.get("status") == "draft" for ticket in by_id.values()):
        warnings.append("没有 ready frontier；请检查是否所有未完成 ticket 都被真实 blocker 阻塞")
    if not errors and not frontier and not incomplete:
        info.append("Task Graph 已全部 verified 或 cancelled")
    return errors, warnings, info


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Task Graph JSON 路径")
    args = parser.parse_args()
    try:
        payload = json.loads(args.path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: 文件不存在: {args.path}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: JSON 无法解析: {exc}")
        return 2

    errors, warnings, info = validate(payload)
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    for message in info:
        print(f"INFO: {message}")
    if errors:
        return 1
    print("OK: Task Graph 结构可执行")
    return 0


if __name__ == "__main__":
    sys.exit(main())
