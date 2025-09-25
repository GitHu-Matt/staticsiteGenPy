#!/usr/bin/env python3
"""
Simple static copying utility for the static-site generator.

Usage:
  from project root:
    ./main.sh         # or python3 src/main.py

This will copy everything from ./static -> ./public, deleting the previous ./public first.
"""
import os
import shutil
from pathlib import Path

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def empty_dir(path: Path):
    """
    Delete the directory if it exists, then recreate an empty directory.
    """
    if path.exists():
        # remove everything in the directory
        if path.is_dir():
            print(f"Removing existing directory {path}")
            shutil.rmtree(path)
        else:
            path.unlink()
    # recreate directory
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
            # create directory and copy recursively
            dst_path.mkdir(parents=True, exist_ok=True)
            copy_recursive(src_path, dst_path)
        elif entry.is_file():
            # copy file metadata and contents
            shutil.copy2(src_path, dst_path)
            print(f"Copied file: {src_path} -> {dst_path}")
        else:
            # symlink or special file - copy as is if possible
            try:
                shutil.copy2(src_path, dst_path)
                print(f"Copied special file: {src_path} -> {dst_path}")
            except Exception as e:
                print(f"Skipping {src_path}: {e}")

def build_static(static_dir: str = "static", public_dir: str = "public"):
    base = Path.cwd()
    src = base / static_dir
    dst = base / public_dir

    # ensure source exists
    if not src.exists():
        raise FileNotFoundError(f"Static source directory not found: {src}")

    # empty the destination dir
    empty_dir(dst)

    # copy all
    print(f"Copying from {src} --> {dst}")
    copy_recursive(src, dst)
    print("Copy complete.")

def main():
    try:
        build_static("static", "public")
    except Exception as e:
        print("Error during build_static:", e)

if __name__ == "__main__":
    main()
