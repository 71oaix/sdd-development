#!/usr/bin/env python3
"""Reject obvious local-machine paths and credential material in tracked files."""

from __future__ import annotations

import subprocess
import sys
import re
from pathlib import Path


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [Path(item) for item in result.stdout.decode("utf-8").split("\0") if item]


def patterns() -> list[tuple[re.Pattern[str], str]]:
    windows_user = "C:" + "\\" + "Users" + "\\"
    github_token = re.escape("ghp" + "_") + r"[A-Za-z0-9]{20,}"
    github_pat = re.escape("github_pat" + "_") + r"[A-Za-z0-9_]{20,}"
    private_key = re.escape("BEGIN " + "PRIVATE KEY")
    openai_key = re.escape("sk" + "-") + r"[A-Za-z0-9]{20,}"
    macos_user = "/" + "Users/"
    linux_user = "/" + "home/"
    root_home = "/" + "root/"
    return [
        (re.compile(re.escape(windows_user)), "Windows user path"),
        (re.compile(re.escape(macos_user)), "macOS user path"),
        (re.compile(re.escape(linux_user)), "Linux user path"),
        (re.compile(re.escape(root_home)), "root home path"),
        (re.compile(github_token), "GitHub token prefix"),
        (re.compile(github_pat), "GitHub fine-grained token prefix"),
        (re.compile(private_key), "private key marker"),
        (re.compile(openai_key), "API key prefix"),
    ]


def main() -> int:
    findings: list[str] = []
    for path in tracked_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for needle, label in patterns():
            if needle.search(text):
                findings.append(f"{path}: {label}")
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}")
        return 1
    print("OK: public surface is free of blocked local paths and obvious credentials")
    return 0


if __name__ == "__main__":
    sys.exit(main())
