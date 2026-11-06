# Visual Quality Assurance (QA) Report: Ellery Kowal LLP Recreation

**Date:** November 2026  
**Reference Site:** [https://ellery-visuvate.framer.website/](https://ellery-visuvate.framer.website/)  
**Local Development:** [http://localhost:3002](http://localhost:3002)  
**Status:** Audit Complete & Core Visual Parity Achieved  

---

## 1. Scope & Viewport Matrix

All routes were verified across four standardized viewport breakpoints matching the original Framer responsive definitions:

| Device Category | Target Dimensions | Breakpoint Class | Verification Method |
| :--- | :--- | :--- | :--- |
| **Desktop** | `1440 × 900` | `xl:` / `2xl:` | Headless Chrome CDP & visual inspection |
| **Laptop** | `1280 × 800` | `lg:` | Headless Chrome CDP |
| **Tablet** | `768 × 1024` | `md:` | Headless Chrome CDP |
| **Mobile** | `390 × 844` | Base / `sm:` | Headless Chrome CDP & touch simulation |

### Routes Audited:
1. **`/` (Homepage)** — Full section flow (Hero, About, Practices, Transparency, Contract Annotator, Matters, Partners, Testimonials, Insights, FAQs, Conflict Intake, Footer).
2. **`/practices`** — Six practice areas, fee schedules, partners, and case outcomes.
3. **`/people`** — Partners directory, trial statistics, admissions, and biographies.
4. **`/matters`** — Filterable matter ledger with categories (`Disputes`, `Transactions`, `Investigations`).
5. **`/firm`** — LaSalle Street office background, partnership structure, and history.
6. **`/insights` & `/insights/[slug]`** — Editorial publication library and individual articles.
7. **`/contact`** — Conflict check intake and office coordinates.
8. **`/privacy` & `/disclaimer`** — Regulatory and bar compliance notices.
9. **`/_not-found`** — Firm-styled custom 404 with navigation back to key practice hubs.

---

## 2. Issues Identified & Corrections Applied

### A. Navigation & Brand Identity
* **Issue:** Generic serif text logo previously lacked the authentic interlocking monogram, and the primary CTA was a simple rounded button.
* **Correction:**
  * Integrated the authentic interlocking `EK` vector monogram SVG (`#9a6a35` gold / `#2a1c12` charcoal).
  * Styled "Ellery Kowal LLP" with small-caps `LLP` typography.
  * Added the `• Home` bullet indicator.
  * Implemented the compound action button `[ Start a conflict check | → ]` with a distinct right arrow chamber and thin separator.

### B. Hero Section Watermark & Lady Justice Centerpiece
* **Issue:** Hero lacked the giant faint background typography and authentic visual centerpiece.
* **Correction:**
  * Added the background watermark word **`EVIDENCE`** rendered at ~282px with an authentic upward gradient mask.
  * Extracted and placed the authentic Lady Justice bronze statue cutout (`1cnUEt6mpq6a6PKK7HuuPjE7BdU.webp`).
  * Integrated the rotating concentric seal ring SVG with `<textPath>` containing `"ELLERY KOWAL LLP · 224 SOUTH LASALLE STREET · CHICAGO · ESTABLISHED 2011 ·"`.
  * Added the 4-partner avatar cluster with the `"Seven partners, one floor of 224 S. LaSalle"` legend.
  * Added the bottom-right floating pill badges (`Trials & Disputes +`, `Corporate & M&A +`, `Employment +`).

### C. Practices Carousel ("Six practices, one floor.")
* **Issue:** Cards used thumbnail layouts with white card backgrounds instead of photographic full-bleed cards.
* **Correction:**
  * Rebuilt practice cards into full-bleed photographic cards (aspect ratio ~3:4.2) with dark bottom gradient overlays.
  * Updated all 6 practice cards with authentic high-resolution Framer imagery.
  * Added top pills (`01`, `From $650/hr`), white serif titles, and micro-footers.

### D. Fee Transparency & Fixed Schedules ("Know the cost...")
* **Issue:** Contained placeholder badges and cards that deviated from the 3-column reference layout.
* **Correction:**
  * Rebuilt into a 3-card grid:
    1. **Card 1 (First Call):** 30-minute consultation scheduler with partner selector avatars and Central Time dropdown.
    2. **Card 2 (Schedule A):** Fixed fee schedule sheet with `$3,500` package and deliverable checklist.
    3. **Card 3 (Monthly Report):** One-page client status report with a 62% budget progress bar and chronological milestone log.

### E. Contract Annotator ("Drafted by people who try cases.")
* **Issue:** Missing the authentic split layout with the coffee table photograph and interactive redlined contract sheet.
* **Correction:**
  * Added the lifestyle photography backdrop (`1P4ZiDmUViRZSPDF7pkkL0gc.webp`).
  * Overlayed the reviewed Master Services Agreement sheet featuring redlined Article 12.2 text with callout pins (`arising out of¹`, `paid or payable²`, `the first written notice of the claim³`).
  * Added synchronized interactive hover/click states between the 3 partner note cards (Owen Pryce, Tomasz Kowal, Margaret Ellery) and the contract marks.

### F. Representative Matters Preview ("Prepared for trial...")
* **Issue:** Contained an enclosed card box with table headers instead of the editorial ledger table.
* **Correction:**
  * Cleaned into an open editorial ledger directly on the `#f4efe6` page background with thin horizontal divider lines.
  * Added category filter tabs (`All`, `Disputes`, `Transactions`, `Investigations`).
  * Aligned the 4 data columns (`Result`, `Matter`, `Forum`, `Year`).

### G. Partner Showcase ("The partner you hire is the one you get.")
* **Issue:** Side-by-side layout was inverted compared to the reference.
* **Correction:**
  * Positioned the high-resolution partner portrait on the left.
  * Positioned active partner biography and trial statistics on the right, followed by a numbered switcher list for the remaining partners and a direct link to `/people`.

### H. Client Quotes, Insights & Footer
* **Issue:** Testimonials used generic speech bubbles, and the footer lacked the large telephone statement.
* **Correction:**
  * Rebuilt client quotes into a split editorial showcase card with practice tag badges and step indicators.
  * Streamlined `Notes from the floor.` into an editorial 3-column publication preview.
  * Cleaned the FAQ accordion list with circular `+` / `−` triggers.
  * Added the pre-footer reception photo strip and dark espresso footer with `(312) 555-0147` headline.

---

## 3. Remaining Intentional Differences (Content Customization)

Per user directive (*"dont implement as it is everything, just do enough for now, i want change some content later"*):
1. **Editable Content Models:** Centralized mock datasets (`src/data/`) remain structured for easy client customization, copy adjustments, and partner updates.
2. **Forms & Intake:** The conflict check and consultation booking forms run entirely in client state with simulated response feedback, ready for integration with any desired form service or email notification hook later.
3. **Build Status:** All 23 routes compile statically and pass build checks with zero errors (`npm run build:webpack`).

