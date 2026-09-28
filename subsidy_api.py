#!/usr/bin/env python3
"""
Lightweight Subsidy API server for farmingtools.in
Provides REST endpoints for:
  - GET  /api/subsidy/schemes
  - GET  /api/subsidy/states
  - GET  /api/subsidy/categories
  - GET  /api/subsidy/machines
  - GET  /api/subsidy/calculate
  - POST /api/subsidy/calculate

Zero external dependencies: uses Python standard library `http.server` & `wsgiref`.
Fully CORS enabled for cross-origin requests from Shopify storefront (farmingtools.in).
"""

import json
import os
import sys
from datetime import datetime
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from subsidy_calculator import (
    calculate_subsidy,
    get_machine_list,
    get_machine,
    get_scheme_list,
    get_states,
    get_farmer_categories
)


def handle_api_request(method: str, path: str, query_params: dict, body: dict = None) -> tuple[int, dict]:
    """Pure router for subsidy API requests."""
    parsed_path = path.rstrip("/")

    # Health check
    if parsed_path in ["", "/health", "/api/health"]:
        return HTTPStatus.OK, {
            "status": "healthy",
            "service": "farmingtools-subsidy-api",
            "version": "3.0.0",
            "schemes": ["SMAM", "CRM", "CHC", "FMB", "NAMO_DRONE_DIDI", "RKVY"]
        }

    # Schemes list
    if parsed_path == "/api/subsidy/schemes":
        state_code = query_params.get("state_code", [None])[0]
        return HTTPStatus.OK, {
            "success": True,
            "schemes": get_scheme_list(state_code=state_code)
        }

    # States list (all 38 Indian States & UTs with portal links)
    if parsed_path == "/api/subsidy/states":
        return HTTPStatus.OK, {
            "success": True,
            "states": get_states()
        }

    # Farmer categories
    if parsed_path == "/api/subsidy/categories":
        return HTTPStatus.OK, {
            "success": True,
            "categories": get_farmer_categories()
        }

    # Machines list
    if parsed_path == "/api/subsidy/machines":
        scheme = query_params.get("scheme", [None])[0]
        cat = query_params.get("category", [None])[0]
        state = query_params.get("state_code", [None])[0]
        machines = get_machine_list(state_code=state, scheme=scheme, category=cat)
        
        # Return clean subset for frontend dropdowns
        machine_items = []
        for m in machines:
            c = m.get("central", {})
            machine_items.append({
                "machine_id": m.get("machine_id"),
                "name": m.get("name"),
                "category": m.get("category"),
                "scheme": c.get("scheme", "SMAM"),
                "priority_pct": c.get("priority", {}).get("percentage", 50),
                "priority_cap": c.get("priority", {}).get("max_subsidy_rp", 0),
                "general_pct": c.get("general", {}).get("percentage", 40),
                "general_cap": c.get("general", {}).get("max_subsidy_rp", 0),
                "has_state_topups": len(m.get("state_topups", [])) > 0
            })
        return HTTPStatus.OK, {
            "success": True,
            "count": len(machine_items),
            "machines": machine_items
        }

    # Subsidy calculation
    if parsed_path in ["/api/subsidy", "/api/subsidy/calculate"]:
        params = body if (method == "POST" and body) else {}
        if not params:
            # Extract from query params
            params = {k: v[0] for k, v in query_params.items()}

        mid = params.get("machine_id")
        cat = params.get("farmer_category", params.get("category", "General"))
        price_raw = params.get("dealer_price", params.get("price", 0))
        state = params.get("state_code", params.get("state", None))
        units_raw = params.get("units", 1)

        if not mid:
            return HTTPStatus.BAD_REQUEST, {
                "success": False,
                "error": "Missing required parameter: machine_id"
            }

        try:
            price = float(price_raw)
            units = int(units_raw)
        except ValueError:
            return HTTPStatus.BAD_REQUEST, {
                "success": False,
                "error": "Invalid numeric format for dealer_price or units"
            }

        result = calculate_subsidy(
            machine_id=mid,
            farmer_category=cat,
            dealer_price=price,
            state_code=state,
            units=units
        )

        if "error" in result:
            return HTTPStatus.NOT_FOUND, {
                "success": False,
                **result
            }

        return HTTPStatus.OK, {
            "success": True,
            "data": result
        }

    return HTTPStatus.NOT_FOUND, {
        "success": False,
        "error": f"Endpoint not found: {path}",
        "available_endpoints": [
            "/health",
            "/api/subsidy/schemes",
            "/api/subsidy/states",
            "/api/subsidy/categories",
            "/api/subsidy/machines",
            "/api/subsidy/calculate"
        ]
    }


class SubsidyHTTPRequestHandler(BaseHTTPRequestHandler):
    """Standard HTTP request handler with full CORS support."""

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json", cache_control: str = "no-cache, no-store, must-revalidate"):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Cache-Control", cache_control)
        self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self._set_headers(HTTPStatus.NO_CONTENT)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # ── Static file serving (widget + data files) ────────────────────
        if path == "/" or path == "/subsidy_widget.html":
            try:
                html_path = BASE_DIR / "subsidy_widget.html"
                content = html_path.read_bytes()
                self._set_headers(HTTPStatus.OK, "text/html; charset=utf-8", "public, max-age=3600")
                self.wfile.write(content)
                return
            except FileNotFoundError:
                pass

        if path.startswith("/subsidy_data/"):
            try:
                file_path = BASE_DIR / path.lstrip("/")
                content = file_path.read_bytes()
                self._set_headers(HTTPStatus.OK, "application/javascript; charset=utf-8", "public, max-age=86400")
                self.wfile.write(content)
                return
            except FileNotFoundError:
                pass

        # API request
        query_params = parse_qs(parsed.query)
        status, response = handle_api_request("GET", path, query_params)
        self._set_headers(status)
        self.wfile.write(json.dumps(response, indent=2).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        query_params = parse_qs(parsed.query)
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = {}
        if content_length > 0:
            try:
                body_bytes = self.rfile.read(content_length)
                body = json.loads(body_bytes.decode("utf-8"))
            except Exception as e:
                self._set_headers(HTTPStatus.BAD_REQUEST)
                self.wfile.write(json.dumps({"success": False, "error": f"Malformed JSON: {e}"}).encode("utf-8"))
                return

        status, response = handle_api_request("POST", parsed.path, query_params, body=body)
        self._set_headers(status)
        self.wfile.write(json.dumps(response, indent=2).encode("utf-8"))

    def log_message(self, format, *args):
        # Concise logging
        sys.stderr.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]} {args[1]} {args[2]}\n")


# WSGI Application entry point for Gunicorn / Render / Serverless
def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")
    query_string = environ.get("QUERY_STRING", "")
    query_params = parse_qs(query_string)

    # ── Static file serving (widget + data files) ──────────────────────────
    if path == "/" or path == "/subsidy_widget.html":
        try:
            html_path = BASE_DIR / "subsidy_widget.html"
            content = html_path.read_bytes()
            headers = [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Cache-Control", "public, max-age=3600"),
                ("Access-Control-Allow-Origin", "*"),
            ]
            start_response("200 OK", headers)
            return [content]
        except FileNotFoundError:
            pass

    if path.startswith("/subsidy_data/"):
        try:
            file_path = BASE_DIR / path.lstrip("/")
            content = file_path.read_bytes()
            mime = "application/javascript; charset=utf-8"
            headers = [
                ("Content-Type", mime),
                ("Cache-Control", "public, max-age=86400"),
                ("Access-Control-Allow-Origin", "*"),
            ]
            start_response("200 OK", headers)
            return [content]
        except FileNotFoundError:
            pass

    # Handle CORS pre-flight
    if method == "OPTIONS":
        status_str = "204 No Content"
        headers = [
            ("Content-Type", "application/json"),
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
            ("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With"),
        ]
        start_response(status_str, headers)
        return [b""]

    body = {}
    if method == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            if content_length > 0:
                body_bytes = environ["wsgi.input"].read(content_length)
                body = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            body = {}

    status, response = handle_api_request(method, path, query_params, body)
    status_str = f"{status.value} {status.phrase}"
    headers = [
        ("Content-Type", "application/json"),
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
        ("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With"),
        ("Cache-Control", "no-cache, no-store, must-revalidate")
    ]
    start_response(status_str, headers)
    return [json.dumps(response).encode("utf-8")]


# Alias for gunicorn/render
app = application


def run_standalone_server(port: int = 8080):
    """Run built-in HTTP server."""
    server_address = ("", port)
    HTTPServer.allow_reuse_address = True
    httpd = HTTPServer(server_address, SubsidyHTTPRequestHandler)
    print(f"🚀 Subsidy API Server listening on port {port}...")
    print(f"   Health check: http://localhost:{port}/health")
    print(f"   Calculate:    http://localhost:{port}/api/subsidy/calculate?machine_id=smam_i_tractor_2wd_08-20&farmer_category=SC&dealer_price=450000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()


if __name__ == "__main__":
    port_env = os.environ.get("PORT", "").strip()
    port = int(port_env) if port_env.isdigit() else int(sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8080)
    run_standalone_server(port)
