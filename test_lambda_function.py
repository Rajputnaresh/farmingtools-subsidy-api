"""
Unit test suite for AWS Lambda handler (lambda_function.py)
Tests Function URLs (Payload v2.0), API Gateway (v1.0), CORS, and static asset serving.
"""

import json
from lambda_function import lambda_handler

def test_lambda_suite():
    print("Testing AWS Lambda Handler...")
    passed = 0
    total = 0

    def check(name, condition, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"  ✅ [PASS] {name}")
        else:
            print(f"  ❌ [FAIL] {name}: {details}")

    # 1. Health check (Function URL v2 format)
    v2_health_event = {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/health",
        "rawQueryString": "",
        "requestContext": {
            "http": {
                "method": "GET",
                "path": "/health"
            }
        }
    }
    resp = lambda_handler(v2_health_event)
    check("Function URL v2 /health", resp["statusCode"] == 200 and "farmingtools-subsidy-api" in resp["body"])

    # 2. CORS Pre-flight (OPTIONS)
    options_event = {
        "version": "2.0",
        "rawPath": "/api/subsidy/calculate",
        "requestContext": {"http": {"method": "OPTIONS"}}
    }
    resp = lambda_handler(options_event)
    check("CORS OPTIONS pre-flight", resp["statusCode"] == 204 and resp["headers"]["Access-Control-Allow-Origin"] == "*")

    # 3. States list
    states_event = {
        "version": "2.0",
        "rawPath": "/api/subsidy/states",
        "requestContext": {"http": {"method": "GET"}}
    }
    resp = lambda_handler(states_event)
    data = json.loads(resp["body"])
    check("States endpoint", resp["statusCode"] == 200 and len(data.get("states", [])) >= 28)

    # 4. Machines list
    machines_event = {
        "version": "2.0",
        "rawPath": "/api/subsidy/machines",
        "requestContext": {"http": {"method": "GET"}}
    }
    resp = lambda_handler(machines_event)
    data = json.loads(resp["body"])
    check("Machines endpoint", resp["statusCode"] == 200 and data.get("count", 0) > 100)

    # 5. Calculation via GET with rawQueryString
    calc_get_event = {
        "version": "2.0",
        "rawPath": "/api/subsidy/calculate",
        "rawQueryString": "machine_id=smam_i_tractor_2wd_08-20&farmer_category=SC&dealer_price=450000&state_code=PB&units=1",
        "requestContext": {"http": {"method": "GET"}}
    }
    resp = lambda_handler(calc_get_event)
    data = json.loads(resp["body"])
    d = data.get("data", {})
    check("Calculate GET (Punjab Tractor SC 50% cap 200k)", 
          resp["statusCode"] == 200 and d.get("total_subsidy", 0) == 200000.0 and d.get("applicable_percentage") == 50,
          f"data: {d}")

    # 6. Calculation via POST with JSON body
    calc_post_event = {
        "version": "2.0",
        "rawPath": "/api/subsidy/calculate",
        "requestContext": {"http": {"method": "POST"}},
        "body": json.dumps({
            "machine_id": "crm_happy_seeder_09_tine",
            "farmer_category": "Small/Marginal",
            "dealer_price": 180000,
            "state_code": "HR",
            "units": 2
        }),
        "isBase64Encoded": False
    }
    resp = lambda_handler(calc_post_event)
    data = json.loads(resp["body"])
    d = data.get("data", {})
    check("Calculate POST (CRM Seeder units=2)", 
          resp["statusCode"] == 200 and d.get("units") == 2 and d.get("total_subsidy", 0) > 0,
          f"data: {d}")

    # 7. Static widget HTML serving
    widget_event = {
        "version": "2.0",
        "rawPath": "/",
        "requestContext": {"http": {"method": "GET"}}
    }
    resp = lambda_handler(widget_event)
    check("Static widget HTML at /",
          resp["statusCode"] == 200 and "text/html" in resp["headers"]["Content-Type"] and "farmingtools.in" in resp["body"].lower())

    # 8. Static JS data serving
    js_event = {
        "version": "2.0",
        "rawPath": "/subsidy_data/full_db.js",
        "requestContext": {"http": {"method": "GET"}}
    }
    resp = lambda_handler(js_event)
    check("Static JS at /subsidy_data/full_db.js",
          resp["statusCode"] == 200 and "application/javascript" in resp["headers"]["Content-Type"] and "FULL_DB" in resp["body"])

    # 9. API Gateway v1.0 payload format compatibility
    v1_event = {
        "httpMethod": "GET",
        "path": "/api/subsidy/calculate",
        "queryStringParameters": {
            "machine_id": "smam_i_tractor_2wd_08-20",
            "farmer_category": "General",
            "dealer_price": "500000"
        }
    }
    resp = lambda_handler(v1_event)
    data = json.loads(resp["body"])
    d = data.get("data", {})
    check("API Gateway v1.0 compatibility (General 40% cap 160k)",
          resp["statusCode"] == 200 and d.get("total_subsidy") == 160000.0)

    print(f"\nLambda Handler Test Summary: {passed}/{total} Passed")
    return passed == total

if __name__ == "__main__":
    success = test_lambda_suite()
    exit(0 if success else 1)
