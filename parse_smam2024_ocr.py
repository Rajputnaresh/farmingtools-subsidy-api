#!/usr/bin/env python3
"""
Parse SMAM 2024 Annexure-I OCR — v5: handle all patterns + trailing no-% amounts.
Key insight: lines like "2.00 50% 1.60" have the 40% amount WITHOUT a % sign.
"""

import json, re
from pathlib import Path

OCR_PATH = Path("/tmp/smam2024_annexure1_ocr.txt")
OUTPUT_PATH = Path("/Users/rajputnaresh/farmingtools.in/data/smam_2024_annexure1.json")

def normalize(line):
    """Fix OCR artifacts."""
    line = re.sub(r'(\d),(\d)', r'\1.\2', line)  # 1,20 → 1.20
    line = re.sub(r'\}', '', line)                   # ii} → ii
    line = re.sub(r'[^\w\s%.()/-]', ' ', line)      # garbage chars
    line = re.sub(r'\s+', ' ', line).strip()
    return line

def join_lines(raw_lines):
    """Join multi-line names with their amounts.
    Key: separator lines (just dashes/garbage) should NOT pollute pending buffer.
    """
    result = []
    pending = []  # buffered name parts waiting for amounts
    
    for raw in raw_lines:
        line = normalize(raw)
        if not line or re.match(r'^[\-–—\s]+$', line):  # skip separator lines
            continue
        
        has_name = bool(re.search(r'[A-Za-z]', line))
        has_pct = bool(re.search(r'\d+\s*%', line))
        has_num = bool(re.search(r'\d+(?:\.\d+)?', line))
        
        if not has_name:
            # Pure amount/% line — attach to pending name if exists
            if pending:
                result.append(' '.join(pending) + ' ' + line)
                pending = []
            # else: orphan amounts with no name — skip
        elif has_pct or (has_num and re.search(r'\d+\.\d+\s+\d+\s*%', line)):
            # Name + amounts on same line — complete record (flush pending first)
            if pending:
                result.append(' '.join(pending))
                pending = []
            result.append(line)
        else:
            # Has letters but no amounts — name fragment, buffer it
            pending.append(line)
    
    if pending:
        result.append(' '.join(pending))
    
    return result

def parse_line(line):
    """Extract machine name + 50%/40% amounts from a joined line.
    Handles: "N.NN 50% M.MM" (40% w/o %), "N.NN 50% M.MM 40%" (both %),
    "N.NN 50% 40%" (missing 40%), and name-only (missing amounts).
    Returns dict or None.
    """
    # Find all "N% " patterns (50% or 40%)
    pct_matches = list(re.finditer(r'(\d+(?:\.\d+)?)\s+(\d+)\s*%', line))
    
    if not pct_matches:
        return None  # no % patterns at all
    
    first = pct_matches[0]
    pri_amt = float(first.group(1))
    pri_pct = int(first.group(2))
    
    if len(pct_matches) >= 2:
        # Both 50% and 40% present with %
        gen_match = pct_matches[-1]
        gen_amt = float(gen_match.group(1))
        gen_pct = int(gen_match.group(2))
    else:
        # Only one % found — check if there's a trailing number WITHOUT % (the 40% amount)
        # Everything after the first (and only) pct_match
        rest = line[first.end():].strip()
        trailing_nums = re.findall(r'(\d+(?:\.\d+)?)', rest)
        if trailing_nums:
            # Last trailing number is likely the 40% amount
            gen_amt = float(trailing_nums[-1])
            gen_pct = 40
        else:
            # "N.NN 50% 40%" pattern — 40% amount missing
            # Check if "40%" appears after the 50%
            forty_pct_match = re.search(r'40\s*%', line[first.end():])
            if forty_pct_match:
                # "40%" appears but no amount before it — missing
                gen_amt = None  # flagged as missing
                gen_pct = 40
            else:
                # Single % with no trailing number and no "40%" — duplicate
                gen_amt = pri_amt
                gen_pct = pri_pct
    
    # Name = everything before first pct_match
    name = line[:first.start()].strip()
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r'^[\(\[\{]\s*', '', name)     # strip leading ( [ {
    name = re.sub(r'[\}\)\,]+\s*$', '', name)    # strip trailing ) ]
    name = re.sub(r'\s+', ' ', name).strip()
    
    if len(name) < 3 or not name[0].isalpha():
        return None
    
    return {
        "name": name,
        "category_50_rp": int(pri_amt * 100000),
        "category_40_rp": int(gen_amt * 100000),
        "priority_percentage": pri_pct,
        "general_percentage": gen_pct,
        "flagged_missing_40": gen_amt is None,
    }

def main():
    print(f"Reading OCR text from {OCR_PATH}...")
    raw_lines = OCR_PATH.read_text().splitlines()
    print(f"Raw lines: {len(raw_lines)}")
    
    # Step 1: Join multi-line names + amounts
    joined = join_lines(raw_lines)
    print(f"After joining: {len(joined)} lines")
    
    # Step 2: Extract machines
    machines = []
    for line in joined:
        entry = parse_line(line)
        if entry:
            machines.append(entry)
    
    print(f"Extracted: {len(machines)} machines")
    
    # Print category breakdown
    def count(pattern):
        return len([m for m in machines if pattern.lower() in m['name'].lower()])
    
    print(f"  Tractors:     {count('tractor')}")
    print(f"  Power Tillers:{count('power tiller')}")
    print(f"  Combines:     {count('combine')}")
    print(f"  Transplanters:{count('transplanter')}")
    print(f"  Drones:       {count('drone')}")
    print(f"  Reapers:      {count('reaper')}")
    print(f"  Weeder:       {count('weeder')}")
    print(f"  Tea harvest:  {count('tea')}")
    print(f"  Forage:       {count('forage')}")
    print(f"  Cage wheel:   {count('cage wheel')}")
    print(f"  Chaff cutter: {count('chaff cutter')}")
    print(f"  Straw chopper:{count('straw chopper')}")
    print(f"  Balers:       {count('baler')}")
    print(f"  Hay/seed:     {count('seed')}")
    print(f"  General Oth:  {count('other')} - {count('general')}")
    print(f"  Flagged missing 40%: {sum(1 for m in machines if m.get('flagged_missing_40'))}")
    
    # Print sample tractor entries
    print("\n=== SAMPLE TRACTOR ENTRIES ===")
    for m in machines:
        if 'tractor' in m['name'].lower():
            print(f"  {m['name'][:60]:60s} | 50%:₹{m['category_50_rp']:>10,} | 40%:₹{m['category_40_rp']:>10,} | flag={m.get('flagged_missing_40')}")
    
    # Save
    output = {"machines": machines, "source": str(OCR_PATH)}
    OUTPUT_PATH.write_text(json.dumps(output, indent=2))
    print(f"\nSaved {len(machines)} machines to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
