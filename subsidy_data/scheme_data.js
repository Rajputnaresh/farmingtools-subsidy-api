// Scheme-specific documents and process steps
// Source: data/registration_info.json
// Generated: 2026-09-28T11:13:47.159683
const SCHEME_DOCS = {
  "SMAM": {
    "full_name": "Sub-Mission on Agricultural Mechanization (SMAM 2024)",
    "target_group": "Individual farmers, Women farmers, SC/ST, Small & Marginal farmers",
    "rates": "50% for SC/ST/Small/Marginal/Women/NE States (capped as per Annexure-I); 40% for General/OBC",
    "guidelines_url": "https://agrimachinery.nic.in/Files/Guidelines/Guidelines_SMAM2024.pdf",
    "portal_url": "https://agrimachinery.nic.in/Farmer/Management/Index",
    "documents": [
      {
        "item": "Aadhaar Card (UID)",
        "mandatory": true,
        "purpose": "Identity verification & DBT linkage",
        "link": "https://uidai.gov.in/"
      },
      {
        "item": "Passport-size photograph",
        "mandatory": true,
        "purpose": "Profile identification on portal",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "Record of Rights (RoR) / Land Record (7/12, Khasra, Khatauni)",
        "mandatory": true,
        "purpose": "Proof of agricultural land holding",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "First page of Bank Passbook / Cancelled Cheque",
        "mandatory": true,
        "purpose": "Bank account IFSC and account number for DBT subsidy credit",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "Government ID Proof (Aadhaar / Voter ID / Driving License / PAN)",
        "mandatory": true,
        "purpose": "Secondary identity verification",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "Caste Certificate (SC/ST/OBC)",
        "mandatory": false,
        "purpose": "Mandatory only for claiming 50% priority subsidy",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      }
    ],
    "process_steps": [
      "1. Register on agrimachinery.nic.in using Aadhaar & mobile number.",
      "2. Select State, District, Sub-District, Block, and Village from dropdowns.",
      "3. Provide land details with scanned RoR document.",
      "4. Choose machine and empanelled dealer from the approved list.",
      "5. Online application submitted to State Level Executive Committee (SLEC).",
      "6. Verification, sanction order issued, and subsidy released directly via DBT."
    ]
  },
  "CRM": {
    "full_name": "Crop Residue Management (CRM) Scheme (In-situ)",
    "target_group": "Farmers, CHCs, FPOs, and Panchayats in Punjab, Haryana, UP, and Delhi",
    "rates": "50% for individual farmers; 80% for Custom Hiring Centres (project cost ₹5L-₹15L)",
    "guidelines_url": "https://agrimachinery.nic.in/Files/Guidelines/CRMGuideline2020-21.pdf",
    "portal_url": "https://agriharyana.gov.in/MechCRMScheme",
    "documents": [
      {
        "item": "Aadhaar Card & Parivar Pehchan Patra (Family ID)",
        "mandatory": true,
        "purpose": "Identification on state portal (e.g. Haryana PPP)",
        "link": "https://meraparivar.haryana.gov.in/"
      },
      {
        "item": "Meri Fasal Mera Byora (MFMB) Registration",
        "mandatory": true,
        "purpose": "Crop registration verification",
        "link": "https://fasal.haryana.gov.in/"
      },
      {
        "item": "Land Record (Jamabandi / Farad)",
        "mandatory": true,
        "purpose": "Proof of land cultivated with paddy/wheat",
        "link": "https://jamabandi.nic.in/"
      },
      {
        "item": "Bank Account Details (Aadhaar-seeded)",
        "mandatory": true,
        "purpose": "DBT transfer",
        "link": "https://agriharyana.gov.in/MechCRMScheme"
      },
      {
        "item": "Under-taking not to burn crop residue",
        "mandatory": true,
        "purpose": "Affidavit against stubble burning",
        "link": "https://agriharyana.gov.in/MechCRMScheme"
      }
    ],
    "process_steps": [
      "1. Register on State CRM Portal (Haryana MechCRM / Punjab Agrimachinery / UP Agriculture).",
      "2. Enter Family ID / Farmer ID to fetch verified land details.",
      "3. Select approved CRM machinery (Super Seeder, Baler, Happy Seeder, Mulcher).",
      "4. State lottery/selection process triggers sanction token.",
      "5. Purchase machine from empanelled dealer and upload invoice & GPS photo.",
      "6. Physical verification by Agriculture Development Officer followed by DBT credit."
    ]
  },
  "CHC": {
    "full_name": "Custom Hiring Centre (CHC) Scheme (SMAM Component 4.2)",
    "target_group": "Rural youth entrepreneurs, Cooperatives, Registered Farmer Societies, FPOs, Panchayats",
    "rates": "40% capital subsidy on project cost up to ₹250 Lakhs (80% up to ₹15L under CRM; 50% up to ₹9L for Agriculture Graduates for Drone CHC)",
    "guidelines_url": "https://agrimachinery.nic.in/Files/Guidelines/Guidelines_SMAM2024.pdf",
    "portal_url": "https://agrimachinery.nic.in/Farmer/Management/Index",
    "documents": [
      {
        "item": "Registration Certificate of Society / FPO / Firm / Partnership",
        "mandatory": true,
        "purpose": "Entity legal status verification",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "Detailed Project Report (DPR)",
        "mandatory": true,
        "purpose": "Machinery list, business viability, and financial plan",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "Bank Loan Sanction Letter / Term Loan Agreement",
        "mandatory": true,
        "purpose": "Credit-linked capital subsidy requirement",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "Land ownership / Lease deed for Machinery Shed (minimum 5-10 years)",
        "mandatory": true,
        "purpose": "Yard and parking infrastructure proof",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "Agriculture Degree Certificate (for Agri-Graduate 50% Drone CHC)",
        "mandatory": false,
        "purpose": "Special 50% concession for agriculture graduates",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      }
    ],
    "process_steps": [
      "1. Formulate Detailed Project Report (DPR) with machine list matching regional cropping patterns.",
      "2. Secure term loan from commercial / cooperative bank (Bank-linked subsidy model).",
      "3. Apply online at agrimachinery.nic.in under CHC component.",
      "4. State Level Executive Committee (SLEC) review and project sanction.",
      "5. Subsidy kept in Subsidy Reserve Fund (SRF) account and adjusted against loan principal."
    ]
  },
  "FMB": {
    "full_name": "Village Level Farm Machinery Bank (FMB) (SMAM Component 4.3)",
    "target_group": "Cooperative Societies, Registered Farmer Societies, SHGs, FPOs, Panchayats",
    "rates": "80% financial assistance up to ₹30 Lakhs (max ₹24L subsidy); 90% up to ₹27L for FRA Patta holders; 95% up to ₹28.5L in NER",
    "guidelines_url": "https://agrimachinery.nic.in/Files/Guidelines/Guidelines_SMAM2024.pdf",
    "portal_url": "https://agrimachinery.nic.in/Farmer/Management/Index",
    "documents": [
      {
        "item": "Society / SHG / FPO Registration Certificate",
        "mandatory": true,
        "purpose": "Legal verification of collective group",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "Resolution of General Body / Executive Committee",
        "mandatory": true,
        "purpose": "Formal resolution to set up Farm Machinery Bank",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "List of Member Farmers with Aadhaar Numbers & Land Holdings",
        "mandatory": true,
        "purpose": "Beneficiary coverage assessment",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "Bank Account Details of the Society / Group",
        "mandatory": true,
        "purpose": "Direct grant disbursement",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      },
      {
        "item": "FRA Patta certificate (if claiming 90% tribal assistance)",
        "mandatory": false,
        "purpose": "Forest Rights Act verification",
        "link": "https://agrimachinery.nic.in/Farmer/Management/Index"
      }
    ],
    "process_steps": [
      "1. Village selection based on low mechanization index in rainfed/aspirational district.",
      "2. Society/SHG submits resolution and machine equipment requisition.",
      "3. Approval by District Nodal Committee and SLEC.",
      "4. Procurement from empanelled manufacturers.",
      "5. Commissioning of machinery bank and online listing on FARMS mobile app."
    ]
  },
  "NAMO_DRONE_DIDI": {
    "full_name": "Central Sector Scheme Namo Drone Didi",
    "target_group": "Women Self Help Groups (SHGs) under DAY-NRLM / State Rural Livelihood Missions",
    "rates": "80% Central Financial Assistance up to ₹8.00 Lakhs for drone, accessories, and training. Balance 20% funded via AIF loan with 3% interest subvention.",
    "guidelines_url": "https://agrimachinery.nic.in/Files/Guidelines/Guidelines_SMAM2024.pdf",
    "portal_url": "https://agrimachinery.nic.in/Farmer/Management/Index",
    "documents": [
      {
        "item": "DAY-NRLM SHG Registration Certificate",
        "mandatory": true,
        "purpose": "Proof of active Women SHG status under SRLM",
        "link": "https://nrlm.gov.in/"
      },
      {
        "item": "Resolution nominating 2 members (1 Drone Pilot, 1 Drone Assistant)",
        "mandatory": true,
        "purpose": "DGCA approved Remote Pilot Training certification",
        "link": "https://nrlm.gov.in/"
      },
      {
        "item": "Educational Certificate (Minimum 10th pass for pilot nominee)",
        "mandatory": true,
        "purpose": "DGCA Remote Pilot License requirement",
        "link": "https://dgca.gov.in/"
      },
      {
        "item": "SHG Bank Passbook / AIF Loan Account Details",
        "mandatory": true,
        "purpose": "Direct grant release & 3% interest subvention",
        "link": "https://agriinfra.dac.gov.in/"
      }
    ],
    "process_steps": [
      "1. Selection of SHG by State Rural Livelihood Mission (SRLM) and Lead Fertilizer Companies (LFC).",
      "2. Nominated member completes 15-day DGCA-certified drone pilot training course.",
      "3. Drone package (DGCA type certified drone, batteries, charging hub, spray nozzles) supplied by empanelled OEM.",
      "4. 80% subsidy released directly; remaining 20% sanctioned under Agriculture Infrastructure Fund (AIF).",
      "5. SHG offers rental spraying services to regional farmers at ₹300-₹500/acre."
    ]
  }
};

const CENTRAL_PORTLINKS = {
  "dbt_portal": "https://agrimachinery.nic.in/Farmer/Management/Index",
  "calculator": "https://agrimachinery.nic.in/index/assistanceCalculator",
  "tracking": "https://agrimachinery.nic.in/index/tracking",
  "guidelines_smam_2024": "https://agrimachinery.nic.in/Files/Guidelines/Guidelines_SMAM2024.pdf",
  "guidelines_smam_2018": "https://agrimachinery.nic.in/Files/Guidelines/smam1920.pdf",
  "guidelines_crm_2020": "https://agrimachinery.nic.in/Files/Guidelines/CRMGuideline2020-21.pdf",
  "dbt_manual_pdf": "https://agrimachinery.nic.in/Files/Product/DBT-FarmerManual----PDF.pdf",
  "farms_chc_app": "https://agrimachinery.nic.in/Files/FAQ_CHC_MobAPP.pdf",
  "helpdesk_email": "support-agrimech@gov.in"
};

if (typeof window !== 'undefined') { window.SCHEME_DOCS = SCHEME_DOCS; window.CENTRAL_PORTLINKS = CENTRAL_PORTLINKS; }
if (typeof module !== 'undefined' && module.exports) { module.exports = { SCHEME_DOCS, CENTRAL_PORTLINKS }; }
