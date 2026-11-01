# FarmingTools Subsidy API Blueprint

## System Overview
The FarmingTools Subsidy API subsystem powers the multi-scheme agricultural machinery subsidy calculation engine, official portal directory, and embeddable calculator widget for [farmingtools.in](https://farmingtools.in). It computes financial assistance across central government schemes (SMAM 2024, CRM, CHC, FMB, Namo Drone Didi, RKVY) and state top-up programs across all 38 Indian States and Union Territories. Designed for high availability and zero operational overhead, the system runs as a serverless AWS Lambda function with zero third-party runtime dependencies.

## Local Interface & Invariants

### Pure Calculation Engine (`subsidy_calculator.py`)
- `calculate_subsidy(machine_id, farmer_category, dealer_price, state_code=None, units=1, strict_state_match=True)`: Pure deterministic function calculating central subsidy allocation, state top-ups, net payable farmer cost, and statutory document checklists.
- `get_machine_list(state_code=None, scheme=None, category=None)`: Catalog retrieval for active machinery models with category-specific assistance rates and price caps.
- `get_machine(machine_id)`: Fetches complete subsidy and technical specification for a single machine.
- `get_states()`: Directory listing of all 38 Indian States and Union Territories with Census/NIC codes and verified DBT agriculture portal links.
- `get_scheme_list(state_code=None)`: Returns active central and state mechanization schemes.
- `get_farmer_categories()`: Supported beneficiary classification tiers (`SC`, `ST`, `SMALL_MARGINAL`, `WOMEN`, `GENERAL`, `OBC`, `FPO`, `SHG`, `PANCHAYAT`, `COOPERATIVE`).

### HTTP API Router (`subsidy_api.py`)
- `handle_api_request(method: str, path: str, query_params: dict, body: dict = None) -> tuple[int, dict]`: Stateless REST router serving `/health`, `/api/subsidy/schemes`, `/api/subsidy/states`, `/api/subsidy/categories`, `/api/subsidy/machines`, and `/api/subsidy/calculate`.
- `run_server(port=8080)`: Development HTTP server running on standard library `http.server`.

### Serverless Entrypoint & Asset Server (`lambda_function.py`)
- `lambda_handler(event: dict, context=None) -> dict`: Universal AWS Lambda handler supporting Function URLs (Payload v2.0), API Gateway HTTP API (v2.0), and REST API (v1.0). Serves both dynamic API routes and static asset paths (`/`, `/subsidy_widget.html`, `/subsidy_data/*`).
- `build_response(status_code, body_content, content_type, cache_control, is_base64)`: Lambda proxy response formatter injecting standard Shopify storefront CORS headers.

### Data ETL & Build Pipeline (`build_multi_scheme_master.py`, `export_subsidy_data.py`, `subsidy_pipeline.py`)
- `build_master()` (`build_multi_scheme_master.py`): Parses government scheme guidelines and updates `data/subsidy_master_latest.json`.
- `export_states()`, `export_schemes()`, `export_full_db()` (`export_subsidy_data.py`): Compiles master JSON records into offline client-side JavaScript assets in `subsidy_data/`.
- `run_pipeline()` (`subsidy_pipeline.py`): Orchestrator for daily sync, data validation, export generation, and deployment packaging.

## Subdirectories & System Boundaries
- [Subsidy Client Data Assets (Peanuts)](./subsidy_data/README.md) - Precompiled static client JavaScript bundles (`full_db.js`, `scheme_data.js`, `states_data.js`) for browser-side offline computation in the embedded Shopify storefront widget.

## Global Invariants
- **Zero Runtime Dependencies**: The entire core calculator, API router, and AWS Lambda handler must run strictly using Python standard library modules (`json`, `pathlib`, `urllib`, `http`, `typing`). No external pip packages may be introduced to the production execution environment.
- **Statutory Financial Caps**: Subsidy computations must strictly cap financial assistance at statutory government maximums (e.g. SMAM 2024 Annexure-I limits) regardless of dealer list prices.
- **Cross-Origin Permissiveness**: All API endpoints and asset routes must emit `Access-Control-Allow-Origin: *` headers to allow embedding within Shopify liquid themes (`subsidy_calculator_section.liquid`) and dealer portals.
- **Data Parity**: The backend Python calculation engine and the frontend JavaScript widget (`subsidy_data/`) must remain synchronized with identical values sourced from `data/subsidy_master_latest.json`.

## Global Side Effects
- Reads local datasets (`data/subsidy_master_latest.json`, `data/registration_info.json`) during calculations.
- Emits bundled deployment archives (`subsidy_lambda.zip`) and updates static script assets during ETL builds.
- Serves HTTP requests via AWS Lambda Function URLs with zero persistent state.

## System Verification
- Run: `python3 test_lambda_function.py && python3 end_to_end_verify.py`
