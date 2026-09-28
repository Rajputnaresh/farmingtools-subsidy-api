import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const TARGET_URL = 'https://farmingtools.in/pages/government-subsidy-farm-equipment-2026';
const CDP_PORT = 9224;

async function run() {
  console.log('1. Launching headless Chrome...');
  const chrome = spawn(CHROME_PATH, [
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    `--remote-debugging-port=${CDP_PORT}`,
    '--remote-debugging-address=127.0.0.1',
    'about:blank'
  ], { stdio: 'ignore' });

  await sleep(1500);

  let tabs = null;
  for (let attempt = 1; attempt <= 10; attempt++) {
    try {
      const tabsRes = await fetch(`http://127.0.0.1:${CDP_PORT}/json`);
      tabs = await tabsRes.json();
      if (tabs && tabs.length > 0) break;
    } catch {
      await sleep(500);
    }
  }

  const pageTab = tabs.find(t => t.type === 'page');
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
    }
  };

  await new Promise(r => ws.onopen = r);

  function sendCommand(method, params = {}) {
    return new Promise((resolve) => {
      const id = msgId++;
      pending.set(id, { resolve });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  await sendCommand('Page.enable');
  await sendCommand('Runtime.enable');

  console.log('2. Navigating to live production store:', TARGET_URL);
  await sendCommand('Page.navigate', { url: TARGET_URL });
  await sleep(5000);

  console.log('3. Inspecting DOM and evaluating calculator on live store...');
  const res = await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const calc = document.getElementById("farmingtools-subsidy-calculator");
      const machineSelect = document.getElementById("ft-machine");
      const stateSelect = document.getElementById("ft-state");
      const title = document.querySelector(".ft-title");
      const countBadge = document.getElementById("ft-machine-count-badge");
      
      const machineCount = machineSelect ? machineSelect.options.length : 0;
      const stateCount = stateSelect ? stateSelect.options.length : 0;
      
      // Select Tractor 20-40 PTO HP and Marginal/Women farmer
      if (machineSelect) {
        for (let i = 0; i < machineSelect.options.length; i++) {
          if (machineSelect.options[i].value.includes("tractor_20_40_pto_hp")) {
            machineSelect.selectedIndex = i;
            machineSelect.dispatchEvent(new Event("change"));
            break;
          }
        }
      }

      const subsidyVal = document.getElementById("ft-res-total-val") ? document.getElementById("ft-res-total-val").textContent : "";
      const farmerVal = document.getElementById("ft-res-farmer-val") ? document.getElementById("ft-res-farmer-val").textContent : "";
      const machineTitle = document.getElementById("ft-res-machine-title") ? document.getElementById("ft-res-machine-title").textContent : "";
      const dealerBtn = document.querySelector(".ft-btn-dealer");
      const waShareBtn = document.querySelector(".ft-btn-whatsapp");

      // Test Language Toggle
      const langBtn = document.getElementById("ft-lang-btn");
      if (langBtn) langBtn.click();
      const hindiTitle = document.querySelector(".ft-title") ? document.querySelector(".ft-title").textContent : "";

      return {
        hasCalculator: !!calc,
        titleText: title ? title.textContent : "",
        hindiTitle,
        availableBadge: countBadge ? countBadge.textContent : "",
        machineOptionsCount: machineCount,
        stateOptionsCount: stateCount,
        selectedMachine: machineSelect ? machineSelect.value : "",
        machineTitle,
        subsidyVal,
        farmerVal,
        hasDealerQuoteBtn: !!dealerBtn,
        hasShareWaBtn: !!waShareBtn
      };
    })()`,
    returnByValue: true
  });

  console.log('\n--- LIVE PRODUCTION VERIFICATION RESULT ---');
  console.log(JSON.stringify(res, null, 2));

  ws.close();
  chrome.kill();
  process.exit(0);
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
