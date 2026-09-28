#!/usr/bin/env python3
"""End-to-end verification of the subsidy calculator system."""
import subprocess, time, json, urllib.request, os, sys

def run():
    port = '9994'
    proc = subprocess.Popen(
        ['python3', 'subsidy_api.py', port],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={**os.environ, 'PORT': port}
    )
    time.sleep(2)
    base = f'http://localhost:{port}'

    def get(path):
        try:
            r = urllib.request.urlopen(base + path, timeout=5)
            return r.status, r.read()
        except Exception as e:
            return 0, str(e).encode()[:100]

    def post(path, data):
        try:
            req = urllib.request.Request(base + path,
                data=json.dumps(data).encode(),
                headers={'Content-Type': 'application/json'},
                method='POST')
            r = urllib.request.urlopen(req, timeout=5)
            return r.status, json.loads(r.read())
        except Exception as e:
            return 0, str(e).encode()[:100]

    print('=== END-TO-END VERIFICATION ===')
    
    ok = True
    
    # Widget HTML
    st, body = get('/')
    txt = body.decode() if isinstance(body, bytes) else ''
    print(f'1. Widget HTML: {len(txt):,} chars')
    refs = {'states_data.js': 'states_data.js' in txt, 
            'scheme_data.js': 'scheme_data.js' in txt,
            'full_db.js': 'full_db.js' in txt}
    for f, present in refs.items():
        mark = 'OK' if present else 'MISSING'
        print(f'   {f}: {mark}')
        if not present: ok = False
    print()
    
    # Data files
    for fname, min_size in [('states_data.js', 100), ('scheme_data.js', 100), ('full_db.js', 10000)]:
        st, body = get(f'/subsidy_data/{fname}')
        ok_file = isinstance(body, bytes) and len(body) > min_size
        print(f'2. /subsidy_data/{fname}: {len(body):,} bytes {"OK" if ok_file else "FAIL"}')
        if not ok_file: ok = False
    print()
    
    # API
    for ep in ['/health', '/api/subsidy/schemes', '/api/subsidy/states', '/api/subsidy/machines']:
        st, body = get(ep)
        if isinstance(body, bytes) and st == 200:
            try:
                d = json.loads(body)
                items = d.get('schemes') or d.get('states') or d.get('machines') or d.get('count', 0)
                count = len(items) if isinstance(items, (list, tuple, dict)) else items
                print(f'3. GET {ep}: {count} items OK')
            except Exception as e:
                print(f'3. GET {ep}: FAIL ({e})')
                ok = False
        else:
            print(f'3. GET {ep}: FAIL ({body[:50]})')
            ok = False
    print()
    
    # Calculator tests
    tests = [
        ('SMAM SC UP (individual, no state top-up)', 'smam_i_tractor_2wd_08-20', 'SC', 500000, '5',
         200000, False),
        ('SMAM FPO WB (project-compatible state top-up)', 'smam_i_tractor_2wd_08-20', 'FPO', 500000, '19',
         200000, True),
        ('Haryana CRM SC Super Seeder (with state top-up)', 'crm_super_seeder', 'SC', 210000, '6',
         105000, True),
        ('Punjab CRM General Super Seeder (with state top-up)', 'crm_super_seeder', 'General', 250000, '3',
         105000, True),
        ('Namo Drone Didi SHG Package', 'namo_drone_didi_shg_package', 'SHG', 1000000, '6',
         800000, False),
    ]
    
    for name, mid, cat, price, state, exp_central_min, exp_state in tests:
        st, body = post('/api/subsidy/calculate', {
            'machine_id': mid, 'farmer_category': cat,
            'dealer_price': price, 'state_code': state
        })
        if isinstance(body, dict):
            data = body.get('data', {})
            central = data.get('central', {}).get('subsidy_amount', 0)
            st_elig = data.get('state_topup', {}).get('eligible', False)
            total = data.get('total_subsidy', 0)
            c_ok = central >= exp_central_min
            s_ok = (st_elig == exp_state)
            status = 'OK' if (c_ok and s_ok) else 'FAIL'
            if not status == 'OK': ok = False
            print(f'4. {name}: central=Rs{central:,.0f} state={"elig" if st_elig else "none"} total=Rs{total:,.0f} -- {status}')
        else:
            print(f'4. {name}: FAIL (API error)')
            ok = False
    
    proc.terminate()
    proc.wait(timeout=5)
    print()
    print('RESULT:', 'ALL PASS' if ok else 'SOME FAILURES')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(run())
