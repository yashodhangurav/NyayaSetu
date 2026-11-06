# Content Replacement Plan: NyayaSetu (न्यायसेतु)
### AI-Powered Legal Advisor & Advocate Matching Platform for India

**Document:** `CONTENT_REPLACEMENT_PLAN.md`  
**Date:** November 2026  
**Project Goal:** Convert the existing Next.js frontend (recreated from Ellery Framer) into a college project: **NyayaSetu (न्यायसेतु) — AI-Powered Legal Advisor and Advocate Matching Platform for India.**  
**Core Constraint:** **100% Visual Design Preservation.** Zero redesigns, zero layout changes, zero font/typography changes, zero color changes, zero component replacements. Only content, labels, copy, mock datasets, and contextual assets are updated.

---

## 1. Visual & Architectural Preservation Guarantees

| Design System Dimension | Current Implementation | Preservation Status |
| :--- | :--- | :--- |
| **Grid & Layouts** | 12-column responsive grid, max-w-[1424px], responsive containers (`sm`, `md`, `lg`, `xl`) | **100% Unchanged** |
| **Color Tokens** | Alabaster `#f4efe6`, ivory `#fffaf2`, bronze `#9a6a35`, espresso `#2a1c12`, borders `#e2d5c1` | **100% Unchanged** |
| **Typography Scale** | `Gambetta` (editorial serif) + `General Sans` (body sans) + `Inter` (mono) | **100% Unchanged** |
| **Spacing & Padding** | Exact section vertical paddings (`py-20 lg:py-28`, `py-16 lg:py-24`), gaps (`gap-6`, `gap-8`, `gap-12`) | **100% Unchanged** |
| **Animations & Timing** | Framer Motion fade-ins, transition ease `[0.16, 1, 0.3, 1]`, duration `0.5s` | **100% Unchanged** |
| **Component Mechanics** | Compound button with separate arrow chamber, sliders, accordions, modals, tabs | **100% Unchanged** |
| **Breakpoints** | Mobile (`390px`), Tablet (`768px`), Laptop (`1280px`), Desktop (`1440px`) | **100% Unchanged** |

---

## 2. Section-by-Section Content Replacement Matrix

### Section 1: Global Navigation & Header
- **Component File:** `src/components/layout/navbar.tsx`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Brand Logo Text: `"Ellery Kowal"` + small-caps `"LLP"`.
  - Monogram SVG: Interlocking `EK` paths.
  - Nav Items: `• Home`, `Practices ˅`, `People`, `Matters`, `Insights`, `The firm`.
  - Dropdown items in Practices: US corporate practice titles.
  - Primary CTA Button: `"Start a conflict check"`.
  - Mobile Drawer Title & Links: Chicago firm references.
- **Suggested NyayaSetu Content:**
  - Brand Logo Text: `"NyayaSetu"` + small-caps `"BHARAT"` or `"INDIA"` (rendered in same font size, weight, and tracking).
  - Monogram SVG: Same vector container featuring a stylized Indian judicial scale / justice bridge symbol in `#9a6a35` and `#2a1c12`.
  - Nav Items: `• Home`, `Legal Areas ˅`, `Find Advocates`, `Precedents`, `Legal Guides`, `About Us`.
  - Dropdown items: `Civil & Property`, `Criminal & Bail`, `Corporate & Startup`, `Cheque Bounce (138 NI)`, `Family & Matrimonial`, `Consumer & Cyber`.
  - Primary CTA Button: Compound button text: `"Ask AI Advisor" | [ → ]`.
  - Mobile Drawer: Updated with NyayaSetu platform links and 24/7 legal helpline.

---

### Section 2: Hero Section (Homepage)
- **Component File:** `src/components/sections/hero-section.tsx`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Watermark Word: `"EVIDENCE"` (font-size 282px, gradient fill).
  - Main Headline: `"Every word is evidence."` (with `"evidence."` in `#9a6a35`).
  - Partner Cluster Caption: `"Seven partners, one floor of 224 S. LaSalle"`.
  - Verdict Subtitle: `"Our trial team has taken 34 cases to verdict. Most of our cases still settle, and opposing counsel knows why."`.
  - Lede Paragraph: `"Business lawyers on LaSalle Street since 2011. Our deal lawyers and trial lawyers draft every contract together, as if it will one day be argued."`.
  - Primary Button: `"Start a conflict check"`.
  - Secondary Ghost Button: `"Our practices"`.
  - Circular Rotating Seal SVG: `"ELLERY KOWAL LLP · 224 SOUTH LASALLE STREET · CHICAGO · ESTABLISHED 2011 ·"`.
  - Bronze Centerpiece Cutout: Bronze Lady Justice holding scales and sword.
  - Floating Practice Badges:
    - `"Trials & Disputes +"`
    - `"Corporate & M&A +"`
    - `"Employment +"`
- **Suggested NyayaSetu Content:**
  - Watermark Word: **`NYAYA`** (न्याय - Justice) or **`JUSTICE`** (rendered with identical gradient mask, letter-spacing, and position).
  - Main Headline: `"Where Indian law meets instant clarity."` (with `"instant clarity."` in `#9a6a35`).
  - Partner Cluster Caption: `"2,800+ verified advocates across 28 High Courts"`.
  - Verdict Subtitle: `"Our AI engine has simplified **150,000+ legal queries**. Instant case analysis, statutory citations, and advocate representation before you step into court."`.
  - Lede Paragraph: `"India’s trusted legal intelligence and advocate matching platform. Explain your dispute in plain language, understand your rights under BNS and central acts, and consult verified counsel."`.
  - Primary Button: Compound button text: `"Ask AI Legal Advisor"` | `[ → ]`.
  - Secondary Ghost Button: `"Explore Legal Areas"`.
  - Circular Rotating Seal SVG: `"NYAYASETU · AI LEGAL ADVISOR & ADVOCATE NETWORK · BHARAT · ESTABLISHED 2026 ·"`.
  - Bronze Centerpiece Cutout: Retain the authentic Lady Justice bronze statue (the universal symbol of Indian jurisprudence and courts).
  - Floating Practice Badges:
    - `"Civil & Property +"`
    - `"Bail & Criminal Law +"`
    - `"Cheque Bounce (138 NI) +"`

---

### Section 3: About Platform Strip & Metrics (Homepage)
- **Component File:** `src/components/sections/about-strip.tsx`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Top Badge: `"About the firm"`.
  - Headline: `"Ellery Kowal has 41 lawyers, six practices and one floor on LaSalle Street..."`.
  - Narrative Paragraph: `"Founded in 2011... 34 cases to verdict... 92% of cases settle..."`.
  - Metric 1: `41` / `"Lawyers on LaSalle"`.
  - Metric 2: `34` / `"Cases to verdict"`.
  - Metric 3: `15` / `"Years on LaSalle"`.
  - Metric 4: `92%` / `"Litigation on budget"`.
  - Photos: Limestone entrance & 31st floor reception.
- **Suggested NyayaSetu Content:**
  - Top Badge: `"About NyayaSetu"`.
  - Headline: `"NyayaSetu bridges India's judicial information divide with AI clarity and verified advocates."`.
  - Narrative Paragraph: `"Over 5 crore cases pend across Indian courts because citizens lack early rights awareness and transparent advocate access. NyayaSetu combines trained Indian legal AI with a nationwide network of Bar Council-enrolled advocates across 28 High Courts and the Supreme Court."`.
  - Metric 1: `2,800+` / `"Verified Advocates"`.
  - Metric 2: `28` / `"High Courts & Supreme Court"`.
  - Metric 3: `150k+` / `"Legal Inquiries Simplified"`.
  - Metric 4: `100%` / `"Bar Council of India Verified"`.
  - Photos: High Court / Supreme Court judicial architecture and modern Indian legal consultation chambers.

---

### Section 4: Legal Areas Horizontal Carousel (Homepage)
- **Component File:** `src/components/sections/practices-slider.tsx` & `src/data/practices.ts`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Section Headline: `"Six practices, one floor."` (with `"one floor."` in `#9a6a35`).
  - Section Subtitle: `"Each practice is led by a partner who picks up the phone, with the fee model stated up front."`.
  - 6 Cards Content (currently US law):
    - Card 01: `"Trials & Disputes"` (`From $650/hr`)
    - Card 02: `"Corporate & M&A"` (`From $3,500`)
    - Card 03: `"Employment"` (`From $1,800`)
    - Card 04: `"Investigations"` (`From $25,000 retainer`)
    - Card 05: `"Real Estate"` (`From $4,500`)
    - Card 06: `"IP & Technology"` (`From $2,400`)
- **Suggested NyayaSetu Content:**
  - Section Headline: `"Six legal domains, verified counsel."` (with `"verified counsel."` in `#9a6a35`).
  - Section Subtitle: `"Each legal domain is backed by Bar Council-verified advocates with transparent consultation fees stated up front."`.
  - 6 Indian Legal Domain Cards:
    - Card 01: `"Civil & Property Law"` | Top Badges: `01` & `From ₹999/consult` | Tagline: `"Partition suits, title deeds, illegal possession, and RERA builder disputes."` | Lead: `"Adv. Rajeshwari Sen & Team"` | Model: `"Fixed consultation or court appearance"`.
    - Card 02: `"Startup & Corporate Law"` | Top Badges: `02` & `From ₹2,499/draft` | Tagline: `"Founder agreements, Companies Act compliance, term sheets, and MCA filings."` | Lead: `"Adv. Vikramaditya Deshmukh"` | Model: `"Fixed package per document"`.
    - Card 03: `"Employment & Labor Law"` | Top Badges: `03` & `From ₹1,499/review` | Tagline: `"Wrongful termination, non-compete validity, POSH compliance, and unpaid dues."` | Lead: `"Adv. Sunita Banerjee"` | Model: `"Per document review or dispute notice"`.
    - Card 04: `"Criminal Defense & Bail"` | Top Badges: `04` & `From ₹1,999/consult` | Tagline: `"Bharatiya Nyaya Sanhita (BNS), Anticipatory Bail under BNSS, and FIR quashing."` | Lead: `"Adv. Harshvardhan Kapoor"` | Model: `"Urgent emergency or regular bail fee"`.
    - Card 05: `"Cheque Bounce & Debt Recovery"` | Top Badges: `05` & `From ₹2,499/notice` | Tagline: `"Section 138 Negotiable Instruments Act statutory notices, summary suits, and recovery."` | Lead: `"Adv. Pradeep Nair"` | Model: `"Fixed statutory notice package"`.
    - Card 06: `"Consumer & Cyber Law"` | Top Badges: `06` & `From ₹999/filing` | Tagline: `"Consumer Protection Act 2019 claims, airline refunds, and Cyber Crime Portal 1930."` | Lead: `"Adv. Ananya Sundaram"` | Model: `"Online complaint filing package"`.

---

### Section 5: Standardized Fees & AI Case Assessment (Homepage)
- **Component File:** `src/components/sections/transparency-preview.tsx`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Section Headline: `"Know the cost, the partner and the next step."` (second line in `#a89682`).
  - Card 1 (Scheduler): `"First call · 30 minutes, no charge"`, `"Central time"`, US partner avatars, `"With Margaret Ellery, by phone or at the office"`.
  - Card 2 (Fixed Fees): `"Schedule A · Fixed fees"`, `"Company formation and operating agreement"`, `"$3,500"`, US checklist.
  - Card 3 (Monthly Status Report): `"Monthly report"`, `"Dear Ms. Alvarez, Discovery closes next month..."`, `"$148,200 of $240,000"`, US court timeline.
- **Suggested NyayaSetu Content:**
  - Section Headline: `"Know your rights, the cost and the next step."` (with `"and the next step."` in `#a89682`).
  - Card 1 (Advocate Consultation Booking):
    - Header: `"Advocate Consultation · 30 minutes"` | Right: `"Indian Standard Time"`.
    - Avatars: 4 Indian Senior Advocates (e.g., Adv. Rajeshwari Sen, Adv. Vikramaditya Deshmukh, Adv. Ananya Sundaram, Adv. Harshvardhan Kapoor).
    - Inputs: `dd/mm/yyyy`, Time selector (`"10:30 AM IST"`, `"2:30 PM IST"`, etc.), Name, Phone/Email.
    - Note: `"With Adv. Rajeshwari Sen, via encrypted video or advocate chamber"`.
    - Compound CTA: `"Book consultation slot"` | `[ → ]`.
  - Card 2 (Fixed Legal Services Schedule):
    - Header: `"Schedule A · Fixed Fees"` | Right: Monogram SVG.
    - The Work Dropdown:
      - `"Legal notice under Section 138 NI Act (Cheque Bounce)"` (`₹2,499`)
      - `"Startup founder agreement drafting & vesting"` (`₹4,999`)
      - `"RERA delay compensation complaint drafting"` (`₹5,999`)
      - `"Consumer forum complaint & affidavit preparation"` (`₹3,499`)
    - Pricing: `₹2,499` / `"delivered in 3 business days by verified advocate"`.
    - Checklist:
      - `✓ Bar Council enrolled advocate drafting`
      - `✓ Preliminary strategy phone call included`
      - `✓ Sent via Registered Speed Post & tracking ID`
      - `✓ Full statutory 15-day notice compliance`
  - Card 3 (AI Legal Dossier & Case Tracker):
    - Header: `"AI Legal Assessment"` | Right: `"Instant Report"`.
    - Title: `"Case Assessment · Security Deposit Dispute"`.
    - Body: `"Landlord has withheld **₹1,20,000 deposit** past 30 days without itemized deductions. Under state rent laws and Indian Contract Act, retention without lawful cause entitles tenant to 12% interest."`.
    - Progress Bar: `84% Legal Merit Score` (Bronze filled bar).
    - Timeline:
      - `Day 1`: AI formal demand notice drafted
      - `Day 5`: Speed post delivery acknowledged
      - `Day 15`: 15-day statutory window expires
    - Next Phase Callout: `"Next: File summary claim before Rent Tribunal or Small Causes Court. Advocate match briefed."`.

---

### Section 6: AI Legal Clause Analyzer (Homepage)
- **Component File:** `src/components/sections/contract-annotator.tsx`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Section Headline: `"Drafted by people who try cases."` (second line in `#a89682`).
  - Section Subtitle: `"Most contract fights turn on a sentence nobody argued about at signing..."`.
  - Redlined Clause: US Master Services Agreement Article 12 (indemnity & liability caps).
  - 3 Callouts & Partner Cards: Owen Pryce, Tomasz Kowal, Margaret Ellery discussing US corporate litigation.
- **Suggested NyayaSetu Content:**
  - Section Headline: `"Reviewed by advocates who argue in court."` (with `"who argue in court."` in `#a89682`).
  - Section Subtitle: `"Most legal disputes in India arise from one-sided clauses buried in contracts. See how our AI and High Court advocates analyze risky terms before you sign."`.
  - Redlined Clause (Indian Employment / Commercial Agreement):
    - Header: `"Standard Employment Agreement · Clause 14 Review"`.
    - Title: `"Clause 14. Non-Compete & Restrictive Covenants"`.
    - Redlined Text:
      `"14.1 Employee agrees that for twenty-four (24) months following termination, Employee shall not `
      `<del>directly or indirectly engage with any competing business across India</del> <mark>arising under Section 27¹</mark> `
      `nor solicit any client, subject to liquidated damages of <del>₹25,00,000</del> <mark>reasonable compensation only²</mark> `
      `subject to exclusive jurisdiction in <del>Singapore</del> <mark>courts where cause of action arose³</mark>."`
  - 3 Advocate Critique Notes:
    - Note 1 (Adv. Rajeshwari Sen · Supreme Court of India · note 1):
      *"Under Section 27 of the Indian Contract Act 1872, all agreements in restraint of trade, profession, or lawful business are void. Post-employment non-compete clauses cannot be enforced against employees in India."*
    - Note 2 (Adv. Vikramaditya Deshmukh · Bombay High Court · note 2):
      *"Indian courts do not award punitive contractual damages under Section 74. The employer must prove genuine actual loss, making arbitrary penalty sums legally unenforceable."*
    - Note 3 (Adv. Ananya Sundaram · Karnataka High Court · note 3):
      *"Parties cannot confer jurisdiction on a foreign court or exclude Indian domestic courts if the cause of action and employment arose entirely within India."*

---

### Section 7: Representative Precedents & Judgments (Homepage)
- **Component File:** `src/components/sections/matters-preview.tsx` & `src/data/matters.ts`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Section Headline: `"Prepared for trial. That’s why most settle."`.
  - Subhead: `"A few recent results, without the client names."`.
  - Category Filter Tabs: `All`, `Disputes`, `Transactions`, `Investigations`.
  - Table Rows: US federal cases ($18.4M jury verdict, $212M food company sale, etc.).
  - Bottom Link: `"All representative matters"`.
- **Suggested NyayaSetu Content:**
  - Section Headline: `"Groundwork in law. That’s why disputes resolve."` (second line in `#a89682`).
  - Subhead: `"Notable precedents, tribunal relief, and advocate outcomes across Indian forums."`.
  - Category Filter Tabs: `All`, `Civil & Property`, `Cheque Bounce & Debt`, `Criminal & Bail`.
  - Table Rows:
    - Row 1: `₹1.4 Cr` | `"Delayed possession interest and refund against real estate builder"` | MahaRERA / Bombay HC | 2025
    - Row 2: `Quashed` | `"Anticipatory bail and quashing of false FIR under Section 528 BNSS"` | Delhi High Court | 2025
    - Row 3: `₹38 Lakh` | `"Summary judgment & bank attachment under Section 138 Negotiable Instruments Act"` | Commercial Court | 2024
    - Row 4: `Dismissed` | `"Defended an MSME vendor against frivolous contractual breach arbitration claim"` | High Court Bench | 2024
    - Row 5: `₹8.5 Lakh` | `"Reversal of unauthorized cyber banking debits within 72-hour zero-liability window"` | Banking Ombudsman | 2023
    - Row 6: `Decreed` | `"Partition decree dividing ancestral agricultural land equally among coparceners"` | Civil Court Senior Div | 2023
  - Bottom Link: `"Explore all legal precedents & case studies →"`.

---

### Section 8: Featured Advocates Roster (Homepage)
- **Component File:** `src/components/sections/partner-showcase.tsx` & `src/data/lawyers.ts`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Section Headline: `"The partner you hire is the one you get."`.
  - Subhead: `"A partner leads every matter and takes your calls..."`.
  - Active Partner: Margaret Ellery, Chicago federal prosecutor background.
  - List of 6 Partners: Tomasz Kowal, Owen Pryce, Danielle Okafor, Marcus Leland, Helen Brandt, Arjun Sethi.
  - Bottom Link: `"Meet all 41 lawyers"`.
- **Suggested NyayaSetu Content:**
  - Section Headline: `"The advocate you choose is the one who represents you."` (second line in `#a89682`).
  - Subhead: `"Every advocate on NyayaSetu is verified with their State Bar Council. You deal directly with your chosen counsel, not intermediaries."`.
  - Active Advocate (Left Photo & Right Bio):
    - Name: `Adv. Rajeshwari Sen`
    - Role: `Senior Advocate · Supreme Court & Delhi High Court`
    - Summary: `"24 years of active trial and appellate standing before the Supreme Court of India and High Court of Delhi. Specializes in constitutional writs, property partition, and corporate disputes."`
    - Stats: In practice: `24 years (Bar Enrolment: D/1420/2000)` | Admitted: `Supreme Court of India · Delhi High Court`
  - Numbered Switcher (02 to 07):
    - `02 Adv. Vikramaditya Deshmukh` (Corporate & M&A · Bombay High Court)
    - `03 Adv. Ananya Sundaram` (Tech, IP & Cyber Law · Karnataka High Court)
    - `04 Adv. Harshvardhan Kapoor` (Criminal Defense & Bail · High Court of Delhi)
    - `05 Adv. Sunita Banerjee` (Family & Civil Law · Calcutta High Court)
    - `06 Adv. Pradeep Nair` (RERA & Real Estate · Kerala High Court)
    - `07 Adv. Alok Chawla` (Insolvency & Debt Recovery · NCLT Principal Bench)
  - Bottom Link: `"Explore all 2,800+ verified advocates →"`.

---

### Section 9: Citizen & Litigant Testimonials (Homepage)
- **Component File:** `src/components/sections/client-quotes.tsx` & `src/data/testimonials.ts`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Section Headline: `"What clients tell us."`.
  - Tag: `Trials & Disputes` / `General counsel`.
  - Quote: US freight carrier quote about Chicago trial lawyers.
- **Suggested NyayaSetu Content:**
  - Section Headline: `"What citizens tell us."` (with `"tell us."` in `#a89682`).
  - Subhead: `"Shared with permission. Real outcomes from individuals, MSMEs, and startups."`.
  - Testimonial 1:
    - Quote: `"When my landlord refused to refund my ₹1,60,000 security deposit after handover, NyayaSetu’s AI evaluated the tenancy agreement and generated a legal notice citing High Court precedents. We matched with a local advocate, and the deposit was returned within a week."`
    - Tag: `Property & Tenancy`
    - Author: `Tech Founder & Tenant` | Detail: `Koramangala, Bengaluru · Verified Consultation`
  - Testimonial 2: MSME vendor recovering dishonoured cheque payment within 15 days of statutory notice.
  - Testimonial 3: Homebuyer securing RERA compensation interest for delayed apartment delivery.
  - Testimonial 4: Employee successfully disputing invalid 2-year non-compete restraint.

---

### Section 10: Kanoon Gyaan Legal Guides (Homepage)
- **Component File:** `src/components/sections/latest-insights.tsx` & `src/data/articles.ts`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Section Headline: `"Notes from the floor."`.
  - Button: `"All insights"`.
  - 3 Articles: US office lease clauses, grand jury subpoenas, BIPA biometric timeclocks.
- **Suggested NyayaSetu Content:**
  - Section Headline: `"Kanoon Gyaan · Legal Guides."` (with `"Legal Guides."` in `#a89682`).
  - Button: `"All legal guides"`.
  - 3 Indian Law Guides:
    - Card 1: `Contracts & Employment` | `Adv. Owen Fernandez` | `Sep 18, 2026 · 4 min read`  
      Title: `"Why non-compete clauses in Indian employment contracts are void under Section 27"`
    - Card 2: `Criminal Law` | `Adv. Harshvardhan Kapoor` | `Aug 27, 2026 · 5 min read`  
      Title: `"BNS 2023 vs IPC: 5 key procedural changes every citizen should understand"`
    - Card 3: `Consumer & Cyber` | `Adv. Ananya Sundaram` | `Aug 4, 2026 · 4 min read`  
      Title: `"48-hour golden window: how to report cyber banking fraud on National Portal 1930"`

---

### Section 11: Frequently Asked Questions (Homepage)
- **Component File:** `src/components/sections/faq-section.tsx` & `src/data/faqs.ts`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Headline: `"Questions, answered."`.
  - Subtitle: `"Still unsure? Call (312) 555-0147 and a lawyer will talk it through."`.
  - 5 Questions: US partner billing rates, Chicago office visits, etc.
- **Suggested NyayaSetu Content:**
  - Headline: `"Questions, answered."` (with `"answered."` in `#a89682`).
  - Subtitle: `"Still unsure? Call 1800-NYAYA-SETU (1800-692-9273) and our legal triage team will assist you."`.
  - 5 Indian Legal FAQs:
    1. `"Is the AI Legal Advisor's assessment legally binding?"` -> *NyayaSetu AI provides rights awareness, relevant statutory sections, and case readiness checklists. Official legal advice and court representation are provided directly by Bar Council-verified advocates.*
    2. `"How does NyayaSetu verify advocate credentials?"` -> *Every advocate profile is cross-verified against their State Bar Council enrolment ID, years of active practice, and primary court jurisdictions.*
    3. `"How do fixed-fee consultations work?"` -> *Consultations are fixed at upfront rates (from ₹999 for 30 minutes). There are zero hidden clerkage, chamber, or surprise hourly fees.*
    4. `"Can NyayaSetu assist with urgent matters like anticipatory bail or arrest?"` -> *Yes. Select 'Emergency (<24h)' in the intake form to connect with on-call criminal defense advocates available for urgent bail drafting.*
    5. `"How does NyayaSetu comply with Bar Council of India (BCI) Rule 36?"` -> *BCI rules strictly prohibit advocate advertising. NyayaSetu operates as an educational tech platform and search directory where litigants initiate contact independently.*

---

### Section 12: AI Legal Assessment & Advocate Match Intake (Homepage)
- **Component File:** `src/components/sections/conflict-intake-section.tsx`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Headline: `"Start with a conflict check."`.
  - Subtitle: `"Before we hear the details, we confirm we can act for you. Tell us who is involved. Nothing confidential yet."`.
  - Left Milestones: Same business day check, Strategy call, Engagement letter, Monthly report.
  - Form Fields: US company, US phone format.
- **Suggested NyayaSetu Content:**
  - Headline: `"Request an AI Legal Assessment & Advocate Match."` (with `"Advocate Match."` in `#a89682`).
  - Subtitle: `"Describe your legal concern. Our AI analyzes your situation against Indian acts and connects you with specialist verified advocates. 100% confidential."`.
  - Left Milestones:
    - `Instant`: **AI Legal Evaluation** / Summary of applicable sections (BNS/BSA/Contract Act) and court checklist.
    - `Same day`: **Advocate Matching** / Matched with 2-3 verified advocates in your city and court bench.
    - `Within 24 hours`: **30-Min Strategy Call** / Video or chamber conference with your selected advocate.
    - `Full tracking`: **Court Milestones** / Ongoing transparency on filing dates and court hearings.
  - Form Fields (100% identical styling):
    - `Full name` | `Company / Entity (optional)`
    - `Email` | `Mobile number (+91)`
    - `Legal domain`: Dropdown (`Civil & Property`, `Cheque Bounce (138 NI)`, `Criminal & Bail`, `Startup & Corporate`, `Consumer & Cyber`)
    - `Other parties involved`: `"Name of other party, landlord, company, or police station if applicable"`
    - `Urgency deadline`: `[ None yet ]` `[ Notice received (15 days) ]` `[ Urgent / Summons (72 hours) ]`
    - Checkbox: `"I understand NyayaSetu is an informational legal platform connecting me with independent verified advocates."`
    - Compound CTA: `"Request assessment & match"` | `[ → ]`.

---

### Section 13: Global Footer
- **Component File:** `src/components/layout/footer.tsx`
- **Can section remain visually unchanged?** **YES (100% visually identical).**
- **Existing Content to Replace:**
  - Left Callout: `"Call the firm. A lawyer answers, not a call center."` / `(312) 555-0147` / Chicago address.
  - Column 1: `Office` / `224 S. LaSalle Street, 31st Floor, Chicago, IL 60604`.
  - Column 2: `Practices` / US corporate groups.
  - Column 3: `Firm` / US firm links.
  - Disclaimer: Illinois Bar advertising notice.
- **Suggested NyayaSetu Content:**
  - Left Callout: `"Bridging citizens and verified advocates across India."` / `1800-NYAYA-SETU (1800-692-9273)` / `"New Delhi · Mumbai · Bengaluru · Kolkata"`.
  - Column 1: `Presence` / Supreme Court & High Court Chambers / `contact@nyayasetu.in` / `Helpline: 8:00 a.m. to 9:00 p.m. IST`.
  - Column 2: `Legal Areas` / Civil & Property / Criminal & Bail / Corporate & Startups / Cheque Bounce (138 NI) / Consumer & Cyber / Matrimonial Law.
  - Column 3: `Platform` / Find Advocates / AI Advisor / Landmark Precedents / Legal Guides / About NyayaSetu / BCI Ethics.
  - Disclaimer: *"Bar Council of India Disclaimer: In accordance with Rule 36 of the Bar Council of India Rules, this platform does not solicit work or advertise advocates. NyayaSetu is an AI-powered legal information platform and search directory."*

---

## 3. Dedicated Sub-Pages Content Mapping

| Existing Route | Component File | Existing Content | Suggested NyayaSetu Content | Visually Unchanged? |
| :--- | :--- | :--- | :--- | :--- |
| **`/practices`** | `src/app/practices/page.tsx` | US corporate law practices hub | **Legal Practice Areas Hub**: In-depth dossiers on 6 Indian domains with anchor navigation (`#civil`, `#criminal`, `#corporate`, `#cheque-bounce`, `#family`, `#cyber`), statutory frameworks (BNS, NI Act, RERA), and standard fees. | **YES (100%)** |
| **`/people`** | `src/app/people/page.tsx` | Chicago 7 partners & associates | **Verified Advocate Directory**: Directory of 7 featured Senior Advocates + searchable roster of Bar Council-enrolled advocates across Delhi HC, Bombay HC, Karnataka HC; search by court bench, languages, city, and consultation fee. | **YES (100%)** |
| **`/matters`** | `src/app/matters/page.tsx` | 16 US federal cases ledger | **Landmark Legal Precedents & Representative Matters**: 16 Indian dispute case studies & judgments (MahaRERA orders, Section 138 NI Act Supreme Court rulings, NCLT insolvency decrees, BNSS 528 FIR quashing). | **YES (100%)** |
| **`/firm`** | `src/app/firm/page.tsx` | LaSalle 15-year firm history | **About NyayaSetu & Ethical Framework**: The mission to bridge India's 5-crore court backlog, 4 core commitments, AI safety benchmarks, and Pro Bono legal aid initiative. | **YES (100%)** |
| **`/insights` & `[slug]`** | `src/app/insights/page.tsx` | 9 Chicago law articles | **Kanoon Gyaan (Legal Guides Library)**: 9 comprehensive Indian legal guides with BNS section references, practical citizen checklists, and expert takeaways. | **YES (100%)** |
| **`/contact`** | `src/app/contact/page.tsx` | LaSalle office directions & form | **Advocate Consultation Booking & Helpdesk**: Multi-step consultation scheduler, emergency helpline, pan-India court jurisdiction coverage. | **YES (100%)** |
| **`/privacy`** | `src/app/privacy/page.tsx` | US privacy policy | **Digital Personal Data Protection (DPDP) Act 2023 Policy**: Compliance with Indian data privacy laws and attorney-client confidentiality norms. | **YES (100%)** |
| **`/disclaimer`** | `src/app/disclaimer/page.tsx` | Illinois Bar legal notice | **Bar Council of India (BCI) Non-Solicitation Disclosure**: Strict compliance with BCI Rule 36 prohibiting advocate advertising. | **YES (100%)** |
| **`not-found.tsx`** | `src/app/not-found.tsx` | Custom 404 screen | **NyayaSetu 404 Recovery**: Clean 404 screen directing back to AI Advisor, Find Advocates, and Legal Guides. | **YES (100%)** |

---

## 4. Centralized Mock Datasets to Update (`src/data/`)

Because the existing project cleanly decouples data from UI components, 90% of the content transformation happens in the centralized data layer:

1. **`src/data/navigation.ts`**: Update brand title, navigation labels, and practice area dropdown items.
2. **`src/data/practices.ts`**: Replace 6 US law practices with 6 Indian Legal Domains (Civil & Property, Criminal & Bail, Corporate & Startup, Matrimonial, Cheque Bounce, Consumer & Cyber).
3. **`src/data/lawyers.ts`**: Replace 7 Chicago partners with 7 verified Indian Senior Advocates across Supreme Court and High Courts.
4. **`src/data/matters.ts`**: Replace 16 US federal cases with 16 Indian landmark judgments and representative dispute outcomes.
5. **`src/data/articles.ts`**: Replace 9 Chicago articles with 9 Kanoon Gyaan Indian legal guides.
6. **`src/data/testimonials.ts`**: Replace client quotes with Indian citizen, MSME, and startup legal stories.
7. **`src/data/faqs.ts`**: Replace FAQs with Indian court, BCI compliance, and AI advisory queries.
8. **`src/data/firm.ts`**: Replace LaSalle firm history with NyayaSetu platform mission and ethical principles.
9. **`src/data/fixed-fees.ts`**: Replace dollar rates with Indian Rupee (₹) consultation and document packages.

---

## 5. Next Steps

With `CONTENT_REPLACEMENT_PLAN.md` complete, we are ready to proceed with implementation when directed:
1. Update centralized data files in `src/data/` (practices, advocates, precedents, articles, FAQs, testimonials).
2. Update static copy and labels in layout components (`navbar.tsx`, `footer.tsx`).
3. Update static copy in homepage section components (`hero-section.tsx`, `about-strip.tsx`, `transparency-preview.tsx`, `contract-annotator.tsx`, `conflict-intake-section.tsx`).
4. Update static copy in inner pages (`/practices`, `/people`, `/matters`, `/firm`, `/insights`, `/contact`, `/privacy`, `/disclaimer`).
5. Run build verification (`npm run build:webpack`) to ensure 100% build health with 0 errors.

