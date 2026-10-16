#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "google-genai",
#   "python-dotenv",
# ]
# ///
"""Helper script to invoke gemini-4-argon via Google AI Studio (google-genai SDK).

Searches for GEMINI_API_KEY in the following priority order:
1. Project root .env file (./.env)
2. OS environment variable GEMINI_API_KEY
3. User home global config ~/.gemini/.env (pathlib.Path.home() / ".gemini" / ".env")
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

SYSTEM_INSTRUCTION = (
    "あなたは高度なソフトウェアアーキテクトおよびエンジニアリングアドバイザーです。"
    "日本語で論理的かつ詳細な設計・解決策を回答すること。"
)


def configure_utf8_io() -> None:
    """Ensure stdout and stderr use UTF-8 across Windows and Linux."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def parse_env_file(env_path: Path) -> dict[str, str]:
    """Read key-value pairs from a .env file using python-dotenv if available, with a fallback parser."""
    if not env_path.is_file():
        return {}
    try:
        from dotenv import dotenv_values  # type: ignore

        values = dotenv_values(env_path)
        return {k: v for k, v in values.items() if k and v is not None}
    except ImportError:
        result: dict[str, str] = {}
        for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            if stripped.startswith("export "):
                stripped = stripped[len("export ") :].strip()
            key, _, val = stripped.partition("=")
            key = key.strip()
            val = val.strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
                val = val[1:-1]
            result[key] = val
        return result


def resolve_api_key(project_root: Path | None = None) -> tuple[str | None, str]:
    """Resolve GEMINI_API_KEY according to the specification priority order."""
    cwd = project_root or Path.cwd()

    # 1. Project root .env file
    local_env = cwd / ".env"
    local_values = parse_env_file(local_env)
    if local_values.get("GEMINI_API_KEY"):
        return local_values["GEMINI_API_KEY"], f"project .env ({local_env.as_posix()})"

    # 2. OS environment variable GEMINI_API_KEY
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key, "OS environment variable (GEMINI_API_KEY)"

    # 3. User home ~/.gemini/.env
    home_env = Path.home() / ".gemini" / ".env"
    home_values = parse_env_file(home_env)
    if home_values.get("GEMINI_API_KEY"):
        return home_values["GEMINI_API_KEY"], f"global config ({home_env.as_posix()})"

    return None, "none"


def build_prompt(prompt_parts: list[str], file_paths: list[str]) -> str:
    """Combine prompt text and context files into a single request payload."""
    sections: list[str] = []

    if prompt_parts:
        sections.append(" ".join(prompt_parts).strip())

    for raw_path in file_paths:
        path = Path(raw_path)
        if not path.is_file():
            raise FileNotFoundError(f"Context file not found: {path.as_posix()}")
        content = path.read_text(encoding="utf-8", errors="replace")
        sections.append(f"--- File: {path.as_posix()} ---\n{content}")

    if not sections and not sys.stdin.isatty():
        stdin_text = sys.stdin.read().strip()
        if stdin_text:
            sections.append(stdin_text)

    return "\n\n".join(s for s in sections if s)


def main(argv: list[str] | None = None) -> int:
    configure_utf8_io()

    parser = argparse.ArgumentParser(
        description="Call gemini-4-argon via Google AI Studio for deep architectural reasoning and bug diagnosis."
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Prompt string or question to send to gemini-4-argon (if a single existing file path is passed, its contents are included).",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="append",
        default=[],
        dest="files",
        help="Path to a context file to include in the prompt (can be specified multiple times).",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=os.environ.get("GEMINI_ARGON_MODEL", "gemini-4-argon"),
        help="Model ID to invoke (default: gemini-4-argon or GEMINI_ARGON_MODEL env var).",
    )
    parser.add_argument(
        "--system",
        default=SYSTEM_INSTRUCTION,
        help="Override the default Japanese system instruction.",
    )
    parser.add_argument(
        "--check-key",
        action="store_true",
        help="Verify whether GEMINI_API_KEY can be resolved and exit without calling the API.",
    )

    args = parser.parse_args(argv)

    api_key, source = resolve_api_key()
    if args.check_key:
        if api_key:
            print(f"OK: GEMINI_API_KEY resolved from {source}.")
            return 0
        print(
            "ERROR: GEMINI_API_KEY not found in ./.env, OS environment, or ~/.gemini/.env.",
            file=sys.stderr,
        )
        return 1

    prompt_args: list[str] = list(args.prompt)
    file_args: list[str] = list(args.files)

    # Support passing a single existing file path as a positional argument
    if len(prompt_args) == 1 and not file_args:
        candidate = Path(prompt_args[0])
        if candidate.is_file():
            file_args.append(prompt_args.pop(0))

    try:
        full_prompt = build_prompt(prompt_args, file_args)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not full_prompt:
        parser.print_help(sys.stderr)
        return 1

    if not api_key:
        print(
            "ERROR: GEMINI_API_KEY が見つかりません。以下のいずれかに設定してください:\n"
            "  1. プロジェクトルートの .env ファイル (GEMINI_API_KEY=...)\n"
            "  2. OSの環境変数 GEMINI_API_KEY\n"
            "  3. ~/.gemini/.env (Windows: C:\\Users\\<User>\\.gemini\\.env)",
            file=sys.stderr,
        )
        return 1

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print(
            "ERROR: 'google-genai' パッケージがインストールされていません。\n"
            "以下のコマンドで実行するか、パッケージをインストールしてください:\n"
            "  uv run .agents/scripts/call_argon.py \"...\"\n"
            "  pip install google-genai python-dotenv",
            file=sys.stderr,
        )
        return 1

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=args.model,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                system_instruction=args.system,
            ),
        )
        if response and response.text:
            print(response.text)
            return 0
        print("WARNING: モデルから空のレスポンスが返されました。", file=sys.stderr)
        return 0
    except Exception as exc:
        print(f"ERROR: gemini-4-argon API 呼び出し中にエラーが発生しました: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
