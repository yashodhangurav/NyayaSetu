# Reverse Engineering Report: Ellery Kowal LLP (`ellery-visuvate.framer.website`)

**Date of Investigation:** November 6, 2026  
**Target Reference URL:** `https://ellery-visuvate.framer.website/`  
**Tooling Employed:** REA (Reverse Engineer Anything) Model Context Protocol Suite (`capture_browser_scenario`, CDP Playwright Scenario Inspector, Accessibility Tree Extractor, Framer Asset and Stylesheet Analyzer).  
**Investigation State:** Complete. No implementation code executed in this phase.

---

## Executive Summary

Ellery Kowal LLP is a high-end commercial boutique law firm website located at 224 S. LaSalle Street, Chicago. Built on Framer, the site projects an authoritative, sober, and sophisticated editorial identity using classical warm neutral background tones, high-contrast serif headlines (**Gambetta**), refined geometric grotesque body copy (**General Sans**), and rich interactive features including an interactive annotated contract review tool, multi-practice tabbed sliders, client testimonial carousels, expandable case-study ledgers, and a multi-step conflict-check inquiry intake flow.

---

## 1. Phase A — Page Discovery & Route Map

A systematic crawl of the site's manifest, canonical links, and search index identified **19 unique, accessible routes**. No private or inaccessible backend endpoints exist; the site is fully static with client-side interactive widgets.

### Comprehensive Route Inventory

| Route | Canonical Page Title | Page Role & Description |
| :--- | :--- | :--- |
| `/` | `Ellery Kowal LLP` | **Homepage**: Hero, firm thesis, metrics, practices slider, fee schedule preview, annotated contract demo, recent matters preview, partner carousel, client quotes, latest insights, FAQs, and conflict check form. |
| `/practices` | `Practices · Ellery Kowal LLP` | **Practices Hub**: Overview of all six firm practices with anchors (`#disputes`, `#corporate`, `#employment`, `#investigations`, `#real-estate`, `#ip-tech`), detailed scopes, fee ranges, and lead partner references. |
| `/people` | `People · Ellery Kowal LLP` | **Attorneys & Team**: The 7 partners detailed with full bios, bar admissions, trial records, education, and direct contact info; plus a categorized roster of counsel and associates. |
| `/matters` | `Matters · Ellery Kowal LLP` | **Representative Matters**: 16 categorized high-stakes case studies across disputes, transactions, and investigations from 2023–2026 with expandable outcome summaries. |
| `/firm` | `The Firm · Ellery Kowal LLP` | **Firm Overview**: 15-year historical interactive timeline (2011–2026), 4 written operational commitments (sample artifacts), target client profiles, and pro bono clinic initiatives. |
| `/insights` | `Insights · Ellery Kowal LLP` | **Legal Insights & Publications**: Filterable index of partner-authored legal articles and commentary across contracts, disputes, deals, privacy, and real estate, plus an alert signup widget. |
| `/insights/five-office-lease-clauses-chicago` | `Five office-lease clauses to read before you sign in Chicago · Ellery Kowal LLP` | **Article**: Real estate practice note by Helen Brandt on lease negotiation traps in Chicago office buildings. |
| `/insights/subpoena-first-twenty-four-hours` | `When a subpoena arrives: the first twenty-four hours · Ellery Kowal LLP` | **Article**: Investigations practice note by Marcus Leland on grand jury and regulatory subpoena responses. |
| `/insights/open-source-in-an-acquisition` | `Open-source code in an acquisition: what buyers ask for · Ellery Kowal LLP` | **Article**: IP & Technology note by Arjun Sethi on open-source code audits in corporate acquisitions. |
| `/insights/workplace-investigation-that-holds-up` | `Running a workplace investigation that will hold up · Ellery Kowal LLP` | **Article**: Employment & Investigations note by Danielle Okafor on board-level executive investigations. |
| `/insights/letter-of-intent-six-terms` | `Six terms in a letter of intent that matter more than the price · Ellery Kowal LLP` | **Article**: Corporate & M&A note by Tomasz Kowal on LOI structures and seller rollover equity. |
| `/insights/first-ninety-days-commercial-lawsuit` | `The first ninety days of a commercial lawsuit · Ellery Kowal LLP` | **Article**: Trials & Disputes note by Margaret Ellery on litigation case budgeting and early motions. |
| `/insights/bipa-compliance-checklist-2026` | `BIPA in 2026: a compliance checklist for employers with timeclocks · Ellery Kowal LLP` | **Article**: Privacy note by Arjun Sethi on biometric timeclock compliance in Illinois. |
| `/insights/illinois-non-competes-2026` | `Illinois non-competes after the Freedom to Work Act: what still holds · Ellery Kowal LLP` | **Article**: Employment note by Danielle Okafor on post-statutory non-compete enforcement. |
| `/insights/limitation-of-liability-three-words` | `Three words that decide most limitation-of-liability fights · Ellery Kowal LLP` | **Article**: Contracts & Disputes note by Owen Pryce on limitation-of-liability clauses and caps. |
| `/contact` | `Contact · Ellery Kowal LLP` | **Contact & Conflict Check**: Conflict check form, office address, phone lines, transit directions, and maps. |
| `/privacy` | `Privacy notice · Ellery Kowal LLP` | **Privacy Policy**: 12-section GDPR/CCPA-compliant notice covering conflict data and retention policies. |
| `/disclaimer` | `Legal notice · Ellery Kowal LLP` | **Regulatory Disclaimers**: Illinois Rules of Professional Conduct, attorney advertising, and privilege terms. |
| `/404` | `Page not found · Ellery Kowal LLP` | **Custom 404**: Clean error state routing users to Practices, People, Insights, and Contact. |

---

## 2. Phase B — Visual Analysis & Section Hierarchy

### Global Layout Grid & Container Widths
* **Desktop Max-Width:** `1424px` content container, centered with responsive side padding (`24px` sm, `48px` md, `64px` lg).
* **Grid System:** 12-column responsive CSS grid with dynamic gutter scaling (`12px` to `24px`).
* **Breakpoints Observed:**
  * **Desktop Large:** `min-width: 1200px` (standard desktop multi-column layouts)
  * **Tablet / Medium:** `min-width: 600px and max-width: 1199.98px` (2-column collapse, simplified nav)
  * **Mobile:** `max-width: 599.98px` (single column vertical stack, horizontal drawers)

### Page-by-Page Section Hierarchy

#### 1. Homepage (`/`)
1. **Global Sticky Header:** Logo text ("Ellery Kowal LLP"), desktop nav (`Practices`, `People`, `Matters`, `Insights`, `The firm`), "Start a conflict check" secondary button, and mobile hamburger trigger.
2. **Hero Section:**
   * Badge / Super-headline: `"EVIDENCE"` with subtle stamp-style visual framing.
   * Lead H1: `"Every word is evidence."`
   * Subhead: `"Seven partners, one floor of 224 S. LaSalle"`
   * Body copy: Two concise paragraphs contrasting trial results with deal drafting.
   * Hero Graphic: Editorial full-height portrait of Lady Justice bronze statue (`1cnUEt6mpq6a6PKK7HuuPjE7BdU.webp`).
   * CTAs: "Start a conflict check" button and "Our practices" text anchor link.
   * Sub-nav quick practice shortcuts (`Trials & Disputes +`, `Corporate & M&A +`, `Employment +`).
3. **Firm Overview ("About the firm"):**
   * Two editorial paragraphs detailing firm origins (2011 founding by federal prosecutor and M&A partner).
   * Two side-by-side architectural photos: LaSalle entrance (`bhhAOZcQmJaXBnbcUcjp1ROF948.webp`) and 31st-floor reception (`REfcmzt4mPpUJT1GGSseLryjp1g.webp`).
   * 4-stat metrics strip: `41` Lawyers, `34` Cases tried to verdict, `15` Years on LaSalle, `92%` Matters within budget.
4. **Practices Carousel ("Six practices, one floor."):**
   * Section header and description.
   * Horizontal slider displaying 6 practice cards:
     * `01 Trials & Disputes`: From $650/hr | Margaret Ellery & Owen Pryce
     * `02 Corporate & M&A`: From $3,500 | Tomasz Kowal
     * `03 Employment`: From $1,800 | Danielle Okafor
     * `04 Investigations`: From $25,000 retainer | Marcus Leland
     * `05 Real Estate`: From $4,500 | Helen Brandt
     * `06 IP & Technology`: From $2,400 | Arjun Sethi
   * Slide controls: Previous / Next arrow buttons and 4 position indicator pills.
5. **Transparency & Fee Models ("Know the cost, the partner and the next step."):**
   * 3-card showcase:
     * Card 1: 30-Minute Consultation Scheduler mock widget with Central Time selector.
     * Card 2: Sample "Schedule A · Fixed Fees" contract sheet ($3,500 LLC formation package).
     * Card 3: Sample Monthly Status Report card (62% budget used, chronological milestone log).
6. **Interactive Contract Annotator ("Drafted by people who try cases."):**
   * Interactive legal document mockup: "Master Services Agreement · Draft 4 · Article 12. Liability".
   * 3 numbered callout pins pointing to exact contract clauses (`arising out of`, `paid or payable`, `the first written notice of the claim`).
   * Interactive note cards from partners (Owen Pryce, Tomasz Kowal, Margaret Ellery) explaining how courtroom litigation tests each word.
7. **Representative Matters Preview ("Prepared for trial. That’s why most settle."):**
   * Filterable ledger table with category tabs: `All`, `Disputes`, `Transactions`, `Investigations`.
   * Columns: Result / Magnitude, Matter Title & Summary, Forum, Year.
   * Displays 7 high-impact matters ($18.4M verdict, $212M sale, 36hr TRO, DOJ closure, BIPA dismissal, $47M Fulton Market deal, $0 defense award).
   * Link: "All representative matters" -> `/matters`.
8. **Partner Showcase ("The partner you hire is the one you get."):**
   * Tabbed partner switcher listing all 7 partners.
   * Large active partner profile card displaying photo, practice lead title, bio, years in practice, and admissions.
   * Link: "Meet all 41 lawyers" -> `/people`.
9. **Client Testimonials ("What clients tell us."):**
   * Horizontal scrollable quote cards with client roles, industries, and partnership tenure (Food manufacturer CEO, Freight carrier GC, Chemicals distributor President, SaaS CFO).
10. **Latest Insights ("Notes from the floor."):**
    * 3-column article card grid with photography, categories, reading times, and authors.
11. **Frequently Asked Questions ("Questions, answered."):**
    * 5 animated accordions addressing consultation costs, conflict checks, fee models, partner staffing, and emergency restraining orders.
    * Direct telephone banner for urgent inquiries (`(312) 555-0147`).
12. **Inquiry / Conflict Check Intake ("Start with a conflict check."):**
    * 4-step process explanation: Same business day check, 2-day strategy call, pre-work engagement letter, monthly reports.
    * Conflict check form with full name, company, email, phone, matter type dropdown, adverse parties textarea, deadline radio buttons, and non-confidential disclaimer checkbox.
13. **Global Dark Footer:**
    * Multi-column layout with office address, telephone numbers, practice links, firm navigation, attorney advertising disclaimer, and copyright.

---

## 3. Phase C — Interaction Inventory & States

| Component / Interaction | Initial State | User Action | Resulting State | Animation / Transition | Mobile Adaptation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mobile Menu** | Hidden off-screen or collapsed header | Tap hamburger icon | Full-screen or slide-down drawer with nav links, contact info & CTA | `250ms` cubic-bezier opacity & translateY | Full viewport drawer |
| **Practices Carousel** | Shows first 2–3 cards (desktop) | Click Next/Prev arrows or drag | Horizontal slide to reveal remaining practice cards | Smooth spring translate transform | Native touch swipe (`touch-action: pan-y`) |
| **Contract Annotator** | Clause text visible with 3 numbered mark highlights | Click or hover callout marker (1, 2, or 3) | Highlights corresponding text block, elevates partner commentary card | Opacity fade and `12px` Y-axis float | Vertical accordion or stacked cards |
| **Matters Filter Tabs** | `All` tab active, showing all rows | Click category pill (`Disputes`, `Transactions`, `Investigations`) | Filtered table rows re-render smoothly | Immediate re-render with subtle fade | Horizontally scrollable pill bar |
| **Matter Row Expansion** | Collapsed table row showing title, result, year | Click row or toggle chevron | Expands full "What happened" summary and lead partner name | Height accordion auto-expansion (`250ms`) | Card-based expansion |
| **Partner Showcase Switcher** | Partner 01 (Margaret Ellery) selected | Click partner list item (02–07) | Active indicator shifts, main photo and bio update to selected partner | Cross-fade image and content swap (`300ms`) | Horizontally scrollable partner selector |
| **FAQ Accordions** | All questions collapsed | Click question button | Toggles chevron 180°, expands answer text below | AnimatePresence height `0 -> auto`, opacity `0 -> 1` | Full-width collapse |
| **Conflict Check Form** | Clean inputs, default radio `"None yet"` | Focus & input text, submit | Validates required fields; on submit replaces form with "Thank you" card | Fade transition to confirmation state | Full single-column form |
| **Consultation Time Picker** | Default "Time, Central" placeholder | Select dropdown option | Sets meeting slot, updates button label | Native browser select UI | Native wheel picker |

---

## 4. Phase D — Design System, Tokens & Assets

### 1. Typography Specifications

```css
/* Display & Headlines */
--font-serif: "Gambetta", Georgia, "Times New Roman", serif;

/* Body & Interface */
--font-sans: "General Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

/* Monospace & Small Data Badges */
--font-mono: "Inter", monospace;
```

#### Exact Type Scale (Derived from CSS Rules)
* **Display H1 (Hero):** `105.6px` (desktop) / `75.2px` (tablet) / `44px` (mobile), line-height: `0.9em`, letter-spacing: `-0.045em`, font-weight: `400`
* **Section H2:** `67.2px` (desktop) / `48px` (tablet) / `36px` (mobile), line-height: `0.98em`, letter-spacing: `-0.045em`, font-weight: `400`
* **Feature H3 / Subheads:** `48px` – `54.4px`, line-height: `1.0em`, letter-spacing: `-0.04em`
* **Card Titles & Pull Quotes:** `28.8px` – `39.2px`, line-height: `1.18em`, letter-spacing: `-0.03em`
* **Body Text (`1cnwo5n`):** `15px`, line-height: `1.6em`, letter-spacing: `0em`, font-weight: `400`
* **Small Metadata & Badges (`vkm7gi`):** `14px`, line-height: `1.0em`, font-weight: `400`

---

### 2. Colour Palette (Exact Hex & Token Mapping)

| Token Name | Hex Code | Visual Role | Usage Area |
| :--- | :--- | :--- | :--- |
| `--token-b7851a8d` | `#f3ece1` | Primary Alabaster / Warm Cream | Page root background on light sections |
| `--token-9b2b5204` | `#ebe1d1` | Secondary Warm Sand | Card surface borders and neutral container fills |
| `--token-dd2b74b5` | `#e2d5c1` | Muted Border Stone | Dividers, table borders, and outline strokes |
| `--token-e387a24e` | `#fffaf2` | Bright Warm White | Cards, modal panels, active tab highlights |
| `--token-6b31e930` | `#2a1c12` | Deep Espresso Roast | Primary text, bold headers, dark buttons |
| `--token-5414fdf6` | `#5b4a3b` | Muted Umber | Secondary body text, subheadings, descriptions |
| `--token-70c5b10f` | `#85725f` | Tertiary Warm Gray | Inactive tabs, metadata labels, icon accents |
| `--token-c584fe1b` | `#9a6a35` | Warm Bronze / Ochre | Accent badges, primary CTA button hover, key links |
| `--token-adbfafe3` | `#7c5226` | Deep Antique Bronze | Active button state, focal point highlights |
| `--token-901d9747` | `#d1a46a` | Light Champagne Gold | Badge borders, highlighted text accents |
| `--token-54bd8eaf` | `#24180f` | Near-Black Espresso | Global footer background, dark section wrapper |
| `--token-bfe65a71` | `#2f2116` | Charcoal Espresso | Contrast card background in dark containers |

---

### 3. Public Asset Inventory & Licensing Notes

| Asset ID / URL | Role / Subject | Dimensions | Page Location | Reuse / License Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| `1cnUEt6mpq6a6PKK7HuuPjE7BdU.webp` | Hero Bronze Lady Justice statue holding scales | 1200 × 2406 | Homepage Hero | Proprietary Framer asset. Replace with licensed stock Lady Justice or architectural bronze. |
| `bhhAOZcQmJaXBnbcUcjp1ROF948.webp` | 224 S. LaSalle entrance limestone facade | 960 × 1200 | About Section | Commercial Chicago architectural image. Replace with Unsplash Chicago Rookery/LaSalle facade. |
| `REfcmzt4mPpUJT1GGSseLryjp1g.webp` | 31st Floor reception interior | 1200 × 900 | About Section | Interior commercial space. Replace with high-end law firm reception photography. |
| `Zap1w5XGkVSiezBmDiPSycYt0.webp` | Federal wood-panelled courtroom trial lawyer | 480 × 600 | Practices (Disputes) | Stock photography. Replace with legal trial courtroom stock. |
| `WzoMN0cZR1mFFYB1iI5EK9yVJ6I.webp` | Lawyers reviewing purchase agreement at dusk | 480 × 600 | Practices (M&A) | Stock corporate legal scene. Replace with licensed deal meeting photography. |
| `MX27nh2ggEqrOo8VishzkP6djaU.webp` | Executives in conference room meeting | 480 × 600 | Practices (Employment)| Replace with corporate meeting stock. |
| `liEbKSf6YjDEu7fliChEDT6SQSw.webp` | Hand pulling archived case record from shelf | 480 × 600 | Practices (Investigations)| Replace with archive records / legal library stock. |
| `XHmKM0bV2On3EfVvwOXgoSbk5g.webp` | Chicago River and Loop skyscrapers at night | 480 × 600 | Practices (Real Estate)| Replace with high-res Chicago Loop nighttime river photography. |
| `6qS34tlW6OMwiM6MECqiTnffU.webp` | Red pen striking sentence from legal agreement | 480 × 600 | Practices (IP & Tech) | Replace with contract review close-up. |
| `6wqwrrqL2BSqXivJHVUwdWLQadU.webp` | Margaret Ellery partner portrait | 720 × 900 | People & Homepage | Model portrait. Replace with professional attorney headshot. |
| `bsgFmeXjRoUQHVqoZVF4RkNAaoI.webp` | Tomasz Kowal partner portrait | 720 × 900 | People & Homepage | Model portrait. Replace with professional attorney headshot. |
| `eUjD6BLkOpLQTOPaCI5UarZtN38.webp` | Owen Pryce partner portrait | 720 × 900 | People & Homepage | Model portrait. Replace with professional attorney headshot. |
| `aXipvz3BV2WnUNn55RHmTB3Dy4.webp` | Danielle Okafor partner portrait | 720 × 900 | People & Homepage | Model portrait. Replace with professional attorney headshot. |
| `iXWrwqT6ofMhuEPvVjRK6omXQ.webp` | Marcus Leland partner portrait | 720 × 900 | People & Homepage | Model portrait. Replace with professional attorney headshot. |
| `TDQIMNAHItttRcW9dZxkSadNMGg.webp` | Helen Brandt partner portrait | 720 × 900 | People & Homepage | Model portrait. Replace with professional attorney headshot. |
| `ntsMj5B7VwIyh6IT46dsUIpx8.webp` | Arjun Sethi partner portrait | 720 × 900 | People & Homepage | Model portrait. Replace with professional attorney headshot. |
| `Ii5ywrz0wGJNs3Kk4IUp6fAT8.webp` | Contract with red-pen edits and coffee cup | 1600 × 1000 | Insights (Article 1) | Replace with styled flatlay legal contract imagery. |
| `PwsO5MvlbOVK0HAEVtrJ1xSOFg.webp` | Empty desk with resignation letter & badge | 1600 × 1000 | Insights (Article 2) | Replace with workplace / HR desk photography. |
| `CZFM2PYLPboBXfjd97sEto88.webp` | Fingerprint biometric timeclock on office wall | 1600 × 1000 | Insights (Article 3) | Replace with biometric / tech office hardware photo. |

---

## 5. Phase E — Evidence, Empirical Verifications & Limitations

### Verified Behaviors (Observed via CDP & Accessibility Tree)
1. **No External Backend Required:** The conflict check form on `ellery-visuvate.framer.website` runs purely on client-side JS; on submission, it triggers state mutation replacing the inputs with a "Thank you" card advising that intake staff will reply.
2. **Anchor-Based Navigation for Practices:** The navigation item `Practices` links directly to `/practices`, and the sub-links use deep anchors (`#disputes`, `#corporate`, etc.) that smoothly scroll to practice cards.
3. **Typography Sources:** Font files are served via Fontshare CDN (`Gambetta` and `General Sans`). Inter is loaded as a fallback.
4. **All 41 Lawyers Context:** While the firm features 7 named equity partners with individual photography, the remaining 34 attorneys (8 counsel and 26 associates) are cataloged by practice group roster with practice tags and credentials.

### Identified Uncertainties & Manual Verifications
1. **Interactive Timeline Scrubbing (`/firm`):** Framer implements a scroll-linked scrub effect for the 2011–2026 timeline. In our Next.js recreation with Framer Motion, this can be implemented via `useScroll` with motion value interpolation or an accessible vertical milestone stepped stepper.
2. **Contract Annotator Marker Hover vs. Click:** In touch environments, marker pins require click-to-activate rather than hover states to maintain accessibility on iOS/Android devices.
3. **Consultation Scheduler:** The time-slot booking card on the homepage functions as an illustrative intake preview rather than a live Calendly/Cal.com sync. We should implement it as a polished local interactive mock selector that connects to the conflict intake modal.

---

## Conclusion & Readiness

The target reference website has been exhaustively analyzed across all routes, structural layouts, design tokens, typography specifications, interactions, and media assets. The project foundation in `/Users/yashodhan/Documents/Projects/REA` is verified and ready for full implementation.

