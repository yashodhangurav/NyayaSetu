# Project Transformation Plan: NyayaSetu (न्यायसेतु)

**Document:** `PROJECT_TRANSFORMATION_PLAN.md`  
**Date:** November 2026  
**Transformation Source:** Ellery Kowal LLP (Chicago Boutique Law Firm Recreation)  
**Target Product:** **NyayaSetu (न्यायसेतु)** — AI-Powered Legal Advisor and Advocate Matching Platform for India  
**Status:** Architecture Specification & Migration Roadmap (No code modified yet)  

---

## Executive Summary

This document specifies the blueprint for transforming the existing Next.js codebase into **NyayaSetu** (न्यायसेतु — *"Bridge to Justice"*), a premier AI-powered legal advisory and advocate-matching platform tailored to the Indian legal ecosystem (Bharatiya Nyaya Sanhita - BNS, Bharatiya Nagarik Suraksha Sanhita - BNSS, Bharatiya Sakshya Adhiniyam - BSA, Indian Contract Act, Supreme Court & High Court jurisdictions).

The transformation preserves the sophisticated editorial design language, typography (Gambetta serif & General Sans), warm sand/bronze/espresso palette, fluid Framer Motion micro-interactions, and modular React architecture established during the previous phase, while completely reorienting the domain, information architecture, data models, and user flows toward Indian litigants, startups, MSMEs, and Bar Council-enrolled advocates.

---

## 1. Codebase Inspection & Baseline Analysis

### 1. Current Next.js Architecture
- **Framework:** Next.js 16 (App Router) with Turbopack and Webpack support.
- **Rendering Strategy:** Static site generation with Partial Prerendering (`cacheComponents: true`, `partialPrefetching: true`) and dynamic route generation via `generateStaticParams()` for publication articles.
- **State Management:** Pure React client state (`useState`, `useRef`, `usePathname`) with zero heavy external database or backend dependencies. Fast, deterministic, and sandboxed.
- **TypeScript:** Strict type checking across `src/types/index.ts` and centralized mock datasets in `src/data/`.
- **Build Health:** 23 static/dynamic routes compile with **0 build errors** (`npm run build:webpack`).

### 2. All Existing Routes
| Existing Route | Current Purpose | Target Role in NyayaSetu |
| :--- | :--- | :--- |
| `/` | Ellery Homepage | **NyayaSetu Portal**: AI Legal Advisor intake, Advocate network preview, Indian practice domains, Clause annotator, Precedents, Legal rights explainers. |
| `/practices` | US Law Practice Hub (6 areas) | **Legal Domains & Services**: 6 core Indian domains (Civil & Property, Criminal Defense & Bail, Corporate & Startup, Matrimonial, Cheque Bounce / 138 NI Act, Consumer & Cyber). |
| `/people` | 7 Chicago Partners + Associates | **Verified Advocate Directory**: High Court & Supreme Court advocates filterable by court, city (Delhi, Mumbai, Bengaluru, etc.), bar standing, and languages. |
| `/matters` | 16 US Federal/Chancery cases | **Landmark Precedents & Scenarios**: 16 Indian dispute case studies & judgments (Supreme Court rulings, RERA orders, NCLT insolvency, Section 482 quashing). |
| `/firm` | LaSalle firm history & commitments | **About NyayaSetu & Ethical Framework**: Platform mission, Bar Council of India (BCI) Rule 36 compliance, AI safety protocols, and Pro Bono access initiative. |
| `/insights` | 9 Chicago legal treatises | **Kanoon Gyaan (Legal Guides)**: Plain-language Indian law guides (BNS 2024 changes, RERA builder disputes, 48-hr cyber fraud portal response, cheque bounce notices). |
| `/insights/[slug]` | Dynamic article template | **Legal Guide Reader**: Rich legal typography, applicable section citations, checklists, and recommended specialist advocates. |
| `/contact` | Conflict check intake form | **Advocate Matching & Consultation Desk**: Consultation scheduler, case intake, and urgent hotline for bail/injunction emergencies. |
| `/privacy` | US/IL legal privacy disclosure | **Privacy Policy**: Compliance with the Digital Personal Data Protection Act (DPDP Act 2023) and client privilege norms. |
| `/disclaimer` | US Attorney advertising | **Legal Disclaimer & BCI Disclosure**: Formal notice under Bar Council of India rules prohibiting solicitation/advertisement; non-law-firm platform status. |
| `not-found.tsx` | Custom 404 screen | **NyayaSetu 404 Recovery**: Preserved with updated Indian legal domain navigation. |

### 3. Existing Reusable Components
- **Layout:** `Navbar`, `Footer`, `Container`, `Section`, `BackToTop`.
- **UI Primitives:** `Button`, `Badge` (stamp, gold, sand, dark, solid, outline), `Card`, `Accordion`, `Tabs`, `Input`, `Select`, `Textarea`, `Modal`, `QuickConsultationModal`.
- **Homepage Sections:** `HeroSection`, `AboutStrip`, `PracticesSlider`, `TransparencyPreview`, `ContractAnnotator`, `MattersPreview`, `PartnerShowcase`, `ClientQuotes`, `LatestInsights`, `FaqSection`, `ConflictIntakeSection`.

### 4. Global CSS & Design Tokens
- **Palette:**
  - Primary Background: `#f3ece1` (warm alabaster) / `#f4efe6`
  - Secondary Background: `#ebe1d1` (warm sand)
  - Card Surface: `#fffaf2` (bright ivory card)
  - Dark Surface / Footer: `#24180f` / `#2a1c12` (deep espresso roast)
  - Accents: `#9a6a35` (warm bronze/ochre), `#d1a46a` (champagne gold), `#7c5226` (antique bronze)
  - Borders: `#e2d5c1` (muted stone)
- **Token Suitability for India:** This colorway evokes the dignity of red sandstone judicial architecture (Supreme Court of India, Delhi High Court), antique Indian paper documents, and bronze scales of justice. It is superior to generic blue SaaS tech styling.

### 5. Typography and Fonts
- **Headings / Editorial:** `Gambetta` (Fontshare serif) — regal, authoritative, timeless. Perfect for NyayaSetu.
- **Body & Controls:** `General Sans` (Fontshare grotesk sans) — high readability, modern, balanced.
- **Mono / Accents:** `Inter` monospace for court numbers, sections (BNS/CrPC), and bar enrolment IDs.

### 6. Existing Images & Media Assets
- Authentic legal imagery (statue of justice cutout, legal documents, conference tables, courthouse architecture, portraits).
- Needs selective substitution:
  - Lady Justice statue is universal to Indian jurisprudence (Supreme Court recently placed the unblindfolded statue holding the Constitution of India).
  - Chicago street/building photos replaced with High Court / Supreme Court / Indian corporate legal settings.
  - US partner portraits replaced with Indian advocate profiles.

### 7. Navigation & Footer
- Header currently has `EK` monogram and Chicago-specific links.
- Needs update to **NyayaSetu (न्यायसेतु)** branding with vector scales/bridge icon and Indian navigation items:
  - `• Home`, `Legal Domains ˅`, `Find Advocates`, `Precedents`, `Legal Guides`, `About NyayaSetu`
  - CTA: `[ Ask AI Advisor | → ]`

### 8. Animations & Micro-Interactions
- Smooth Framer Motion fade-ins, tab switches, and hover effects.
- Compound action button hover physics.
- Accordion open/collapse transitions.
- All animation primitives are 100% reusable.

### 9. Interactive Components
- **Practices Slider:** Smooth horizontal scrolling carousel with dot indicators.
- **Transparency Scheduler:** Day/time picker and dynamic partner fee calculators.
- **Contract Annotator:** Clickable redlined clauses synchronized with lawyer critique cards.
- **Matters Ledger:** Filter tabs and expandable case briefs.
- **Partner Showcase:** Interactive profile switcher.
- **Consultation Modals:** Multi-step intake and quick booking dialogs.

### 10. Responsive Layouts
- Verified at 4 breakpoints: `1440×900` (Desktop), `1280×800` (Laptop), `768×1024` (Tablet), and `390×844` (Mobile).
- Zero horizontal overflows; mobile drawer navigation fully functional.

---

## 2. Transformation Strategy: Ellery Kowal → NyayaSetu

```
Ellery Kowal LLP (US Law Firm)                NyayaSetu (न्यायसेतु)
┌─────────────────────────────────┐           ┌───────────────────────────────────────────────┐
│ • LaSalle Street Chicago firm   │           │ • AI Legal Advisor & Advocate Match (India)   │
│ • 7 Private equity & trial attys│    ───►   │ • 2,800+ Verified Bar Council Advocates       │
│ • US Federal/Cook County law    │           │ • BNS, BNSS, BSA, Contract Act, RERA, NI Act  │
│ • Billable hourly rates ($650+) │           │ • Transparent fixed consultations (from ₹499) │
│ • Conflict check for corporate  │           │ • Multi-jurisdiction (SC, HC, District Courts)│
└─────────────────────────────────┘           └───────────────────────────────────────────────┘
```

---

## 3. Component Inventory: Reuse, Redesign & Creation

### A. Components to Reuse Directly (With Content & Prop Updates)
1. **`src/components/layout/container.tsx`** — Responsive max-width wrappers (`sm`, `md`, `lg`, `xl`, `full`).
2. **`src/components/layout/section.tsx`** — Section spacing and background wrapper.
3. **`src/components/layout/back-to-top.tsx`** — Smooth back-to-top button.
4. **`src/components/ui/button.tsx`** — Compound button, bronze button, dark outline button.
5. **`src/components/ui/badge.tsx`** — Stamp, gold, sand, and dark badge variants.
6. **`src/components/ui/accordion.tsx`** — Expandable FAQ and document accordion.
7. **`src/components/ui/tabs.tsx`** — Filter tabs for court jurisdictions and categories.
8. **`src/components/ui/modal.tsx`** — Accessible dialog container.
9. **`src/components/ui/input.tsx`** — Styled inputs, selects, and textareas.
10. **`src/components/sections/practices-slider.tsx`** — Carousel repurposed for 6 Indian Legal Domains.
11. **`src/components/sections/client-quotes.tsx`** — Litigant and startup founder testimonial slider.
12. **`src/components/sections/faq-section.tsx`** — Common queries regarding AI legal advice, advocate matching, and BCI compliance.

---

### B. Components Requiring Redesign / Adaptation
1. **`src/components/layout/navbar.tsx`:**
   - Replace `EK` monogram with **NyayaSetu (न्यायसेतु)** logo featuring an Indian legal seal (concentric Ashoka-inspired ring with Scales of Justice & Bridge motif).
   - Update nav links to: `Home`, `Legal Domains ˅`, `Find Advocates`, `Precedents`, `Legal Guides`, `About`.
   - Update CTA to `[ Ask AI Advisor | → ]`.
2. **`src/components/sections/hero-section.tsx`:**
   - Background watermark: change `EVIDENCE` to **`NYAYA`** (न्याय - Justice) or **`DHARMA`**.
   - Headline: *"Where Indian law meets instant clarity."* / *"Your bridge to legal clarity and verified advocates across India."*
   - Seal text: `"NYAYA SETU · AI LEGAL ADVISOR & ADVOCATE NETWORK · BHARAT · ESTD 2026 ·"`.
   - Floating chips: `Property & RERA +`, `BNS & Criminal Bail +`, `Cheque Bounce (138 NI) +`.
   - Action buttons: `[ Ask AI Legal Advisor | → ]` and `[ Find Verified Advocates ]`.
3. **`src/components/sections/about-strip.tsx`:**
   - Adapt 4 metrics:
     - `2,800+` Verified Advocates Enrolled
     - `28` High Courts & Supreme Court Covered
     - `150,000+` Legal Inquiries Simplified
     - `100%` Bar Council of India (BCI) Rule 36 Ethical Compliance
   - Photo replacements: Heritage architecture of Delhi High Court / Bombay High Court and modern legal tech workspaces.
4. **`src/components/sections/transparency-preview.tsx`:**
   - **Card 1 (First Consultation):** 30-minute verified advocate consultation booking (from ₹999, audio/video or chamber visit).
   - **Card 2 (Fixed Fee Packages):** Standard legal notice (₹2,499), RERA complaint draft (₹4,999), Startup founder agreement (₹5,999).
   - **Card 3 (AI Legal Assessment Report):** Case merit score, applicable BNS/BNSS sections, statute of limitations timeline, and checklist of required court evidence.
5. **`src/components/sections/contract-annotator.tsx`:**
   - Adapt into **"AI Legal Clause Analyzer"** showcasing Indian contract law:
     - Real Indian clause: Restrictive Employment Non-Compete or Builder-Buyer Delay Penalty.
     - Redlined with statutory commentary under **Section 27 of the Indian Contract Act, 1872** (agreements in restraint of trade void) and **Section 18 of RERA 2016** (unilateral one-sided clauses void).
     - Notes from Senior Advocates (Delhi High Court, Bombay High Court).
6. **`src/components/sections/matters-preview.tsx`:**
   - Adapt into **"Landmark Precedents & Representative Matters"**:
     - Categories: `All`, `Civil & Property`, `Criminal & Bail`, `Commercial & Startup`, `Consumer & Cyber`.
     - Columns: `Outcome / Relief`, `Subject / Landmark Precedent`, `Forum / Bench`, `Year`.
7. **`src/components/sections/partner-showcase.tsx`:**
   - Adapt into **"Featured Advocates & Legal Experts"**:
     - Highlights senior advocates across Supreme Court, Delhi HC, Bombay HC, Karnataka HC.
     - Shows Bar Council enrolment number, years of standing, languages spoken, and primary bench.
8. **`src/components/sections/conflict-intake-section.tsx`:**
   - Adapt into **"Get AI Legal Guidance & Matched Counsel"**:
     - Multi-step intake: Legal category, Court level (District / High Court / Supreme Court), State & City, Urgency (e.g. Anticipatory Bail / 24h, 15-day notice response, general advisory), and non-solicitation disclaimer.
9. **`src/components/layout/footer.tsx`:**
   - Replace Chicago coordinates with Pan-India presence: New Delhi, Mumbai, Bengaluru, Hyderabad.
   - Helpline: `1800-NYAYA-SETU` / `+91 (11) 4555-0199`.
   - Bar Council of India Rule 36 compliance statement: *NyayaSetu is an AI-powered legal information platform and advocate directory, not a law firm.*

---

### C. New Components to Create
1. **`src/components/sections/ai-advisor-preview.tsx`:**
   - An interactive preview of the **NyayaSetu AI Legal Assistant**:
   - Allows users to test typical queries (e.g., *"My landlord is refusing to return my security deposit"*, *"Received a Section 138 notice for cheque bounce"*, *"Can a company enforce a 2-year non-compete in India?"*).
   - Demonstrates instant AI citation of Indian legal acts, remedies, and estimated court timelines.
2. **`src/components/ui/court-badge.tsx`:**
   - Specialized badge displaying Indian court jurisdictions: `Supreme Court of India`, `Delhi High Court`, `Bombay High Court`, `NCLT Principal Bench`, `District & Sessions Court`.
3. **`src/components/ui/advocate-card.tsx`:**
   - Rich advocate card component showing Bar Council verification badge, court standing, languages, consultation fee, and instant booking CTA.

---

### D. Content & Data to Remove / Replace
| Old US Content to Remove | New Indian Replacement in NyayaSetu |
| :--- | :--- |
| Ellery Kowal LLP / Chicago firm | **NyayaSetu (न्यायसेतु)** — Pan-India Legal Tech Platform |
| 224 S. LaSalle Street, 31st Floor | Jurisdictions across Supreme Court of India, 28 High Courts, 600+ District Courts |
| US Federal Court (N.D. Ill.), 7th Circuit, Cook County | Supreme Court of India, High Courts (Delhi, Bombay, etc.), NCLT, RERA, Consumer Commissions |
| US Statutes: BIPA, IL Freedom to Work Act, Delaware Chancery | Indian Statutes: BNS 2023, BNSS 2023, BSA 2023, Indian Contract Act 1872, NI Act Sec 138, RERA 2016, DPDP Act 2023 |
| American attorney hourly billing ($650–$825/hr) | Transparent Indian fee models: Free AI query assessment, fixed consultation (₹999–₹2,500), transparent appearance fees |
| Partner names: Margaret Ellery, Tomasz Kowal, Owen Pryce | Indian Advocates: Adv. Rajeshwari Sen (SC/Delhi HC), Adv. Vikramaditya Deshmukh (Bombay HC), Adv. Ananya Sundaram (Karnataka HC), etc. |

---

## 4. Target Route Architecture for NyayaSetu

```
src/app/
├── layout.tsx                     # Global HTML, NyayaSetu metadata, fonts, header & footer
├── page.tsx                       # Homepage (AI Advisor, Advocate Match, Domains, Precedents)
├── globals.css                    # Tailwind v4, Indian sandstone/bronze palette, Gambetta/General Sans
├── practices/                     # Legal Domains & Services Hub (Civil, Criminal, Corporate, etc.)
│   └── page.tsx
├── people/                        # Verified Advocate Directory (Filter by High Court, City, Standing)
│   └── page.tsx
├── matters/                       # Landmark Legal Precedents & Case Studies
│   └── page.tsx
├── firm/                          # About NyayaSetu, BCI Ethics, AI Safety & Pro Bono
│   └── page.tsx
├── insights/                      # Kanoon Gyaan (Legal Guides & Plain-English Explanations)
│   ├── page.tsx
│   └── [slug]/page.tsx            # Dynamic pre-rendered legal guide pages
├── contact/                       # Advocate Consultation Booking & Litigant Helpdesk
│   └── page.tsx
├── privacy/                       # DPDP Act 2023 & Confidentiality Policy
│   └── page.tsx
├── disclaimer/                    # Bar Council of India (BCI) Non-Solicitation Notice
│   └── page.tsx
└── not-found.tsx                  # Custom 404 with Indian Legal Navigation
```

---

## 5. Mock Data Restructuring Strategy (`src/data/`)

All data files will be rewritten with authentic, detailed Indian legal data while preserving existing TypeScript interfaces:

1. **`src/data/practices.ts` (6 Core Legal Domains):**
   - `01`: Civil & Property Law (Partition, Title Disputes, RERA, Injunctions)
   - `02`: Corporate & Startup Law (Companies Act 2013, Founder Agreements, Term Sheets, M&A)
   - `03`: Criminal Defense & Bail (Bharatiya Nyaya Sanhita - BNS, Regular & Anticipatory Bail under BNSS)
   - `04`: Matrimonial & Family Law (Mutual Divorce, Child Custody, Maintenance under BNS/HMA)
   - `05`: Cheque Bounce & Debt Recovery (Section 138 NI Act, Commercial Courts, Summary Suits)
   - `06`: Consumer & Cyber Fraud (Consumer Protection Act 2019, Cyber Crime Portal 1930, IT Act)

2. **`src/data/lawyers.ts` (Verified Indian Advocates Roster):**
   - 7 Senior Advocate profiles with real Bar Council enrolment formats (`D/1420/2004`, `MAH/2841/1998`, etc.), practice courts (Supreme Court of India, Delhi HC, Bombay HC), years of standing (14 to 28 years), educational backgrounds (NLSIU Bengaluru, Faculty of Law DU, ILS Pune), languages (English, Hindi, Marathi, Kannada, Bengali), and verified fee structures.

3. **`src/data/matters.ts` (16 Landmark Precedents & Scenarios):**
   - Cases spanning Section 138 NI Act, RERA compensation, anticipatory bail quashing, consumer airline refunds, trademark protection, and shareholder dispute resolutions before NCLT.

4. **`src/data/articles.ts` (9 Kanoon Gyaan Legal Guides):**
   - *Understanding the new BNS vs IPC: key changes for citizens*
   - *Cheque bounce under Section 138 NI Act: timeline, notice & defenses*
   - *RERA delay penalty: how homebuyers can claim refund and interest*
   - *Non-compete clauses in Indian employment: why Section 27 makes them void*
   - *Cyber crime financial fraud: the first 48 hours and portal 1930*
   - *Mutual consent divorce in India: step-by-step procedure & cooling-off period*
   - *How to respond to a police notice under Section 35(3) BNSS*
   - *Startup co-founder agreement: 5 essential terms before taking funding*
   - *Tenant rights and security deposit refund in Delhi, Mumbai and Bengaluru*

5. **`src/data/faqs.ts` (Indian Litigant FAQs):**
   - Is AI legal advice legally binding?
   - How does NyayaSetu verify advocate bar council credentials?
   - How do fixed-fee consultations work?
   - Can NyayaSetu help with urgent bail matters?
   - How does the platform comply with Bar Council of India rules?

6. **`src/data/firm.ts` (NyayaSetu Platform Mission & BCI Compliance):**
   - Mission: Bridging the 5-crore pending case backlog in India through AI triage, rights literacy, and ethical advocate matching.
   - Four core commitments: Zero hidden clerk fees, 100% verified Bar Council advocates, plain-language legal clarity, and free pro bono access for underprivileged citizens.

---

## 6. Phased Implementation Roadmap

To maintain build stability throughout the transformation, the rollout will follow strict phases:

### Phase 1: Data Models & Mock Datasets (`src/data/` & `src/types/`)
- Update `src/types/index.ts` with Indian jurisdiction models (Bar Council enrolment, Court types, Indian legal acts).
- Overwrite all datasets in `src/data/` with the authentic NyayaSetu Indian legal domain content.
- Verify TypeScript compilation (`npm run build:webpack`).

### Phase 2: Brand Identity, Navigation & Global Layout
- Update `src/app/layout.tsx` with NyayaSetu metadata, title templates, and open-graph tags.
- Update `src/components/layout/navbar.tsx` with NyayaSetu branding, new nav links, and CTA.
- Update `src/components/layout/footer.tsx` with Indian office hubs, helpline numbers, and BCI Rule 36 disclaimers.

### Phase 3: Homepage Sections Transformation
- **Hero:** Watermark `NYAYA`, Indian law headline, Ashoka seal ring, and new action buttons.
- **About Strip:** Indian metrics (`2,800+` Advocates, `28` Courts) and narrative.
- **Practices Slider:** 6 Indian legal domains with authentic imagery.
- **Fee Transparency:** Standardized consultation slots and fixed packages in Indian Rupees (₹).
- **Contract Annotator:** Redlined Section 27 Indian Contract Act non-compete clause.
- **Matters Preview:** Landmark Indian legal precedents ledger with category filters.
- **Partner Showcase:** Featured Advocates across Supreme Court and High Courts.
- **Testimonials & Insights:** Litigant stories and Kanoon Gyaan articles.
- **FAQ & Intake:** Indian court procedures and legal assessment intake form.

### Phase 4: Sub-Pages Transformation
- `/practices`: Complete Indian Legal Domains dossier with court jurisdictions and fee ranges.
- `/people`: Advocate directory with search and filter by Court / City / Standing.
- `/matters`: Landmark precedents catalog with expandable case briefs.
- `/firm`: NyayaSetu mission, BCI ethics, and Pro Bono legal aid.
- `/insights` & `/insights/[slug]`: 9 Indian legal treatises.
- `/contact`: Consultation booking and litigant intake desk.
- `/privacy` & `/disclaimer`: DPDP Act 2023 and Bar Council of India non-solicitation notice.

### Phase 5: Verification & QA
- Viewport verification at `1440px`, `1280px`, `768px`, and `390px`.
- Verification of zero TypeScript or hydration errors.
- Verification of full production build via `npm run build:webpack`.

---

## 7. Compliance with Constraints

1. **Preserve Existing Codebase:** No project deletion; no starting from scratch.
2. **Preserve High-Quality Visual Design:** Editorial serif typography, warm sandstone palette, fine borders, and micro-interactions retained in full.
3. **No Automatic Background Dev Servers:** Commands will run safely within standard build and verification tools.
4. **Zero Backend Requirement:** Runs entirely in client-side React state with rich interactive feedback.

