"""
AWS Lambda handler for farmingtools.in subsidy calculator API & widget.

Supports:
  1. AWS Lambda Function URLs (Payload format 2.0) — zero-cost direct HTTPS endpoint.
  2. AWS API Gateway HTTP API (Payload format 2.0).
  3. AWS API Gateway REST API (Payload format 1.0).

Endpoints served:
  - GET  /                                  -> subsidy_widget.html
  - GET  /subsidy_widget.html               -> subsidy_widget.html
  - GET  /subsidy_data/<file>.js            -> static JS data asset
  - GET  /health                            -> service health check
  - GET  /api/subsidy/schemes               -> available schemes
  - GET  /api/subsidy/states                -> all 38 states/UTs with portals
  - GET  /api/subsidy/categories            -> farmer categories & priority list
  - GET  /api/subsidy/machines              -> machines list (with scheme/caps)
  - GET  /api/subsidy/calculate             -> calculate subsidy (query params)
  - POST /api/subsidy/calculate             -> calculate subsidy (JSON body)
  - OPTIONS /*                              -> CORS pre-flight

Zero external dependencies — pure Python standard library.
"""

import base64
import json
import os
import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote

# Ensure current directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from subsidy_api import handle_api_request

# Standard CORS headers for Shopify storefront integration
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
}


def build_response(status_code: int, body_content: str, content_type: str = "application/json", cache_control: str = None, is_base64: bool = False) -> dict:
    """Build a standard Lambda proxy response compatible with Function URLs & API Gateway."""
    headers = {
        **CORS_HEADERS,
        "Content-Type": content_type,
    }
    if cache_control:
        headers["Cache-Control"] = cache_control
    else:
        headers["Cache-Control"] = "no-cache, no-store, must-revalidate"

    return {
        "statusCode": status_code,
        "headers": headers,
        "body": body_content,
        "isBase64Encoded": is_base64
    }


def lambda_handler(event: dict, context=None) -> dict:
    """Universal AWS Lambda handler for Function URLs, HTTP API, and REST API."""
    if not isinstance(event, dict):
        return build_response(400, json.dumps({"error": "Invalid event format"}))

    # ── 1. Extract HTTP Method ─────────────────────────────────────────────
    # Payload v2.0 (Function URL / HTTP API): event["requestContext"]["http"]["method"]
    # Payload v1.0 (REST API): event["httpMethod"]
    method = (
        event.get("requestContext", {}).get("http", {}).get("method")
        or event.get("httpMethod")
        or "GET"
    ).upper()

    # ── 2. Handle CORS Pre-flight (OPTIONS) ─────────────────────────────────
    if method == "OPTIONS":
        return {
            "statusCode": 204,
            "headers": {
                **CORS_HEADERS,
                "Content-Type": "application/json",
            },
            "body": "",
            "isBase64Encoded": False
        }

    # ── 3. Extract Path ────────────────────────────────────────────────────
    # Payload v2.0: event["rawPath"]
    # Payload v1.0: event["path"]
    path = event.get("rawPath") or event.get("path") or "/"
    # Clean any multiple slashes
    if path.startswith("//"):
        path = "/" + path.lstrip("/")

    # ── 4. Extract Query Parameters ────────────────────────────────────────
    raw_qs = event.get("rawQueryString", "")
    if raw_qs:
        query_params = parse_qs(raw_qs)
    else:
        # Fallback to queryStringParameters dictionary
        qs_params = event.get("queryStringParameters") or {}
        query_params = {}
        for k, v in qs_params.items():
            query_params[k] = v if isinstance(v, list) else [v]

    # ── 5. Extract Body (for POST requests) ────────────────────────────────
    body = {}
    if method == "POST":
        raw_body = event.get("body")
        if raw_body:
            if event.get("isBase64Encoded", False):
                try:
                    raw_body = base64.b64decode(raw_body).decode("utf-8")
                except Exception:
                    pass
            try:
                body = json.loads(raw_body)
            except Exception:
                body = {}

    # ── 6. Serve Static Files (Widget HTML & JS assets) ───────────────────
    if path in ["/", "/subsidy_widget.html"]:
        widget_file = BASE_DIR / "subsidy_widget.html"
        if widget_file.exists():
            return build_response(
                status_code=200,
                body_content=widget_file.read_text(encoding="utf-8"),
                content_type="text/html; charset=utf-8",
                cache_control="public, max-age=3600"
            )

    if path.startswith("/subsidy_data/"):
        rel_path = path.lstrip("/")
        asset_file = BASE_DIR / rel_path
        if asset_file.exists() and asset_file.is_file():
            return build_response(
                status_code=200,
                body_content=asset_file.read_text(encoding="utf-8"),
                content_type="application/javascript; charset=utf-8",
                cache_control="public, max-age=86400"
            )

    # ── 7. Handle Subsidy API Endpoints ────────────────────────────────────
    status, response_data = handle_api_request(
        method=method,
        path=path,
        query_params=query_params,
        body=body
    )

    return build_response(
        status_code=status.value if hasattr(status, "value") else int(status),
        body_content=json.dumps(response_data, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
        cache_control="no-cache, no-store, must-revalidate"
    )
