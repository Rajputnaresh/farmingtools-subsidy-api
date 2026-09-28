#!/usr/bin/env python3
"""
Export verified subsidy master data and registration metadata into
static JavaScript data files for offline and client-side widget consumption.

Generates:
  - subsidy_data/states_data.js
  - subsidy_data/scheme_data.js
  - subsidy_data/full_db.js
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "subsidy_data"
OUTPUT_DIR.mkdir(exist_ok=True)

MASTER_FILE = DATA_DIR / "subsidy_master_latest.json"
REG_FILE = DATA_DIR / "registration_info.json"


def export_states():
    if not REG_FILE.exists():
        print(f"⚠️ Warning: {REG_FILE} missing, skipping states export")
        return
    with open(REG_FILE, "r", encoding="utf-8") as f:
        reg = json.load(f)

    states_dict = reg.get("states", {})
    sorted_states = sorted(states_dict.values(), key=lambda s: int(s["code"]) if s.get("code", "").isdigit() else 999)

    clean_states = []
    for s in sorted_states:
        clean_states.append({
            "code": str(s.get("code")),
            "name": s.get("name"),
            "portal": s.get("portal"),
            "portal_name": s.get("portal_name")
        })

    out_file = OUTPUT_DIR / "states_data.js"
    content = f"// State Registry ({len(clean_states)} States and Union Territories)\n"
    content += f"// Source: data/registration_info.json\n"
    content += f"// Generated: {datetime.now().isoformat()}\n"
    content += "const STATES = " + json.dumps(clean_states, indent=2, ensure_ascii=False) + ";\n\n"
    content += "if (typeof window !== 'undefined') { window.STATES = STATES; }\n"
    content += "if (typeof module !== 'undefined' && module.exports) { module.exports = { STATES }; }\n"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Exported {len(clean_states)} states to {out_file} ({out_file.stat().st_size:,} bytes)")


def export_schemes():
    if not REG_FILE.exists():
        return
    with open(REG_FILE, "r", encoding="utf-8") as f:
        reg = json.load(f)

    schemes = reg.get("schemes", {})
    portals = reg.get("central_portals", {})

    out_file = OUTPUT_DIR / "scheme_data.js"
    content = "// Scheme-specific documents and process steps\n"
    content += "// Source: data/registration_info.json\n"
    content += f"// Generated: {datetime.now().isoformat()}\n"
    content += "const SCHEME_DOCS = " + json.dumps(schemes, indent=2, ensure_ascii=False) + ";\n\n"
    content += "const CENTRAL_PORTLINKS = " + json.dumps(portals, indent=2, ensure_ascii=False) + ";\n\n"
    content += "if (typeof window !== 'undefined') { window.SCHEME_DOCS = SCHEME_DOCS; window.CENTRAL_PORTLINKS = CENTRAL_PORTLINKS; }\n"
    content += "if (typeof module !== 'undefined' && module.exports) { module.exports = { SCHEME_DOCS, CENTRAL_PORTLINKS }; }\n"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Exported {len(schemes)} schemes to {out_file} ({out_file.stat().st_size:,} bytes)")


def export_full_db():
    if not MASTER_FILE.exists():
        print(f"⚠️ Warning: {MASTER_FILE} missing, skipping db export")
        return
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        master = json.load(f)

    machines = master.get("machines", [])
    db = {}

    for m in machines:
        mid = m["machine_id"]
        c = m.get("central", {})
        pri = c.get("priority", {})
        gen = c.get("general", {})

        topups = []
        for st in m.get("state_topups", []):
            st_sub = st.get("state_subsidy", {})
            topups.append({
                "state": st.get("state"),
                "pct": st_sub.get("percentage", 0),
                "flat": st_sub.get("flat_amount_rp", 0),
                "source": st_sub.get("source_doc") or st.get("source_doc", "State Agriculture Department"),
                "scheme": st.get("scheme", "")
            })

        db[mid] = {
            "name": m.get("name"),
            "cat": m.get("category", "General"),
            "scheme": c.get("scheme", "SMAM"),
            "pPct": pri.get("percentage", 50),
            "pCap": pri.get("max_subsidy_rp", 0),
            "gPct": gen.get("percentage", 40),
            "gCap": gen.get("max_subsidy_rp", 0),
            "sourceUrl": c.get("source_url", "https://agrimachinery.nic.in/Files/Guidelines/Guidelines_SMAM2024.pdf"),
            "stateTopups": topups
        }

    out_file = OUTPUT_DIR / "full_db.js"
    content = f"// Full verified machinery database ({len(db)} machines)\n"
    content += f"// Source: agrimachinery.nic.in SMAM 2024 Guidelines Annexure-II(c)\n"
    content += f"// Generated: {datetime.now().isoformat()}\n"
    content += "const FULL_DB = " + json.dumps(db, indent=2, ensure_ascii=False) + ";\n\n"
    content += "if (typeof window !== 'undefined') { window.FULL_DB = FULL_DB; }\n"
    content += "if (typeof module !== 'undefined' && module.exports) { module.exports = { FULL_DB }; }\n"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Exported {len(db)} machines to {out_file} ({out_file.stat().st_size:,} bytes)")


def main():
    print("=" * 60)
    print("  EXPORTING SUBSIDY STATIC JAVASCRIPT DATA ASSETS")
    print("=" * 60)
    export_states()
    export_schemes()
    export_full_db()
    print("✨ All static assets exported successfully.\n")


if __name__ == "__main__":
    main()
