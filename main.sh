#!/usr/bin/env bash
set -euo pipefail

# Build the site
python3 src/main.py

# Serve public/ on port 8888
cd public
python3 -m http.server 8888
