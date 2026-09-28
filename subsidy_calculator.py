#!/usr/bin/env python3
"""
Multi-Scheme Subsidy Calculator for farmingtools.in

Pure function: calculate_subsidy(machine_id, farmer_category, dealer_price, state_code=None, units=1, strict_state_match=True)
Covers ALL subsidy schemes:
  - SMAM 2024 (Sub-Mission on Agricultural Mechanization)
  - CRM 2020-21 (Crop Residue Management in Punjab, Haryana, UP, NCT Delhi)
  - CHC (Custom Hiring Centres - 40% up to ₹250 Lakhs, CRM CHC 80% up to ₹15 Lakhs, Graduate Drone 50% up to ₹9 Lakhs)
  - FMB (Farm Machinery Banks - 80% up to ₹30 Lakhs, FRA 90% up to ₹27 Lakhs, NER 95% up to ₹28.5 Lakhs)
  - Namo Drone Didi / Kisan Drone (80% up to ₹8 Lakhs for Women SHGs, 75% FPO, 50%/40% Individual)
  - RKVY (Farm Mechanization stream)
  - State Top-ups & verified state portals for all 38 Indian States/UTs.

Usage:
    from subsidy_calculator import calculate_subsidy, get_machine_list, get_states, get_scheme_list
    
    result = calculate_subsidy(
        machine_id="smam_i_tractor_2wd_08-20",
        farmer_category="SC",
        dealer_price=450000,
        state_code="19"  # West Bengal
    )
    print(result)
"""

import json
from pathlib import Path
from typing import Optional, Union

DATA_DIR = Path(__file__).parent / "data"
LATEST_DATA = DATA_DIR / "subsidy_master_latest.json"
REGISTRATION_DATA = DATA_DIR / "registration_info.json"


def _load_data() -> dict:
    """Load the latest subsidy master dataset."""
    if not LATEST_DATA.exists():
        raise FileNotFoundError(f"No subsidy data found at {LATEST_DATA}. Run build_multi_scheme_master.py first.")
    with open(LATEST_DATA, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_registration_info() -> dict:
    """Load registration guidelines and state portal metadata."""
    if not REGISTRATION_DATA.exists():
        return {}
    with open(REGISTRATION_DATA, "r", encoding="utf-8") as f:
        return json.load(f)


def get_states() -> list[dict]:
    """Get list of all 38 Indian States and Union Territories with NIC codes and portals."""
    reg = _load_registration_info()
    states_dict = reg.get("states", {})
    results = []
    for code, info in states_dict.items():
        results.append({
            "code": code,
            "name": info.get("name"),
            "portal": info.get("portal"),
            "portal_name": info.get("portal_name")
        })
    # Sort by numeric code if possible
    return sorted(results, key=lambda x: int(x["code"]) if x["code"].isdigit() else 999)


def get_state_code_mapping() -> dict[str, str]:
    """Return mapping of NIC state codes to uppercase state keys."""
    states = get_states()
    mapping = {}
    for s in states:
        code = s["code"]
        name_key = s["name"].upper().replace(" & ", "_").replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "").replace(".", "")
        mapping[code] = name_key
    # Add common aliases
    mapping.update({
        "19": "WEST_BENGAL",
        "6": "HARYANA",
        "3": "PUNJAB",
        "5": "UTTAR_PRADESH",
        "23": "MADHYA_PRADESH",
        "10": "BIHAR",
        "27": "MAHARASHTRA",
        "24": "GUJARAT",
        "8": "RAJASTHAN",
        "28": "ANDHRA_PRADESH",
        "29": "KARNATAKA",
        "33": "TAMIL_NADU",
        "36": "TELANGANA",
        "21": "ODISHA",
        "22": "CHHATTISGARH",
        "32": "KERALA",
        "18": "ASSAM"
    })
    return mapping


def _state_code_to_name(code: str) -> Optional[str]:
    """Map NIC state code to state key."""
    mapping = get_state_code_mapping()
    return mapping.get(str(code).strip())


def get_machine_list(state_code: Optional[str] = None,
                      scheme: Optional[str] = None,
                      category: Optional[str] = None) -> list[dict]:
    """
    Get list of available machines and equipment packages, optionally filtered.
    
    Args:
        state_code: NIC state code (e.g. "19" for WB, "6" for Haryana)
        scheme: Scheme code (e.g. "SMAM", "CRM", "CHC", "FMB", "NAMO_DRONE_DIDI")
        category: Machine category filter
    """
    data = _load_data()
    machines = data.get("machines", [])

    if scheme:
        scheme_upper = scheme.upper().strip()
        machines = [m for m in machines if m.get("central", {}).get("scheme", "").upper() == scheme_upper]

    if category:
        cat_upper = category.upper().strip()
        machines = [m for m in machines if cat_upper in m.get("category", "").upper()]

    if state_code:
        state_key = _state_code_to_name(state_code)
        # For CRM scheme, only Punjab, Haryana, UP, Delhi are eligible
        if scheme == "CRM" and state_key not in ["PUNJAB", "HARYANA", "UTTAR_PRADESH", "DELHI"]:
            return []

    return machines


def get_machine(machine_id: str) -> Optional[dict]:
    """Retrieve a single machine/package record by its machine_id."""
    data = _load_data()
    for m in data.get("machines", []):
        if m.get("machine_id") == machine_id:
            return m
    return None


def get_scheme_list(state_code: Optional[str] = None) -> list[dict]:
    """Get list of all supported subsidy schemes with official descriptions and sources."""
    data = _load_data()
    schemes = data.get("schemes", {})
    machines = data.get("machines", [])

    # Count machines per scheme
    counts = {}
    for m in machines:
        s = m.get("central", {}).get("scheme", "SMAM")
        counts[s] = counts.get(s, 0) + 1

    results = []
    for key, meta in schemes.items():
        results.append({
            "code": key,
            "name": meta.get("full_name", key),
            "source_doc": meta.get("source_doc"),
            "source_url": meta.get("source_url"),
            "source_date": meta.get("source_date"),
            "machine_count": counts.get(key, 0),
            "central_share": meta.get("central_share", "60% to 100%"),
            "primary_portal": meta.get("primary_portal", "https://agrimachinery.nic.in/")
        })
    return results


def get_farmer_categories() -> list[dict]:
    """List of selectable farmer categories with subsidy tier classification."""
    return [
        {"code": "SC", "label": "Scheduled Caste (SC) — 50% Priority", "priority": True},
        {"code": "ST", "label": "Scheduled Tribe (ST) — 50% Priority", "priority": True},
        {"code": "Small", "label": "Small Farmer (1-2 Hectare) — 50% Priority", "priority": True},
        {"code": "Marginal", "label": "Marginal Farmer (< 1 Hectare) — 50% Priority", "priority": True},
        {"code": "Women", "label": "Women Farmer — 50% Priority", "priority": True},
        {"code": "NE_State", "label": "North Eastern / Himalayan States — 50% Priority", "priority": True},
        {"code": "General", "label": "General Farmer — 40% Standard", "priority": False},
        {"code": "OBC", "label": "Other Backward Class (OBC) — 40% Standard", "priority": False},
        {"code": "FRA", "label": "Forest Rights Act (FRA) Patta Holder — 90% Special Tier", "priority": True},
        {"code": "SHG", "label": "Women Self Help Group (DAY-NRLM) — 80% Tier", "priority": True},
        {"code": "FPO", "label": "Farmer Producer Organization (FPO) — 75%-80% Tier", "priority": True},
        {"code": "Cooperative", "label": "Primary Agricultural Cooperative Society — 80% Tier", "priority": True},
        {"code": "Rural_Youth", "label": "Rural Youth / Entrepreneur (CHC) — 40% Tier", "priority": False}
    ]


def calculate_subsidy(machine_id: str,
                      farmer_category: str,
                      dealer_price: float,
                      state_code: Optional[Union[str, int]] = None,
                      units: int = 1,
                      strict_state_match: bool = True) -> dict:
    """
    Calculate subsidy for a given machine, farmer category, dealer price, and state.
    
    Returns central subsidy + state top-up + effective total + farmer contribution +
    required documents + step-by-step registration process + live verified links.
    """
    data = _load_data()
    reg_info = _load_registration_info()
    machine = get_machine(machine_id)

    if not machine:
        return {
            "error": f"Machine not found: {machine_id}",
            "hint": "Check machine_id against get_machine_list()",
            "available_machines_count": len(data.get("machines", []))
        }

    central = machine.get("central", {})
    scheme_code = central.get("scheme", "SMAM")
    total_dealer = float(dealer_price) * int(units)

    # 1. Determine priority eligibility
    eligible_priority = central.get("priority", {}).get("eligible_categories", [])
    is_priority = (farmer_category in eligible_priority) or (farmer_category in ["SC", "ST", "Small", "Marginal", "Women", "NE_State", "SHG", "FPO", "Cooperative", "FRA"])

    pct_config = central.get("priority", {}) if is_priority else central.get("general", {})
    applicable_pct = pct_config.get("percentage", 40)
    applicable_cap = pct_config.get("max_subsidy_rp", 0)

    # Central subsidy calculation
    central_subsidy = (applicable_pct / 100.0) * total_dealer
    central_applicable = min(central_subsidy, float(applicable_cap * units)) if applicable_cap > 0 else central_subsidy

    # 2. State Top-Up Calculation
    state_code_str = str(state_code).strip() if state_code is not None else None
    state_result = {"eligible": False, "applicable_amount": 0.0}
    state_subsidy_amount = 0.0
    state_name = None
    state_portal_info = None
    matched_topup = None

    if state_code_str:
        state_name = _state_code_to_name(state_code_str)
        states_reg = reg_info.get("states", {})
        state_portal_info = states_reg.get(state_code_str)

        if state_name:
            # Collect all matching state_topups for this state
            matching_topups = []
            for st in machine.get("state_topups", []):
                if st.get("state", "").upper() == state_name.upper():
                    matching_topups.append(st)

            matched_topup = None
            if matching_topups:
                # Score each match: prefer exact scheme match, then farmer-type compatibility
                central_scheme = machine.get("central", {}).get("scheme", "").upper()
                project_categories = {"FPO", "COOPERATIVE", "RURAL_YOUTH", "FRA"}
                is_project_purchase = farmer_category.upper() in project_categories

                def score_topup(st_entry):
                    st_scheme = st_entry.get("scheme", "").upper()
                    s = 0
                    # Exact scheme match (central scheme == state scheme) — strongest
                    if st_scheme == central_scheme:
                        s += 100
                    # State scheme is a project-type scheme (CHC/FMB) but central is individual (SMAM/CRM)
                    # — only allow if the state explicitly lists this machine under its scheme
                    # For individual purchases, non-project state schemes are preferred
                    if not is_project_purchase and st_scheme not in ("CHC", "FMB"):
                        s += 50
                    # For project purchases, FMB/CHC state schemes are compatible
                    if is_project_purchase and st_scheme in ("CHC", "FMB"):
                        s += 50
                    # Prefer entry with source_doc populated
                    if st_entry.get("source_doc"):
                        s += 1
                    return s

                matching_topups.sort(key=score_topup, reverse=True)
                best = matching_topups[0] if matching_topups else None
                # Require minimum score of 50: source_doc-only matches (score=1)
                # must not win when no scheme-compatible entry exists
                if best and score_topup(best) < 50:
                    best = None
                matched_topup = best

            if matched_topup:
                st_data = matched_topup.get("state_subsidy", {})
                st_pct = st_data.get("percentage", 0)
                st_flat = st_data.get("flat_amount_rp", 0)
                st_calc = (st_pct / 100.0) * total_dealer
                st_applicable = min(st_calc, float(st_flat * units)) if st_flat > 0 else st_calc

                state_subsidy_amount = st_applicable
                state_result = {
                    "eligible": True,
                    "state_name": state_name,
                    "percentage": st_pct,
                    "subsidy_amount": round(st_calc, 2),
                    "cap_per_unit": st_flat,
                    "applicable_amount": round(st_applicable, 2),
                    "source": st_data.get("source_doc", f"{state_name} Agriculture Department"),
                    "source_url": st_data.get("source_url", state_portal_info.get("portal") if state_portal_info else None),
                    "additional_incentive": st_data.get("additional_incentive")
                }
            else:
                # State specified but no state top-up for this machine
                portal_url = state_portal_info.get("portal") if state_portal_info else "https://agrimachinery.nic.in/"
                portal_title = state_portal_info.get("portal_name") if state_portal_info else f"{state_name} Agriculture Portal"
                state_result = {
                    "eligible": False,
                    "state_name": state_name,
                    "applicable_amount": 0.0,
                    "message": "No additional state top-up on record — central subsidy applies",
                    "contact_state_portal": portal_url,
                    "portal_name": portal_title,
                    "status": "Rate not available — contact state agriculture office"
                }

    # 3. Aggregation & Caps
    total_subsidy = central_applicable + state_subsidy_amount
    effective_subsidy = min(total_subsidy, total_dealer)
    farmer_contribution = max(0.0, total_dealer - effective_subsidy)

    # 4. Source Citation
    source_parts = [f"Central: {central.get('source_doc', 'SMAM Guidelines 2024')} ({central.get('source_date', '2024')})"]
    if state_result.get("eligible"):
        source_parts.append(f"State: {state_result.get('source', 'State Agriculture Department')}")
    elif state_portal_info:
        source_parts.append(f"State Portal: {state_portal_info.get('portal_name')} ({state_portal_info.get('portal')})")

    # 5. Documents Checklist
    scheme_details = reg_info.get("schemes", {}).get(scheme_code, {})
    documents_required = scheme_details.get("documents", [])
    if not documents_required:
        # Default fallback documents
        documents_required = [
            {"item": "Aadhaar Card (UID)", "mandatory": True, "purpose": "Farmer identity verification for DBT", "link": "https://uidai.gov.in/"},
            {"item": "Passport-size photo of farmer", "mandatory": True, "purpose": "Identity photograph for registration", "link": "https://agrimachinery.nic.in/Farmer/Management/Index"},
            {"item": "Record of Right (RoR) / 7-12 / Khasra-Khatauni", "mandatory": True, "purpose": "Proof of agricultural land holding", "link": "https://agrimachinery.nic.in/Farmer/Management/Index"},
            {"item": "Bank Passbook First Page copy", "mandatory": True, "purpose": "Bank account details for Direct Benefit Transfer (DBT)", "link": "https://agrimachinery.nic.in/Farmer/Management/Index"},
            {"item": "Caste Certificate (SC/ST/OBC)", "mandatory": is_priority, "purpose": "Priority subsidy rate eligibility", "link": "https://agrimachinery.nic.in/Farmer/Management/Index"}
        ]

    # 6. Registration Process & Live Links
    process_steps = scheme_details.get("process_steps", [
        "1. Register on agrimachinery.nic.in using Aadhaar & mobile number.",
        "2. Select District, Block, and Village from dropdowns.",
        "3. Upload land RoR, bank passbook, and photo.",
        "4. Choose machine and dealer, submit application for SLEC sanction.",
        "5. Physical verification followed by direct DBT credit to bank account."
    ])

    portals = reg_info.get("central_portals", {})
    registration_process = {
        "steps": process_steps,
        "scheme": scheme_code,
        "portal_main": portals.get("calculator", "https://agrimachinery.nic.in/index/assistanceCalculator"),
        "portal_register": portals.get("dbt_portal", "https://agrimachinery.nic.in/Farmer/Management/Index"),
        "portal_tracking": portals.get("tracking", "https://agrimachinery.nic.in/index/tracking"),
        "guidelines_pdf": central.get("source_url", portals.get("guidelines_smam_2024")),
        "helpdesk_email": portals.get("helpdesk_email", "support-agrimech@gov.in"),
        "state_portal": state_portal_info.get("portal") if state_portal_info else None,
        "state_portal_name": state_portal_info.get("portal_name") if state_portal_info else None
    }

    return {
        "machine_id": machine_id,
        "machine_name": machine.get("name"),
        "category": machine.get("category"),
        "scheme": scheme_code,
        "dealer_price": dealer_price,
        "units": units,
        "total_dealer_price": total_dealer,
        
        "farmer_category": farmer_category,
        "category_eligible_priority": is_priority,
        "applicable_percentage": applicable_pct,
        
        "central": {
            "scheme": scheme_code,
            "scheme_version": central.get("scheme_version", "SMAM 2024"),
            "percentage": applicable_pct,
            "subsidy_amount": round(central_subsidy, 2),
            "cap_per_unit": applicable_cap,
            "total_cap": applicable_cap * units,
            "applicable_amount": round(central_applicable, 2),
            "source_doc": central.get("source_doc"),
            "source_url": central.get("source_url")
        },
        
        "state_topup": state_result,
        "state_topups": machine.get("state_topups", []),
        "state_portal": state_portal_info.get("portal") if state_portal_info else None,
        "state_portal_name": state_portal_info.get("portal_name") if state_portal_info else None,
        
        "total_subsidy": round(total_subsidy, 2),
        "effective_subsidy": round(effective_subsidy, 2),
        "farmer_contribution": round(farmer_contribution, 2),
        
        "source_citation": " | ".join(source_parts),
        "central_source_doc": central.get("source_doc"),
        "central_source_url": central.get("source_url"),
        "source_doc": (matched_topup.get("state_subsidy", {}).get("source_doc") or matched_topup.get("source_doc")) if matched_topup else None,
        "source_url": (matched_topup.get("state_subsidy", {}).get("source_url") or matched_topup.get("source_url")) if matched_topup else (state_portal_info.get("portal") if state_portal_info else None),
        "data_freshness": data.get("metadata", {}).get("extracted_at"),
        
        "documents_required": documents_required,
        "registration_process": registration_process
    }


if __name__ == "__main__":
    print("=" * 70)
    print("  MULTI-SCHEME SUBSIDY CALCULATOR — VERIFICATION TESTS")
    print("=" * 70)

    # Test 1: Tractor 2WD (20-40 HP) — SMAM 2024 increased rate test
    print("\n📋 Test 1: Tractor 2WD (20-40 HP) — SC Category (50%)")
    r1 = calculate_subsidy("smam_iii_tractor_2wd_above_20-40", "SC", 600000)
    print(f"  Machine:    {r1['machine_name']}")
    print(f"  Central:    {r1['central']['percentage']}% → Cap: ₹{r1['central']['cap_per_unit']:,} | Amount: ₹{r1['central']['applicable_amount']:,}")
    print(f"  Farmer pay: ₹{r1['farmer_contribution']:,}")

    # Test 2: Tractor 4WD (20-40 HP) — General Category (40%)
    print("\n📋 Test 2: Tractor 4WD (20-40 HP) — General Category (40%)")
    r2 = calculate_subsidy("smam_iv_tractor_4wd_above_20-40", "General", 800000)
    print(f"  Machine:    {r2['machine_name']}")
    print(f"  Central:    {r2['central']['percentage']}% → Cap: ₹{r2['central']['cap_per_unit']:,} | Amount: ₹{r2['central']['applicable_amount']:,}")
    print(f"  Farmer pay: ₹{r2['farmer_contribution']:,}")

    # Test 3: CRM Super Seeder in Haryana
    print("\n📋 Test 3: CRM Super Seeder in Haryana (State Code 6)")
    r3 = calculate_subsidy("crm_super_seeder", "General", 250000, state_code="6")
    print(f"  Machine:    {r3['machine_name']}")
    print(f"  Scheme:     {r3['scheme']}")
    print(f"  Central:    {r3['central']['percentage']}% → ₹{r3['central']['applicable_amount']:,}")
    print(f"  State:      {r3['state_topup']}")
    print(f"  Farmer pay: ₹{r3['farmer_contribution']:,}")

    # Test 4: Namo Drone Didi Package for Women SHG
    print("\n📋 Test 4: Namo Drone Didi Package (Women SHG)")
    r4 = calculate_subsidy("namo_drone_didi_shg_package", "SHG", 1000000)
    print(f"  Machine:    {r4['machine_name']}")
    print(f"  Central:    {r4['central']['percentage']}% → Cap: ₹{r4['central']['cap_per_unit']:,} | Amount: ₹{r4['central']['applicable_amount']:,}")
    print(f"  Farmer pay: ₹{r4['farmer_contribution']:,}")

    # Test 5: Custom Hiring Centre (SMAM Component 4.2)
    print("\n📋 Test 5: Custom Hiring Centre (CHC) Project (₹50 Lakhs)")
    r5 = calculate_subsidy("chc_custom_hiring_centre_smam", "Rural_Youth", 5000000)
    print(f"  Package:    {r5['machine_name']}")
    print(f"  Subsidy:    {r5['central']['percentage']}% → Cap: ₹{r5['central']['cap_per_unit']:,} | Amount: ₹{r5['central']['applicable_amount']:,}")
    print(f"  Farmer pay: ₹{r5['farmer_contribution']:,}")

    print("\n✅ All calculator verification tests executed successfully.")
