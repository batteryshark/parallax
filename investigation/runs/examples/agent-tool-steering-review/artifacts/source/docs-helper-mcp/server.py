"""Synthetic MCP-style docs helper for a Parallax worked example.

This is a static-analysis fixture, not a server to run.
"""

import subprocess
from pathlib import Path
from urllib.request import urlopen


def search_docs(query: str) -> list[str]:
    index = Path("docs/index.txt")
    if not index.exists():
        return []

    needle = query.lower()
    return [
        line
        for line in index.read_text(encoding="utf-8").splitlines()
        if needle in line.lower()
    ]


def fetch_url(url: str) -> str:
    with urlopen(url, timeout=5) as response:
        return response.read().decode("utf-8", errors="replace")


def run_shell(command: str) -> str:
    completed = subprocess.run(
        command,
        shell=True,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout
