# Implementation Plan: Ellery Kowal LLP Next.js Frontend Recreation

**Project Name:** Ellery Kowal LLP Frontend Recreation  
**Reference Target:** `https://ellery-visuvate.framer.website/`  
**Foundation Document:** [`REVERSE_ENGINEERING_REPORT.md`](file:///Users/yashodhan/Documents/Projects/REA/REVERSE_ENGINEERING_REPORT.md)  
**Technology Stack:** Next.js 16 (App Router), TypeScript 5, Tailwind CSS v4, React 19, Framer Motion 14, Lucide React  
**Authoring Date:** November 6, 2026  
**Status:** Approved Architecture Plan — Ready for Phased Implementation  

---

## Table of Contents
1. [Route Architecture & Next.js Mapping](#1-route-architecture--nextjs-mapping)
2. [Component Architecture & Directory Organization](#2-component-architecture--directory-organization)
3. [Interaction Mapping to React & Framer Motion](#3-interaction-mapping-to-react--framer-motion)
4. [Design Token System & Tailwind Configuration](#4-design-token-system--tailwind-configuration)
5. [Local Asset Strategy & Media Inventory](#5-local-asset-strategy--media-inventory)
6. [Data Models & Mock Datasets Strategy](#6-data-models--mock-datasets-strategy)
7. [Responsive Breakpoints & Layout Specifications](#7-responsive-breakpoints--layout-specifications)
8. [Animation & Transition Specifications](#8-animation--transition-specifications)
9. [Form Validation, Intake Workflow & State Handling](#9-form-validation-intake-workflow--state-handling)
10. [Visual Quality Assurance & Verification Strategy](#10-visual-quality-assurance--verification-strategy)
11. [Phased Implementation Roadmap](#11-phased-implementation-roadmap)

---

## 1. Route Architecture & Next.js Mapping

Every single one of the 19 discovered routes from `REVERSE_ENGINEERING_REPORT.md` is mapped to an App Router route. No routes are combined, omitted, or simplified.

### Route Mapping Matrix

| # | Discovered Reference Route | Next.js App Router File | Page Role & Contents | Metadata Title |
| :- | :--- | :--- | :--- | :--- |
| 1 | `/` | `src/app/page.tsx` | **Homepage**: Hero, About Strip (4 metrics + LaSalle photos), Practices Slider, Transparency & Fee Models, Interactive Contract Annotator, Representative Matters Preview, Partner Showcase, Client Quotes, Latest Insights, FAQs, Conflict Check Intake, Footer. | `Ellery Kowal LLP · Commercial Law & Trials · LaSalle Street, Chicago` |
| 2 | `/practices` | `src/app/practices/page.tsx` | **Practices Hub**: 6 in-depth practice dossiers with anchors (`#disputes`, `#corporate`, `#employment`, `#investigations`, `#real-estate`, `#ip-tech`), scopes of work, fee ranges, client trigger criteria, and partner leadership. | `Practices · Ellery Kowal LLP` |
| 3 | `/people` | `src/app/people/page.tsx` | **Attorneys & Team**: In-depth profiles of all 7 equity partners (bios, admissions, trial records, education, direct phone/email) + searchable/filterable roster of counsel and associates. | `People · Ellery Kowal LLP` |
| 4 | `/matters` | `src/app/matters/page.tsx` | **Representative Matters Ledger**: Complete catalog of 16 high-stakes matters (2023–2026), filterable by `All`, `Disputes`, `Transactions`, `Investigations`, with expandable case details and forum tags. | `Matters · Ellery Kowal LLP` |
| 5 | `/firm` | `src/app/firm/page.tsx` | **Firm Overview**: 15-year interactive historical timeline (2011–2026), 4 written operational commitments with sample document previews, 3 target client archetypes, and LaSalle Street pro bono legal clinic details. | `The Firm · Ellery Kowal LLP` |
| 6 | `/insights` | `src/app/insights/page.tsx` | **Legal Insights & Publications**: Filterable editorial index of 9 partner-authored treatises across Contracts, Employment, Privacy, Disputes, Deals, Investigations, Real Estate, Technology, with search and newsletter intake. | `Insights · Ellery Kowal LLP` |
| 7 | `/insights/five-office-lease-clauses-chicago` | `src/app/insights/[slug]/page.tsx` | **Article**: Helen Brandt on Chicago commercial office lease traps, operating expense pass-throughs, and audit rights. | `Five office-lease clauses to read before you sign in Chicago · Ellery Kowal LLP` |
| 8 | `/insights/subpoena-first-twenty-four-hours` | `src/app/insights/[slug]/page.tsx` | **Article**: Marcus Leland on grand jury and federal regulatory subpoena response protocols, document holds, and privilege logs. | `When a subpoena arrives: the first twenty-four hours · Ellery Kowal LLP` |
| 9 | `/insights/open-source-in-an-acquisition` | `src/app/insights/[slug]/page.tsx` | **Article**: Arjun Sethi on open-source software license audits, GPL contamination, and technical seller reps. | `Open-source code in an acquisition: what buyers ask for · Ellery Kowal LLP` |
| 10 | `/insights/workplace-investigation-that-holds-up` | `src/app/insights/[slug]/page.tsx` | **Article**: Danielle Okafor on conducting executive misconduct investigations that withstand EEOC and board scrutiny. | `Running a workplace investigation that will hold up · Ellery Kowal LLP` |
| 11 | `/insights/letter-of-intent-six-terms` | `src/app/insights/[slug]/page.tsx` | **Article**: Tomasz Kowal on LOI negotiating points that surpass headline valuation, including rollover equity and indemnity escrows. | `Six terms in a letter of intent that matter more than the price · Ellery Kowal LLP` |
| 12 | `/insights/first-ninety-days-commercial-lawsuit` | `src/app/insights/[slug]/page.tsx` | **Article**: Margaret Ellery on commercial litigation budgeting, early dispositive motions, and Rule 26 initial disclosures. | `The first ninety days of a commercial lawsuit · Ellery Kowal LLP` |
| 13 | `/insights/bipa-compliance-checklist-2026` | `src/app/insights/[slug]/page.tsx` | **Article**: Arjun Sethi on the 2026 Illinois Biometric Information Privacy Act statutory updates, consent forms, and timeclocks. | `BIPA in 2026: a compliance checklist for employers with timeclocks · Ellery Kowal LLP` |
| 14 | `/insights/illinois-non-competes-2026` | `src/app/insights/[slug]/page.tsx` | **Article**: Danielle Okafor on post-Freedom to Work Act restrictive covenants, salary thresholds, and non-solicitation enforcement. | `Illinois non-competes after the Freedom to Work Act: what still holds · Ellery Kowal LLP` |
| 15 | `/insights/limitation-of-liability-three-words` | `src/app/insights/[slug]/page.tsx` | **Article**: Owen Pryce on critical contractual liability caps, consequential damage waivers, and gross negligence carve-outs. | `Three words that decide most limitation-of-liability fights · Ellery Kowal LLP` |
| 16 | `/contact` | `src/app/contact/page.tsx` | **Contact & Conflict Clearance**: Intake form, direct office lines, 224 S. LaSalle directions via Metra and 'L', parking, and courier delivery specifications. | `Contact & Conflict Check · Ellery Kowal LLP` |
| 17 | `/privacy` | `src/app/privacy/page.tsx` | **Privacy Policy**: 12-section compliance policy covering conflict check data retention, client confidentiality, cookies, and IL privilege. | `Privacy Notice · Ellery Kowal LLP` |
| 18 | `/disclaimer` | `src/app/disclaimer/page.tsx` | **Legal Notice & Attorney Advertising**: Formal disclaimer under Illinois Rules of Professional Conduct 7.1–7.5, non-privilege notice, and past results disclosure. | `Legal Notice & Disclaimers · Ellery Kowal LLP` |
| 19 | `/404` | `src/app/not-found.tsx` | **Custom 404 Page**: Architectural error screen with direct recovery navigation to Practices, People, Matters, Insights, and Conflict Check. | `Page Not Found · Ellery Kowal LLP` |

### Dynamic Route Generation (`generateStaticParams`)
For `/insights/[slug]`, `generateStaticParams()` will statically pre-render all 9 articles at build time:
```typescript
export async function generateStaticParams() {
  return articles.map((article) => ({
    slug: article.slug,
  }));
}
```

---

## 2. Component Architecture & Directory Organization

The application structure adheres strictly to modular separation of concerns:

```
src/
├── app/
│   ├── layout.tsx                     # Root HTML wrapper with fonts, global navigation & footer
│   ├── page.tsx                       # Homepage
│   ├── globals.css                    # Tailwind v4 import, font definitions, design token vars
│   ├── favicon.ico                    # Favicon
│   ├── practices/
│   │   └── page.tsx                   # Practices Hub with anchor navigation
│   ├── people/
│   │   └── page.tsx                   # Partners & attorneys directory
│   ├── matters/
│   │   └── page.tsx                   # Filterable representative matters ledger
│   ├── firm/
│   │   └── page.tsx                   # Firm history, timeline, commitments & pro bono
│   ├── insights/
│   │   ├── page.tsx                   # Publications filterable index
│   │   └── [slug]/
│   │       └── page.tsx               # Dynamic article template with rich legal typography
│   ├── contact/
│   │   └── page.tsx                   # Conflict check intake & office directions
│   ├── privacy/
│   │   └── page.tsx                   # 12-section privacy disclosure
│   ├── disclaimer/
│   │   └── page.tsx                   # Attorney advertising & regulatory notice
│   └── not-found.tsx                  # Custom 404 error page
├── components/
│   ├── layout/
│   │   ├── navbar.tsx                 # Sticky navigation with mobile menu trigger
│   │   ├── footer.tsx                 # Dark espresso global footer with links & disclaimers
│   │   ├── container.tsx              # 1424px max-width responsive layout constraint
│   │   └── section.tsx                # Standard section wrapper with consistent padding
│   ├── navigation/
│   │   ├── mobile-drawer.tsx          # Full-screen animated mobile menu with links & CTA
│   │   ├── breadcrumbs.tsx            # Sub-page navigation breadcrumb trail
│   │   └── practice-anchors.tsx       # Sticky anchor pill bar for practices hub
│   ├── sections/
│   │   ├── hero-section.tsx           # Homepage hero with Lady Justice portrait & CTAs
│   │   ├── about-strip.tsx            # LaSalle photos & 4 key metrics counter
│   │   ├── practices-slider.tsx       # 6-practice horizontal drag/arrow carousel
│   │   ├── transparency-preview.tsx   # 3-card showcase (Fee schedule, consultation, monthly report)
│   │   ├── contract-annotator.tsx     # Interactive MSA Article 12 contract review tool
│   │   ├── matters-preview.tsx        # Filterable matters ledger preview table
│   │   ├── partner-showcase.tsx       # Tabbed partner switcher with high-res portrait & bio
│   │   ├── client-quotes.tsx          # Horizontally scrollable client testimonial quotes
│   │   ├── latest-insights.tsx        # 3-card recent article preview grid
│   │   ├── faq-section.tsx            # Animated accordion list with urgent call banner
│   │   ├── conflict-intake-section.tsx # 4-step process + conflict check form container
│   │   ├── firm-timeline.tsx          # Interactive 2011–2026 history stepper
│   │   ├── firm-commitments.tsx       # 4 written operational commitments with document previews
│   │   ├── firm-client-types.tsx      # 3 client archetypes (Founders, Mid-market, GC overflow)
│   │   └── firm-pro-bono.tsx          # LaSalle Street legal clinic feature
│   ├── cards/
│   │   ├── practice-card.tsx          # Practice card with fee basis, partner names, details
│   │   ├── lawyer-card.tsx            # Partner portrait card with bio, credentials, contact
│   │   ├── matter-row.tsx             # Expandable matter ledger row with outcome summary
│   │   ├── article-card.tsx           # Insight article thumbnail, read time, author pill
│   │   ├── testimonial-card.tsx       # Quote card with client role, company, and tenure
│   │   ├── sample-fee-sheet.tsx       # Architectural fixed-fee contract document card
│   │   ├── sample-status-report.tsx   # Monthly client status report card with budget %
│   │   └── commitment-artifact.tsx    # Sample policy card with stamp badge
│   ├── forms/
│   │   ├── conflict-check-form.tsx    # Complete intake form with validation & success state
│   │   ├── consultation-picker.tsx    # Interactive Central Time slot booking mockup
│   │   └── newsletter-signup.tsx      # Email subscription intake for insights
│   ├── ui/
│   │   ├── button.tsx                 # Primary, secondary, outline, ghost button variants
│   │   ├── badge.tsx                  # Architectural tag badge (e.g., "EVIDENCE", "FIXED FEE")
│   │   ├── card.tsx                   # Base cream and white card wrappers with subtle borders
│   │   ├── accordion.tsx              # Accessible animated accordion primitive
│   │   ├── tabs.tsx                   # Accessible filter tab pill strip
│   │   ├── input.tsx                  # Styled text/email/tel input with label & error
│   │   ├── textarea.tsx               # Styled multiline input with character count
│   │   ├── select.tsx                 # Styled dropdown menu selector
│   │   └── modal.tsx                  # Accessible focus-trapped dialog modal
│   └── animations/
│       ├── motion-wrapper.tsx         # Framer motion fade/slide wrapper
│       └── stagger-container.tsx      # Staggered children animator
├── data/
│   ├── lawyers.ts                     # 7 partners + counsel and associates roster
│   ├── practices.ts                   # 6 practice areas with deep dossiers & fee models
│   ├── matters.ts                     # 16 representative matters with full details
│   ├── articles.ts                    # 9 complete insight articles with author links
│   ├── testimonials.ts                # 4 client quotes
│   ├── faqs.ts                        # 5 homepage FAQs + practice-specific questions
│   ├── firm.ts                        # Timeline milestones, commitments, client types, pro bono
│   ├── fixed-fees.ts                  # Fixed-fee schedule items and consultation slots
│   ├── navigation.ts                  # Header, footer, and sub-nav link definitions
│   └── index.ts                       # Barrel export for all mock data
├── hooks/
│   ├── use-scroll-position.ts         # Hook to detect scroll offset for sticky header
│   ├── use-media-query.ts             # Responsive breakpoint listener
│   └── use-lock-scroll.ts             # Body scroll-lock for mobile navigation drawer
├── lib/
│   ├── utils.ts                       # `cn()` clsx + tailwind-merge helper
│   └── formatters.ts                  # Currency, date, and phone formatting utilities
└── types/
    └── index.ts                       # Master TypeScript interfaces and data types
```

---

## 3. Interaction Mapping to React & Framer Motion

Each interaction observed on the reference website is mapped directly to a concrete React state implementation:

### 1. Global Sticky Header & Mobile Drawer
- **Initial State:** Header fixed at top with transparent or semi-translucent cream background; mobile menu drawer closed (`isMobileMenuOpen = false`).
- **Scroll Action:** When `window.scrollY > 30px`, header transitions to backdrop-blur with a crisp bottom border (`#E2D5C1`), elevating above content (`z-50`).
- **Mobile Menu Toggle:** Clicking the hamburger button triggers `isMobileMenuOpen = true`.
- **Animation:**
  - Backdrop fade: `opacity: 0 -> 1` (`0.2s ease`).
  - Mobile drawer: Framer Motion slide down or full-screen overlay (`y: -20px -> 0px`, `opacity: 0 -> 1`, `duration: 0.25s`).
  - Body scroll is locked via `document.body.style.overflow = 'hidden'`.

### 2. Practices Horizontal Carousel (`PracticesSlider`)
- **Initial State:** Displays practice cards 01 (`Trials & Disputes`) and 02 (`Corporate & M&A`).
- **User Actions:** Click Next/Prev chevron buttons, drag/swipe across cards, or click position indicator dots.
- **State Machine:**
  - `currentIndex: number` (0 to 5).
  - Framer Motion `motion.div` track with `x: -currentIndex * cardWidthWithGap`.
  - Drag constraints: `drag="x"`, `dragConstraints={{ left: -maxOffset, right: 0 }}`, `dragElastic={0.1}`.
- **Mobile Adaptation:** Uses native touch scrolling with snap points (`snap-x snap-mandatory overflow-x-auto`) or spring drag controls.

### 3. Interactive Contract Annotator (`ContractAnnotator`)
- **Component Purpose:** High-fidelity simulation of an attorney reviewing a contract clause (Master Services Agreement · Article 12 Liability).
- **Initial State:** Shows legal agreement text with 3 highlighted spans marked with numbered badges (`①`, `②`, `③`). Marker `①` (`arising out of`) is active by default.
- **User Action:** Clicking or hovering over pins `①`, `②`, or `③` updates `activePin: 1 | 2 | 3`.
- **Visual Reaction:**
  - The corresponding text block in the contract illuminates with a warm amber highlight background (`#EBE1D1` with border `#9A6A35`).
  - The side commentary card updates via Framer Motion cross-fade (`opacity: 0 -> 1`, `y: 8px -> 0px`) to display the partner's trial analysis:
    - *Pin 1 (Owen Pryce):* "Three words that expand indemnification to claims never intended..."
    - *Pin 2 (Tomasz Kowal):* "Limiting liability to 'fees paid or payable' creates a circular trap if payment is disputed..."
    - *Pin 3 (Margaret Ellery):* "A 30-day notice requirement that operates as a forfeiture clause before the bench."

### 4. Representative Matters Ledger Filter & Drawer Expansion
- **Initial State:** Category tab set to `"All"`. Displays rows for representative cases. All rows collapsed.
- **Category Filter Action:** Clicking `"Disputes"`, `"Transactions"`, or `"Investigations"` sets `selectedCategory`. Rows filter instantly with a gentle stagger fade (`duration: 0.2s`).
- **Row Expansion Action:** Clicking any matter row toggles its ID in `expandedRowIds: Set<string>`.
- **Animation:**
  - Accordion expansion using Framer Motion `AnimatePresence`:
    ```tsx
    <motion.div
      initial={{ height: 0, opacity: 0 }}
      animate={{ height: "auto", opacity: 1 }}
      exit={{ height: 0, opacity: 0 }}
      transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
    >
    ```
  - Displays the detailed "What happened" case background, client profile, lead partner name, and forum citation.
  - Chevron icon smoothly rotates 180 degrees.

### 5. Partner Showcase Switcher (`PartnerShowcase`)
- **Initial State:** Margaret Ellery (Founding Partner, Trials & Disputes) active.
- **User Action:** Clicking any partner in the 7-person roster sets `selectedPartnerId`.
- **Visual Reaction:**
  - Active button gains deep espresso fill (`#2A1C12`) with cream text (`#F3ECE1`).
  - The main partner card swaps the high-resolution portrait, quote, years in practice badge, bar admissions list, education, and trial record list.
  - Image and bio update with cross-fade animation (`duration: 0.3s`).

### 6. Interactive Consultation Scheduler Preview
- **Initial State:** Consultation Card with selectable date pills (Monday–Friday) and time dropdown placeholder ("Time, Central").
- **User Action:** Selecting a date and time slot sets local state (`selectedSlot`).
- **Result:** Button text updates to "Reserve [Selected Time] CT". Clicking opens the Conflict Check modal with the consultation time pre-populated in the notes.

### 7. FAQ Accordion System
- **Initial State:** All 5 questions collapsed.
- **User Action:** Clicking any question toggles that item's expanded state.
- **Animation:** Smooth height expansion (`0 -> auto`) with opacity cross-fade; chevron rotates 180°.

### 8. Conflict Check Intake Workflow
- **Initial State:** Clean form fields, default radio set to `"None yet"`, non-confidential disclaimer checkbox unchecked.
- **Submission Action:** User fills required fields and clicks "Submit conflict check".
- **Validation:** If required fields (Name, Email, Adverse Parties, Disclaimer) are invalid, errors highlight in red/amber with descriptive messages.
- **Success State:** If valid, form transitions to a confirmation card:
  - Header: `"Conflict check initiated."`
  - Body: Confirmation that conflict counsel will clear the adverse parties against the firm's database and reply within 1 business day.
  - Action: "Submit another inquiry" button to reset form.

---

## 4. Design Token System & Tailwind Configuration

The design tokens derived from `REVERSE_ENGINEERING_REPORT.md` are integrated directly into `src/app/globals.css` and Tailwind CSS v4 `@theme inline`:

### Color System

```css
@theme inline {
  /* Backgrounds */
  --color-bg-primary: #f3ece1;      /* Light alabaster cream (root page background) */
  --color-bg-secondary: #ebe1d1;    /* Warm sand (containers, cards, hover backgrounds) */
  --color-bg-card: #fffaf2;         /* Bright warm white (highlighted card surfaces) */
  --color-bg-dark: #24180f;         /* Near-black espresso (global footer & dark sections) */
  --color-bg-dark-card: #2f2116;    /* Charcoal espresso (contrast cards inside dark footer) */

  /* Borders & Dividers */
  --color-border-subtle: #e2d5c1;   /* Muted stone (dividers, table lines, button outlines) */
  --color-border-hover: #cfbe9e;    /* Border on hover */
  --color-border-dark: #3f2c1f;     /* Border inside dark sections */

  /* Typography / Text Colors */
  --color-text-primary: #2a1c12;    /* Deep espresso roast (H1, H2, titles, high contrast) */
  --color-text-secondary: #5b4a3b;  /* Muted umber (body text, descriptions, subtitles) */
  --color-text-tertiary: #85725f;   /* Warm stone gray (labels, metadata, timestamps) */
  --color-text-on-dark: #f3ece1;    /* Primary text on dark backgrounds */
  --color-text-muted-dark: #b8a695; /* Secondary text on dark backgrounds */

  /* Accents & Highlights */
  --color-accent-bronze: #9a6a35;   /* Warm bronze / ochre (primary accents, button hover) */
  --color-accent-bronze-deep: #7c5226; /* Deep antique bronze (active buttons, focus rings) */
  --color-accent-gold: #d1a46a;     /* Light champagne gold (borders on active badges) */
  --color-highlight-bg: #f9f2e7;    /* Subtle highlight background for contract annotator */
  --color-error: #9e2a2b;           /* Legal burgundy error state */
}
```

### Typography Scale & Font Mapping

```css
/* Font Families */
--font-serif: "Gambetta", Georgia, "Times New Roman", serif;
--font-sans: "General Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-mono: "Inter", monospace;
```

#### Typographic Scale Hierarchy:
| Level | Font Family | Size (Desktop / Tablet / Mobile) | Line Height | Letter Spacing | Weight |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero H1** | Serif (Gambetta) | `105.6px` / `75.2px` / `44px` | `0.9em` | `-0.045em` | 400 |
| **Section H2** | Serif (Gambetta) | `67.2px` / `48px` / `36px` | `0.98em` | `-0.045em` | 400 |
| **Subhead H3** | Serif (Gambetta) | `48px` / `36px` / `28px` | `1.05em` | `-0.04em` | 400 |
| **Card H4** | Serif (Gambetta) | `32px` / `26px` / `22px` | `1.15em` | `-0.03em` | 400 |
| **Pull Quote** | Serif (Gambetta) | `26px` / `22px` / `18px` | `1.25em` | `-0.02em` | 400 |
| **Body Large** | Sans (General Sans) | `17px` / `16px` / `15px` | `1.65em` | `0em` | 400 |
| **Body Normal** | Sans (General Sans) | `15px` / `15px` / `14px` | `1.6em` | `0em` | 400 |
| **Small / Meta** | Sans (General Sans) | `13px` / `13px` / `12px` | `1.4em` | `0.01em` | 400 |
| **Micro Badge** | Sans (General Sans) | `11px` / `11px` / `10px` | `1.0em` | `0.08em` (uppercase) | 500 / 600 |

### Elevation, Borders & Shadows
- **Card Radius:** Architectural minimal radius: `rounded-none` or `rounded-xs` (1px–2px) for a crisp, high-end editorial feel; inner UI elements use `rounded-xs` or `rounded-sm`.
- **Card Shadow:** Soft ambient lighting: `shadow-[0_2px_12px_rgba(42,28,18,0.04)]` or `shadow-[0_4px_24px_rgba(42,28,18,0.06)]`.
- **Dividers:** 1px solid `var(--color-border-subtle)` (`#e2d5c1`).

---

## 5. Local Asset Strategy & Media Inventory

To maintain high visual fidelity and eliminate broken image dependencies, the 32 reference assets are mapped to high-resolution, commercially licensed or royalty-free architectural and legal imagery with identical aspect ratios and editorial tones.

### Complete Asset Mapping Table

| Reference Asset Role | Reference Dimensions | Next.js Local Asset Path / High-Res Unsplash Equivalent | Visual Tone & Composition |
| :--- | :--- | :--- | :--- |
| **Hero Lady Justice** | 1200 × 2406 | `https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=1200` | Classical bronze Lady Justice statue holding scales of justice, warm dramatic lighting. |
| **224 S. LaSalle Facade** | 960 × 1200 | `https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=960` | Historic Chicago limestone high-rise architectural facade, LaSalle Financial District. |
| **31st Floor Reception** | 1200 × 900 | `https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1200` | Elegant mid-century wood-panelled law firm reception and conference suite. |
| **Disputes Practice** | 480 × 600 | `https://images.unsplash.com/photo-1453733197781-79dfb8c54146?auto=format&fit=crop&q=80&w=600` | Federal wood-panelled courtroom trial benches and law volumes. |
| **M&A Practice** | 480 × 600 | `https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&q=80&w=600` | Commercial attorneys reviewing purchase agreement across walnut boardroom table. |
| **Employment Practice** | 480 × 600 | `https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&q=80&w=600` | Corporate leadership and board executive consultation in conference room. |
| **Investigations Practice** | 480 × 600 | `https://images.unsplash.com/photo-1505664194779-8beaceb93744?auto=format&fit=crop&q=80&w=600` | Archived legal case records, bound volumes, and evidence files. |
| **Real Estate Practice** | 480 × 600 | `https://images.unsplash.com/photo-1477959858617-67f30bc75b82?auto=format&fit=crop&q=80&w=600` | Chicago River architecture and Loop high-rises illuminated at dusk. |
| **IP & Tech Practice** | 480 × 600 | `https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&q=80&w=600` | Red ink markup on technical contract agreement with fountain pen. |
| **Margaret Ellery** | 720 × 900 | `https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=900` | Professional senior female trial partner portrait, dark blazer, confident posture. |
| **Tomasz Kowal** | 720 × 900 | `https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=900` | Senior corporate M&A founding partner portrait, tailored suit, warm executive expression. |
| **Owen Pryce** | 720 × 900 | `https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&q=80&w=900` | Senior commercial litigation partner portrait, thoughtful gaze, LaSalle office background. |
| **Danielle Okafor** | 720 × 900 | `https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&q=80&w=900` | Employment & investigations partner portrait, authoritative presence. |
| **Marcus Leland** | 720 × 900 | `https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=900` | Government investigations and white-collar defense partner portrait. |
| **Helen Brandt** | 720 × 900 | `https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?auto=format&fit=crop&q=80&w=900` | Commercial real estate transactions partner portrait, poised and professional. |
| **Arjun Sethi** | 720 × 900 | `https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=900` | IP and emerging technology partner portrait, sharp modern styling. |
| **Article 1 (Lease Clauses)** | 1600 × 1000 | `https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&q=80&w=1600` | Chicago office interior overlooking downtown street grid. |
| **Article 2 (Subpoena 24h)** | 1600 × 1000 | `https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&q=80&w=1600` | Formal subpoena document folder stamped U.S. District Court. |
| **Article 3 (Open Source M&A)**| 1600 × 1000 | `https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&q=80&w=1600` | Software repository code review on dual high-resolution displays. |
| **Article 4 (Workplace Invest)**| 1600 × 1000 | `https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&q=80&w=1600` | Confidential boardroom interview setting with notepad and digital recorder. |
| **Article 5 (LOI 6 Terms)** | 1600 × 1000 | `https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&q=80&w=1600` | Financial valuation spreadsheets and marked-up letter of intent draft. |
| **Article 6 (90-Day Lawsuit)** | 1600 × 1000 | `https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=1600` | Litigation binder, court summons, and case calendar schedule. |
| **Article 7 (BIPA 2026)** | 1600 × 1000 | `https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&q=80&w=1600` | Biometric fingerprint timeclock and privacy compliance manual. |
| **Article 8 (Non-Competes)** | 1600 × 1000 | `https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&q=80&w=1600` | Executive separation agreement with severance schedules. |
| **Article 9 (Limitation Liab)** | 1600 × 1000 | `https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&q=80&w=1600` | Commercial contract Article 12 close-up with red ink annotations. |

### Image Optimization Rules
- All images render via Next.js `<Image />` with:
  - `priority` flag for the Hero Lady Justice image to maximize LCP.
  - `sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 33vw"`.
  - Placeholder background: `#EBE1D1` to eliminate layout shift during loading.
  - Correct aspect ratios via Tailwind `aspect-[3/4]`, `aspect-[16/10]`, or `aspect-[4/3]`.

---

## 6. Data Models & Mock Datasets Strategy

All mock data is centralized in `src/data/` using rigorous TypeScript types defined in `src/types/index.ts`. No mock data will use generic placeholders; every record uses authentic legal data directly extracted from the reference site.

### Master TypeScript Interfaces

```typescript
// Lawyer & Partner Profile
export interface Lawyer {
  id: string;
  name: string;
  role: string;
  practice: string;
  bio: string;
  inPracticeYears: number;
  admissions: string[];
  education: string[];
  priorExperience?: string;
  keyResults: string[];
  phone: string;
  email: string;
  image: string;
  isPartner: boolean;
}

// Practice Dossier
export interface Practice {
  id: string;
  slug: string;
  num: string; // "01", "02", etc.
  title: string;
  tagline: string;
  description: string;
  startingFee: string;
  feeType: string;
  feeBasis: string;
  feeDetail: string;
  partnerNames: string;
  partnerIds: string[];
  image: string;
  whatWeHandle: string[];
  whenClientsCall: string[];
  whereWeArgue?: string[];
  results?: { metric: string; description: string; forum: string }[];
}

// Representative Matter Record
export interface Matter {
  id: string;
  slug: string;
  result: string;
  resultUnit?: string;
  title: string;
  summary: string;
  whatHappened: string;
  leadPartner: string;
  practice: string;
  forum: string;
  year: string;
  category: "Disputes" | "Transactions" | "Investigations";
}

// Insight Article
export interface Article {
  id: string;
  slug: string;
  title: string;
  subtitle: string;
  category: string;
  date: string;
  readTime: string;
  author: string;
  authorRole: string;
  authorPractice: string;
  authorImage: string;
  pullQuote: string;
  paragraphs: string[];
  takeaways?: string[];
  image: string;
}

// Client Testimonial
export interface Testimonial {
  id: string;
  quote: string;
  role: string;
  company: string;
  clientSince: string;
}

// Frequently Asked Question
export interface FAQ {
  id: string;
  question: string;
  answer: string;
}

// Historical Milestone (The Firm)
export interface TimelineMilestone {
  year: string;
  title: string;
  description: string;
  keyMatters?: string[];
}

// Written Operational Commitment
export interface WrittenCommitment {
  id: string;
  number: string;
  title: string;
  summary: string;
  fullPolicy: string;
  artifactTitle: string;
}
```

### Mock Datasets to be Implemented

1. **`src/data/lawyers.ts`:**
   - 7 Equity Partners: Margaret Ellery, Tomasz Kowal, Owen Pryce, Danielle Okafor, Marcus Leland, Helen Brandt, Arjun Sethi.
   - Counsel & Associates Directory: 8 senior counsel and 26 associates categorized across the 6 practices with law school credentials and bar admissions.
2. **`src/data/practices.ts`:**
   - 6 Full Practice Areas:
     - `01 Trials & Disputes` (Margaret Ellery & Owen Pryce | From $650/hr)
     - `02 Corporate & M&A` (Tomasz Kowal | From $3,500)
     - `03 Employment` (Danielle Okafor | From $1,800)
     - `04 Investigations` (Marcus Leland | From $25,000 retainer)
     - `05 Real Estate` (Helen Brandt | From $4,500)
     - `06 IP & Technology` (Arjun Sethi | From $2,400)
3. **`src/data/matters.ts`:**
   - 16 High-Stakes Representative Matters across 2023–2026:
     1. `$18.4M Jury Verdict` (N.D. Ill.) — Freight logistics contract breach
     2. `$212M Company Sale` — 3rd-generation food manufacturer to private equity
     3. `Emergency 36-Hour TRO` (Cook County) — Chemical trade secrets protection
     4. `Zero-Charge DOJ Closure` — Healthcare fraud and False Claims Act investigation
     5. `Complete BIPA Defense Dismissal` — Biometric employee timeclock class action
     6. `$47M Fulton Market Acquisition` — Mixed-use commercial development
     7. `$0 Defense Arbitration Award` (AAA) — Executive severance claim defeat
     8. `$86M Strategic M&A Sale` — Commercial HVAC regional platform
     9. `SEC Regulatory Declination` — Insider trading investigation in fintech
     10. `Patent Non-Infringement Victory` (Fed. Cir.) — Industrial machinery sensor patent
     11. `7th Circuit Affirmance` — Breach of warranty summary judgment defense
     12. `$65M Industrial Warehouse Portfolio` — Sale-leaseback transaction
     13. `Audit Committee Special Investigation` — Whistleblower financial reporting inquiry
     14. `Restrictive Covenant Injunction` — Non-compete enforcement against defecting VP
     15. `$18M Series B Growth Equity` — Digital health platform financing
     16. `JAMS $9.6M Arbitration Award` — Supply chain price-escalation dispute
4. **`src/data/articles.ts`:**
   - 9 complete, long-form legal articles matching the reference site's exact slugs, subtitles, pull quotes, and multi-paragraph analyses.
5. **`src/data/testimonials.ts`:**
   - 4 client statements representing Chicago-area manufacturing, transport, chemicals, and SaaS clients.
6. **`src/data/faqs.ts`:**
   - 5 comprehensive questions covering conflict check turnaround, consultation fees, fixed-fee schedules, partner staffing guarantees, and emergency TRO availability.
7. **`src/data/firm.ts`:**
   - 15-year timeline from 2011 founding to 2026; 4 written commitments (No Surprise Bills, Partner on the Call, Real Deadlines, Clear Writing); 3 client profiles; LaSalle pro bono clinic.

---

## 7. Responsive Breakpoints & Layout Specifications

### Responsive Layout Rules

| Screen Category | Viewport Width | Navigation Layout | Grid & Columns | Container Padding |
| :--- | :--- | :--- | :--- | :--- |
| **Desktop Large** | `≥ 1200px` | Horizontal text menu + CTA button + logo | Full 12-column grid; 2-column hero split; 2-3 visible cards in slider; 2-column partner showcase | `px-12` or `px-16` (`max-w-[1424px]`) |
| **Tablet / Medium**| `600px – 1199px` | Simplified nav links or hamburger trigger | 2-column grid collapse; single-column hero with stacked Lady Justice portrait; 1.5 cards in slider | `px-6` or `px-8` |
| **Mobile** | `< 600px` | Logo + Hamburger trigger button | Single-column stack (`flex-col`); horizontally scrollable pill tabs; full-width buttons (44px min tap height) | `px-4` or `px-6` |

### Specific Layout Blueprint per Section

1. **Header:**
   - Desktop: Flex row: `[Ellery Kowal LLP Logo]` <spacer> `[Practices | People | Matters | Insights | The firm]` <spacer> `[Start a conflict check Button]`.
   - Mobile: Flex row: `[Ellery Kowal LLP Logo]` <spacer> `[Start a conflict check (compact)]` `[Hamburger Icon]`.
2. **Hero:**
   - Desktop: 2-column split (60% left column: Badge, H1, subhead, paragraph, CTAs; 40% right column: Tall bronze Lady Justice portrait).
   - Mobile: Vertical stack (Left column content first, followed by cropped landscape/square Lady Justice portrait).
3. **About Firm Strip:**
   - Desktop: Editorial text on left, 2 architectural images side-by-side on right, horizontal 4-stat metrics bar below.
   - Mobile: Editorial text, stacked images, 2x2 grid for the 4 metrics (`41 Lawyers`, `34 Trials`, `15 Years`, `92% Budget`).
4. **Interactive Contract Annotator:**
   - Desktop: 2-column layout (Left: Contract page mockup with floating number pins; Right: Partner commentary card).
   - Mobile: Contract page with pins above, commentary card directly beneath with swipe or tap indicator.
5. **Representative Matters Ledger:**
   - Desktop: Clean table ledger with columns `[Result]`, `[Title & Summary]`, `[Forum]`, `[Year]`, `[Toggle Chevron]`.
   - Mobile: Card-based list where result badge is on top, title below, forum/year as footer metadata.
6. **Conflict Check Intake:**
   - Desktop: 2-column split (Left: 4-step intake process explanation & phone numbers; Right: Complete conflict check form card).
   - Mobile: 4-step process in vertical order, followed by full-width conflict check form.

---

## 8. Animation & Transition Specifications

All animations leverage Framer Motion and comply with accessible motion preferences (`prefers-reduced-motion`).

### Motion Presets

```typescript
// Fade In Up Preset
export const fadeInUp = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] },
  },
};

// Stagger Container Preset
export const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

// Accordion Expand/Collapse Preset
export const accordionTransition = {
  initial: { height: 0, opacity: 0 },
  animate: {
    height: "auto",
    opacity: 1,
    transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] },
  },
  exit: {
    height: 0,
    opacity: 0,
    transition: { duration: 0.2, ease: [0.16, 1, 0.3, 1] },
  },
};

// Tab Crossfade Preset
export const crossfadeTransition = {
  initial: { opacity: 0, x: 8 },
  animate: { opacity: 1, x: 0, transition: { duration: 0.25, ease: "easeOut" } },
  exit: { opacity: 0, x: -8, transition: { duration: 0.15, ease: "easeIn" } },
};

// Slider Spring Transition
export const sliderSpring = {
  type: "spring",
  stiffness: 320,
  damping: 32,
};
```

---

## 9. Form Validation, Intake Workflow & State Handling

The conflict check intake flow is a central interactive feature. Because no external server is connected, the form validates inputs client-side and manages state through React `useState`.

### Form State Interface

```typescript
export interface ConflictCheckFormData {
  fullName: string;
  companyName: string;
  email: string;
  phone: string;
  matterType: string;
  adverseParties: string;
  urgency: "urgent-48h" | "upcoming-30d" | "none-yet";
  preferredDate?: string;
  preferredTime?: string;
  nonConfidentialAcknowledged: boolean;
}

export interface FormErrors {
  fullName?: string;
  companyName?: string;
  email?: string;
  phone?: string;
  matterType?: string;
  adverseParties?: string;
  nonConfidentialAcknowledged?: string;
}
```

### Validation Rules
1. `fullName`: Must be non-empty and contains at least 2 words.
2. `companyName`: Must be non-empty.
3. `email`: Must match standard email regex (`/^[^\s@]+@[^\s@]+\.[^\s@]+$/`).
4. `phone`: Must contain at least 10 digits.
5. `matterType`: Must have a selected value from the 6 practice areas.
6. `adverseParties`: Must be non-empty (law firms require adverse parties to run database conflict searches).
7. `nonConfidentialAcknowledged`: Must be `true` (regulatory legal requirement before attorney-client relationship is formed).

### Workflow States:
1. `idle`: Clean form, validation errors hidden until field blur or submit attempt.
2. `submitting`: Submit button shows animated spinner, inputs disabled for 600ms.
3. `success`: Form card smoothly animates out and is replaced by the confirmation view:
   - Message: *"Conflict check initiated for [Company Name]. Our conflicts committee and intake team at 224 S. LaSalle will review the adverse parties against our client roster and respond by 5:00 PM CT."*
   - Direct emergency hotline shown: `(312) 555-0163`.
   - "Submit another conflict check" button to reset form.

---

## 10. Visual Quality Assurance & Verification Strategy

A multi-phase verification checklist ensures pixel-perfect fidelity:

### QA Checklist Matrix

| Dimension | Verification Points | Pass Criteria |
| :--- | :--- | :--- |
| **Typography & Fonts** | Fontshare `@import` of `Gambetta` and `General Sans` loaded; fallbacks configured. | Inspect H1 and H2 rendered font family; ensure no unstyled serif/sans flash. |
| **Color Fidelity** | All background tones (`#f3ece1`, `#ebe1d1`, `#fffaf2`, `#24180f`) match reference. | Hex check against elements across light and dark sections. |
| **Route Navigation** | All 19 routes load without 404s or hydration mismatches. | Automated curl / page visit check on all paths. |
| **Interactive Widgets** | 1. Practice slider arrows and drag work smoothly.<br>2. Contract annotator pins toggle partner cards.<br>3. Matters ledger filters and expands.<br>4. Partner switcher swaps bios.<br>5. FAQ accordions open/close. | Manual interaction test for every state and event. |
| **Conflict Intake** | Form validates required fields, shows field errors, and transitions to confirmation screen. | Test empty submit, invalid email, and successful submission. |
| **Responsive Layouts** | Tested at `390px` (iPhone), `768px` (iPad), and `1440px` (Desktop). | Zero horizontal overflow; clean reflow; mobile drawer operates. |
| **Production Build** | `npm run build` executes with zero TypeScript errors and zero lint warnings. | Terminal exit code 0. |

---

## 11. Phased Implementation Roadmap

To ensure rapid, clean execution without regressions, the recreation will proceed through structured phases:

### Phase 1: Foundation, Tokens & Centralized Data
- Refine `src/app/globals.css` with exact `@theme inline` colors, font imports, and typography scale.
- Update `src/types/index.ts` with all complete interfaces.
- Create full, authentic datasets in `src/data/`:
  - `lawyers.ts` (7 partners + counsel and associates)
  - `practices.ts` (6 practices with detailed scopes & fee formulas)
  - `matters.ts` (16 representative matters with summaries & forums)
  - `articles.ts` (9 full insight articles)
  - `testimonials.ts` (4 client quotes)
  - `faqs.ts` (5 FAQs)
  - `firm.ts` (milestones, commitments, client types, pro bono)
  - `navigation.ts` (nav links & footer structure)
  - `fixed-fees.ts` (fee schedules & consultation slots)

### Phase 2: Core Layout & Navigation Components
- Enhance `src/components/layout/navbar.tsx` with sticky scroll blur, active links, conflict check trigger, and mobile drawer.
- Implement `src/components/layout/footer.tsx` with dark espresso styling, office address, phone lines, practice links, and legal disclaimers.
- Build UI primitives: `button.tsx`, `badge.tsx`, `card.tsx`, `accordion.tsx`, `tabs.tsx`, `input.tsx`, `select.tsx`, `textarea.tsx`, `modal.tsx`.

### Phase 3: Homepage Interactive Sections
- Hero section (`hero-section.tsx`) with Lady Justice bronze imagery and headline typography.
- About firm strip (`about-strip.tsx`) with LaSalle architecture photography and 4 metrics.
- Practices horizontal carousel (`practices-slider.tsx`) with next/prev buttons and slide cards.
- Transparency & fee models (`transparency-preview.tsx`) with consultation scheduler preview, sample fee sheet, and status report.
- Interactive contract annotator (`contract-annotator.tsx`) with 3 clickable clause pins and partner commentary cards.
- Matters preview table (`matters-preview.tsx`) with category tabs and expandable summaries.
- Partner showcase (`partner-showcase.tsx`) with 7-partner tabbed selector.
- Client testimonials slider (`client-quotes.tsx`).
- Latest insights 3-card grid (`latest-insights.tsx`).
- FAQ accordion section (`faq-section.tsx`).
- Conflict intake container (`conflict-intake-section.tsx`) with interactive form.

### Phase 4: Sub-Pages Implementation
- `/practices`: Full practices hub with anchor links (`#disputes`, `#corporate`, etc.), detailed scopes, fee ranges, and partner leads.
- `/people`: Partners showcase with comprehensive bios, admissions, trial wins, education, and the counsel/associates directory.
- `/matters`: Filterable representative matters ledger with category pills and expandable details for all 16 cases.
- `/firm`: Firm history, 15-year timeline (2011–2026), 4 operational commitments, client profiles, and pro bono clinic.
- `/insights`: Filterable articles index with category pills and newsletter signup.
- `/insights/[slug]`: 9 rich legal article pages with `generateStaticParams`, author bio cards, pull quotes, and related article links.
- `/contact`: Dedicated conflict check form, office address, LaSalle directions (Metra, 'L', driving), and direct phone lines.
- `/privacy` & `/disclaimer`: Formal legal notices.
- `/404`: Custom 404 error page.

### Phase 5: Polish, Responsive QA & Build Verification
- Verification across Mobile, Tablet, and Desktop viewports.
- Transition and animation tuning with Framer Motion.
- Final `npm run build` verification to guarantee zero build errors and pristine performance.

---

## Conclusion

This implementation plan provides a complete, deterministic, and faithful engineering specification for recreating the reference website `https://ellery-visuvate.framer.website/` down to every route, layout, interaction, design token, and mock dataset. Implementation will proceed strictly according to these specifications.

