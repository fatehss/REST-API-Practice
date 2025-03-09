# scripts/generate_openapi.py

import json
from pathlib import Path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # add ../ to sys.path

from app.server import app
def generate_openapi_json():
    openapi_json = app.openapi()
    output_path = Path("../openapi.json")
    output_path.write_text(json.dumps(openapi_json, indent=2))
    print(f"Generated {output_path}")

if __name__ == "__main__":
    generate_openapi_json()
