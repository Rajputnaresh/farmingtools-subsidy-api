# Generative Engine Optimization (GEO) Audit: FarmingTools.in

**Target Domain:** [farmingtools.in](https://farmingtools.in)  
**Parent Entity:** KRISHIGEARS INDIA PRIVATE LIMITED  
**Audit Date:** October 27, 2026  
**Framework:** AI Search / GEO Standards (Google Search Central AI Optimization Guide, RFC 9309, Ahrefs & SE Ranking Empirical Citations Benchmarks)

---

## 1. Executive Summary & GEO Readiness Score

### **Overall GEO Readiness Score: 70 / 100**

FarmingTools.in demonstrates high technical maturity in structured commerce data (native Shopify SSR, rich JSON-LD for products, organization, and breadcrumbs, plus Universal Commerce Protocol integration). However, its visibility in conversational AI search engines (ChatGPT, Perplexity) is constrained by a lack of off-site brand mentions (Wikipedia, Reddit) and client-injected FAQ schema that headless AI crawlers cannot execute.

```
┌───────────────────────────────────────┬────────┬───────────┐
│ Evaluation Dimension                  │ Weight │ Score     │
├───────────────────────────────────────┼────────┼───────────┤
│ 1. Citability & Passage Structure     │ 25%    │ 18 / 25   │
│ 2. Structural Readability             │ 20%    │ 16 / 20   │
│ 3. Multi-Modal & Interactive Media    │ 15%    │ 12 / 15   │
│ 4. Authority & Brand Mentions         │ 20%    │ 10 / 20   │
│ 5. Technical Accessibility & Crawlers │ 20%    │ 14 / 20   │
├───────────────────────────────────────┼────────┼───────────┤
│ TOTAL GEO READINESS SCORE             │ 100%   │ 70 / 100  │
└───────────────────────────────────────┴────────┴───────────┘
```

---

## 2. Platform-Specific Visibility Breakdown

> *Note on Measurement:* Quantitative Share-of-Voice (SOV) tracking across ChatGPT Search and Google AI Overviews requires continuous DataForSEO or SE Ranking API monitoring. The assessments below represent qualitative architectural readiness and citation propensity.

### Google AI Overviews & AI Mode: **High Readiness**
- **Citation Logic:** 92% of AI Overview citations derive from top-10 ranking pages. AI Mode draws from a broader pool (~9 domains/query) where entity authority and fresh data override position.
- **Site Status:** Strong foundation. Server-side rendered (SSR) Liquid pages, comprehensive `Product` schema (`shippingDetails`, `hasMerchantReturnPolicy`, `aggregateRating`), canonical category breadcrumbs, and fast response times. High eligibility for inclusion in both standard AI Overviews and AI Mode conversational drill-downs.

### ChatGPT (OpenAI Search): **Moderate Readiness**
- **Citation Logic:** Heavily reliant on authoritative web references (Wikipedia accounts for ~47.9% of top citations; Reddit represents ~11.3%).
- **Site Status:** `OAI-SearchBot` is explicitly permitted to crawl `/products/`, `/collections/`, `/pages/`, and `/blogs/`. However, zero brand presence on Wikipedia and Reddit creates an entity corroboration deficit, making ChatGPT less likely to select FarmingTools.in as a primary third-party reference for generalized queries.

### Perplexity AI: **Low-to-Moderate Readiness**
- **Citation Logic:** Strongly favors community validation, technical comparison threads, and forum discussions (~46.7% Reddit citations).
- **Site Status:** `PerplexityBot` is allowed in `robots.txt`. However, Perplexity relies on raw HTML parsing (no JavaScript execution) and user-generated community verification. The site's client-side injected FAQ schema is invisible to Perplexity, and the absence of Reddit mentions dampens citation confidence.

### Claude Search (Anthropic): **Moderate Readiness**
- **Citation Logic:** Honors search crawler instructions and prioritizes deeply structured, highly factual, un-hyped prose.
- **Site Status:** `ClaudeBot` (Anthropic training crawler) is explicitly allowed. However, `Claude-SearchBot` (the crawler governing Claude search citability) is omitted from specific directives and falls back to default wildcard rules.

---

## 3. AI Crawler Access Status

Search citability crawlers and model-training crawlers govern entirely different capabilities. Below is the audited breakdown from `farmingtools.in/robots.txt`:

| Crawler User-Agent | Controlling Entity | Governed Capability | Status in robots.txt | Assessment & Impact |
|---|---|---|---|---|
| **`Googlebot`** | Google | Google Search, AI Overviews, AI Mode | **ALLOWED** | Unrestricted access to products, collections, policies, and blogs. Fully eligible for Google generative features. |
| **`OAI-SearchBot`** | OpenAI | ChatGPT Search Citability | **ALLOWED** | Whitelisted for `/products/`, `/collections/`, `/pages/`, `/blogs/`. Content is citable in ChatGPT real-time search. |
| **`PerplexityBot`** | Perplexity | Perplexity AI Search Citability | **ALLOWED** | Whitelisted for core catalog and content paths. Search indexable. |
| **`Claude-SearchBot`** | Anthropic | Claude Search Citability | **FALLBACK (`*`)** | **MISSING EXPLICIT DIRECTIVE.** Falls back to `User-agent: *`. Should be explicitly whitelisted alongside `OAI-SearchBot`. |
| **`Applebot`** | Apple | Siri, Spotlight, Safari Web Search | **FALLBACK (`*`)** | Inherits standard crawl allowances. Search discoverable. |
| **`GPTBot`** | OpenAI | OpenAI Model Training Only | **ALLOWED** | Allowed across site and `/pages/llms`. Note: Duplicate conflicting blocks detected in `robots.txt.liquid`. |
| **`ClaudeBot`** | Anthropic | Anthropic Model Training Only | **ALLOWED** | Allowed across catalog and `/pages/llms`. |
| **`Google-Extended`** | Google | Gemini / Vertex AI Training & Grounding | **ALLOWED** | Explicitly allowed on `/` and `/pages/llms`. (Does not govern AI Overviews). |
| **`Applebot-Extended`**| Apple | Apple Intelligence Model Training | **NOT OPTED OUT** | Falls back to generic rules. Allowed to train Apple foundation models. |
| **`CCBot`** | Common Crawl | LLM Training Corpora | **FALLBACK (`*`)** | Allowed via wildcard. |

> [!WARNING]
> **Robots.txt Duplicate Block Warning:** `templates/robots.txt.liquid` defines `User-agent: GPTBot`, `User-agent: ClaudeBot`, and `User-agent: PerplexityBot` twice—once in the upper category-filtered block and once under `# Generative Engine Optimization & LLM Discovery` with `Allow: /`. Consolidate these blocks to prevent non-standard parser truncation.

---

## 4. `llms.txt` & Agentic Standards Status

- **Status:** **PRESENT** at both `https://farmingtools.in/llms.txt` and `https://farmingtools.in/agents.md`.
- **Linked in Sitemap:** Yes, declared in `sitemap_agentic_discovery.xml`.
- **Current Content:** The file contains Shopify's standardized agent-commerce guide (covering the Shop skill, Universal Commerce Protocol / UCP direct MCP endpoints at `/api/ucp/mcp`, and WebMCP browser tools).
- **GEO Finding:**
  - Per Google Search Central documentation, Google Search and AI Overviews ignore `llms.txt`.
  - However, for non-Google LLMs and autonomous shopping assistants, the current file is strictly platform boilerplate. It does not mention:
    - Legal Entity: KRISHIGEARS INDIA PRIVATE LIMITED
    - Core Categories: Power Weeders (7HP / 9HP), Brush Cutters (2-Stroke / 4-Stroke), Battery Sprayers, Earth Augers, Spares
    - Direct catalog endpoints, subsidy assistance URLs (`/pages/government-subsidy-farm-equipment-2026`), or customer support coordinates.
- **Recommendation:** Append a domain-specific `# Agricultural Equipment Catalog & Machinery Specs` block beneath the UCP instructions.

---

## 5. Off-Site Brand Mentions & Entity Authority

Empirical studies (Ahrefs benchmark of 75,000 brands) confirm that **brand mentions correlate 3x more strongly with AI citations than backlinks** (YouTube ~0.737, Reddit high, Wikipedia high; Domain Rating backlinks ~0.266).

| Channel | Current Brand Footprint | Citation Impact & Gap |
|---|---|---|
| **Wikipedia / Wikidata** | **0 mentions** (No page or Wikidata entity) | Major bottleneck for ChatGPT and Google Knowledge Graph entity linking. |
| **Reddit** | **0 mentions** across r/farming, r/agriculture, or Indian regional subs | Severe deficit for Perplexity and ChatGPT citations, which rely heavily on Reddit for community sentiment. |
| **YouTube** | **Active Presence** (Demo videos, KG Reels, Balwaan sprayer demonstrations) | Strongest current AI visibility signal. Video schemas are properly linked via `ft-youtube-facade.liquid`. |
| **LinkedIn** | Minimal / Unindexed under primary brand names | Moderate authority gap; needs structured corporate profile linked via Organization `sameAs`. |
| **Government / B2B** | Strong presence on IndiaMART (`indiamart.com/krishigears/`), verified GSTIN, CIN | Establishes high business legitimacy; already connected via `ft-organization-json-ld.liquid`. |

---

## 6. Passage-Level Citability Analysis

AI engines select self-contained passages that directly answer specific queries. Studies indicate that **~44% of citations originate from the first 30% of a page**, and passages of 130–170 words with a direct answer in the first 40–60 words are optimal.

### Current Gaps Identified:
1. **Buried Definitions:** Many collection intros open with marketing taglines rather than definitive entity definitions (e.g., *"Power weeders are secondary tillage machines equipped with rotating blades driven by 7HP to 9HP engines designed to weed, aerate, and prepare soil between crop rows"*).
2. **Tabular vs Paragraph Specs:** Where technical parameters (engine displacement, fuel capacity, RPM, tilling width) are buried in flowing text, AI extraction confidence drops compared to semantic HTML comparison tables.
3. **The "Who/How/Why" Author Signal:** Article and guide authors frequently default to `"FarmingTools Agricultural Machinery Editorial Team"`, which AI engines score lower than credentialed domain specialists (e.g., Agricultural Engineers, Agronomists).

---

## 7. Server-Side Rendering (SSR) & Technical Accessibility

### The Good:
- Shopify Liquid compiles product titles, descriptions, breadcrumbs, prices, and specifications into server-rendered HTML.
- Crawlers that do not execute client-side JavaScript (e.g., `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`) receive full product titles, specs, and base markup upon initial HTTP response.

### The Critical Vulnerability: Client-Side Injected FAQ Schema
In `snippets/ft-faq-jsonld.liquid`:
```javascript
// Current Implementation:
(function(){
  function run(){
    var heads = document.querySelectorAll('h2');
    ...
    var ld = {'@context':'https://schema.org', '@type':'FAQPage', 'mainEntity': pairs...};
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.textContent = JSON.stringify(ld);
    document.head.appendChild(s);
  }
})();
```
- **Why this hurts GEO:** While Googlebot renders JavaScript and eventually evaluates this DOM script, **OpenAI's `OAI-SearchBot` and Perplexity's crawlers do not execute JavaScript**. To non-Google AI engines, this entire FAQPage schema is completely invisible.
- **Solution:** Render the `FAQPage` JSON-LD on the server using Liquid templating, exactly as done in `snippets/ft-faq-json-ld.liquid` and `sections/ft-product-jsonld.liquid`.

---

## 8. Top 5 Highest-Impact GEO Changes

1. **Migrate FAQ Schema to Server-Side Liquid (Technical):**
   Eliminate the client-side `document.createElement('script')` injection in `snippets/ft-faq-jsonld.liquid`. Emit `FAQPage` JSON-LD directly into the initial server HTML so `OAI-SearchBot` and `PerplexityBot` can extract questions and answers.
2. **Add Explicit `Claude-SearchBot` to robots.txt (Crawler Access):**
   Update `templates/robots.txt.liquid` to explicitly whitelist `Claude-SearchBot` alongside `OAI-SearchBot` and `PerplexityBot`, and eliminate duplicate `GPTBot` blocks.
3. **Seed Agricultural Machinery Entity Footprint on Reddit (Brand Authority):**
   Establish genuine, educational participation in subreddits (`r/IndianAgriculture`, `r/farming`, `r/gardening`) covering power weeder maintenance, small engine troubleshooting, and SMAM subsidy application processes.
4. **Deploy Self-Contained 130–170 Word Answer Blocks on Top Collections (Citability):**
   Add an explicit, quotable answer block answering "Which [machine] is best for [crop/land size]?" within the first 30% of each major collection page.
5. **Enrich `snippets/ft-organization-json-ld.liquid` with `knowsAbout` & Named Author Entities (Schema):**
   Add explicit `knowsAbout` agricultural entity tags to the organization schema, and replace anonymous editorial team bylines with credentialed author profiles.

---

## 9. Schema Recommendations for AI Discoverability

### A. Add `knowsAbout` to `snippets/ft-organization-json-ld.liquid`
Add an explicit entity graph declaration so LLMs recognize domain topical authority:
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://farmingtools.in/#organization",
  "name": "FarmingTools",
  "legalName": "KRISHIGEARS INDIA PRIVATE LIMITED",
  "knowsAbout": [
    "Agricultural Machinery",
    "Power Weeders and Tillers",
    "Brush Cutters and Crop Harvesters",
    "Sub-Mission on Agricultural Mechanization (SMAM)",
    "Small Engine Carburetor Maintenance",
    "Farm Equipment Subsidies in India"
  ],
  "areaServed": "IN"
}
```

### B. Standardize Author Entity on Guides (`snippets/ft-article-json-ld.liquid`)
Transform generic editorial strings into authoritative `Person` entities:
```json
"author": {
  "@type": "Person",
  "name": "Naresh Singh Bhau",
  "jobTitle": "Agricultural Machinery Specialist",
  "worksFor": {
    "@id": "https://farmingtools.in/#organization"
  },
  "sameAs": [
    "https://krishigears.com/about",
    "https://www.linkedin.com/company/krishigears"
  ]
}
```

---

## 10. Content Reformatting: Before & After Quotable Passages

### Example 1: Power Weeder Collection / Category Hub

#### ❌ Current / Conventional Copy (Vague, Sales-Heavy, Low Citability):
> *"Welcome to FarmingTools.in, India's favorite destination for top-rated power weeders. We offer durable machines with heavy-duty gearboxes and fuel-efficient engines from top brands like Balwaan and Neptune at unbeatable prices. Shop today with doorstep delivery!"*

#### ✅ GEO-Optimized Quotable Answer Block (142 Words, Self-Contained, Spec-Dense):
> **What is a power weeder and how do you choose the right horsepower?**  
> A power weeder (rotary tiller) is a secondary tillage machine powered by a 7 HP to 9 HP petrol or diesel engine designed to uproot weeds, aerate topsoil, and ridge soil between standing crops. For small landholdings (1 to 3 acres) and vegetables or sugarcane, a 7 HP 4-stroke petrol weeder with a 3-foot tilling width and belt-pulley drive offers optimum maneuverability and low fuel consumption (0.8–1.0 L/hr). For heavy black cotton soils or commercial plots exceeding 4 acres, a 9 HP direct-gear-driven diesel model delivers the torque required for deeper 6-to-8 inch tilling. Under the central SMAM (Sub-Mission on Agricultural Mechanization) scheme, eligible Indian farmers can receive 40% to 50% government subsidies on approved models through state agricultural portals.

---

### Example 2: Government Subsidy Hub (`/pages/government-subsidy-farm-equipment-2026`)

#### ❌ Current / Conventional Copy:
> *"Looking for farm machinery subsidies? You can save a lot of money on your next power weeder or brush cutter purchase through government programs. Check out our calculator to see what you qualify for."*

#### ✅ GEO-Optimized Quotable Answer Block (154 Words, Direct Fact-Matching):
> **How do Indian farmers claim 40%–50% machinery subsidies under SMAM 2026?**  
> Under India's Sub-Mission on Agricultural Mechanization (SMAM) and aligned state portals (such as DBT Agriculture Bihar, MahaDBT Maharashtra, and Rajkisan Rajasthan), small, marginal, SC/ST, and women farmers are eligible for up to 50% capital subsidies (capped between ₹25,000 and ₹65,000) on power weeders, sprayers, and brush cutters. General category farmers typically receive 40% financial assistance. To qualify, equipment must be tested by a certified FMTTI (Farm Machinery Training and Testing Institute) center and purchased through an authorized dealer with a GST invoice. Required documentation includes the 7/12 land record (Jamabandi), Aadhaar card, active bank passbook, and caste certificate where applicable. Farmers must apply online through their respective state agriculture DBT portal before purchasing to secure subsidy token approval.
