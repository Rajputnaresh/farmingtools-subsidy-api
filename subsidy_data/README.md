# Subsidy Client Data Assets (Peanuts)

## Overview
Component package providing static client-side JavaScript database artifacts for the farmingtools.in subsidy calculator widget and offline browser execution. These assets allow the embedded Shopify widget to calculate agricultural machinery subsidies and display document requirements instantly in the buyer's browser without requiring network calls to the backend API.

## Interface
- `window.STATES_DATA` (`subsidy_data/states_data.js`): Global array containing 38 Indian States and Union Territories with Census/NIC codes, names, and official state DBT agriculture portal URLs.
- `window.SCHEME_DOCS` (`subsidy_data/scheme_data.js`): Global dictionary mapping subsidy scheme identifiers (`SMAM`, `CRM`, `CHC`, `FMB`, `NAMO_DRONE_DIDI`, `RKVY`) to guideline URLs, beneficiary target groups, subsidy caps, and mandatory document checklists.
- `window.SUBSIDY_DB` (`subsidy_data/full_db.js`): Comprehensive client-side database mapping normalized machine IDs to eligible schemes, central subsidy caps, category multipliers, and state top-up rules.

## Invariants
- All files must be pure ES5/ES6 browser JavaScript runnable directly inside `<script>` tags without bundlers, transpilation, or external dependencies.
- State codes in `STATES_DATA` must be 2-digit string representations strictly aligned with national DBT standards.
- Data artifacts must remain strictly synchronized with `data/subsidy_master_latest.json` and `data/registration_info.json`; manual direct editing is prohibited. Regenerate via `export_subsidy_data.py`.

## Side Effects
- Injects `STATES_DATA`, `SCHEME_DOCS`, and `SUBSIDY_DB` into the browser global execution context (`window` object).
- Served statically with HTTP caching headers by `lambda_function.py` under the `/subsidy_data/*` path.

## Verification
- Run: `python3 -c "import os; assert os.path.exists('subsidy_data/full_db.js') and os.path.exists('subsidy_data/scheme_data.js') and os.path.exists('subsidy_data/states_data.js'); print('Client assets present')"`
