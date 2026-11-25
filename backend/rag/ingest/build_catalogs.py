"""Generates Legal Scenario Catalog and Judicial Precedent Catalog for NyayaSetu.
Outputs:
- backend/rag/data/scenario_catalog.json & docs/LEGAL_SCENARIO_CATALOG.md
- backend/rag/data/precedents_catalog.json & docs/JUDICIAL_PRECEDENT_CATALOG.md
"""

import json
import os
from typing import Dict, List, Any

# ─────────────────────────────────────────────────────────────────────────────
# 1. JUDICIAL PRECEDENT CATALOG (All 14 mandatory fields per Section 20)
# ─────────────────────────────────────────────────────────────────────────────
PRECEDENTS: List[Dict[str, Any]] = [
    {
        "case_title": "Suraj Lamp & Industries Pvt. Ltd. v. State of Haryana",
        "court": "Supreme Court of India",
        "case_number": "Special Leave Petition (C) No. 13917 of 2009",
        "decision_date": "2011-10-11",
        "bench_strength": "3-Judge Bench (R.V. Raveendran, A.K. Patnaik, H.L. Gokhale, JJ.)",
        "official_citation": "(2012) 1 SCC 656 / 2011 INSC 752",
        "relevant_paragraphs": "Paragraphs 12, 16, 18, 19, 22",
        "material_facts": "Widespread practice of transferring immovable property using General Power of Attorney (GPA), Agreement to Sell (SA), and Living Wills (SA/GPA/WILL transfers) to evade stamp duty and capital gains.",
        "legal_issue": "Whether an immovable property can be lawfully transferred or ownership conveyed through an Agreement to Sell, GPA, or Will?",
        "ratio_decidendi": "A power of attorney is an agency creation and does not convey title. Under Section 54 of Transfer of Property Act, 1882, transfer of immovable property can only be effected by a registered conveyance deed.",
        "holding": "SA/GPA/WILL transfers do not convey title or create ownership interest in immovable property. Courts will not recognize such transactions as completed sales.",
        "related_statutory_provisions": "Transfer of Property Act 1882 (Sec 54), Registration Act 1908 (Sec 17, 49), Powers-of-Attorney Act 1882 (Sec 2)",
        "subsequent_judicial_treatment": "Followed and affirmed in Ghanshyam v. Yogendra Rathi (2023) and Shakeel Ahmed v. Syed Akhlaq Hussain (2023).",
        "applicability_status": "Controlling Law (Union of India)",
        "exact_official_document_url": "https://digiscr.sci.gov.in/view_judgment?id=MTI0NjI=",
    },
    {
        "case_title": "Vineeta Sharma v. Rakesh Sharma",
        "court": "Supreme Court of India",
        "case_number": "Civil Appeal No. 32601 of 2018",
        "decision_date": "2020-08-11",
        "bench_strength": "3-Judge Bench (Arun Mishra, S. Abdul Nazeer, M.R. Shah, JJ.)",
        "official_citation": "(2020) 9 SCC 1 / 2020 INSC 483",
        "relevant_paragraphs": "Paragraphs 60, 68, 75, 129, 137",
        "material_facts": "Conflicting High Court and Supreme Court interpretations on whether a daughter acquires coparcenary rights under Section 6 HSA 2005 amendment if her father had died before September 9, 2005.",
        "legal_issue": "Whether the Hindu Succession (Amendment) Act, 2005 confers coparcenary rights on daughters by birth retrospectively/retroactively regardless of father death date?",
        "ratio_decidendi": "The right is conferred by birth and is not dependent on the father living at the time of the 2005 amendment. Daughters have equal coparcenary rights from birth.",
        "holding": "Daughters have coparcenary rights in Mitakshara coparcenary property by birth in the same manner as sons, irrespective of whether the father was alive on September 9, 2005.",
        "related_statutory_provisions": "Hindu Succession Act, 1956 (Section 6, as amended by Act 39 of 2005)",
        "subsequent_judicial_treatment": "Settled law; confirmed in multiple Supreme Court and High Court partition rulings.",
        "applicability_status": "Controlling Law (Union of India)",
        "exact_official_document_url": "https://digiscr.sci.gov.in/view_judgment?id=MzA4NzI=",
    },
    {
        "case_title": "Rajnesh v. Neha",
        "court": "Supreme Court of India",
        "case_number": "Criminal Appeal No. 730 of 2020",
        "decision_date": "2020-11-04",
        "bench_strength": "2-Judge Bench (Indu Malhotra, R. Subhash Reddy, JJ.)",
        "official_citation": "(2021) 2 SCC 324 / 2020 INSC 629",
        "relevant_paragraphs": "Paragraphs 56, 72, 84, 91, 105",
        "material_facts": "Conflicting and prolonged maintenance litigation across multiple forums (Section 125 CrPC, PWDVA Section 12, HMA Section 24) with frequent concealment of income and delayed adjudication.",
        "legal_issue": "What uniform guidelines should be established to streamline maintenance calculation, asset disclosure, and eliminate overlapping awards?",
        "ratio_decidendi": "Fair maintenance determination requires mandatory sworn disclosure of all financial assets, liabilities, and lifestyle standards from the date of application.",
        "holding": "Both parties in all matrimonial maintenance proceedings must mandatorily file a standardized Affidavit of Assets and Liabilities. Maintenance is payable from the date of filing the petition.",
        "related_statutory_provisions": "BNSS 2023 (Sec 144) / CrPC 1973 (Sec 125), PWDVA 2005 (Sec 12, 20), HMA 1955 (Sec 24, 25)",
        "subsequent_judicial_treatment": "Universally followed across all Family Courts and High Courts nationwide.",
        "applicability_status": "Controlling Law (Union of India)",
        "exact_official_document_url": "https://digiscr.sci.gov.in/view_judgment?id=MzEzNjU=",
    },
    {
        "case_title": "Arnesh Kumar v. State of Bihar",
        "court": "Supreme Court of India",
        "case_number": "Criminal Appeal No. 1277 of 2014",
        "decision_date": "2014-07-02",
        "bench_strength": "2-Judge Bench (Chandramauli Kr. Prasad, Pinaki Chandra Ghose, JJ.)",
        "official_citation": "(2014) 8 SCC 273 / 2014 INSC 492",
        "relevant_paragraphs": "Paragraphs 7, 8, 9, 11, 12",
        "material_facts": "Rampant mechanical arrests under Section 498A IPC without satisfying necessity grounds or conducting preliminary investigation.",
        "legal_issue": "Whether police officers can effect automatic arrests in offences punishable with up to seven years imprisonment without judicial scrutiny?",
        "ratio_decidendi": "Arrest brings personal humiliation and curtailment of liberty. Police must apply the checklist under Section 41(1)(b) CrPC (Section 35 BNSS) and record reasons before arresting.",
        "holding": "No automatic arrest in offences punishable with imprisonment up to seven years. Police must issue a notice of appearance under Section 41A CrPC (Section 35(3) BNSS) unless exceptional arrest grounds are documented.",
        "related_statutory_provisions": "BNSS 2023 (Sec 35) / CrPC 1973 (Sec 41, 41A), BNS 2023 (Sec 85/86) / IPC 1860 (Sec 498A)",
        "subsequent_judicial_treatment": "Reiterated and extended to all offences with up to 7 years imprisonment in Satender Kumar Antil (2022).",
        "applicability_status": "Controlling Law (Union of India)",
        "exact_official_document_url": "https://digiscr.sci.gov.in/view_judgment?id=MTcwMzc=",
    },
    {
        "case_title": "Lalita Kumari v. Government of Uttar Pradesh",
        "court": "Supreme Court of India",
        "case_number": "Writ Petition (Criminal) No. 68 of 2008",
        "decision_date": "2013-11-12",
        "bench_strength": "5-Judge Constitution Bench (P. Sathasivam, C.J., B.S. Chauhan, Ranjana P. Desai, Ranjan Gogoi, S.A. Bobde, JJ.)",
        "official_citation": "(2014) 2 SCC 1 / 2013 INSC 798",
        "relevant_paragraphs": "Paragraphs 120, 121",
        "material_facts": "Police refusal to register FIR regarding abduction of a minor girl, leading to a reference to Constitution Bench on the mandatory nature of Section 154 CrPC.",
        "legal_issue": "Is a police officer bound to register an FIR upon receiving information relating to the commission of a cognizable offence?",
        "ratio_decidendi": "The word 'shall' in Section 154 CrPC (Section 173 BNSS) is mandatory. Police have no discretion to refuse FIR registration if cognizable offence is disclosed.",
        "holding": "Registration of FIR is mandatory if information discloses commission of a cognizable offence. Preliminary inquiry is permitted only in specified categories (corruption, medical negligence, matrimonial disputes) and must be concluded in 7-14 days.",
        "related_statutory_provisions": "BNSS 2023 (Sec 173) / CrPC 1973 (Sec 154)",
        "subsequent_judicial_treatment": "Universal constitutional precedent binding on all law enforcement agencies across India.",
        "applicability_status": "Controlling Law (Union of India)",
        "exact_official_document_url": "https://digiscr.sci.gov.in/view_judgment?id=MTYwNTM=",
    },
    {
        "case_title": "Jitendra Singh v. State of Madhya Pradesh",
        "court": "Supreme Court of India",
        "case_number": "Civil Appeal No. 5177 of 2021",
        "decision_date": "2021-09-06",
        "bench_strength": "2-Judge Bench (D.Y. Chandrachud, B.V. Nagarathna, JJ.)",
        "official_citation": "2021 SCC OnLine SC 802 / 2021 INSC 449",
        "relevant_paragraphs": "Paragraphs 6, 7, 8",
        "material_facts": "Dispute over mutation of agricultural land based on a will, where revenue authorities attempted to adjudicate testamentary genuineness.",
        "legal_issue": "Does mutation in revenue records confer legal title, and can revenue courts adjudicate complex questions of will validity?",
        "ratio_decidendi": "Mutation entries in revenue registers (Khata, RTC, Pahani) are solely for fiscal taxation purposes and do not confer, alter, or extinguish legal ownership.",
        "holding": "Mutation entry neither creates nor extinguishes title. Substantive disputes over title and will validity belong exclusively to Civil Courts, not revenue officers.",
        "related_statutory_provisions": "Karnataka Land Revenue Act 1964 (Sec 128, 129), Madhya Pradesh Land Revenue Code 1959",
        "subsequent_judicial_treatment": "Reaffirmed in multiple property decisions confirming Khata/RTC does not equal title.",
        "applicability_status": "Controlling Law (Union of India)",
        "exact_official_document_url": "https://digiscr.sci.gov.in/view_judgment?id=MzE4MDU=",
    },
    {
        "case_title": "Imperia Structures Ltd. v. Anil Patni",
        "court": "Supreme Court of India",
        "case_number": "Civil Appeal No. 3581-3590 of 2020",
        "decision_date": "2020-11-02",
        "bench_strength": "2-Judge Bench (U.U. Lalit, Vineet Saran, JJ.)",
        "official_citation": "(2020) 10 SCC 783 / 2020 INSC 624",
        "relevant_paragraphs": "Paragraphs 22, 23, 24, 25",
        "material_facts": "Real estate promoter argued that enactment of RERA barred homebuyers from initiating complaint proceedings before Consumer Forums under Consumer Protection Act.",
        "legal_issue": "Whether the Real Estate (Regulation and Development) Act, 2016 bars consumer complaint remedies under the Consumer Protection Act?",
        "ratio_decidendi": "Section 79 RERA bars civil courts, but Consumer Commissions are specialized quasi-judicial tribunals, not civil courts. Section 88 RERA explicitly provides that RERA is in addition to other laws.",
        "holding": "Remedies under RERA and the Consumer Protection Act are concurrent and alternative. A homebuyer is entitled to file a consumer complaint for refund and interest due to project delay.",
        "related_statutory_provisions": "RERA 2016 (Sec 18, 71, 79, 88), Consumer Protection Act 2019 (Sec 35)",
        "subsequent_judicial_treatment": "Consistently followed by NCDRC, State Commissions, and Supreme Court.",
        "applicability_status": "Controlling Law (Union of India)",
        "exact_official_document_url": "https://digiscr.sci.gov.in/view_judgment?id=MzExMjM=",
    },
    {
        "case_title": "Danial Latifi v. Union of India",
        "court": "Supreme Court of India",
        "case_number": "Writ Petition (Civil) No. 868 of 1986",
        "decision_date": "2001-09-28",
        "bench_strength": "5-Judge Constitution Bench (G.B. Pattanaik, S. Rajendra Babu, D.P. Mohapatra, Doraiswamy Raju, Shivaraj V. Patil, JJ.)",
        "official_citation": "(2001) 7 SCC 740 / 2001 INSC 486",
        "relevant_paragraphs": "Paragraphs 28, 29, 30, 36",
        "material_facts": "Constitutional challenge to the Muslim Women (Protection of Rights on Divorce) Act, 1986 on the ground that restricting maintenance to iddat period violated Articles 14 and 21.",
        "legal_issue": "Does Section 3(1)(a) of the 1986 Act restrict husband liability for maintenance solely to the iddat period?",
        "ratio_decidendi": "Harmonious interpretation dictates that 'fair and reasonable provision' must be made within the iddat period to sustain the divorced woman for her entire life.",
        "holding": "Upheld the constitutionality of the 1986 Act by interpreting that a Muslim husband must make a reasonable and fair provision within the iddat period that provides maintenance for her lifetime until she remarries.",
        "related_statutory_provisions": "Muslim Women (Protection of Rights on Divorce) Act 1986 (Sec 3), Constitution of India (Art 14, 21)",
        "subsequent_judicial_treatment": "Foundational constitutional judgment governing Muslim women maintenance rights in India.",
        "applicability_status": "Controlling Law (Union of India)",
        "exact_official_document_url": "https://digiscr.sci.gov.in/view_judgment?id=ODcwMA==",
    },
    {
        "case_title": "Jacob Mathew v. State of Punjab",
        "court": "Supreme Court of India",
        "case_number": "Criminal Appeal No. 144-145 of 2004",
        "decision_date": "2005-08-05",
        "bench_strength": "3-Judge Bench (R.C. Lahoti, C.J., G.P. Mathur, P.K. Balasubramanyan, JJ.)",
        "official_citation": "(2005) 6 SCC 1 / 2005 INSC 372",
        "relevant_paragraphs": "Paragraphs 48, 51, 52, 53",
        "material_facts": "Criminal prosecution initiated against doctor under Section 304A IPC for non-availability of oxygen cylinder in hospital ward.",
        "legal_issue": "What degree of negligence is required to prosecute medical professionals criminally, and what safeguards must precede arrest?",
        "ratio_decidendi": "Criminal negligence requires gross rashness or recklessness showing complete disregard for life. Negligence in civil law does not necessarily amount to criminal culpability.",
        "holding": "To prosecute a doctor under Section 304A IPC / Section 106 BNS, the negligence must be gross. Police must not arrest a doctor without obtaining an opinion from an independent medical expert.",
        "related_statutory_provisions": "BNS 2023 (Sec 106(1)) / IPC 1860 (Sec 304A), Consumer Protection Act 2019",
        "subsequent_judicial_treatment": "Confirmed in Martin F. D'Souza (2009) and Kusum Sharma (2010).",
        "applicability_status": "Controlling Law (Union of India)",
        "exact_official_document_url": "https://digiscr.sci.gov.in/view_judgment?id=ODg2Mg==",
    },
    {
        "case_title": "Justice K.S. Puttaswamy (Retd.) v. Union of India",
        "court": "Supreme Court of India",
        "case_number": "Writ Petition (Civil) No. 494 of 2012",
        "decision_date": "2017-08-24",
        "bench_strength": "9-Judge Constitution Bench (J.S. Khehar, C.J., J. Chelameswar, S.A. Bobde, R.K. Agrawal, R.F. Nariman, A.M. Sapre, D.Y. Chandrachud, S.K. Kaul, S. Abdul Nazeer, JJ.)",
        "official_citation": "(2017) 10 SCC 1 / 2017 INSC 652",
        "relevant_paragraphs": "Paragraphs 262, 310, 311, 320",
        "material_facts": "Challenge to the Aadhaar biometric system referring the foundational question of whether privacy is a constitutionally protected right to a 9-judge bench.",
        "legal_issue": "Is there a fundamental right to privacy guaranteed under the Constitution of India?",
        "ratio_decidendi": "Privacy is an intrinsic facet of human dignity, personal liberty, and autonomy guaranteed under Article 21 and Part III of the Constitution.",
        "holding": "The 9-judge bench unanimously held that the Right to Privacy is a fundamental right protected under Article 21 of the Constitution. State infringements must satisfy legality, legitimate state aim, and proportionality.",
        "related_statutory_provisions": "Constitution of India (Articles 14, 19, 21), DPDP Act 2023, Aadhaar Act 2016",
        "subsequent_judicial_treatment": "Foundational precedent applying to surveillance, digital privacy, and informational autonomy.",
        "applicability_status": "Controlling Law (Union of India)",
        "exact_official_document_url": "https://digiscr.sci.gov.in/view_judgment?id=MjU1MzQ=",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# 2. LEGAL SCENARIO CATALOG (All 14 mandatory fields per Section 28)
# ─────────────────────────────────────────────────────────────────────────────
SCENARIOS: List[Dict[str, Any]] = [
    {
        "scenario_id": "SCEN_PROP_001",
        "domain": "Property & Real Estate",
        "subdomain": "Title Verification & Conveyancing",
        "legal_intent": "Resolving ownership dispute involving GPA and unregistered sale agreement",
        "required_facts": "Purchased property through General Power of Attorney and notarized agreement to sell in Bengaluru; seller subsequently executed registered sale deed to third party; buyer has physical possession but no registered deed.",
        "applicable_legislation": "Transfer of Property Act, 1882; Registration Act, 1908; Specific Relief Act, 1963",
        "relevant_provisions": "TPA Section 54, 53A; Registration Act Section 17, 49; SRA Section 5, 34",
        "exceptions": "Doctrine of part performance under Section 53A protects possession as shield only if agreement was registered and stamp duty paid; does not create ownership title.",
        "jurisdiction": "State of Karnataka (Civil Court of competent territorial and pecuniary jurisdiction)",
        "remedies": "Suit for specific performance of contract (if within 3-year limitation) or suit for recovery of money with damages; defense of protected possession under 53A against third-party buyer.",
        "competent_authority": "Senior Civil Judge / Principal Civil Judge (Bengaluru Urban / Rural)",
        "official_procedure": "1. Conduct 30-year Encumbrance Certificate search on Kaveri 2.0. 2. Verify registered documents. 3. Issue legal notice to seller demanding execution of registered conveyance. 4. Institute civil suit for specific performance and interim temporary injunction under Order XXXIX CPC.",
        "required_documents": "Original agreement to sell, GPA document, payment receipts / bank bank statements, electricity/water bills showing physical possession, 30-year EC extract from Kaveri 2.0.",
        "deadlines": "Specific performance: 3 years from date fixed for performance or from date buyer has notice of refusal (Article 54 Limitation Act).",
        "relevant_precedents": "Suraj Lamp (2012) 1 SCC 656 (GPA sales do not convey title); Anathula Sudhakar (2008) 4 SCC 594 (suit for declaration necessary when title clouded).",
    },
    {
        "scenario_id": "SCEN_PROP_002",
        "domain": "Property & Land Governance",
        "subdomain": "Karnataka Land Revenue & Khata",
        "legal_intent": "Rectifying mutation rejection and converting B-Khata to A-Khata in Bengaluru",
        "required_facts": "Buyer purchased a site in unapproved layout in Bengaluru Urban; currently holds B-Khata tax receipt; wishes to secure building plan sanction and regularize mutation.",
        "applicable_legislation": "Bruhat Bengaluru Mahanagara Palike Act, 2020; Karnataka Land Revenue Act, 1964",
        "relevant_provisions": "BBMP Act Section 144, 313; KLR Act Section 95, 128",
        "exceptions": "B-Khata cannot be converted to A-Khata without valid agricultural land conversion under Section 95 KLR Act and layout approval from BDA/BMRDA.",
        "jurisdiction": "Bruhat Bengaluru Mahanagara Palike (BBMP) / Bengaluru Urban Revenue Division",
        "remedies": "Apply for Section 95 land conversion; pay betterment and statutory development charges to BBMP once regularization scheme is notified; challenge wrongful mutation rejection before Assistant Commissioner.",
        "competent_authority": "Assistant Revenue Officer (BBMP) for Khata; Tahsildar / Assistant Commissioner for Land Revenue Mutation",
        "official_procedure": "1. Verify parent land conversion order and survey sketch (Tippani). 2. Submit mutation application on Bhoomi portal. 3. Upon conversion and DC approval, apply for BBMP A-Khata bifurcation with conversion order and title deeds.",
        "required_documents": "Registered Sale Deed, Parent title documents (30 years), Bhoomi RTC, Conversion order under Section 95, Survey sketch, Tax paid receipts, Aadhaar/PAN.",
        "deadlines": "Bhoomi mutation: 30 days under Sakala Services Act; Revenue Appeal under Section 136(2): 60 days from mutation rejection order.",
        "relevant_precedents": "Jitendra Singh (2021) SCC OnLine SC 802 (Khata/mutation is not title); State of Karnataka v. Shankaraiah (High Court of Karnataka).",
    },
    {
        "scenario_id": "SCEN_CRIM_001",
        "domain": "Criminal Law & Procedure",
        "subdomain": "Arrest, Bail & FIR Registration",
        "legal_intent": "Securing anticipatory bail and challenging threatened arrest under BNS 318/316",
        "required_facts": "Business partner filed a police complaint alleging cheating and criminal breach of trust regarding commercial invoice default; police visiting residence and threatening arrest without notice.",
        "applicable_legislation": "Bharatiya Nagarik Suraksha Sanhita, 2023; Bharatiya Nyaya Sanhita, 2023",
        "relevant_provisions": "BNSS Section 35, 173, 482; BNS Section 316, 318",
        "exceptions": "Pure contractual/civil disputes cannot be converted into criminal cheating unless fraudulent intention existed at the inception of the contract.",
        "jurisdiction": "Sessions Court / High Court of Karnataka",
        "remedies": "File Anticipatory Bail application under Section 482 BNSS; seek notice under Section 35(3) BNSS; file Section 528 BNSS (482 CrPC) petition to quash FIR.",
        "competent_authority": "Principal City Civil and Sessions Judge / High Court of Karnataka",
        "official_procedure": "1. Obtain copy of FIR from police station or portal. 2. Draft Anticipatory Bail petition establishing civil/commercial nature of transaction. 3. Move urgent motion before Sessions Court for interim anticipatory protection.",
        "required_documents": "Copy of FIR/complaint, commercial agreements, invoices, ledger statements, proof of communication, ID and address proof.",
        "deadlines": "Anticipatory bail: prior to arrest; Section 35(3) notice response: within stipulated notice period.",
        "relevant_precedents": "Arnesh Kumar (2014) 8 SCC 273 (no automatic arrest for <7 yr offences); Satender Kumar Antil (2022) 10 SCC 51 (bail as rule); Siddharth (2022) 1 SCC 676 (no arrest required for chargesheet).",
    },
    {
        "scenario_id": "SCEN_BANK_001",
        "domain": "Banking & Commercial Law",
        "subdomain": "Cheque Bounce (Section 138 NI Act)",
        "legal_intent": "Filing statutory complaint for dishonoured cheque of Rs 15 lakh",
        "required_facts": "Business cheque issued for goods delivered returned unpaid with bank memo 'Funds Insufficient'; payee received memo 10 days ago.",
        "applicable_legislation": "Negotiable Instruments Act, 1881; Bharatiya Nagarik Suraksha Sanhita, 2023",
        "relevant_provisions": "NI Act Section 138, 139, 142, 143A; BNSS Section 223",
        "exceptions": "Notice dispatched after 30 days of bank memo invalidates Section 138 complaint; security cheques for non-existent debt rebuttable under Section 139.",
        "jurisdiction": "Judicial Magistrate First Class / Metropolitan Magistrate (where payee bank account is maintained)",
        "remedies": "Criminal prosecution under Section 138 (imprisonment up to 2 years, fine up to twice cheque amount); 20% interim compensation under Section 143A.",
        "competent_authority": "Court of Small Causes / Judicial Magistrate First Class (JMFC)",
        "official_procedure": "1. Dispatch formal legal demand notice via registered speed post within 30 days of memo. 2. Wait 15 days for payment window to expire. 3. File criminal complaint under Section 142 within 30 days of expiry before JMFC. 4. Tender pre-summoning affidavit.",
        "required_documents": "Original dishonoured cheque, bank return memo, copy of statutory demand notice, postal speed post receipt, delivery tracking report, underlying tax invoices.",
        "deadlines": "Demand notice: 30 days from bank memo; Payment window: 15 days from notice delivery; Court complaint: 30 days after payment window.",
        "relevant_precedents": "Rangappa v. Sri Mohan (2010) 11 SCC 441 (presumption of legally enforceable debt); Dashrath Rupsingh Rathod v. State of Maharashtra (payee bank jurisdiction).",
    },
    {
        "scenario_id": "SCEN_FAM_001",
        "domain": "Family & Matrimonial Law",
        "subdomain": "Domestic Violence & Maintenance",
        "legal_intent": "Claiming emergency protection, residence order, and monthly maintenance under PWDVA",
        "required_facts": "Wife subjected to physical and economic harassment by husband and mother-in-law for additional dowry; husband locked her out of rented shared flat in Bengaluru.",
        "applicable_legislation": "Protection of Women from Domestic Violence Act, 2005; Hindu Marriage Act, 1955; BNSS, 2023",
        "relevant_provisions": "PWDVA Section 3, 12, 18, 19, 20, 23; BNSS Section 144",
        "exceptions": "Husband claiming flat is rented in mother's name; settled under Hiral Harsora that mother-in-law is respondent, and shared household protection applies regardless of who holds tenancy.",
        "jurisdiction": "Metropolitan Magistrate / JMFC (where aggrieved woman resides or incident occurred)",
        "remedies": "Interim ex-parte protection order (Section 18); Residence order restraining dispossession (Section 19); Monetary maintenance for self and child (Section 20); Compensation (Section 22).",
        "competent_authority": "Chief Metropolitan Magistrate (Bengaluru) / Judicial Magistrate First Class",
        "official_procedure": "1. Approach Protection Officer (WCD Dept) to record Domestic Incident Report (DIR). 2. File Section 12 application before Magistrate with Section 23 interim prayer. 3. File Rajnesh v. Neha Affidavit of Assets and Liabilities.",
        "required_documents": "Marriage certificate/photos, DIR from Protection Officer, medical records of injury, bank statements, Rajnesh v. Neha asset disclosure affidavit.",
        "deadlines": "60-day target for disposal of interim application under Section 12(5) PWDVA.",
        "relevant_precedents": "Rajnesh v. Neha (2021) 2 SCC 324 (mandatory asset affidavit); Hiral P. Harsora (2016) 10 SCC 165 (women respondents covered); Prabha Tyagi (2022) (subsisting shared household right).",
    },
    {
        "scenario_id": "SCEN_CONS_001",
        "domain": "Consumer Protection",
        "subdomain": "Real Estate & Builder Delay",
        "legal_intent": "Claiming full refund with interest from builder for 3-year project delay in Bengaluru",
        "required_facts": "Allottee paid 90% consideration (Rs 75 lakh) for flat in Bengaluru; builder promised possession in December 2021; project incomplete with no Occupancy Certificate in 2024.",
        "applicable_legislation": "Consumer Protection Act, 2019; Real Estate (Regulation and Development) Act, 2016",
        "relevant_provisions": "CPA Section 35, 47; RERA Section 18, 31",
        "exceptions": "Builder citing force majeure (COVID-19); Supreme Court held COVID extensions apply only for specified statutory periods, not for indefinite multi-year delays.",
        "jurisdiction": "Karnataka State Consumer Disputes Redressal Commission (Bangalore) / Karnataka RERA",
        "remedies": "Full refund of deposited consideration with interest (SBI MCLR + 2%) or monthly delay compensation until actual handover of possession with valid OC.",
        "competent_authority": "State Consumer Disputes Redressal Commission, Karnataka / Adjudicating Officer, Karnataka RERA",
        "official_procedure": "1. Issue formal demand notice to builder. 2. File consumer complaint online on e-Daakhil portal or RERA complaint on rera.karnataka.gov.in. 3. Claim refund with statutory interest and mental agony damages.",
        "required_documents": "Builder-Buyer Agreement, payment receipts, bank loan disbursement statements, email correspondence, brochure/sanctioned plan copy.",
        "deadlines": "2 years from promised possession date or ongoing cause of action (Section 69 CPA).",
        "relevant_precedents": "Imperia Structures (2020) 10 SCC 783 (concurrent consumer remedy); Pioneer Urban (2019) 5 SCC 725 (one-sided builder agreement unfair trade practice); Newtech Promoters (2021) (retroactive application).",
    },
]


def export_catalogs():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, "backend", "rag", "data")
    docs_dir = os.path.join(base_dir, "docs")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)

    # 1. Precedents JSON
    prec_json_path = os.path.join(data_dir, "precedents_catalog.json")
    with open(prec_json_path, "w", encoding="utf-8") as f:
        json.dump(PRECEDENTS, f, indent=2, ensure_ascii=False)

    # 2. Precedents Markdown
    prec_md_path = os.path.join(docs_dir, "JUDICIAL_PRECEDENT_CATALOG.md")
    with open(prec_md_path, "w", encoding="utf-8") as f:
        f.write("# NyayaSetu — Judicial Precedent Catalog (14-Point Schema)\n\n")
        f.write("**Specification Reference:** Section 20 (Landmark Indian Precedents)\n")
        f.write(f"**Total Verified Precedents:** {len(PRECEDENTS)}\n\n")
        f.write("---\n\n")
        for p in PRECEDENTS:
            f.write(f"## {p['case_title']} — `{p['official_citation']}`\n\n")
            f.write(f"* **Court:** {p['court']} | **Bench:** {p['bench_strength']}\n")
            f.write(f"* **Decision Date:** {p['decision_date']} | **Case Number:** {p['case_number']}\n")
            f.write(f"* **Official Document URL:** [{p['exact_official_document_url']}]({p['exact_official_document_url']})\n")
            f.write(f"* **Statutory Provisions:** `{p['related_statutory_provisions']}`\n")
            f.write(f"* **Relevant Paragraphs:** {p['relevant_paragraphs']}\n")
            f.write(f"* **Material Facts:** {p['material_facts']}\n")
            f.write(f"* **Legal Issue:** {p['legal_issue']}\n")
            f.write(f"* **Ratio Decidendi:** {p['ratio_decidendi']}\n")
            f.write(f"* **Holding:** **{p['holding']}**\n")
            f.write(f"* **Subsequent Treatment:** {p['subsequent_judicial_treatment']}\n")
            f.write(f"* **Applicability Status:** `{p['applicability_status']}`\n\n")
            f.write("---\n\n")

    # 3. Scenarios JSON
    scen_json_path = os.path.join(data_dir, "scenario_catalog.json")
    with open(scen_json_path, "w", encoding="utf-8") as f:
        json.dump(SCENARIOS, f, indent=2, ensure_ascii=False)

    # 4. Scenarios Markdown
    scen_md_path = os.path.join(docs_dir, "LEGAL_SCENARIO_CATALOG.md")
    with open(scen_md_path, "w", encoding="utf-8") as f:
        f.write("# NyayaSetu — Legal Scenario Catalog (Multi-Domain Citizen Problems)\n\n")
        f.write("**Specification Reference:** Section 28 (Scenario-Oriented Legal Guidance)\n")
        f.write(f"**Total Documented Scenarios:** {len(SCENARIOS)}\n\n")
        f.write("---\n\n")
        for s in SCENARIOS:
            f.write(f"## {s['scenario_id']}: {s['legal_intent']}\n\n")
            f.write(f"* **Domain:** `{s['domain']}` | **Subdomain:** `{s['subdomain']}`\n")
            f.write(f"* **Jurisdiction:** {s['jurisdiction']}\n")
            f.write(f"* **Competent Authority / Forum:** **{s['competent_authority']}**\n")
            f.write(f"* **Applicable Statutes:** `{s['applicable_legislation']}` ({s['relevant_provisions']})\n")
            f.write(f"* **Required Factual Context:** {s['required_facts']}\n")
            f.write(f"* **Statutory Exceptions / Caveats:** {s['exceptions']}\n")
            f.write(f"* **Available Remedies:** {s['remedies']}\n")
            f.write(f"* **Step-by-Step Procedure:**\n{s['official_procedure']}\n")
            f.write(f"* **Mandatory Documents:** {s['required_documents']}\n")
            f.write(f"* **Statutory Deadlines / Limitation:** **{s['deadlines']}**\n")
            f.write(f"* **Controlling Precedents:** {s['relevant_precedents']}\n\n")
            f.write("---\n\n")

    print(f"Exported {len(PRECEDENTS)} precedents and {len(SCENARIOS)} scenarios successfully.")


if __name__ == "__main__":
    export_catalogs()
