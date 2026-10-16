#!/usr/bin/env python3
"""Cross-platform skill linker for Windows and Linux.

Links all active skills (outside `deprecated/` and `misc/`) into:
- Workspace skill directory: `.agents/skills/<skill-name>` (relative symlink on POSIX, junction/copy fallback on Windows)
- User global skill directories: `~/.agents/skills/<skill-name>` and `~/.claude/skills/<skill-name>` (unless `--workspace-only` is passed)
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

EXCLUDED_BUCKETS = {"deprecated", "misc", "node_modules"}


def configure_utf8_io() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def discover_skills(repo_root: Path) -> list[Path]:
    skills_root = repo_root / "skills"
    found: list[Path] = []
    for skill_md in sorted(skills_root.rglob("SKILL.md")):
        rel_parts = skill_md.relative_to(skills_root).parts
        if any(part in EXCLUDED_BUCKETS for part in rel_parts):
            continue
        found.append(skill_md.parent)
    return found


def remove_existing_target(target: Path) -> None:
    if target.is_symlink() or target.is_file():
        target.unlink()
    elif target.is_dir():
        # On Windows, directory junctions may be detected as is_dir()
        try:
            target.rmdir()
        except OSError:
            shutil.rmtree(target)


def create_directory_link(src: Path, target: Path, use_relative: bool = False) -> str:
    remove_existing_target(target)
    target.parent.mkdir(parents=True, exist_ok=True)

    link_source: Path | str = (
        os.path.relpath(src, start=target.parent) if use_relative else src
    )

    try:
        os.symlink(link_source, target, target_is_directory=True)
        return "symlink"
    except OSError:
        if os.name == "nt":
            # Fallback to NTFS directory junction on Windows (requires no elevation)
            res = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(target), str(src)],
                capture_output=True,
                text=True,
            )
            if res.returncode == 0:
                return "junction"
        shutil.copytree(src, target)
        return "copy"


def link_into_destination(
    skills: list[Path], dest_dir: Path, repo_root: Path, use_relative: bool
) -> None:
    if dest_dir.is_symlink():
        resolved = dest_dir.resolve()
        if resolved == repo_root or repo_root in resolved.parents:
            print(
                f"error: {dest_dir.as_posix()} is a symlink into this repo ({resolved.as_posix()}).\n"
                f"Remove it and re-run; the script will recreate it as a real directory.",
                file=sys.stderr,
            )
            sys.exit(1)

    dest_dir.mkdir(parents=True, exist_ok=True)
    for src in skills:
        target = dest_dir / src.name
        mode = create_directory_link(src, target, use_relative=use_relative)
        print(f"linked ({mode}) {src.name} -> {src.as_posix()} ({dest_dir.as_posix()})")


def main(argv: list[str] | None = None) -> int:
    configure_utf8_io()

    parser = argparse.ArgumentParser(
        description="Link skills into workspace (.agents/skills) and global (~/.agents/skills, ~/.claude/skills) directories."
    )
    parser.add_argument(
        "--workspace-only",
        action="store_true",
        help="Only link skills into the repository's .agents/skills directory.",
    )
    parser.add_argument(
        "--global-only",
        action="store_true",
        help="Only link skills into ~/.agents/skills and ~/.claude/skills.",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parent.parent
    skills = discover_skills(repo_root)

    if not args.global_only:
        workspace_dest = repo_root / ".agents" / "skills"
        link_into_destination(
            skills,
            workspace_dest,
            repo_root,
            use_relative=(os.name != "nt"),
        )

    if not args.workspace_only:
        home = Path.home()
        for global_dest in (home / ".claude" / "skills", home / ".agents" / "skills"):
            link_into_destination(
                skills,
                global_dest,
                repo_root,
                use_relative=False,
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
