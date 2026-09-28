#!/usr/bin/env python3
"""
PDF to JSON parser for RKVY/CHC/FMB/Namo Drone scheme PDFs.
Downloads from agrimachinery.nic.in/Files/Guidelines/ and parses rate tables.
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DATA = Path('/Users/rajputnaresh/farmingtools.in/data')
MASTER = DATA / 'subsidy_master_latest.json'

def extract_text(pdf_path):
    """Extract text from PDF using pdftotext or pymupdf."""
    try:
        import fitz  # pymupdf
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except ImportError:
        result = subprocess.run(['pdftotext', str(pdf_path), '-'], 
                              capture_output=True, text=True)
        return result.stdout

def parse_crm_pdf(pdf_path):
    """Parse CRM (Crop Residue Management) guidelines PDF."""
    text = extract_text(pdf_path)
    
    machines = []
    # CRM scheme covers: Happy Seeder, Zero Till Drill, Balers, Mulchers, Rotavators
    # Pattern: Machine Name → 50% for SC/ST/Small/Marginal/Women/NE, 40% for General/OBC
    
    return {
        "scheme": "CRM",
        "full_name": "Crop Residue Management Scheme (In-situ)",
        "source_doc": "Revised Guidelines of In-situ Crop Residue Management Scheme 2020",
        "source_url": "https://agrimachinery.nic.in/Files/Guidelines/CRMGuideline2020-21.pdf",
        "source_date": "2020",
        "machines": []
    }

def parse_chc_pdf(pdf_path):
    """Parse CHC (Custom Hiring Centre) related PDF."""
    text = extract_text(pdf_path)
    return {
        "scheme": "CHC",
        "full_name": "Custom Hiring Centres",
        "source_doc": "CHC Guidelines",
        "source_url": "https://agrimachinery.nic.in/Files/Guidelines/CHCguidelines.pdf",
        "source_date": "2024",
        "machines": []
    }

def main():
    pdfs = {
        'CRM': '/tmp/CRMGuideline2020-21.pdf',
        'SMAM_2024': '/tmp/Guidelines_SMAM2024.pdf',
    }
    
    results = {}
    for name, path in pdfs.items():
        if Path(path).exists():
            print(f"Parsing {name}: {path}")
            if name == 'CRM':
                results[name] = parse_crm_pdf(path)
            print(f"  → Found {len(results[name].get('machines', []))} machine entries")
    
    # Save parsed results
    for name, data in results.items():
        out = DATA / f'scheme_{name.lower()}_parsed.json'
        with open(out, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"  Saved: {out}")
    
    print("\nNote: RKVY/CHC/FMB/Namo Drone PDFs were NOT real PDFs (HTML error pages).")
    print("Only CRM PDF downloaded successfully.")
    print("See state_topup_scrape.py for state portal scraping notes.")

if __name__ == '__main__':
    main()
