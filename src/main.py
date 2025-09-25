#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

from generate_page import generate_page

def empty_dir(path: Path):
    """
    Delete the directory if it exists (recursively) and recreate it empty.
    """
    if path.exists():
        if path.is_dir():
            print(f"Removing existing directory {path}")
            shutil.rmtree(path)
        else:
            path.unlink()
    path.mkdir(parents=True, exist_ok=True)

def copy_recursive(src: Path, dst: Path):
    """
    Recursively copy src -> dst. Logs each copied file.
    """
    if not src.exists():
        raise FileNotFoundError(f"Source path does not exist: {src}")

    for entry in src.iterdir():
        src_path = entry
        dst_path = dst / entry.name
        if entry.is_dir():
            dst_path.mkdir(parents=True, exist_ok=True)
            copy_recursive(src_path, dst_path)
        elif entry.is_file():
            shutil.copy2(src_path, dst_path)
            print(f"Copied file: {src_path} -> {dst_path}")
        else:
            try:
                shutil.copy2(src_path, dst_path)
                print(f"Copied special file: {src_path} -> {dst_path}")
            except Exception as e:
                print(f"Skipping {src_path}: {e}")

def build_static(static_dir: str = "static", public_dir: str = "public"):
    """
    Copy all files from static/ into public/
    """
    base = Path.cwd()
    src = base / static_dir
    dst = base / public_dir

    if not src.exists():
        raise FileNotFoundError(f"Static source directory not found: {src}")

    # empty the destination dir
    empty_dir(dst)

    # copy all
    print(f"Copying from {src} --> {dst}")
    copy_recursive(src, dst)
    print("Copy complete.")

def main():
    # 1) copy static files
    build_static("static", "public")

    # 2) generate the page from content/index.md using template.html
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
