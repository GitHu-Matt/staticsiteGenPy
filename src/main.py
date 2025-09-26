#!/usr/bin/env python3
from pathlib import Path
import shutil

from generate_page import generate_pages_recursive

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
    shutil.copytree(src, dest)
    print("Copy complete.")


def main():
    # 1) Remove and recreate public (clean build)
    remove_public(PUBLIC_DIR)

    # 2) Copy static into public
    if STATIC_DIR.exists():
        copy_static(STATIC_DIR, PUBLIC_DIR)
    else:
        PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    # 3) Generate pages for every .md under content/ recursively
    if CONTENT_DIR.exists():
        generate_pages_recursive(str(CONTENT_DIR), str(TEMPLATE_PATH), str(PUBLIC_DIR))
    else:
        print(f"No content directory found at {CONTENT_DIR}. Nothing to generate.")


if __name__ == "__main__":
    main()
