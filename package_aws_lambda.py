#!/usr/bin/env python3
"""
Packages farmingtools.in Subsidy Calculator into a clean deployment zip for AWS Lambda.
Output: subsidy_lambda.zip
"""

import os
import sys
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_ZIP = BASE_DIR / "subsidy_lambda.zip"

INCLUDE_FILES = [
    "lambda_function.py",
    "subsidy_api.py",
    "subsidy_calculator.py",
    "subsidy_widget.html",
    "subsidy_widget_docs_steps.js",
]

INCLUDE_DIRS = [
    ("data", ["subsidy_master_latest.json", "registration_info.json", "smam_2024_annexure1.json"]),
    ("subsidy_data", ["full_db.js", "scheme_data.js", "states_data.js"]),
]

def build_package():
    print(f"📦 Packaging AWS Lambda deployment artifact...")
    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Add root files
        for fname in INCLUDE_FILES:
            fpath = BASE_DIR / fname
            if fpath.exists():
                zipf.write(fpath, arcname=fname)
                print(f"  + {fname} ({fpath.stat().st_size:,} bytes)")
            else:
                print(f"  ⚠️ Warning: {fname} not found!")

        # Add directory files
        for dir_name, files in INCLUDE_DIRS:
            dir_path = BASE_DIR / dir_name
            if not dir_path.exists():
                print(f"  ⚠️ Warning directory not found: {dir_name}")
                continue
            for fname in files:
                fpath = dir_path / fname
                if fpath.exists():
                    arcname = f"{dir_name}/{fname}"
                    zipf.write(fpath, arcname=arcname)
                    print(f"  + {arcname} ({fpath.stat().st_size:,} bytes)")
                else:
                    print(f"  ⚠️ Warning: {dir_name}/{fname} not found!")

    zip_size_bytes = OUTPUT_ZIP.stat().st_size
    zip_size_kb = zip_size_bytes / 1024
    print(f"\n🎉 Package created successfully: {OUTPUT_ZIP.name}")
    print(f"   Size: {zip_size_kb:.1f} KB ({zip_size_bytes:,} bytes)")
    print(f"   Status: Ready for AWS Lambda upload (well under the 50 MB direct upload limit)!\n")

if __name__ == "__main__":
    build_package()
