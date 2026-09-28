import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const PORT = 9988;
const CDP_PORT = 9223;

function getChromePath() {
  if (process.env.CHROME_BIN && fs.existsSync(process.env.CHROME_BIN)) {
    return process.env.CHROME_BIN;
  }
  const platform = os.platform();
  if (platform === 'darwin') {
    return '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  } else if (platform === 'win32') {
    return 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  } else {
    const candidates = [
      '/usr/bin/google-chrome',
      '/usr/bin/google-chrome-stable',
      '/usr/bin/chromium-browser',
      '/usr/bin/chromium'
    ];
    for (const c of candidates) {
      if (fs.existsSync(c)) return c;
    }
    return 'google-chrome';
  }
}

const CHROME_PATH = getChromePath();

async function main() {
  console.log('====================================================');
  console.log('  STARTING REAL BROWSER END-TO-END TEST (CHROME CDP)');
  console.log('====================================================\n');

  // 1. Start Subsidy API Server
  console.log(`1. Launching Subsidy API server on port ${PORT}...`);
  const server = spawn('python3', ['subsidy_api.py', String(PORT)], {
    env: { ...process.env, PORT: String(PORT) },
    stdio: 'ignore'
  });
  await sleep(1500);

  // 2. Launch Google Chrome headless
  console.log(`2. Launching Headless Chrome on CDP port ${CDP_PORT} using ${CHROME_PATH}...`);
  const tmpProfile = fs.mkdtempSync(path.join(os.tmpdir(), 'chrome-test-'));
  const chromeArgs = [
    '--headless=new',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    `--user-data-dir=${tmpProfile}`,
    `--remote-debugging-port=${CDP_PORT}`,
    '--remote-debugging-address=127.0.0.1',
    `http://127.0.0.1:${PORT}/`
  ];
  const chrome = spawn(CHROME_PATH, chromeArgs);
  chrome.stderr?.on('data', (d) => {
    const s = d.toString();
    if (!s.includes('DevTools listening') && !s.includes('created a new window')) {
      // Keep stderr quiet unless there is a fatal error
    }
  });

  let passed = true;

  try {
    // 3. Connect to Chrome CDP with retry loop (up to 20 attempts = 10s)
    let tabs = null;
    for (let attempt = 1; attempt <= 20; attempt++) {
      try {
        const tabsRes = await fetch(`http://127.0.0.1:${CDP_PORT}/json`);
        tabs = await tabsRes.json();
        if (tabs && tabs.length > 0) break;
      } catch (err) {
        if (attempt === 20) throw err;
        await sleep(500);
      }
    }
    const pageTab = tabs.find(t => t.type === 'page');
    if (!pageTab || !pageTab.webSocketDebuggerUrl) {
      throw new Error('Could not find Chrome page tab WebSocket URL');
    }

    const ws = new WebSocket(pageTab.webSocketDebuggerUrl);
    let msgId = 1;
    const pending = new Map();
    const consoleLogs = [];

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.id && pending.has(data.id)) {
        const { resolve } = pending.get(data.id);
        pending.delete(data.id);
        resolve(data.result);
      }
      if (data.method === 'Runtime.consoleAPICalled') {
        consoleLogs.push(data.params);
      }
      if (data.method === 'Runtime.exceptionThrown') {
        console.error('❌ Browser Exception:', data.params.exceptionDetails);
        passed = false;
      }
    };

    await new Promise((resolve) => ws.onopen = resolve);

    function sendCommand(method, params = {}) {
      return new Promise((resolve) => {
        const id = msgId++;
        pending.set(id, { resolve });
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    // Enable Runtime domain
    await sendCommand('Runtime.enable');
    await sendCommand('Page.enable');
    console.log(`  Navigating Chrome to http://127.0.0.1:${PORT}/...`);
    await sendCommand('Page.navigate', { url: `http://127.0.0.1:${PORT}/` });
    await sleep(3000);

    async function evaluate(expression) {
      const res = await sendCommand('Runtime.evaluate', {
        expression,
        returnByValue: true,
        awaitPromise: true
      });
      if (res.exceptionDetails) {
        const desc = res.exceptionDetails.exception?.description || JSON.stringify(res.exceptionDetails);
        throw new Error(desc);
      }
      return res.result?.value;
    }

    // TEST 1: Check Data Files and Global Variables
    console.log('\n--- Test 1: Verify Static Data Assets in Browser Context ---');
    const statesLen = await evaluate('window.STATES?.length || 0');
    const schemesLen = await evaluate('Object.keys(window.SCHEME_DOCS || {}).length');
    const machinesLen = await evaluate('Object.keys(window.FULL_DB || {}).length');
    console.log(`  STATES array loaded:       ${statesLen} states (Expected: 37)`);
    console.log(`  SCHEME_DOCS object loaded: ${schemesLen} schemes (Expected: 5)`);
    console.log(`  FULL_DB object loaded:     ${machinesLen} machines (Expected: 175)`);
    if (statesLen === 37 && schemesLen === 5 && machinesLen === 175) {
      console.log('  ✅ Test 1 PASSED');
    } else {
      console.log('  ❌ Test 1 FAILED');
      passed = false;
    }

    // TEST 2: Check Machine & State Dropdown Options
    console.log('\n--- Test 2: Verify Dropdown DOM Population ---');
    const machineOpts = await evaluate('document.getElementById("ft-machine")?.options.length || 0');
    const stateOpts = await evaluate('document.getElementById("ft-state")?.options.length || 0');
    console.log(`  Machine dropdown options: ${machineOpts} (Expected: 175)`);
    console.log(`  State dropdown options:   ${stateOpts} (Expected: 38 including default)`);
    if (machineOpts === 175 && stateOpts === 38) {
      console.log('  ✅ Test 2 PASSED');
    } else {
      console.log('  ❌ Test 2 FAILED');
      passed = false;
    }

    // TEST 3: Calculate SMAM Tractor for SC Category
    console.log('\n--- Test 3: Calculate SMAM Tractor 2WD (SC Category, ₹500,000) ---');
    await evaluate(`
      document.getElementById("ft-machine").value = "smam_i_tractor_2wd_08-20";
      document.getElementById("ft-category").value = "SC";
      document.getElementById("ft-state").value = "";
      document.getElementById("ft-price").value = "500000";
      runCalculation();
    `);
    await sleep(500);

    const resCentral3 = await evaluate('document.getElementById("ft-res-central-val")?.textContent');
    const resTotal3 = await evaluate('document.getElementById("ft-res-total-val")?.textContent');
    const resFarmer3 = await evaluate('document.getElementById("ft-res-farmer-val")?.textContent');
    console.log(`  Central Subsidy: ${resCentral3} (Expected: ₹2,00,000)`);
    console.log(`  Total Subsidy:   ${resTotal3} (Expected: ₹2,00,000)`);
    console.log(`  Farmer Share:    ${resFarmer3} (Expected: ₹3,00,000)`);
    if (resCentral3 === '₹2,00,000' && resTotal3 === '₹2,00,000' && resFarmer3 === '₹3,00,000') {
      console.log('  ✅ Test 3 PASSED');
    } else {
      console.log('  ❌ Test 3 FAILED');
      passed = false;
    }

    // TEST 4: Calculate Haryana CRM Super Seeder (with State Top-Up)
    console.log('\n--- Test 4: Calculate Haryana CRM Super Seeder (SC Category, ₹210,000) ---');
    await evaluate(`
      document.getElementById("ft-scheme").value = "CRM";
      onSchemeChange();
      document.getElementById("ft-machine").value = "crm_super_seeder";
      document.getElementById("ft-category").value = "SC";
      document.getElementById("ft-state").value = "6"; // Haryana
      document.getElementById("ft-price").value = "210000";
      runCalculation();
    `);
    await sleep(600);

    const resCentral4 = await evaluate('document.getElementById("ft-res-central-val")?.textContent');
    const resState4 = await evaluate('document.getElementById("ft-res-state-val")?.textContent');
    const resTotal4 = await evaluate('document.getElementById("ft-res-total-val")?.textContent');
    const resFarmer4 = await evaluate('document.getElementById("ft-res-farmer-val")?.textContent');
    console.log(`  Central Subsidy: ${resCentral4} (Expected: ₹1,05,000)`);
    console.log(`  State Top-up:    ${resState4} (Expected: ₹1,05,000)`);
    console.log(`  Total Subsidy:   ${resTotal4} (Expected: ₹2,10,000)`);
    console.log(`  Farmer Share:    ${resFarmer4} (Expected: ₹0)`);
    if (resCentral4 === '₹1,05,000' && resState4 === '₹1,05,000' && resTotal4 === '₹2,10,000' && resFarmer4 === '₹0') {
      console.log('  ✅ Test 4 PASSED');
    } else {
      console.log('  ❌ Test 4 FAILED');
      passed = false;
    }

    // TEST 5: Verify Document Checklist and Steps Rendering
    console.log('\n--- Test 5: Verify Document Checklist & Step Rendering ---');
    const docsCount = await evaluate('document.getElementById("ft-docs-list")?.children.length || 0');
    const stepsCount = await evaluate('document.getElementById("ft-steps-list")?.children.length || 0');
    console.log(`  Documents checklist items rendered: ${docsCount}`);
    console.log(`  Application steps rendered:         ${stepsCount}`);
    if (docsCount >= 4 && stepsCount >= 5) {
      console.log('  ✅ Test 5 PASSED');
    } else {
      console.log('  ❌ Test 5 FAILED');
      passed = false;
    }

    // TEST 6: Verify Scheme Filtering Dynamic Switch
    console.log('\n--- Test 6: Verify Scheme Filtering ---');
    await evaluate(`
      document.getElementById("ft-scheme").value = "CRM";
      onSchemeChange();
    `);
    const crmMachinesCount = await evaluate('document.getElementById("ft-machine")?.options.length || 0');
    console.log(`  CRM filtered machine count: ${crmMachinesCount} (Expected: 28)`);
    if (crmMachinesCount === 28) {
      console.log('  ✅ Test 6 PASSED');
    } else {
      console.log('  ❌ Test 6 FAILED');
      passed = false;
    }

    // TEST 7: Verify Machine Search
    console.log('\n--- Test 7: Verify Instant Machine Search ---');
    await evaluate(`
      document.getElementById("ft-scheme").value = "ALL";
      document.getElementById("ft-machine-search").value = "Baler";
      onSearchChange();
    `);
    const balerCount = await evaluate('document.getElementById("ft-machine")?.options.length || 0');
    console.log(`  Baler search result count: ${balerCount} (Expected: 4)`);
    if (balerCount === 4) {
      console.log('  ✅ Test 7 PASSED');
    } else {
      console.log('  ❌ Test 7 FAILED');
      passed = false;
    }

    // TEST 8: Verify Language Toggle (Bilingual English / Hindi)
    console.log('\n--- Test 8: Verify Bilingual Language Toggle ---');
    await evaluate(`toggleLanguage();`);
    const hindiTitle = await evaluate('document.querySelector(".ft-title")?.textContent');
    console.log(`  Hindi title rendered: "${hindiTitle}"`);
    await evaluate(`toggleLanguage();`);
    const engTitle = await evaluate('document.querySelector(".ft-title")?.textContent');
    console.log(`  English title restored: "${engTitle}"`);
    if (hindiTitle === 'कृषि यंत्र सब्सिडी कैलकुलेटर' && engTitle === 'Krishi Yantra Subsidy Calculator') {
      console.log('  ✅ Test 8 PASSED');
    } else {
      console.log('  ❌ Test 8 FAILED');
      passed = false;
    }

    // TEST 9: Verify Units Scaling & 12% GST Treatment
    console.log('\n--- Test 9: Verify Units Scaling & 12% GST Breakdown ---');
    await evaluate(`
      document.getElementById("ft-machine-search").value = "";
      document.getElementById("ft-scheme").value = "SMAM";
      onSchemeChange();
      document.getElementById("ft-machine").value = "smam_i_tractor_2wd_08-20";
      document.getElementById("ft-category").value = "SC";
      document.getElementById("ft-state").value = "";
      document.getElementById("ft-price").value = "500000";
      document.getElementById("ft-units").value = "2";
      document.getElementById("ft-gst-inclusive").checked = true;
      runCalculation();
    `);
    await sleep(400);
    const gstTotal = await evaluate('document.getElementById("ft-gst-total")?.textContent');
    const centralUnitsVal = await evaluate('document.getElementById("ft-res-central-val")?.textContent');
    console.log(`  2 Units total with GST: ${gstTotal} (Expected: ₹10,00,000)`);
    console.log(`  Central subsidy (scaled for 2 units): ${centralUnitsVal}`);
    if (gstTotal === '₹10,00,000' && centralUnitsVal === '₹4,00,000') {
      console.log('  ✅ Test 9 PASSED');
    } else {
      console.log('  ❌ Test 9 FAILED');
      passed = false;
    }

    // TEST 10: Verify Action Buttons in Result Card
    console.log('\n--- Test 10: Verify Share, Print, and Copy Actions ---');
    const hasWhatsApp = await evaluate('!!document.querySelector(".ft-btn-whatsapp")');
    const hasPrint = await evaluate('!!document.querySelector(".ft-btn-print")');
    const hasCopy = await evaluate('!!document.querySelector(".ft-btn-copy")');
    console.log(`  WhatsApp Share Button present: ${hasWhatsApp}`);
    console.log(`  Print / Save PDF Button present: ${hasPrint}`);
    console.log(`  Copy Estimate Button present:    ${hasCopy}`);
    if (hasWhatsApp && hasPrint && hasCopy) {
      console.log('  ✅ Test 10 PASSED');
    } else {
      console.log('  ❌ Test 10 FAILED');
      passed = false;
    }

    ws.close();
  } catch (err) {
    console.error('❌ Browser Test Error:', err);
    passed = false;
  } finally {
    try { chrome.kill('SIGTERM'); } catch {}
    try { server.kill('SIGTERM'); } catch {}
    try { fs.rmSync(tmpProfile, { recursive: true, force: true }); } catch {}
  }

  console.log('\n====================================================');
  console.log('  BROWSER END-TO-END VERIFICATION RESULT:', passed ? '🏆 ALL PASS' : '❌ FAILED');
  console.log('====================================================\n');
  process.exit(passed ? 0 : 1);
}

main();
