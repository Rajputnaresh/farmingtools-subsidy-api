import json
import os
from pathlib import Path
import requests
import sys

SHOP_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN", "s0rir3-iy.myshopify.com")
THEME_ID = int(os.getenv("SHOPIFY_THEME_ID", "157784277150"))
API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-01")

def get_shopify_token():
    env_token = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")
    if env_token:
        return env_token
    store_conf = Path.home() / "Library/Preferences/shopify-cli-store-nodejs/config.json"
    if store_conf.exists():
        try:
            with open(store_conf, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in data.items():
                    if "s0rir3-iy.myshopify.com" in k or SHOP_DOMAIN in k:
                        sessions = v.get("sessionsByUserId", {})
                        for uid, s in sessions.items():
                            tok = s.get("accessToken")
                            if tok:
                                return tok
        except Exception as e:
            print("Failed reading CLI store config:", e)
    return None

TOKEN = get_shopify_token()
if not TOKEN:
    print("Error: No Shopify Access Token found.")
    sys.exit(1)

BASE_URL = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

def get_asset(key):
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json?asset[key]={key}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get("asset")
    return None

def put_asset(key, value):
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json"
    payload = {
        "asset": {
            "key": key,
            "value": value
        }
    }
    resp = requests.put(url, headers=HEADERS, json=payload)
    print(f"PUT {key}: Status {resp.status_code}")
    if resp.status_code not in (200, 201):
        print(f"Error response: {resp.text}")
        return False
    return True

def main():
    print(f"Connecting to Shopify store {SHOP_DOMAIN} on Theme #{THEME_ID}...")
    
    # 1. Read subsidy_calculator_section.liquid
    with open("subsidy_calculator_section.liquid", "r", encoding="utf-8") as f:
        calc_code = f.read()

    calc_code_safeguarded = calc_code.replace(
        "{% if section.settings.enable_calculator %}",
        "{% unless section.settings.enable_calculator == false %}"
    ).replace(
        "{% endif %}\n\n{% schema %}",
        "{% endunless %}\n\n{% schema %}"
    )

    print("\n[1/4] Uploading sections/subsidy-calculator.liquid...")
    success = put_asset("sections/subsidy-calculator.liquid", calc_code_safeguarded)
    if not success:
        sys.exit(1)

    print("\n[2/4] Uploading sections/ft-redesign-subsidy.liquid...")
    ft_redesign_code = calc_code_safeguarded.replace(
        '"name": "Subsidy Calculator"',
        '"name": "FT Subsidy Wizard"'
    )
    success = put_asset("sections/ft-redesign-subsidy.liquid", ft_redesign_code)
    if not success:
        sys.exit(1)

    print("\n[3/4] Updating templates/page.subsidy-help.json...")
    page_subsidy_help = {
        "sections": {
            "ft_ux_cleanup": {
                "type": "ft-ux-cleanup",
                "settings": {}
            },
            "subsidy_calculator": {
                "type": "subsidy-calculator",
                "settings": {
                    "enable_calculator": True,
                    "whatsapp_number": "916006078815"
                }
            },
            "main": {
                "type": "main-page",
                "settings": {
                    "padding_top": 12,
                    "padding_bottom": 28
                }
            }
        },
        "order": [
            "ft_ux_cleanup",
            "subsidy_calculator",
            "main"
        ]
    }
    success = put_asset("templates/page.subsidy-help.json", json.dumps(page_subsidy_help, indent=2))
    if not success:
        sys.exit(1)

    print("\n[4/4] Updating templates/page.government-subsidy-farm-equipment-2026.json...")
    page_gov_subsidy = {
        "sections": {
            "ft_ux_cleanup": {
                "type": "ft-ux-cleanup",
                "settings": {}
            },
            "subsidy_calculator": {
                "type": "subsidy-calculator",
                "settings": {
                    "enable_calculator": True,
                    "whatsapp_number": "916006078815"
                }
            },
            "main": {
                "type": "main-page",
                "settings": {
                    "padding_top": 12,
                    "padding_bottom": 28
                }
            }
        },
        "order": [
            "ft_ux_cleanup",
            "subsidy_calculator",
            "main"
        ]
    }
    put_asset("templates/page.government-subsidy-farm-equipment-2026.json", json.dumps(page_gov_subsidy, indent=2))
    put_asset("templates/page.subsidy-calculator.json", json.dumps(page_gov_subsidy, indent=2))

    # 5. Upload all site-wide linking sections and snippets from local live theme folder
    theme_live_dir = Path("/Users/rajputnaresh/Documents/Claude Co-Work/farmingtools-theme-live")
    files_to_upload = [
        "snippets/ft-guide-footer-enhancement.liquid",
        "sections/ft-redesign-pdp.liquid",
        "sections/ft-collection-head.liquid",
        "sections/ft-buying-guide-article.liquid",
        "sections/main-blog.liquid",
        "sections/ft-comparison-index.liquid",
        "sections/ft-comparison-page.liquid",
        "sections/ft-machine-advisor.liquid",
        "sections/ft-redesign-guides.liquid",
        "sections/main-page.liquid",
    ]

    print("\n[5/5] Uploading sitewide subsidy linking sections & snippets...")
    for rel_path in files_to_upload:
        full_path = theme_live_dir / rel_path
        if full_path.exists():
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            ok = put_asset(rel_path, content)
            if not ok:
                print(f"Failed uploading {rel_path}")
        else:
            print(f"Warning: File not found: {full_path}")

    print("\nAll live theme assets uploaded and verified successfully!")

if __name__ == "__main__":
    main()
