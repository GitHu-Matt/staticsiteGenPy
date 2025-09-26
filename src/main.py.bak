#!/usr/bin/env python3
from pathlib import Path
import shutil
import os
import sys

from generate_page import generate_page

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = PROJECT_ROOT / "static"
CONTENT_DIR = PROJECT_ROOT / "content"
PUBLIC_DIR = PROJECT_ROOT / "public"
TEMPLATE_PATH = PROJECT_ROOT / "template.html"

def remove_public(dest: Path) -> None:
    if dest.exists():
        print(f"Removing existing directory {dest}")
        shutil.rmtree(dest)
    else:
        print(f"No existing {dest} to remove")

def copy_static(src: Path, dest: Path) -> None:
    print(f"Copying from {src} --> {dest}")
    # copytree requires dest not to exist
    shutil.copytree(src, dest)
    print("Copy complete.")

def generate_all_pages(content_root: Path, template_path: Path, public_root: Path) -> None:
    if not content_root.exists():
        print(f"No content directory found at {content_root}. Nothing to generate.")
        return

    # Walk through the content directory and find index.md files
    for dirpath, dirnames, filenames in os.walk(content_root):
        dirpath = Path(dirpath)
        if "index.md" in filenames:
            from_path = dirpath / "index.md"
            # compute relative path under content_root
            rel = dirpath.relative_to(content_root)
            dest_dir = public_root / rel
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = dest_dir / "index.html"
            # generate page
            generate_page(str(from_path), str(template_path), str(dest_path))

def main():
    # 1) Remove and recreate public (clean build)
    remove_public(PUBLIC_DIR)

    # 2) Copy static into public
    if STATIC_DIR.exists():
        copy_static(STATIC_DIR, PUBLIC_DIR)
    else:
        # Create empty public dir if no static
        PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    # 3) Generate pages for every index.md under content/
    generate_all_pages(CONTENT_DIR, TEMPLATE_PATH, PUBLIC_DIR)

if __name__ == "__main__":
    main()
