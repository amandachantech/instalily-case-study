# /backend/utils/partselect_utils.py

import json
import os

# Get the absolute path of the JSON file
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/partselect_parts.json")

# Read the JSON file and return as a Python list
def load_parts():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Search parts by keyword (matches part_number or name, case-insensitive)
def search_parts(keyword: str):
    keyword = keyword.lower()
    parts = load_parts()
    results = []

    for part in parts:
        if keyword in part["part_number"].lower() or keyword in part["name"].lower():
            results.append(part)

    return results
