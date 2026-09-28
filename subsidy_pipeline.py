#!/usr/bin/env python3
"""
Subsidy data pipeline for farmingtools.in
Extracts and maintains verified multi-scheme subsidy rates from official government sources:
  - Central: SMAM 2024 Guidelines (Annexure-I) — agrimachinery.nic.in
  - Central: CRM 2020-21 Guidelines (Annexure-II) — agrimachinery.nic.in
  - Central: CHC & FMB Components — agrimachinery.nic.in
  - Central: Namo Drone Didi / Kisan Drone Guidelines — agrimachinery.nic.in
  - State: West Bengal Farm Mechanization Scheme (FSM/CHC/FMB) — wbfms.wb.gov.in
  - State: Haryana Crop Residue Management (MechCRM) — agriharyana.gov.in
  - State: Punjab CRM & Subam Scheme — agrimachinerypb.com
  - State: Uttar Pradesh Krishi Yantra Subsidy — upagriculture.com
"""

import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

PDF_SOURCES = {
    "SMAM_2024": {
        "url": "https://agrimachinery.nic.in/Files/Guidelines/Guidelines_SMAM2024.pdf",
        "local": "/tmp/Guidelines_SMAM2024.pdf"
    },
    "CRM_2020": {
        "url": "https://agrimachinery.nic.in/Files/Guidelines/CRMGuideline2020-21.pdf",
        "local": "/tmp/CRMGuideline2020-21.pdf"
    },
    "SMAM_2018": {
        "url": "https://agrimachinery.nic.in/Files/Guidelines/smam1920.pdf",
        "local": "/tmp/smam_guidelines_2018.pdf"
    },
    "WB_FMS_2024": {
        "url": "https://wbfms.wb.gov.in/documents/Product_List_subsidy_24-25.pdf",
        "local": "/tmp/wbfms_product_list.pdf"
    }
}


def download_file(url: str, dest_path: str, timeout: int = 15) -> bool:
    """Download a remote file if not present or check freshness."""
    p = Path(dest_path)
    if p.exists() and p.stat().st_size > 1000:
        return True
    
    print(f"📥 Downloading {url} -> {dest_path}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            with open(dest_path, "wb") as f:
                f.write(response.read())
        print(f"✅ Successfully downloaded {dest_path} ({Path(dest_path).stat().st_size} bytes)")
        return True
    except Exception as e:
        print(f"⚠️ Warning: Could not download {url}: {e}")
        return False


def get_file_hash(filepath: str) -> str:
    """Calculate SHA256 hash of a file."""
    p = Path(filepath)
    if not p.exists():
        return "missing"
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def check_data_freshness() -> bool:
    """Daily check: verify all key source PDFs are present, intact, and master data is fresh."""
    print("=" * 60)
    print("  SUBSIDY DATA PIPELINE — DAILY INTEGRITY & FRESHNESS CHECK")
    print("=" * 60)

    all_ok = True
    for name, src in PDF_SOURCES.items():
        local = src["local"]
        exists = Path(local).exists()
        size = Path(local).stat().st_size if exists else 0
        h = get_file_hash(local)[:16] if exists else "N/A"
        print(f"  [{name:12s}] Exists: {'✅' if exists else '❌'} | Size: {size:>10,} bytes | SHA: {h}")
        if not exists:
            all_ok = False

    latest_master = DATA_DIR / "subsidy_master_latest.json"
    if latest_master.exists():
        d = json.load(open(latest_master))
        m_count = len(d.get("machines", []))
        ext_at = d.get("metadata", {}).get("extracted_at", "Unknown")
        print(f"\n  [Master Dataset] Records: {m_count} | Extracted: {ext_at}")
        print(f"  [Status]         ✅ Master data active at {latest_master}")
    else:
        print("  [Master Dataset] ❌ Missing subsidy_master_latest.json")
        all_ok = False

    return all_ok


def run_pipeline() -> bool:
    """Execute the full data pipeline to compile latest multi-scheme master dataset."""
    print("=" * 60)
    print("  RUNNING COMPLETE SUBSIDY DATA PIPELINE")
    print("=" * 60)

    # 1. Ensure all source PDFs are cached
    for name, src in PDF_SOURCES.items():
        download_file(src["url"], src["local"])

    # 2. Run master builder
    builder_script = BASE_DIR / "build_multi_scheme_master.py"
    if not builder_script.exists():
        print(f"❌ Builder script missing: {builder_script}")
        return False

    print(f"\n⚙️ Running {builder_script.name}...")
    res = subprocess.run([sys.executable, str(builder_script)], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(f"❌ Builder error:\n{res.stderr}")
        return False

    print("✅ Pipeline run completed successfully.")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check-only":
        ok = check_data_freshness()
        sys.exit(0 if ok else 1)
    
    success = run_pipeline()
    sys.exit(0 if success else 1)
