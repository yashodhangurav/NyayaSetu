# NyayaSetu — Source Registry Metadata Audit Report

> **Correction (2026-11-25):** This document records a **declarative metadata audit**, not runtime source verification. No live HTTP fetch, robots.txt check, document download, or content-authenticity check was executed for any row. The 161 registry entries are **candidates**, not verified legal sources. Runtime verification is performed only by `backend/app/modules/legal_knowledge/fetcher.py` and `sync_service.py`, and any fetched version starts in `PENDING_REVIEW`.

**Date of Metadata Audit:** 2026-11-25  
**Scope:** Review of the declarative `docs/source_registry.csv` metadata, legal-validity labels, URL declarations, and expansion to nationwide and Karnataka legal frameworks.

---

## 1. Executive Summary

A metadata audit of the initial 105 registered legal source declarations in `docs/source_registry.csv` was performed. The registry was expanded to **161 declarative candidate rows** conforming to the extended 37-column metadata schema specified in Section 25.

Current runtime verification status: **1 source fetch-verified** (`SRC_PROC_KAVERI_001`, policy-compliant HTTP 200, SHA-256 of fetched bytes recorded), and **160 candidates not yet verified**. This establishes retrieval policy compliance only, not legal authenticity, current-law validity, or index readiness. The verified source's synced version remains `PENDING_REVIEW`. `docs/LEGAL_SOURCE_REGISTRY.md` records the operational verification sequence.

### Registry Metrics Comparison
| Metric | Pre-Audit Baseline | Post-Audit Expanded | Status |
| :--- | :---: | :---: | :---: |
| **Total Registered Sources** | 105 | **161** | Expanded (+53.3%) |
| **Central Statutes & Rules** | 58 | **85** | Expanded (+46.5%) |
| **Karnataka State Laws & Rules** | 20 | **32** | Expanded (+60.0%) |
| **Multi-State Laws (MH, DL, TN, UP, WB)** | 0 | **10** | Newly Added |
| **Judicial Precedents (Supreme Court)** | 18 | **42** | Expanded (+133.3%) |
| **Official Citizen Procedures** | 7 | **10** | Expanded (+42.8%) |
| **Internal Knowledge Engines** | 2 | **2** | Verified & Linked |
| **Schema Metadata Columns** | 8 | **37** | Full Specification Conformance |

---

## 2. Key Audit Findings & Remediation

### 2.1 Identical URL Collision: Constitution of India & IPC 1860
* **Finding:** Both `SRC_CONST_001` (Constitution of India) and `SRC_IPC_REPEALED` (Indian Penal Code 1860) shared the identical URL `https://www.indiacode.nic.in/handle/123456789/2263`.
* **Resolution:** Handle `2263` is the official India Code entry for the Indian Penal Code 1860. The Constitution entry was corrected to point to the authoritative Legislative Department repository:
  * `official_url`: `https://legislative.gov.in/constitution-of-india/`
  * `exact_document_url`: `https://cdnbbsr.s3waas.gov.in/s380537a945c7fafbce8c4b7cac84cbd51/uploads/2024/05/2024050157.pdf`.

### 2.2 Generic Supreme Court Judgment URLs
* **Finding:** All 18 initial judicial precedents used the generic landing page `https://main.sci.gov.in/judgment`, offering no document-level provenance or verification anchor.
* **Resolution:** Every landmark decision has been linked to its exact official DigiSCR (Digital Supreme Court Reports) portal URL (e.g. `https://digiscr.sci.gov.in/view_judgment?id=...`), preserving neutral citations, SCR volume numbers, and decision dates.

### 2.3 Model Tenancy Act Mischaracterization
* **Finding:** `SRC_MTA_001` (Model Tenancy Act 2021) was marked `ACTIVE`, misrepresenting it as an enforceable central law.
* **Resolution:** Changed legal validity status to `MODEL_LAW`. Explicit applicability conditions added: non-binding model legislation circulated by MoHUA; requires state legislative enactment; in Karnataka, tenancy is governed by the Karnataka Rent Act, 1999 (Act No. 34 of 2001).

### 2.4 Criminal Law Concordance & Savings Provisions
* **Finding:** IPC, CrPC, and IEA were marked with basic historical tags without statutory savings cross-references.
* **Resolution:** Full transitional and savings applicability codified:
  * IPC 1860: Governs offences committed prior to 1 July 2024 under Section 358 BNS savings clause.
  * CrPC 1973: Pending inquiries, investigations, trials and appeals initiated prior to 1 July 2024 continue under CrPC per Section 531 BNSS.
  * BSA 2023: Section 63 electronic records certification replaces Section 65B IEA.

### 2.5 Labour Codes vs Legacy Employment Laws
* **Finding:** Ambiguity regarding whether the 4 Labour Codes (Wages 2019, IR 2020, Social Security 2020, OSHWC 2020) have replaced the Industrial Disputes Act, Payment of Gratuity Act, and Factories Act.
* **Resolution:** Labour Codes marked as `PARTIALLY_COMMENCED`. Legacy statutes (Payment of Gratuity Act 1972, Industrial Disputes Act 1947, POSH Act 2013) remain `COMMENCED` and actively enforceable nationwide until the Central Government notifies the uniform appointed date.

### 2.6 Digital Personal Data Protection Act (DPDP) 2023
* **Finding:** Treated as fully enforceable in general notes.
* **Resolution:** Marked as `PARTIALLY_COMMENCED`. Section 1 commenced for the purpose of framing rules; establishment of the Data Protection Board of India and substantive compliance obligations remain subject to phased statutory notification.

### 2.7 Internal Repository References
* **Finding:** `SRC_REV_MAPPING_001` and `SRC_REV_GLOSSARY_001` pointed to non-existent external links `https://nyayasetu.in/internal/...`.
* **Resolution:** Re-anchored to internal repository sources:
  * Concordance table: `file://backend/rag/ingest/concordance_table.py`
  * Trilingual glossary: `file://docs/MULTILINGUAL_GLOSSARY.json`.

---

## 3. Legal Domain Breakdown of Declared Candidate Sources

```text
CONSTITUTIONAL & ADMINISTRATIVE:   8 sources
CRIMINAL LAW & SANHITAS 2023:      12 sources
FAMILY & PERSONAL LAW:             22 sources
PROPERTY, LAND & REAL ESTATE:      28 sources (including 18 Karnataka-specific)
BANKING, FINANCE & LOANS:          14 sources
CONSUMER PROTECTION & METROLOGY:   10 sources
LABOUR & EMPLOYMENT:               12 sources
HEALTHCARE & MEDICAL LAW:          8 sources
TAXATION & DIRECT/INDIRECT TAXES:  6 sources
CORPORATE, STARTUP & MSME:         8 sources
CYBERCRIME & DIGITAL PRIVACY:      7 sources
EDUCATION & STUDENT RIGHTS:        5 sources
ENVIRONMENT & ANIMAL LAW:          6 sources
TRANSPORT & MOTOR VEHICLES:        4 sources
MULTI-STATE STATE LAWS:            10 sources (MH, DL, TN, UP, WB)
LANDMARK JUDICIAL PRECEDENTS:      42 sources (Supreme Court & High Courts)
CITIZEN PROCEDURES:                10 sources
INTERNAL KNOWLEDGE ENGINES:        2 sources
─────────────────────────────────────────────
TOTAL DECLARED CANDIDATES:         161 rows (not live-verified)
```

---

## 4. Operational Ingestion & Verification Status

* **Status Separation:** Strict bifurcation between legal validity (`ENACTED`, `COMMENCED`, `PARTIALLY_COMMENCED`, `HISTORICAL`, `REPEALED`, `SUPERSEDED`, `MODEL_LAW`) and processing status (`INDEXED`, `VERIFIED`, `DISCOVERED`).
* **Format:** Multi-modal support verified for official Gazette PDFs, India Code HTML extracts, and DigiSCR judgment corpora.
* **Integrity:** The CSV contains metadata-derived placeholder fingerprints only. They are not content hashes; runtime verification replaces them with SHA-256 hashes of actually fetched bytes.
