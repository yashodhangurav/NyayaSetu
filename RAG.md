# NyayaSetu (न्यायसेतु) — Legal RAG & AI Assistant Specification

> **The Single Authoritative Reference for NyayaSetu's Retrieval-Augmented Generation (RAG) Architecture, Statutory Knowledge Base, and Legal Chatbot Scope.**

---

## 1. Scope of the Legal Chatbot

### 1.1 Objective & Target Audience
NyayaSetu's AI Legal Assistant is an India-focused citizen legal intelligence platform established in 2026. Its core mission is to demystify complex Indian statutes, empower citizens with immediate, verifiable, and plain-language legal clarity, and connect them with verified, empanelled advocates when formal legal intervention is required.

**Primary User Personas:**
- **Tenants & Landlords**: Security deposit disputes, unlawful eviction, maintenance duties, commercial and residential rent agreements.
- **Consumers**: Defective products, e-commerce fraud, unfair trade practices, deficiency in services, online e-Daakhil filing.
- **Property Owners & Inheritors**: Land conversion (Section 95 KLRA), Bhoomi RTC / Pahani extracts, mutation (Pouthi Khata), A/B-Khata, Kaveri 2.0 encumbrance search, ancestral coparcenary partition.
- **Marginalized Communities & SC/ST Grantees**: Protection under the Karnataka PTCL Act 1978, restoration of granted land, civil rights protections.
- **Employees & Workers**: Unlawful termination, non-payment of gratuity, workplace harassment (POSH Act), non-compete clause enforceability.
- **Citizens in Distress**: Cheque bounce notices (Section 138 NI Act), police FIR registration refusal, arrest safeguards (D.K. Basu guidelines), anticipatory bail, domestic violence protection orders, maintenance claims.

---

### 1.2 Geographic & Statutory Scope
The system operates on a dual-tier statutory hierarchy:
1. **India-Wide Central Jurisdiction (Union of India)**:
   - The 2023 Criminal Sanhitas (**BNS**, **BNSS**, **BSA**).
   - Core civil, commercial, and rights legislation (Transfer of Property Act, Contract Act, Specific Relief Act, Limitation Act, Registration Act, Easements Act, NI Act, Consumer Protection Act, RERA, SARFAESI, Hindu Marriage Act, Hindu Succession Act, PWDVA, RTI Act, DPDP Act, POSH Act, Motor Vehicles Act).
2. **Karnataka State Jurisdiction (Deep State Focus)**:
   - Land administration & revenue: **Karnataka Land Revenue Act, 1964** (KLRA), **Karnataka Land Reforms Act, 1961**, **Karnataka Land Grabbing Prohibition Act, 2011**, **Karnataka Apartment Ownership Act, 1972**.
   - Special protection: **Karnataka PTCL Act, 1978** (SC/ST granted land protection & restoration).
   - Tenancy: **Karnataka Rent Act, 1999** (Sections 14, 27).
   - Citizen services: **Karnataka Sakala Services Act, 2011** (guaranteed statutory delivery timelines).
   - Digital administrative portals: **Bhoomi** (RTC / Pahani, Mutation), **Kaveri 2.0** (Deed registration, Encumbrance Certificates), **e-Swathu** (Gram Panchayat Form 9/11A).

---

### 1.3 Supported Languages & Vernacular Processing
The assistant natively supports trilingual citizen communication with phonetic transliteration handling:
- **English**: Formal legal terminology and conversational English.
- **Kannada (ಕನ್ನಡ)**: Official state administrative language (e.g., ಪಹಣಿ, ಖಾತಾ, ನಾಮಾಂತರ, ಬಾಡಿಗೆ ಠೇವಣಿ, ಜಮೀನು).
- **Hindi (हिन्दी)**: National statutory and colloquial legal vocabulary (e.g., खतौनी, दाखिल खारिज, पैतृक संपत्ति, सुरक्षा जमा, जमानत).
- **Phonetic Mixed Scripts (Kanglish & Hinglish)**: Natural citizen search behavior in Roman script (e.g., `pahani download`, `khata transfer`, `jameen kabza`, `advance deposit refund`, `cheque bounce notice`).

---

### 1.4 Assistant Answer Anatomy & Output Contract
Every legal assessment adheres to an editorial, evidence-grounded anatomy:
1. **Decision Badge**:
   - `Self-help first`: For administrative disputes, RTI applications, consumer complaints, or demand notices manageable by the citizen.
   - `Advocate advised`: For complex title disputes, partition suits, high-value contracts, or contested divorces.
   - `Time-sensitive`: When statutory limitation deadlines are actively expiring (e.g., 30-day Section 138 NI Act notice, 6-month Section 6 SRA suit).
   - `Urgent`: For imminent arrest, custodial detention, domestic violence emergencies, or police refusal to register an FIR.
2. **Plain-Language Legal Explanation**: 2–3 structured paragraphs explaining legal rights, statutory provisions, and remedies without confusing jargon.
3. **Actionable Next Steps**: Numbered steps (maximum 4), with the first step prominently flagged as **"Do this in 48 hours"**.
4. **Court Deadlines & Limitation**: Explicitly calculated statutory time limits with direct integration into the user's court docket calendar.
5. **Authentic Source Citations**: Collapsible citation chips linking to verified Bare Act sections, gazette citations, or Supreme Court decisions with verified source URLs.
6. **Key Records to Gather**: Pragmatic checklist of documents (e.g., bank return memo, original lease deed, RTC extract, WhatsApp chat exports).
7. **Facts to Confirm**: Crucial factual clarifications that could alter the legal strategy (e.g., date of dishonour, registered vs unregistered deed).

---

### 1.5 Regulatory Compliance & Strict Guardrails
1. **Bar Council of India (BCI) Rule 36 Compliance**:
   - NyayaSetu strictly prohibits advocate advertising, commercial fee bidding, or paid priority placements.
   - Matching between citizens and advocates is purely merit-based, deterministic, and objective (scored by practice fit, court jurisdiction, language, and verified bar enrollment).
2. **Mandatory Non-Advice Disclaimer**:
   - *"NyayaSetu provides an AI-assisted preliminary legal assessment and advocate-discovery platform. It is not a law firm and does not provide formal legal advice. Submitting an inquiry does not establish an advocate-client relationship."*
3. **Limitation Act Disclaimers**:
   - Statutory limitation periods (e.g., Limitation Act 1963, NI Act Section 142) provide preliminary guidance and must be verified by an empanelled advocate before legal filing.
4. **Digital Personal Data Protection Act, 2023 (DPDP)**:
   - Private evidence files and citizen queries are stored securely with strict consent logging and access control.
5. **Negative Scope (Hard Rejections)**:
   - The assistant strictly declines: criminal bypass or evidence destruction advice, automated fraudulent drafting, tax evasion schemes, questions outside Indian jurisdiction, and extraterrestrial/unrelated inquiries.

---

## 2. Working of the Legal RAG System

```
                                  USER QUERY
                      (English / Kannada / Hindi / Mixed)
                                      │
                                      ▼
                      ┌─────────────────────────────────┐
                      │   Trilingual Query Rewriter     │
                      │  - Language Detection           │
                      │  - 37-Domain Taxonomy Routing   │
                      │  - Vernacular Synonym Expansion │
                      │  - Concordance Mapping (IPC→BNS)│
                      └────────────────┬────────────────┘
                                       │
                  ┌────────────────────┴────────────────────┐
                  ▼                                         ▼
      ┌───────────────────────┐                 ┌───────────────────────┐
      │  BM25 Lexical Search  │                 │  Semantic Dense Store │
      │  - Statutory terms    │                 │  - BGE-M3 / Vector    │
      │  - Act & section nos  │                 │  - 768-dim embeddings │
      └───────────┬───────────┘                 └───────────┬───────────┘
                  │                                         │
                  └────────────────────┬────────────────────┘
                                       ▼
                      ┌─────────────────────────────────┐
                      │  Reciprocal Rank Fusion (RRF)   │
                      │  - Merges Top 30 candidate hits │
                      └────────────────┬────────────────┘
                                       │
                                       ▼
                      ┌─────────────────────────────────┐
                      │   Cross-Encoder Reranker        │
                      │   - Scored statutory relevance  │
                      │   - Confidence Gating (>= 0.45) │
                      └────────────────┬────────────────┘
                                       │
               ┌───────────────────────┴───────────────────────┐
               ▼                                               ▼
     [High Confidence]                               [Low Confidence / OOS]
             │                                                 │
             ▼                                                 ▼
┌─────────────────────────────┐                    ┌────────────────────────┐
│  Grounded Prompt Generation │                    │ Safe Fallback Response │
│  - Groq LLM (Qwen 2.5 27B)  │                    │ - No hallucination     │
│  - Structured JSON schema   │                    │ - Excerpt-only guide   │
└──────────────┬──────────────┘                    └────────────────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Citation Validator Engine   │
│ - Checksum integrity match  │
│ - Hallucination pruning     │
│ - Prose sanitization        │
└──────────────┬──────────────┘
               │
               ▼
     STRUCTURED API RESPONSE
 (Answer, Badge, Deadlines, Sources)
```

### 2.1 Query Rewriting & Trilingual Expansion
Incoming queries pass through `backend/rag/search/query_rewriter.py`. The rewriter performs:
1. **Language Detection**: Distinguishes English, Kannada, and Hindi.
2. **Domain Classification**: Routes the query to one of **37 legal subdomains** (e.g., `PROP_LAND_REVENUE`, `COMM_CHEQUE_BOUNCE`, `CRIM_SANHITAS`).
3. **Vernacular Translation**: Expands vernacular words into legal equivalents (e.g., `"ಪಹಣಿ"` $\rightarrow$ `"Record of Rights RTC Pahani Karnataka Land Revenue Act Section 133"`).
4. **Out-of-Scope Screening**: Flags extraterrestrial, fictional, or non-legal prompts before retrieval.

### 2.2 Statutory Concordance Engine (Legacy to 2023 Sanhitas)
Because citizens frequently search using pre-2024 colonial provisions (e.g., "IPC 420 case", "CrPC 154 FIR", "498A domestic violence"), `backend/rag/ingest/concordance_table.py` maps historical terms to the current 2023 Sanhitas:
- **IPC 420 (Cheating)** $\rightarrow$ **BNS Section 318(4)**
- **IPC 498A (Cruelty)** $\rightarrow$ **BNS Section 85**
- **IPC 379/380 (Theft)** $\rightarrow$ **BNS Section 303(2) / 305**
- **IPC 302 (Murder)** $\rightarrow$ **BNS Section 103**
- **CrPC 154 (FIR)** $\rightarrow$ **BNSS Section 173**
- **CrPC 41A (Notice of Appearance)** $\rightarrow$ **BNSS Section 35(3)**
- **CrPC 438 (Anticipatory Bail)** $\rightarrow$ **BNSS Section 482**
- **IEA 65B (Electronic Evidence)** $\rightarrow$ **BSA Section 63**

### 2.3 Dual-Path Hybrid Search & Reranking
Retrieval combines two complementary indexing paths:
1. **BM25 Lexical Index**: Ensures exact keyword and section number matches (e.g., "Section 138", "Form 15", "Pahani").
2. **Dense Semantic Embeddings**: Hashed multilingual / dense vector representations capturing natural language semantic intent.
3. **Reciprocal Rank Fusion (RRF)**: Merges top 30 candidates with rank constants $k=60$ ($RRF(d) = \sum \frac{1}{k + r_i(d)}$).
4. **Cross-Encoder Reranker & Confidence Gating**: Reranks top 6–8 chunks. If top score $< 0.45$, the system triggers a low-confidence safe fallback, eliminating ungrounded answers.

### 2.4 LLM Generation & Structured Output
- **Model**: Groq-hosted `qwen/qwen3.8-27b` (with fallback to `gemini-2.5-flash` or deterministic mock in test environments).
- **Prompt Structure**: Injects retrieved authentic Bare Act sections, clause headings, and judgment summaries.
- **Strict Format**: Enforces a validated JSON schema containing `decision_badge`, `answer`, `legal_points`, `next_steps`, `deadline`, and `cited_references`.

### 2.5 Anti-Hallucination & Post-Generation Citation Validation
Every LLM response is processed through `backend/app/modules/legal_assistant/citation_validator.py`:
1. **Grounding Verification**: Verifies every cited reference against retrieved chunk checksums and source IDs.
2. **Hallucination Pruning**: Extracts all statutory mentions (`Section \d+`) in the answer text. Any section not present in retrieved authentic chunks is flagged and pruned.
3. **Prose Sanitization**: Neutralizes hallucinated mentions in the answer prose, replacing unsupported numbers with generic statutory references before returning the answer to the user.

### 2.6 Dual-Mode Resilience (Database + Bundled Corpus)
- **Primary Mode**: PostgreSQL 16 + pgvector storing curated legal sources and embeddings.
- **Offline Fallback Mode**: When running without an active PostgreSQL instance, `service.py` automatically falls back to `backend/rag/data/processed/canonical_corpus.json` (128 verified canonical chunks across 161 expanded sources), ensuring zero development or operational downtime.

---

## 3. Complete Inventory of All RAG Legal Sources

### 3.1 Tier 1: Central Legislation (Union of India)

| Source ID | Statute Title | Citation / Act No. | Key Provisions / Sections Covered | Official Portal URL |
|---|---|---|---|---|
| `SRC_CONST_001` | Constitution of India, 1950 | Constitution of India | Article 21 (Life & Liberty), Article 22 (Arrest & Detention safeguards) | [India Code](https://www.indiacode.nic.in) |
| `SRC_BNS_001` | Bharatiya Nyaya Sanhita, 2023 | Act No. 45 of 2023 | Section 318(4) (Cheating), Section 85 (Cruelty), Section 303(2) (Theft), Section 115(2) (Hurt), Section 351(2) (Intimidation), Section 103 (Murder) | [India Code](https://www.indiacode.nic.in) |
| `SRC_BNSS_001` | Bharatiya Nagarik Suraksha Sanhita, 2023 | Act No. 46 of 2023 | Section 35 (Arrest safeguards & notice), Section 173 (FIR & Zero FIR), Section 479 (Undertrial bail), Section 482 (Anticipatory bail) | [India Code](https://www.indiacode.nic.in) |
| `SRC_BSA_001` | Bharatiya Sakshya Adhiniyam, 2023 | Act No. 47 of 2023 | Section 61 & 63 (Admissibility of electronic records and certificates) | [India Code](https://www.indiacode.nic.in) |
| `SRC_NIA_001` | Negotiable Instruments Act, 1881 | Act No. 26 of 1881 | Section 138 (Cheque dishonour, 30-day notice, 15-day cure), Section 139 (Presumption), Section 142 (Cognizance & limitation) | [India Code](https://www.indiacode.nic.in) |
| `SRC_CPA_001` | Consumer Protection Act, 2019 | Act No. 35 of 2019 | Section 2(7) (Consumer definition), Section 35 (Filing complaint), Section 2(47) (Unfair trade practices), Section 69 (2-year limitation) | [e-Daakhil](https://edaakhil.nic.in) |
| `SRC_TPA_001` | Transfer of Property Act, 1882 | Act No. 4 of 1882 | Section 54 (Sale & registration), Section 53A (Part performance), Section 58 (Mortgages), Section 106 & 108 (Leases & security deposits), Section 122 (Gifts) | [India Code](https://www.indiacode.nic.in) |
| `SRC_REG_001` | Registration Act, 1908 | Act No. 16 of 1908 | Section 17 (Compulsory registration of sale, gift, leases > 1 yr), Section 49 (Effect of non-registration) | [India Code](https://www.indiacode.nic.in) |
| `SRC_EAS_001` | Indian Easements Act, 1882 | Act No. 5 of 1882 | Section 4 (Easement definition), Section 15 (20-year prescription pathway right of way) | [India Code](https://www.indiacode.nic.in) |
| `SRC_SRA_001` | Specific Relief Act, 1963 | Act No. 47 of 1963 | Section 6 (Summary suit for possession within 6 months), Section 10 (Specific performance), Section 34 (Declaration of title), Section 38 (Perpetual injunction) | [India Code](https://www.indiacode.nic.in) |
| `SRC_LIM_001` | Limitation Act, 1963 | Act No. 36 of 1963 | Section 3 & 5 (Limitation bar & condonation of delay), Article 54 (3-year specific performance), Article 65 (12-year adverse possession) | [India Code](https://www.indiacode.nic.in) |
| `SRC_RERA_001` | Real Estate (Regulation and Development) Act, 2016 | Act No. 16 of 2016 | Section 11 (Promoter duties), Section 14 (Sanctioned plans & 5-year defect liability), Section 18 (Possession delay refunds with interest) | [RERA Portal](https://rera.karnataka.gov.in) |
| `SRC_SARFAESI_001` | SARFAESI Act, 2002 | Act No. 54 of 2002 | Section 13 (Enforcement of security interest, 60-day statutory demand notice) | [India Code](https://www.indiacode.nic.in) |
| `SRC_HMA_001` | Hindu Marriage Act, 1955 | Act No. 25 of 1955 | Section 13B (Mutual consent divorce, 6-month cooling off waiver rules) | [India Code](https://www.indiacode.nic.in) |
| `SRC_HSA_001` | Hindu Succession Act, 1956 | Act No. 30 of 1956 | Section 6 (Equal coparcenary rights for daughters in ancestral property by birth) | [India Code](https://www.indiacode.nic.in) |
| `SRC_PWDVA_001` | Protection of Women from Domestic Violence Act, 2005 | Act No. 43 of 2005 | Section 12 (Application), Section 17 & 19 (Right to reside in shared household), Section 18 (Protection orders) | [India Code](https://www.indiacode.nic.in) |
| `SRC_RTI_001` | Right to Information Act, 2005 | Act No. 22 of 2005 | Section 6 (Filing request), Section 7 (30-day disposal, 48-hour life/liberty window), Section 19 (Appeals) | [RTI Online](https://rtionline.gov.in) |
| `SRC_DPDP_001` | Digital Personal Data Protection Act, 2023 | Act No. 22 of 2023 | Section 6 (Consent requirements and notices), Section 8 (Data fiduciary duties) | [MeitY](https://www.meity.gov.in) |
| `SRC_POSH_001` | Sexual Harassment of Women at Workplace (POSH) Act, 2013 | Act No. 14 of 2013 | Section 4 (Internal Complaints Committee), Section 9 (90-day complaint timeline) | [Ministry of WCD](https://wcd.nic.in) |
| `SRC_ICA_001` | Indian Contract Act, 1872 | Act No. 9 of 1872 | Section 10 (Essential elements), Section 27 (Agreement in restraint of trade void), Section 73 (Breach damages) | [India Code](https://www.indiacode.nic.in) |
| `SRC_MVA_001` | Motor Vehicles Act, 1988 / 2019 | Act No. 59 of 1988 | Section 166 (MACT claim petitions), Section 161 (Special scheme for hit and run) | [MoRTH](https://morth.nic.in) |
| `SRC_IDA_001` | Industrial Disputes Act, 1947 | Act No. 14 of 1947 | Section 2A (Individual industrial dispute), Section 25F (Retrenchment notice & compensation) | [Labour Ministry](https://labour.gov.in) |
| `SRC_PGA_001` | Payment of Gratuity Act, 1972 | Act No. 39 of 1972 | Section 4 (Eligibility on 5 years continuous service, calculation formula) | [Labour Ministry](https://labour.gov.in) |
| `SRC_COPYRIGHT_001` | Copyright Act, 1957 | Act No. 14 of 1957 | Section 51 (Infringement), Section 52 (Fair dealing exceptions) | [Copyright Office](https://copyright.gov.in) |
| `SRC_TRADEMARKS_001` | Trade Marks Act, 1999 | Act No. 47 of 1999 | Section 29 (Infringement of registered marks), Section 134 (Suit jurisdiction) | [IP India](https://ipindia.gov.in) |

---

### 3.2 Tier 2: Karnataka State Legislation & Rules

| Source ID | Statute Title | Citation / Act No. | Key Provisions / Sections Covered | Official Portal URL |
|---|---|---|---|---|
| `SRC_KAR_LRA_001` | Karnataka Land Revenue Act, 1964 | Karnataka Act 12 of 1964 | Section 95 (Land conversion agricultural to non-agricultural), Section 128 (Reporting title acquisition), Section 133 (RTC / Pahani entries presumption) | [Karnataka DPAL](https://dpal.karnataka.gov.in) |
| `SRC_KAR_RENT_001` | Karnataka Rent Act, 1999 | Karnataka Act 34 of 2001 | Section 14 (Landlord repair duty, essential services), Section 27 (Eviction protection, security deposit refund within 30 days) | [Karnataka DPAL](https://dpal.karnataka.gov.in) |
| `SRC_KAR_LREFORMS_001` | Karnataka Land Reforms Act, 1961 | Karnataka Act 10 of 1962 | Section 79A/B (Omitted by Act 29 of 2020), Section 132 (Bar of civil court jurisdiction) | [Karnataka DPAL](https://dpal.karnataka.gov.in) |
| `SRC_KAR_PTCL_001` | Karnataka SC/ST (Prohibition of Transfer of Certain Lands) Act, 1978 | Karnataka Act 2 of 1979 | Section 4 (Prohibition of transfer of granted land without Govt permission; void ab initio), Section 5 (Resumption & restitution to grantee) | [Karnataka DPAL](https://dpal.karnataka.gov.in) |
| `SRC_KAR_LANDGRAB_001` | Karnataka Land Grabbing Prohibition Act, 2011 | Karnataka Act 38 of 2014 | Section 3 & 4 (Prohibition of land grabbing of government/wakf land), Section 7 (Special Court powers) | [Karnataka DPAL](https://dpal.karnataka.gov.in) |
| `SRC_KAR_APT_001` | Karnataka Apartment Ownership Act, 1972 | Karnataka Act 17 of 1973 | Section 5 (Undivided interest in common areas & facilities), Section 10 (Deed of Declaration) | [Karnataka DPAL](https://dpal.karnataka.gov.in) |
| `SRC_KAR_SAKALA_001` | Karnataka Sakala Services Act, 2011 | Karnataka Act 30 of 2011 | Enforceable statutory timelines for RTC issuance, mutation, phodi durasti, and conversion | [Sakala Online](https://sakala.kar.nic.in) |

---

### 3.3 Tier 3: Citizen Procedures & Portals

| Source ID | Guide Title | Administrative Steps / Scope | Official Portal URL |
|---|---|---|---|
| `SRC_PROC_BHOOMI_001` | Bhoomi Karnataka Land Portal Guide | Online verification of RTC / Pahani (Columns 9, 10, 11, 12), mutation status tracking, digital signed extract downloads | [Bhoomi](https://bhoomi.karnataka.gov.in) |
| `SRC_PROC_KAVERI_001` | Kaveri 2.0 Property Registration & EC | Online Encumbrance Certificate search (Form 15 & Form 16 over 15-30 years), stamp duty calculation, SRO booking | [Kaveri 2.0](https://kaveri.karnataka.gov.in) |
| `SRC_PROC_FIR_001` | FIR & Zero FIR Procedure | Mandatory registration under Section 173 BNSS, Zero FIR at any police station, remedy to SP/Commissioner, Section 175(3) BNSS Magistrate complaint | [National Police Services](https://digitalpolice.gov.in) |
| `SRC_PROC_EDAAKHIL_001` | e-Daakhil Online Consumer Complaint | Online filing on edaakhil.nic.in, zero fee up to ₹5 Lakhs, 21-day admission timeline, notice issuance | [e-Daakhil](https://edaakhil.nic.in) |
| `SRC_PROC_NALSA_001` | Free Legal Aid & 15100 Helpline | Eligibility under Legal Services Authorities Act Section 12 (women, children, SC/ST, custody, income < ₹3 Lakhs) | [NALSA](https://nalsa.gov.in) |
| `SRC_PROC_CYBER_001` | National Cyber Crime Helpline 1930 | Golden hour reporting for financial cyber fraud, freezing fraudulent transactions, filing on cybercrime.gov.in | [Cyber Crime Portal](https://cybercrime.gov.in) |

---

### 3.4 Tier 4: Landmark Judicial Precedents

| Source ID | Case Citation | Court & Date | Legal Issue & Core Ratio Decidendi |
|---|---|---|---|
| `SRC_CASE_SURAJLAMP_001` | *Suraj Lamp & Industries Pvt. Ltd. v. State of Haryana* (2012) 1 SCC 656 | Supreme Court of India (11.10.2011) | **GPA transfers do not convey title**: Immovable property can only be transferred by registered deed of conveyance. SA/GPA/Will transactions convey no title. |
| `SRC_CASE_VINEETA_001` | *Vineeta Sharma v. Rakesh Sharma* (2020) 9 SCC 1 | Supreme Court (3-Judge Bench, 11.08.2020) | **Daughter's equal coparcenary rights by birth**: Daughters possess equal rights by birth under Section 6 HSA regardless of whether the father was alive on 09.09.2005. |
| `SRC_CASE_JITENDRA_001` | *Jitendra Singh v. State of Madhya Pradesh* (2021) SCC OnLine SC 802 | Supreme Court of India (06.09.2021) | **Mutation does not confer title**: Revenue mutation is solely for fiscal tax collection purposes; title must be established in civil court. |
| `SRC_CASE_RAVINDER_001` | *Ravinder Kaur Grewal v. Manjit Kaur* (2019) 8 SCC 729 | Supreme Court (3-Judge Bench, 07.08.2019) | **Adverse possession as a sword**: A possessor who has perfected title after 12 years of hostile possession under Article 65 can affirmatively sue for declaration of title. |
| `SRC_CASE_ANATHULA_001` | *Anathula Sudhakar v. P. Buchi Reddy* (2008) 4 SCC 594 | Supreme Court of India (25.03.2008) | **Injunction vs. Declaration of Title**: Where title is disputed or under cloud, a suit for bare injunction is not maintainable; plaintiff must sue for declaration of title. |
| `SRC_CASE_DKBASU_001` | *D.K. Basu v. State of West Bengal* (1997) 1 SCC 416 | Supreme Court of India (18.12.1996) | **Arrest safeguards**: 11 mandatory guidelines including arrest memo, right to inform relative within 8-12 hours, and medical checkup every 48 hours. |
| `SRC_CASE_ARNESH_001` | *Arnesh Kumar v. State of Bihar* (2014) 8 SCC 273 | Supreme Court of India (02.07.2014) | **No automatic arrest**: Mandatory Section 41A CrPC (now Section 35(3) BNSS) notice for offences punishable with imprisonment up to 7 years. |
| `SRC_CASE_LALITA_001` | *Lalita Kumari v. Govt. of U.P.* (2014) 2 SCC 1 | Supreme Court (5-Judge Bench, 12.11.2013) | **Mandatory FIR registration**: Registration of FIR under Section 154 CrPC (Section 173 BNSS) is mandatory if cognizable offence is disclosed. |
| `SRC_CASE_PUTTASWAMY_001` | *Justice K.S. Puttaswamy v. Union of India* (2017) 10 SCC 1 | Supreme Court (9-Judge Bench, 24.08.2017) | **Fundamental Right to Privacy**: Privacy is an intrinsic fundamental right under Article 21; requires legality, legitimate state aim, and proportionality. |
| `SRC_CASE_RAJNESH_001` | *Rajnesh v. Neha* (2021) 2 SCC 324 | Supreme Court of India (04.11.2020) | **Uniform maintenance guidelines**: Mandatory filing of Affidavit of Assets and Liabilities by both spouses in matrimonial maintenance disputes. |
| `SRC_CASE_VISHAKA_001` | *Vishaka v. State of Rajasthan* (1997) 6 SCC 241 | Supreme Court of India (13.08.1997) | **Workplace sexual harassment safeguards**: Foundational guidelines for institutional complaints committees, codified in POSH Act 2013. |
| `SRC_CASE_RANGAPPA_001` | *Rangappa v. Sri Mohan* (2010) 11 SCC 441 | Supreme Court (3-Judge Bench, 07.05.2010) | **Section 139 NI Act presumption**: Reverse onus on drawer to rebut existence of legally enforceable debt once cheque signature is admitted. |

---

### 3.5 Tier 5: Trilingual Glossaries & Vernacular Lexicon
Covers 500+ localized terms in `backend/rag/search/query_rewriter.py` ensuring natural citizen vernacular correctly translates to authentic statutory provisions:
- **Pahani / RTC (ಪಹಣಿ / ಆರ್‌ಟಿಸಿ / खतौनी)**: Record of Rights extract under KLRA Section 133.
- **Mutation (ನಾಮಾಂತರ / ಪೌತಿ ಖಾತಾ / दाखिल खारिज)**: Administrative registration of succession under KLRA Section 128.
- **A-Khata / B-Khata (ಎ-ಖಾತಾ / ಬಿ-ಖಾತಾ)**: Municipal property register classifications in Bangalore.
- **Encumbrance Certificate (ಭಾರಮುಕ್ತ ಪ್ರಮಾಣಪತ್ರ / भारमुक्त प्रमाण पत्र)**: Kaveri 2.0 registered charge search (Form 15 / Form 16).
- **Phodi / Durasti (ಫೋಡಿ / ದುರಸ್ತಿ / हदबंदी)**: Survey and land sub-division under Karnataka Revenue rules.
- **Anticipatory Bail (ನಿರೀಕ್ಷಣಾ ಜಾಮೀನು / अग्रिम जमानत)**: Section 482 BNSS relief.
- **Security Deposit (ಭದ್ರತಾ ಠೇವಣಿ / सुरक्षा जमा)**: Karnataka Rent Act Section 27 and TPA Section 108.

---

## 4. Verification & Operational Health Check

To verify the RAG system, query rewriter, and offline canonical corpus:
```powershell
# From backend/
python scripts/verify_health.py

# Generate or refresh canonical corpus:
python -m rag.ingest.corpus_builder

# Test hybrid search from CLI:
python -c "from rag.search.hybrid_search import LegalHybridSearchEngine; e = LegalHybridSearchEngine(); print(e.search('Bhoomi RTC Pahani', top_k=2))"
```
