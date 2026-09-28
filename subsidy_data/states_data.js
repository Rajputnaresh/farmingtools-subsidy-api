// State Registry (37 States and Union Territories)
// Source: data/registration_info.json
// Generated: 2026-09-28T11:13:47.159253
const STATES = [
  {
    "code": "1",
    "name": "Jammu & Kashmir",
    "portal": "https://hadp.jk.gov.in/",
    "portal_name": "HADP J&K / Directorate of Agriculture Jammu"
  },
  {
    "code": "2",
    "name": "Himachal Pradesh",
    "portal": "https://krishi.hp.gov.in/",
    "portal_name": "HP Agriculture Department Portal"
  },
  {
    "code": "3",
    "name": "Punjab",
    "portal": "https://agrimachinerypb.com/",
    "portal_name": "Punjab CRM / Subam Mechanization Portal"
  },
  {
    "code": "4",
    "name": "Chandigarh",
    "portal": "https://chandigarh.gov.in/",
    "portal_name": "Chandigarh UT Agriculture Office"
  },
  {
    "code": "5",
    "name": "Uttar Pradesh",
    "portal": "http://upagriculture.com/",
    "portal_name": "UP Agriculture DBT & Token Portal"
  },
  {
    "code": "6",
    "name": "Haryana",
    "portal": "https://agriharyana.gov.in/MechCRMScheme",
    "portal_name": "Agri Haryana MechCRM / Meri Fasal Mera Byora"
  },
  {
    "code": "7",
    "name": "Delhi",
    "portal": "https://delhi.gov.in/",
    "portal_name": "Delhi Agriculture Unit"
  },
  {
    "code": "8",
    "name": "Rajasthan",
    "portal": "https://rajkisan.rajasthan.gov.in/",
    "portal_name": "Rajkisan Sathi Portal"
  },
  {
    "code": "9",
    "name": "Uttarakhand",
    "portal": "https://agriculture.uk.gov.in/",
    "portal_name": "Uttarakhand Agriculture Directorate"
  },
  {
    "code": "10",
    "name": "Bihar",
    "portal": "https://dbtagriculture.bihar.gov.in/",
    "portal_name": "Bihar DBT Agriculture (OFMAS)"
  },
  {
    "code": "11",
    "name": "Sikkim",
    "portal": "https://sikkim.gov.in/departments/agriculture-department",
    "portal_name": "Sikkim Organic Agriculture Portal"
  },
  {
    "code": "12",
    "name": "Arunachal Pradesh",
    "portal": "https://agri.arunachal.gov.in/",
    "portal_name": "Arunachal Agriculture Department"
  },
  {
    "code": "13",
    "name": "Nagaland",
    "portal": "https://agriculture.nagaland.gov.in/",
    "portal_name": "Nagaland Agri Portal"
  },
  {
    "code": "14",
    "name": "Manipur",
    "portal": "https://agrimanipur.mn.gov.in/",
    "portal_name": "Manipur Agriculture Directorate"
  },
  {
    "code": "15",
    "name": "Mizoram",
    "portal": "https://agriculturemizoram.nic.in/",
    "portal_name": "Mizoram Agriculture Portal"
  },
  {
    "code": "16",
    "name": "Tripura",
    "portal": "https://agri.tripura.gov.in/",
    "portal_name": "Tripura Agri Portal"
  },
  {
    "code": "17",
    "name": "Meghalaya",
    "portal": "https://megagriculture.gov.in/",
    "portal_name": "Meghalaya Agriculture Department"
  },
  {
    "code": "18",
    "name": "Assam",
    "portal": "https://diragri.assam.gov.in/",
    "portal_name": "Assam Directorate of Agriculture"
  },
  {
    "code": "19",
    "name": "West Bengal",
    "portal": "https://wbfms.wb.gov.in/",
    "portal_name": "WBFMS / Matir Katha Portal"
  },
  {
    "code": "20",
    "name": "Jharkhand",
    "portal": "https://agri.jharkhand.gov.in/",
    "portal_name": "Jharkhand Krishi Department"
  },
  {
    "code": "21",
    "name": "Odisha",
    "portal": "https://agrisnetodisha.ori.nic.in/",
    "portal_name": "SAFAL / Agrisnet Odisha"
  },
  {
    "code": "22",
    "name": "Chhattisgarh",
    "portal": "https://agriportal.cg.nic.in/",
    "portal_name": "Chhattisgarh Kisan Portal"
  },
  {
    "code": "23",
    "name": "Madhya Pradesh",
    "portal": "https://dbt.mpdage.org/",
    "portal_name": "MP e-Krishi Yantra Anudan DBT Portal"
  },
  {
    "code": "24",
    "name": "Gujarat",
    "portal": "https://ikhedut.gujarat.gov.in/",
    "portal_name": "i-Khedut Gujarat Portal"
  },
  {
    "code": "25",
    "name": "Daman & Diu",
    "portal": "https://daman.nic.in/",
    "portal_name": "Daman & Diu UT Agri Administration"
  },
  {
    "code": "26",
    "name": "Dadra & Nagar Haveli",
    "portal": "https://dnh.gov.in/",
    "portal_name": "DNH UT Agri Administration"
  },
  {
    "code": "27",
    "name": "Maharashtra",
    "portal": "https://mahadbt.maharashtra.gov.in/",
    "portal_name": "MahaDBT Farmer Mechanization Portal"
  },
  {
    "code": "28",
    "name": "Andhra Pradesh",
    "portal": "https://rythubharosa.ap.gov.in/",
    "portal_name": "YSR Rythu Bharosa / Yantra Seva Portal"
  },
  {
    "code": "29",
    "name": "Karnataka",
    "portal": "https://raitamitra.karnataka.gov.in/",
    "portal_name": "Raita Mitra / FRUITS Portal"
  },
  {
    "code": "30",
    "name": "Goa",
    "portal": "https://agri.goa.gov.in/",
    "portal_name": "Goa Directorate of Agriculture"
  },
  {
    "code": "31",
    "name": "Lakshadweep",
    "portal": "https://lakshadweep.gov.in/",
    "portal_name": "Lakshadweep Agri Unit"
  },
  {
    "code": "32",
    "name": "Kerala",
    "portal": "https://aims.kerala.gov.in/",
    "portal_name": "AIMS Kerala / Karshaka Information Portal"
  },
  {
    "code": "33",
    "name": "Tamil Nadu",
    "portal": "https://www.agristnet.tn.gov.in/",
    "portal_name": "AGRISNET / Uzhavan Mobile App Portal"
  },
  {
    "code": "34",
    "name": "Puducherry",
    "portal": "https://agri.py.gov.in/",
    "portal_name": "Puducherry Agriculture Portal"
  },
  {
    "code": "35",
    "name": "Andaman & Nicobar Islands",
    "portal": "https://agri.andaman.gov.in/",
    "portal_name": "A&N Islands Agriculture Department"
  },
  {
    "code": "36",
    "name": "Telangana",
    "portal": "https://karshak.telangana.gov.in/",
    "portal_name": "Karshak / Rythu Bandhu Telangana"
  },
  {
    "code": "37",
    "name": "Ladakh",
    "portal": "https://ladakh.nic.in/",
    "portal_name": "UT Ladakh Agriculture Department"
  }
];

if (typeof window !== 'undefined') { window.STATES = STATES; }
if (typeof module !== 'undefined' && module.exports) { module.exports = { STATES }; }
