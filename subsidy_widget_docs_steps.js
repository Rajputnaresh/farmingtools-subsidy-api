
  // ── Render scheme-specific documents from verified registration_info.json data ──
  function updateDocumentsList(scheme, isPriority, cat, machineName) {
    const list = document.getElementById("ft-docs-list");
    if (!list) return;

    // Base mandatory documents (ALL schemes, ALL categories)
    const baseDocs = [
      { name: "Aadhaar Card (UID)", link: "https://uidai.gov.in/", note: "Name + DOB must match EXACTLY — OTP authentication is Aadhaar-linked" },
      { name: "Passport-size Photograph (coloured, JPEG < 50 KB)", link: "https://agrimachinery.nic.in/Farmer/Management/Index", note: "Recent photo for portal profile identification" },
      { name: "Land Record / RoR / 7-12 Extract / Khatauni / Khasra", link: "https://agrimachinery.nic.in/Farmer/Management/Index", note: "Land must be in applicant's name. For CRM schemes also upload MFMB-compatible Jamabandi/Fard." },
      { name: "Bank Passbook First Page / Cancelled Cheque (with IFSC)", link: "https://agrimachinery.nic.in/Farmer/Management/Index", note: "Account must be Aadhaar-seeded for Direct Benefit Transfer (DBT) credit" }
    ];

    // Scheme-specific documents — mirrors the verified registration_info.json data
    let schemeDocs = [];

    if (scheme === "SMAM") {
      if (isPriority) {
        schemeDocs.push({
          name: "Caste Certificate (SC/ST/OBC) — issued by Tehsildar / SDM",
          link: "https://agrimachinery.nic.in/Farmer/Management/Index",
          note: "Mandatory to claim the 50% priority subsidy rate instead of standard 40%"
        });
      }
      if (["Small", "Marginal"].includes(cat)) {
        schemeDocs.push({
          name: "Land Holding Certificate / Small & Marginal Farmer Certificate",
          link: "https://agrimachinery.nic.in/Farmer/Management/Index",
          note: "Required to claim small/marginal priority status"
        });
      }
    } else if (scheme === "CRM") {
      schemeDocs.push({
        name: "Meri Fasal Mera Byora (MFMB) Registration / State CRM Portal Registration",
        link: "https://fasal.haryana.gov.in/",
        note: "Primary CRM registration — Haryana farmers use MFMB. Punjab: Subam Portal. UP: UP Agriculture DBT."
      });
      schemeDocs.push({
        name: "Parivar Pehchan Patra (PPP) / State Family ID",
        link: "https://meraparivar.haryana.gov.in/",
        note: "Linked to land records for automatic validation. UP: create via UP Agri portal."
      });
      schemeDocs.push({
        name: "Undertaking / Affidavit: Not to burn paddy crop residue",
        link: "https://agriharyana.gov.in/MechCRMScheme",
        note: "Signed affidavit or online undertaking against stubble burning — mandatory for CRM eligibility"
      });
      schemeDocs.push({
        name: "Geo-tagged Field Photographs (before & after machine operation)",
        link: "https://agriharyana.gov.in/MechCRMScheme",
        note: "Upload post-harvest photos with GPS coordinates as proof of in-situ residue management"
      });
    } else if (scheme === "CHC") {
      schemeDocs.push({
        name: "Entity Registration — Society / FPO / Firm / Company / Panchayat",
        link: "https://agrimachinery.nic.in/Farmer/Management/Index",
        note: "Registrar of Societies / FES / Panchayat resolution. For rural youth enterprises: Udyam Aadhaar registration."
      });
      schemeDocs.push({
        name: "Detailed Project Report (DPR) — machine list, capacity, ROI projection",
        link: "https://agrimachinery.nic.in/Farmer/Management/Index",
        note: "DPR must list machines with technical specs, unit costs, land area, staff plan, and repayment schedule"
      });
      schemeDocs.push({
        name: "Term Loan Sanction Letter from Bank / Cooperative / NABARD",
        link: "https://agrimachinery.nic.in/Farmer/Management/Index",
        note: "CREDIT-LINKED SUBSIDY: bank loan is mandatory before portal application. Subsidy adjusts against loan principal."
      });
      schemeDocs.push({
        name: "Land Deed / Lease for Machinery Shed (minimum 5 years)",
        link: "https://agrimachinery.nic.in/Farmer/Management/Index",
        note: "Yard + parking + covered storage proof. 5–10 year lease or ownership deed required."
      });
      if (cat === "FPO" || cat === "Cooperative") {
        schemeDocs.push({
          name: "FPO / Cooperative Certificate + Board Resolution to set up CHC",
          link: "https://agrimachinery.nic.in/Farmer/Management/Index",
          note: "Board resolution authorising CHC project and naming the project director"
        });
      }
      if (cat === "Rural_Youth") {
        schemeDocs.push({
          name: "Proof of Rural Residence + Age 18–45 (Aadhaar / Voter ID)",
          link: "https://uidai.gov.in/",
          note: "Rural youth entrepreneurship scheme — age and rural-status proof required"
        });
      }
    } else if (scheme === "FMB") {
      schemeDocs.push({
        name: "Society / SHG / FPO / Panchayat Registration Certificate",
        link: "https://agrimachinery.nic.in/Farmer/Management/Index",
        note: "Cooperative Society (State Cooperative Act) / SHG (SRLM-registered) / FPO (SFAC)"
      });
      schemeDocs.push({
        name: "General Body / Executive Committee Resolution to establish Farm Machinery Bank",
        link: "https://agrimachinery.nic.in/Farmer/Management/Index",
        note: "Resolution specifying village, machines to procure, and member beneficiary roster"
      });
      schemeDocs.push({
        name: "List of Member Farmers — Name, Aadhaar Number, Land Holdings",
        link: "https://agrimachinery.nic.in/Farmer/Management/Index",
        note: "Beneficiary roster: at least 51% small & marginal farmers; women ≥ 30% where applicable"
      });
      if (cat === "FRA") {
        schemeDocs.push({
          name: "Forest Rights Act (FRA) Patta Certificate — individual or community",
          link: "https://agrimachinery.nic.in/Farmer/Management/Index",
          note: "Required to claim 90% FMB subsidy rate for forest-dwelling ST families"
        });
      }
    } else if (scheme === "NAMO_DRONE_DIDI") {
      schemeDocs.push({
        name: "DAY-NRLM SHG Registration Certificate (State Rural Livelihood Mission)",
        link: "https://nrlm.gov.in/",
        note: "Active SHG member list, SHG name, federation, bank linkage, Aadhaar-seeded accounts"
      });
      schemeDocs.push({
        name: "SHG Resolution: Nominate 2 Women Members — Drone Pilot + Drone Assistant",
        link: "https://nrlm.gov.in/",
        note: "Resolution passed in general body meeting with nominee details, Aadhaar, and educational qualification"
      });
      schemeDocs.push({
        name: "Educational Certificate: Minimum 10th Pass (for nominated Pilot)",
        link: "https://dgca.gov.in/",
        note: "DGCA Remote Pilot License eligibility requires minimum 10th standard pass"
      });
      schemeDocs.push({
        name: "DGCA Remote Pilot Training Certificate / RPTO Completion Proof",
        link: "https://dgca.gov.in/",
        note: "15-day DGCA-certified training at empanelled Remote Pilot Training Organisation (RPTO)"
      });
      schemeDocs.push({
        name: "AIF Loan Application / SHG Bank Account / AIF Portal Registration",
        link: "https://agriinfra.dac.gov.in/",
        note: "20% balance (₹2 Lakhs on ₹10L package) funded via Agriculture Infrastructure Fund loan — 3% interest subvention for 7 years"
      });
    }

    // Combine base + scheme-specific
    const allDocs = [...baseDocs, ...schemeDocs];

    // Render document list
    list.innerHTML = allDocs.map(d => `
      <li>
        <span class="ft-check-icon">✓</span>
        <div>
          <b>${d.name}</b><br>
          <span style="color:#64748b; font-size:12px;">${d.note}</span><br>
          <a href="${d.link}" target="_blank" rel="noopener" class="ft-doc-link">Official Link ↗</a>
        </div>
      </li>
    `).join("");
  }

  // ── Render step-by-step registration process from verified registration_info.json data ──
  function updateStepsList(scheme, statePortal) {
    const list = document.getElementById("ft-steps-list");
    if (!list) return;

    // Central steps (common to all schemes)
    const centralSteps = [
      `<b>Step 1 — Aadhaar-Based Farmer Registration:</b> Visit <a href="https://agrimachinery.nic.in/Farmer/Management/Index" target="_blank" style="color:#1b4d3e;">Central DBT Portal</a>. Search by Aadhaar Number. Select State → District → Sub-District → Block → Village. Create profile with mobile OTP authentication.`,
      `<b>Step 2 — Upload Mandatory Documents:</b> Scan and upload Aadhaar, land record, bank passbook, and photograph. Ensure Name & Date of Birth match Aadhaar EXACTLY.`,

      `<b>Step 3 — Select Machine & Empanelled Dealer:</b> Choose machine from scheme-specific list. Select an authorised dealer who has current-year price quotes registered on the portal. System validates dealer + machine combination.`,
      `<b>Step 4 — Online Application & SLEC Approval:</b> Application submitted to State Level Executive Committee (SLEC). Digital sanction order issued. For CHC/FMB: DPR reviewed. For CRM: lottery / first-come selection process.`,
      `<b>Step 5 — Purchase & Physical Verification:</b> Buy machine from empanelled dealer. Upload invoice and geo-tagged installation photograph. District Agriculture Officer verifies physical delivery on site.`,
      `<b>Step 6 — DBT Release to Bank Account:</b> Subsidy credited DIRECTLY to your Aadhaar-seeded bank account — no middleman, no cash. Track status at <a href="https://agrimachinery.nic.in/index/ApplicationTracking" target="_blank" style="color:#1b4d3e;">Tracking Portal ↗</a>.`
    ];

    // Scheme-specific step insertions
    if (scheme === "CRM") {
      centralSteps.splice(1, 0,
        `<b>CRM-Specific — State Portal Pre-Registration (BEFORE central application):</b> Register on your state CRM portal first.
        Haryana → <a href="https://agriharyana.gov.in/MechCRMScheme" target="_blank" style="color:#1b4d3e;">Meri Fasal Mera Byora</a> &nbsp;|&nbsp;
        Punjab → <a href="https://agrimachinerypb.com/" target="_blank" style="color:#1b4d3e;">Subam Mechanization Portal</a> &nbsp;|&nbsp;
        Uttar Pradesh → <a href="http://upagriculture.com/" target="_blank" style="color:#1b4d3e;">UP Agriculture DBT Portal</a>.
        Register crop, land holding, and desired CRM machine choice.`
      );
    } else if (scheme === "CHC") {
      centralSteps.splice(1, 0,
        `<b>CHC-Specific — Bank Loan FIRST (before portal application):</b> Apply for term loan at your bank. Bank sanction letter is MANDATORY for portal submission. Subsidy is credit-linked: released amount adjusts directly against your loan principal — you do not receive cash.`
      );
      centralSteps.splice(2, 0,
        `<b>CHC-Specific — Prepare Detailed Project Report (DPR):</b> DPR must list machines with technical specifications, unit costs, land area, staff plan, operational model, and 5-year financial projection. Submit DPR to District Nodal Officer for SLEC review.`
      );
    } else if (scheme === "FMB") {
      centralSteps.splice(1, 0,
        `<b>FMB-Specific — Entity Formation (if not already formed):</b> Register Cooperative Society (under State Cooperative Act) OR register SHG with State Rural Livelihood Mission (SRLM) OR register FPO with SFAC. Pass a General Body / Executive Committee resolution authorising the Farm Machinery Bank project.`
      );
    } else if (scheme === "NAMO_DRONE_DIDI") {
      centralSteps.splice(1, 0,
        `<b>Namo Drone Didi — SHG Selection by SRLM (pre-requisite):</b> SHG must be selected by the State Rural Livelihood Mission (SRLM) and a Lead Fertilizer Company (LFC). Confirm SHG eligibility at <a href="https://nrlm.gov.in/" target="_blank" style="color:#1b4d3e;">NRLM Portal ↗</a>. Only selected SHGs can apply.`
      );
      centralSteps.splice(3, 0,
        `<b>Namo Drone Didi — DGCA Remote Pilot Training:</b> The nominated SHG member (Drone Pilot) must complete a 15-day DGCA-certified Remote Pilot Training course at an empanelled Remote Pilot Training Organisation (RPTO). Pass the skill test to obtain the DGCA Remote Pilot License.`
      );
      centralSteps.splice(5, 0,
        `<b>Namo Drone Didi — AIF Loan for 20% Balance Amount:</b> The remaining 20% (e.g. ₹2 Lakhs on a ₹10 Lakh drone package) is funded through an Agriculture Infrastructure Fund (AIF) loan at 3% interest subvention for 7 years. Apply at <a href="https://agriinfra.dac.gov.in/" target="_blank" style="color:#1b4d3e;">AIF Portal ↗</a>. The 80% central grant is released directly — you only repay the AIF loan.`
      );
    }

    // Insert state portal step after Step 2 if a state is selected
    if (statePortal) {
      const stateStep =
        `<b>State-Specific Step — Register on ${statePortal.name}:</b> Also register your profile on <a href="${statePortal.portal}" target="_blank" style="color:#1b4d3e;">${statePortal.portal_name} ↗</a>. This enables access to the state quota, application for state top-up (where available), and tracking of state-level disbursement timelines.`;
      centralSteps.splice(2, 0, stateStep);
    }

    list.innerHTML = centralSteps.map(s => `<li>${s}</li>`).join("");
  }
