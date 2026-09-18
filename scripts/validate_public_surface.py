#!/usr/bin/env python3
"""Reject obvious local-machine paths and credential material in tracked files."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [Path(item) for item in result.stdout.decode("utf-8").split("\0") if item]


def patterns() -> list[tuple[str, str]]:
    windows_user = "C:" + "\\" + "Users" + "\\"
    github_token = "ghp" + "_"
    github_pat = "github_pat" + "_"
    private_key = "BEGIN " + "PRIVATE KEY"
    openai_key = "sk" + "-"
    macos_user = "/" + "Users/"
    linux_user = "/" + "home/"
    root_home = "/" + "root/"
    return [
        (windows_user, "Windows user path"),
        (macos_user, "macOS user path"),
        (linux_user, "Linux user path"),
        (root_home, "root home path"),
        (github_token, "GitHub token prefix"),
        (github_pat, "GitHub fine-grained token prefix"),
        (private_key, "private key marker"),
        (openai_key, "API key prefix"),
    ]


def main() -> int:
    findings: list[str] = []
    for path in tracked_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for needle, label in patterns():
            if needle in text:
                findings.append(f"{path}: {label}")
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}")
        return 1
    print("OK: public surface is free of blocked local paths and obvious credentials")
    return 0


if __name__ == "__main__":
    sys.exit(main())
