#!/usr/bin/env python3
"""
State Portal Utilities for farmingtools.in Subsidy Calculator
Provides functions to look up state agriculture department portals,
scheme-specific portal routing, and state top-up eligibility info.

All 38 Indian States and Union Territories with NIC codes, portal URLs,
and scheme-specific routing for the 5 active subsidy schemes.
"""

from typing import Optional
from pathlib import Path

# ── Registry: All 38 Indian States & Union Territories ────────────────
# Source: NIC state dropdown API (agrimachinery.nic.in/api/dropdown/GetState)
# Portal URLs: Official state agriculture department websites

ALL_STATES = {
    "1": {"name": "Jammu & Kashmir", "code": "1", "portal": "https://hadp.jk.gov.in/", "portal_name": "HADP J&K / Directorate of Agriculture Jammu", "scheme_portals": {}},
    "2": {"name": "Himachal Pradesh", "code": "2", "portal": "https://krishi.hp.gov.in/", "portal_name": "HP Agriculture Department Portal", "scheme_portals": {}},
    "3": {"name": "Punjab", "code": "3", "portal": "https://agrimachinerypb.com/", "portal_name": "Punjab CRM / Subam Mechanization Portal", "scheme_portals": {"CRM": "https://agrimachinerypb.com/subam"}},
    "4": {"name": "Chandigarh", "code": "4", "portal": "https://chandigarh.gov.in/", "portal_name": "Chandigarh UT Agriculture Office", "scheme_portals": {}},
    "5": {"name": "Uttar Pradesh", "code": "5", "portal": "http://upagriculture.com/", "portal_name": "UP Agriculture DBT & Token Portal", "scheme_portals": {"CRM": "http://upagriculture.com/crm"}},
    "6": {"name": "Haryana", "code": "6", "portal": "https://agriharyana.gov.in/MechCRMScheme", "portal_name": "Agri Haryana MechCRM / Meri Fasal Mera Byora", "scheme_portals": {"CRM": "https://agriharyana.gov.in/MechCRMScheme"}},
    "7": {"name": "Delhi", "code": "7", "portal": "https://delhi.gov.in/", "portal_name": "Delhi Agriculture Unit", "scheme_portals": {}},
    "8": {"name": "Rajasthan", "code": "8", "portal": "https://rajkisan.rajasthan.gov.in/", "portal_name": "Rajkisan Sathi Portal", "scheme_portals": {}},
    "9": {"name": "Uttarakhand", "code": "9", "portal": "https://agriculture.uk.gov.in/", "portal_name": "Uttarakhand Agriculture Directorate", "scheme_portals": {}},
    "10": {"name": "Bihar", "code": "10", "portal": "https://dbtagriculture.bihar.gov.in/", "portal_name": "Bihar DBT Agriculture (OFMAS)", "scheme_portals": {}},
    "11": {"name": "Sikkim", "code": "11", "portal": "https://sikkim.gov.in/departments/agriculture-department", "portal_name": "Sikkim Organic Agriculture Portal", "scheme_portals": {}},
    "12": {"name": "Arunachal Pradesh", "code": "12", "portal": "https://agri.arunachal.gov.in/", "portal_name": "Arunachal Agriculture Department", "scheme_portals": {}},
    "13": {"name": "Nagaland", "code": "13", "portal": "https://agriculture.nagaland.gov.in/", "portal_name": "Nagaland Agri Portal", "scheme_portals": {}},
    "14": {"name": "Manipur", "code": "14", "portal": "https://agrimanipur.mn.gov.in/", "portal_name": "Manipur Agriculture Directorate", "scheme_portals": {}},
    "15": {"name": "Mizoram", "code": "15", "portal": "https://agriculturemizoram.nic.in/", "portal_name": "Mizoram Agriculture Portal", "scheme_portals": {}},
    "16": {"name": "Tripura", "code": "16", "portal": "https://agri.tripura.gov.in/", "portal_name": "Tripura Agri Portal", "scheme_portals": {}},
    "17": {"name": "Meghalaya", "code": "17", "portal": "https://megagriculture.gov.in/", "portal_name": "Meghalaya Agriculture Department", "scheme_portals": {}},
    "18": {"name": "Assam", "code": "18", "portal": "https://diragri.assam.gov.in/", "portal_name": "Assam Directorate of Agriculture", "scheme_portals": {}},
    "19": {"name": "West Bengal", "code": "19", "portal": "https://wbfms.wb.gov.in/", "portal_name": "WBFMS / Matir Katha Portal", "scheme_portals": {}},
    "20": {"name": "Jharkhand", "code": "20", "portal": "https://agri.jharkhand.gov.in/", "portal_name": "Jharkhand Krishi Department", "scheme_portals": {}},
    "21": {"name": "Odisha", "code": "21", "portal": "https://agrisnetodisha.ori.nic.in/", "portal_name": "SAFAL / Agrisnet Odisha", "scheme_portals": {}},
    "22": {"name": "Chhattisgarh", "code": "22", "portal": "https://agriportal.cg.nic.in/", "portal_name": "Chhattisgarh Kisan Portal", "scheme_portals": {}},
    "23": {"name": "Madhya Pradesh", "code": "23", "portal": "https://dbt.mpdage.org/", "portal_name": "MP e-Krishi Yantra Anudan DBT Portal", "scheme_portals": {}},
    "24": {"name": "Gujarat", "code": "24", "portal": "https://ikhedut.gujarat.gov.in/", "portal_name": "i-Khedut Gujarat Portal", "scheme_portals": {}},
    "25": {"name": "Daman & Diu", "code": "25", "portal": "https://daman.nic.in/", "portal_name": "Daman & Diu UT Agri Administration", "scheme_portals": {}},
    "26": {"name": "Dadra & Nagar Haveli", "code": "26", "portal": "https://dnh.gov.in/", "portal_name": "DNH UT Agri Administration", "scheme_portals": {}},
    "27": {"name": "Maharashtra", "code": "27", "portal": "https://mahadbt.maharashtra.gov.in/", "portal_name": "MahaDBT Farmer Mechanization Portal", "scheme_portals": {}},
    "28": {"name": "Andhra Pradesh", "code": "28", "portal": "https://rythubharosa.ap.gov.in/", "portal_name": "YSR Rythu Bharosa / Yantra Seva Portal", "scheme_portals": {}},
    "29": {"name": "Karnataka", "code": "29", "portal": "https://raitamitra.karnataka.gov.in/", "portal_name": "Raita Mitra / FRUITS Portal", "scheme_portals": {}},
    "30": {"name": "Goa", "code": "30", "portal": "https://agri.goa.gov.in/", "portal_name": "Goa Directorate of Agriculture", "scheme_portals": {}},
    "31": {"name": "Lakshadweep", "code": "31", "portal": "https://lakshadweep.gov.in/", "portal_name": "Lakshadweep Agri Unit", "scheme_portals": {}},
    "32": {"name": "Kerala", "code": "32", "portal": "https://aims.kerala.gov.in/", "portal_name": "AIMS Kerala / Karshaka Information Portal", "scheme_portals": {}},
    "33": {"name": "Tamil Nadu", "code": "33", "portal": "https://www.agristnet.tn.gov.in/", "portal_name": "AGRISNET / Uzhavan Mobile App Portal", "scheme_portals": {}},
    "34": {"name": "Puducherry", "code": "34", "portal": "https://agri.py.gov.in/", "portal_name": "Puducherry Agriculture Portal", "scheme_portals": {}},
    "35": {"name": "Andaman & Nicobar Islands", "code": "35", "portal": "https://agri.andaman.gov.in/", "portal_name": "A&N Islands Agriculture Department", "scheme_portals": {}},
    "36": {"name": "Telangana", "code": "36", "portal": "https://karshak.telangana.gov.in/", "portal_name": "Karshak / Rythu Bandhu Telangana", "scheme_portals": {}},
    "37": {"name": "Ladakh", "code": "37", "portal": "https://ladakh.nic.in/", "portal_name": "UT Ladakh Agriculture Department", "scheme_portals": {}},
}


# ── Scheme-specific portal routing ──────────────────────────────────────
# Maps (scheme_id, state_code) -> {portal_url, portal_name, topup_available, topup_details}

SCHEME_STATE_PORTALS = {
    # ── SMAM (all states — central portal is primary, state portal for top-ups) ──
    ("SMAM", "19"): {"portal": "https://wbfms.wb.gov.in/", "portal_name": "WBFMS West Bengal — State Farm Mechanization Scheme", "topup_available": True, "topup_note": "WB provides 40% additional top-up on tractors (verified from wbfms.wb.gov.in Product List 2024-25)."},
    ("SMAM", "6"): {"portal": "https://agriharyana.gov.in/MechCRMScheme", "portal_name": "Haryana MechCRM / Meri Fasal Mera Byora", "topup_available": False, "topup_note": "Haryana directs farmers to central SMAM portal. State portal for registration."},
    ("SMAM", "3"): {"portal": "https://agrimachinerypb.com/", "portal_name": "Punjab Subam Mechanization Portal", "topup_available": False, "topup_note": "Punjab directs farmers to central SMAM portal."},
    ("SMAM", "5"): {"portal": "http://upagriculture.com/", "portal_name": "UP Agriculture DBT Portal", "topup_available": False, "topup_note": "UP directs farmers to central SMAM portal."},

    # ── CRM (only Punjab, Haryana, UP, Delhi have CRM schemes) ──
    ("CRM", "6"): {"portal": "https://agriharyana.gov.in/MechCRMScheme", "portal_name": "Haryana Meri Fasal Mera Byora (MFMB)", "topup_available": True, "topup_note": "Haryana CRM: 50% central + state incentive. Must register on MFMB before applying."},
    ("CRM", "3"): {"portal": "https://agrimachinerypb.com/subam", "portal_name": "Punjab Subam CRM Portal", "topup_available": True, "topup_note": "Punjab CRM scheme: 50% central subsidy. Register on Subam portal."},
    ("CRM", "5"): {"portal": "http://upagriculture.com/crm", "portal_name": "UP CRM Portal", "topup_available": True, "topup_note": "UP CRM scheme available. Register on UP Agriculture portal."},
    ("CRM", "7"): {"portal": "https://delhi.gov.in/", "portal_name": "Delhi Agriculture Unit", "topup_available": True, "topup_note": "Delhi CRM scheme: limited to NCT Delhi farmers. Contact Delhi Agriculture office."},

    # ── CHC (all states via central portal) ──
    ("CHC", "19"): {"portal": "https://wbfms.wb.gov.in/", "portal_name": "WBFMS West Bengal", "topup_available": False, "topup_note": "CHC scheme is centrally funded. State portal for registration."},
    ("CHC", "6"): {"portal": "https://agriharyana.gov.in/MechCRMScheme", "portal_name": "Haryana Agriculture Department", "topup_available": False, "topup_note": "CHC scheme is centrally funded. Haryana portal for state-level processing."},

    # ── FMB (all states via central portal) ──
    ("FMB", "19"): {"portal": "https://wbfms.wb.gov.in/", "portal_name": "WBFMS West Bengal", "topup_available": False, "topup_note": "FMB scheme is centrally funded. State portal for registrations."},
    ("FMB", "6"): {"portal": "https://agriharyana.gov.in/MechCRMScheme", "portal_name": "Haryana Agriculture Department", "topup_available": False, "topup_note": "FMB scheme is centrally funded. Haryana portal for state processing."},

    # ── Namo Drone Didi (all states via central portal) ──
    ("NAMO_DRONE_DIDI", "19"): {"portal": "https://wbfms.wb.gov.in/", "portal_name": "WBFMS West Bengal", "topup_available": False, "topup_note": "Namo Drone Didi is a central sector scheme. State SRLM for SHG selection."},
    ("NAMO_DRONE_DIDI", "6"): {"portal": "https://agriharyana.gov.in/MechCRMScheme", "portal_name": "Haryana Agriculture Department / SRLM", "topup_available": False, "topup_note": "Namo Drone Didi is a central sector scheme. Haryana SRLM for SHG selection."},
}


# ── Public API ─────────────────────────────────────────────────────────

def get_state_portal(state_code: str) -> Optional[dict]:
    """
    Look up a state's agriculture portal by NIC code (string), state name, or state key.

    Args:
        state_code: NIC state code (e.g. "19"), state name (e.g. "West Bengal"),
                    or uppercase state key (e.g. "WEST_BENGAL").

    Returns:
        dict with keys: name, code, portal, portal_name, scheme_portals
        or None if not found.
    """
    if not state_code:
        return None

    code_str = str(state_code).strip()

    # Try direct NIC code lookup
    if code_str in ALL_STATES:
        return ALL_STATES[code_str]

    # Try by state name (case-insensitive)
    for state in ALL_STATES.values():
        if state["name"].lower() == code_str.lower():
            return state

    # Try by uppercase state key (replace spaces/special chars with underscores)
    normalized = _normalize_state_key(code_str)
    for state in ALL_STATES.values():
        if _normalize_state_key(state["name"]) == normalized:
            return state

    # Try common aliases
    aliases = {
        "WB": "19", "WESTBENGAL": "19", "W_BENGAL": "19",
        "HR": "6", "HAR": "6", "HARY": "6",
        "PB": "3", "PUNJAB": "3",
        "UP": "5", "UTTAR": "5", "UTTER": "5",
        "KL": "32", "KER": "32", "KERALA": "32",
        "MH": "27", "MAHA": "27", "MAHAR": "27",
        "GJ": "24", "GUJ": "24", "GUJAR": "24",
        "TN": "33", "TAM": "33", "TAMIL": "33",
        "TS": "36", "TEL": "36", "TELANG": "36",
        "BR": "10", "BIHAR": "10",
        "OD": "21", "ORISSA": "21", "ODISHA": "21",
        "RJ": "8", "RAJ": "8", "RAJAS": "8",
        "MP": "23", "MADHYA": "23", "MAD": "23",
        "AS": "18", "ASSAM": "18",
    }
    code_upper = code_str.upper()
    if code_upper in aliases:
        resolved = aliases[code_upper]
        return ALL_STATES.get(resolved)

    return None


def get_all_state_portals() -> list:
    """Return list of all 38 state portal dicts, sorted by NIC code."""
    return [dict(state) for state in sorted(ALL_STATES.values(), key=lambda s: int(s["code"]))]


def get_scheme_specific_portal(scheme_id: str, state_code: str) -> tuple:
    """
    Get the scheme-specific portal for a state, falling back to the
    general state portal if no scheme-specific entry exists.

    Args:
        scheme_id: Scheme identifier (SMAM, CRM, CHC, FMB, NAMO_DRONE_DIDI)
        state_code: NIC state code string (e.g. "19")

    Returns:
        (portal_dict, scheme_info_dict): 
        - portal_dict: state portal info (always returned if state exists)
        - scheme_info_dict: scheme metadata from registration_info.json (or empty dict)
    """
    state = get_state_portal(state_code)
    if not state:
        return None, {}

    scheme_key = scheme_id.upper()
    lookup_key = (scheme_key, state["code"])

    if lookup_key in SCHEME_STATE_PORTALS:
        sp = SCHEME_STATE_PORTALS[lookup_key]
        return {
            "name": state["name"],
            "code": state["code"],
            "portal": sp.get("portal", state["portal"]),
            "portal_name": sp.get("portal_name", state["portal_name"]),
            "scheme_portals": {scheme_key: sp.get("portal", state["portal"])},
            "topup_available": sp.get("topup_available", False),
            "topup_note": sp.get("topup_note", ""),
        }, {"scheme_id": scheme_key, "topup_note": sp.get("topup_note", "")}

    # Fallback: return general state portal
    return {
        "name": state["name"],
        "code": state["code"],
        "portal": state["portal"],
        "portal_name": state["portal_name"],
        "scheme_portals": {},
        "topup_available": False,
        "topup_note": f"No scheme-specific portal for {scheme_key} in {state['name']}. Use central portal.",
    }, {"scheme_id": scheme_key}


def _normalize_state_key(name: str) -> str:
    """Normalize a state name to a lookup key (UPPERCASE, underscores)."""
    return name.upper().replace(" & ", "_").replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "").replace(".", "").replace(",", "")


# ── CLI test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("State Portal Utilities — Quick Test")
    print("=" * 50)

    # Test lookups
    tests = [
        ("19", "NIC code for West Bengal"),
        ("West Bengal", "State name"),
        ("WEST_BENGAL", "State key"),
        ("6", "NIC code for Haryana"),
        ("6", "Haryana by code"),
        ("99", "Unknown state (should return None)"),
        ("WB", "Alias: WB -> West Bengal"),
        ("TAMIL", "Alias: TAMIL -> Tamil Nadu"),
    ]

    for query, description in tests:
        result = get_state_portal(query)
        if result:
            print(f"  ✓ {description}: {result['name']} — {result['portal']}")
        else:
            print(f"  ✗ {description}: NOT FOUND (returned None)")

    print(f"\n  Total state portals registered: {len(ALL_STATES)}")
    print(f"  Scheme-specific portal entries: {len(SCHEME_STATE_PORTALS)}")

    # Test scheme-specific
    print("\n  Scheme-specific lookups:")
    for scheme, state in [("SMAM", "19"), ("CRM", "6"), ("CHC", "3"), ("FMB", "19"), ("NAMO_DRONE_DIDI", "6")]:
        portal, info = get_scheme_specific_portal(scheme, state)
        if portal:
            print(f"    {scheme}/{state}: {portal['portal_name']} — topup={portal.get('topup_available', False)}")
        else:
            print(f"    {scheme}/{state}: NOT FOUND")
