"""Supplementary authoritative sources across all specialized and multi-state Indian legal domains.
Supplements build_expanded_registry.py with full statutory fidelity.
"""

from typing import List, Dict, Any


def get_supplementary_sources(create_source_fn) -> List[Dict[str, Any]]:
    cs = create_source_fn
    sources: List[Dict[str, Any]] = []

    # =========================================================================
    # 1. SPECIALIZED FAMILY, GUARDIANSHIP & SUCCESSION
    # =========================================================================
    sources.append(cs(
        source_id="SRC_CARA_RULES_001",
        title="Adoption Regulations, 2022 (CARA Regulations under JJ Act)",
        source_type="REGULATIONS",
        tier="Tier 2",
        authority="Central Adoption Resource Authority (CARA) / MWCD",
        official_url="https://cara.wcd.gov.in/",
        exact_document_url="https://cara.wcd.gov.in/PDF/Adoption%20Regulations%202022.pdf",
        jurisdiction="Union of India",
        published_date="2022-09-23",
        effective_date="2022-09-23",
        legal_domains="Family Law; Child Adoption; CARA Guidelines",
        legal_intents="Prospective Adoptive Parents (PAPs) eligibility; Home Study Report (HSR); District Magistrate adoption order under 2021 JJ Amendment; Relative and step-parent adoption procedures",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_PCMA_001",
        title="Prohibition of Child Marriage Act, 2006",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Women and Child Development",
        official_url="https://www.indiacode.nic.in/handle/123456789/2054",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/2054/1/A2007-06.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 6 of 2007",
        act_year="2006",
        legal_domains="Family Law; Child Protection; Marriage Validity",
        legal_intents="Child marriage voidable at option of contracting party who was child (Section 3 - petition within 2 years of attaining majority); Maintenance and residence of female contracting party; Independent Thought Supreme Court ruling (marital rape exception struck down for minors)",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_FMA_001",
        title="Foreign Marriage Act, 1969",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of External Affairs / Ministry of Law and Justice",
        official_url="https://www.indiacode.nic.in/handle/123456789/1567",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/1567/1/A1969-33.pdf",
        jurisdiction="Union of India / Overseas Missions",
        act_number="Act No. 33 of 1969",
        act_year="1969",
        legal_domains="Family Law; International Marriage; NRI Law",
        legal_intents="Solemnization of marriage between citizens of India outside India before Marriage Officer at Indian Diplomatic Mission; Notice of intended marriage; Registration of foreign marriages",
        commencement_status="COMMENCED",
        indexed_chunk_count=3,
    ))

    sources.append(cs(
        source_id="SRC_ANAND_001",
        title="Anand Marriage Act, 1909 (Amended 2012)",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Law and Justice",
        official_url="https://www.indiacode.nic.in/handle/123456789/2311",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/2311/1/A1909-07.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 7 of 1909",
        act_year="1909",
        legal_domains="Family Law; Sikh Marriage; Marriage Registration",
        legal_intents="Validity of Anand Karaj marriage ceremony between Sikhs; Registration of Anand marriages under 2012 Amendment",
        commencement_status="COMMENCED",
        indexed_chunk_count=3,
    ))

    sources.append(cs(
        source_id="SRC_KAR_CONVERSION_001",
        title="Karnataka Protection of Right to Freedom of Religion Act, 2022 (Act No. 25 of 2022)",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Department of Parliamentary Affairs, Karnataka",
        official_url="https://dpal.karnataka.gov.in/",
        exact_document_url="https://dpal.karnataka.gov.in/storage/pdf-files/Acts/25%20of%202022%20(E).pdf",
        jurisdiction="State of Karnataka",
        state="Karnataka",
        act_number="Act No. 25 of 2022",
        act_year="2022",
        legal_domains="Constitutional Law; Religious Freedom; Marriage; Criminal Law",
        legal_intents="Prohibition of unlawful conversion by misrepresentation, force, undue influence, coercion, allurement or marriage; Declaration before District Magistrate 30 days prior; Burden of proof on person who converted; Marriages for sole purpose of unlawful conversion declared void",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    # =========================================================================
    # 2. KARNATAKA LAND & MUNICIPAL GOVERNANCE EXPANSIONS
    # =========================================================================
    sources.append(cs(
        source_id="SRC_KAR_KLRR_001",
        title="Karnataka Land Revenue Rules, 1966",
        source_type="STATE_RULES",
        tier="Tier 2",
        authority="Revenue Department, Government of Karnataka",
        official_url="https://revenue.karnataka.gov.in/",
        exact_document_url="https://revenue.karnataka.gov.in/storage/pdf-files/KLR%20Rules%201966.pdf",
        jurisdiction="State of Karnataka",
        state="Karnataka",
        published_date="1966-03-15",
        effective_date="1966-03-15",
        legal_domains="Land Revenue; Revenue Records; Mutation; Form 12; Form 16",
        legal_intents="Detailed procedure for mutation entry (Rule 42-45); Publication of notice (Form 21); Disputed case register (Form 12); Phodi and durasti survey procedure; Durasti sketch preparation; Boundary demarcation",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    sources.append(cs(
        source_id="SRC_KAR_KHB_001",
        title="Karnataka Housing Board Act, 1962 (Act No. 10 of 1963)",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Housing Department, Government of Karnataka",
        official_url="https://khb.karnataka.gov.in/",
        exact_document_url="https://dpal.karnataka.gov.in/storage/pdf-files/Acts/10%20of%201963%20(E).pdf",
        jurisdiction="State of Karnataka",
        state="Karnataka",
        act_number="Act No. 10 of 1963",
        act_year="1962",
        legal_domains="Housing; Allotment; Eviction; Real Estate",
        legal_intents="KHB residential site and house allotment; Lease-cum-sale agreements; Transfer of ownership on completion of lease period; Eviction from unauthorized occupation (Section 45)",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_KAR_KIADB_001",
        title="Karnataka Industrial Areas Development Act, 1966 (Act No. 18 of 1966)",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Commerce and Industries Department, Government of Karnataka",
        official_url="https://kiadb.karnataka.gov.in/",
        exact_document_url="https://dpal.karnataka.gov.in/storage/pdf-files/Acts/18%20of%201966%20(E).pdf",
        jurisdiction="State of Karnataka",
        state="Karnataka",
        act_number="Act No. 18 of 1966",
        act_year="1966",
        legal_domains="Industrial Development; Land Acquisition; Compensation",
        legal_intents="Declaration of industrial area (Section 3); Compulsory land acquisition (Section 28); Notice to landowners and inquiry (Section 28(2)-(3)); Final declaration (Section 28(4)); Determination of compensation (Section 29/30)",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    sources.append(cs(
        source_id="SRC_KAR_GRAM_001",
        title="Karnataka Gram Swaraj and Panchayat Raj Act, 1993 (Act No. 14 of 1993)",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Rural Development and Panchayat Raj Department, Karnataka",
        official_url="https://rdpr.karnataka.gov.in/",
        exact_document_url="https://dpal.karnataka.gov.in/storage/pdf-files/Acts/14%20of%201993%20(E).pdf",
        jurisdiction="State of Karnataka",
        state="Karnataka",
        act_number="Act No. 14 of 1993",
        act_year="1993",
        legal_domains="Panchayat Governance; Rural Property; e-Swathu; Form 9 & 11",
        legal_intents="Gram Panchayat property tax assessment (Section 199); e-Swathu portal mandatory Form 9 and Form 11 extracts; Regulation of building construction in rural areas (Section 64); Water and sanitation regulation",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    sources.append(cs(
        source_id="SRC_KAR_MUNICIPAL_001",
        title="Karnataka Municipalities Act, 1964 (Act No. 22 of 1964)",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Urban Development Department, Karnataka",
        official_url="https://dpal.karnataka.gov.in/",
        exact_document_url="https://dpal.karnataka.gov.in/storage/pdf-files/Acts/22%20of%201964%20(E).pdf",
        jurisdiction="State of Karnataka",
        state="Karnataka",
        act_number="Act No. 22 of 1964",
        act_year="1964",
        legal_domains="Municipal Law; Town Municipal Councils; Building Sanctions; Property Tax",
        legal_intents="Town Municipal Council (TMC) and City Municipal Council (CMC) powers; Property tax assessment; Building plan license; Encroachment removal; Trade licenses",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_WAQF_001",
        title="Waqf Act, 1995 (Amended 2013)",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Minority Affairs",
        official_url="https://www.indiacode.nic.in/handle/123456789/1974",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/1974/1/A1995-43.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 43 of 1995",
        act_year="1995",
        legal_domains="Property Law; Waqf Property; Religious Endowments",
        legal_intents="Survey of Waqf properties (Section 4); Central Waqf Council and State Waqf Boards; Powers to alienate Waqf property (Section 51 - restrictions); Waqf Tribunal jurisdiction (Section 83/85 - bar on civil court jurisdiction); Karnataka Board of Wakf v GoI precedent",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    sources.append(cs(
        source_id="SRC_FEMA_PROP_001",
        title="FEMA (Acquisition and Transfer of Immovable Property in India) Regulations, 2018",
        source_type="REGULATIONS",
        tier="Tier 2",
        authority="Reserve Bank of India / Ministry of Finance",
        official_url="https://www.rbi.org.in/",
        exact_document_url="https://rbidocs.rbi.org.in/rdocs/notification/PDFs/552R16012018590CD3BC0DAF47018B6327E7DF917E9A.PDF",
        jurisdiction="Union of India / Cross-Border",
        published_date="2018-01-16",
        effective_date="2018-01-16",
        legal_domains="Property Law; FEMA; NRI / OCI Property; Foreign Investment",
        legal_intents="Acquisition of residential/commercial immovable property by NRI or OCI; Prohibition on NRI/OCI purchasing agricultural land, farm house or plantation property; Repatriation of sale proceeds up to USD 1 million per financial year via NRO account",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    # =========================================================================
    # 3. SPECIAL CRIMINAL STATUTES & VICTIM RIGHTS
    # =========================================================================
    sources.append(cs(
        source_id="SRC_ARMS_001",
        title="Arms Act, 1959 (Amended 2019)",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Home Affairs",
        official_url="https://www.indiacode.nic.in/handle/123456789/1572",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/1572/1/A1959-54.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 54 of 1959",
        act_year="1959",
        legal_domains="Criminal Law; Arms & Weapons; Licencing",
        legal_intents="Acquisition and possession of firearms; Firearm licence requirement (Section 3); Restriction on number of firearms (maximum 2 firearms per licence); Penalties for illegal possession (Section 25); Celebratory gunfire prohibition",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_UAPA_001",
        title="Unlawful Activities (Prevention) Act, 1967 (UAPA)",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Home Affairs",
        official_url="https://www.indiacode.nic.in/handle/123456789/1564",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/1564/1/A1967-37.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 37 of 1967",
        act_year="1967",
        legal_domains="Criminal Law; National Security; Terrorism; Special Offences",
        legal_intents="Unlawful activity defined (Section 2(o)); Terrorist act defined (Section 15); Section 43D(5) stringent bar on bail if prima facie case exists; Designation of individuals as terrorists; NIA investigation",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    sources.append(cs(
        source_id="SRC_ITPA_001",
        title="Immoral Traffic (Prevention) Act, 1956",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Women and Child Development",
        official_url="https://www.indiacode.nic.in/handle/123456789/1557",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/1557/1/A1956-104.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 104 of 1956",
        act_year="1956",
        legal_domains="Criminal Law; Trafficking; Human Rights; Women Protection",
        legal_intents="Offences of brothel keeping, pimping, trafficking; Distinction between voluntary sex work and exploitation; Rescue and rehabilitation under protective homes; Budhadev Karmaskar Supreme Court directions",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_VICTIM_COMP_001",
        title="Victim Compensation Scheme (BNSS Section 396 / CrPC Section 357A)",
        source_type="STATUTORY_SCHEME",
        tier="Tier 2",
        authority="Ministry of Home Affairs / NALSA / State Legal Services Authorities",
        official_url="https://nalsa.gov.in/",
        exact_document_url="https://nalsa.gov.in/acts-rules/schemes/nalsa-s-compensation-scheme-for-women-victims-survivors-of-sexual-assault-other-crimes-2018",
        jurisdiction="Union of India / State Legal Services",
        published_date="2018-10-02",
        effective_date="2018-10-02",
        legal_domains="Criminal Procedure; Victim Rights; Compensation; Legal Aid",
        legal_intents="Statutory victim compensation under Section 396 BNSS (357A CrPC); Application to DLSA/SLSA; Interim compensation for rape, acid attack, grievously injured victims; Relief irrespective of whether offender identified or convicted",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    # =========================================================================
    # 4. BANKING, FINANCE & MONEY LENDING
    # =========================================================================
    sources.append(cs(
        source_id="SRC_BRA_1949",
        title="Banking Regulation Act, 1949",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Reserve Bank of India / Ministry of Finance",
        official_url="https://www.indiacode.nic.in/handle/123456789/2281",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/2281/1/A1949-10.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 10 of 1949",
        act_year="1949",
        legal_domains="Banking; Financial Regulation; Public Depositors",
        legal_intents="Licensing of banking companies (Section 22); RBI power to issue binding directions (Section 35A); RBI intervention in stressed assets and insolvency resolution (Section 35AA/35AB)",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_PSS_2007",
        title="Payment and Settlement Systems Act, 2007",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Reserve Bank of India",
        official_url="https://www.indiacode.nic.in/handle/123456789/2056",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/2056/1/A2007-51.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 51 of 2007",
        act_year="2007",
        legal_domains="Fintech; Digital Payments; UPI; Settlement Systems",
        legal_intents="Regulation of payment systems (UPI, NEFT, RTGS, Card networks, wallets); Section 25 dishonour of electronic fund transfer (criminal liability equivalent to Section 138 NI Act); Settlement finality",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_BUDS_2019",
        title="Banning of Unregulated Deposit Schemes Act, 2019 (BUDS Act)",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Finance / Department of Financial Services",
        official_url="https://www.indiacode.nic.in/handle/123456789/15174",
        exact_document_url="https://egazette.gov.in/WriteReadData/2019/209680.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 21 of 2019",
        act_year="2019",
        legal_domains="Banking; Ponzi Schemes; Consumer Protection; Economic Offences",
        legal_intents="Complete ban on unregulated deposit schemes (Section 3); Attachment of properties of deposit taker (Section 7); Designated Court for restitution to depositors; Severe criminal penalties for fraudulent defaults",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_KAR_MONEY_001",
        title="Karnataka Money Lenders Act, 1961 (Act No. 12 of 1962)",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Department of Cooperation, Government of Karnataka",
        official_url="https://dpal.karnataka.gov.in/",
        exact_document_url="https://dpal.karnataka.gov.in/storage/pdf-files/Acts/12%20of%201962%20(E).pdf",
        jurisdiction="State of Karnataka",
        state="Karnataka",
        act_number="Act No. 12 of 1962",
        act_year="1961",
        legal_domains="Money Lending; Loans; Usury; Harassment",
        legal_intents="Mandatory licensing of money lenders (Section 5); Maximum interest rate prescribed by State; Duty to maintain books of accounts and deliver receipts; Bar on suits by unlicensed money lenders (Section 11)",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_KAR_EXORBITANT_001",
        title="Karnataka Prohibition of Charging Exorbitant Interest Act, 2004 (Act No. 14 of 2004)",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Department of Law and Parliamentary Affairs, Karnataka",
        official_url="https://dpal.karnataka.gov.in/",
        exact_document_url="https://dpal.karnataka.gov.in/storage/pdf-files/Acts/14%20of%202004%20(E).pdf",
        jurisdiction="State of Karnataka",
        state="Karnataka",
        act_number="Act No. 14 of 2004",
        act_year="2004",
        legal_domains="Loans; Private Financing; Exorbitant Interest; Harassment",
        legal_intents="Prohibition of charging exorbitant interest (daily interest, meter vaddi, kandu vaddi); Penalty up to 3 years imprisonment (Section 4); Petition before Court to deposit loan amount and stop harassment (Section 5); Restoration of seized property",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_SEBI_1992",
        title="Securities and Exchange Board of India Act, 1992",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Securities and Exchange Board of India (SEBI)",
        official_url="https://www.sebi.gov.in/",
        exact_document_url="https://www.sebi.gov.in/sebi_data/attachdocs/1456380272563.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 15 of 1992",
        act_year="1992",
        legal_domains="Securities Law; Capital Markets; Investor Protection",
        legal_intents="Protection of investors in securities; Regulation of stock brokers, mutual funds, listed companies; SCORES online grievance redressal; Prohibition of insider trading and fraudulent trade practices (Section 12A); Securities Appellate Tribunal (SAT) appeals",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_IRDAI_1999",
        title="Insurance Regulatory and Development Authority Act, 1999",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Insurance Regulatory and Development Authority of India (IRDAI)",
        official_url="https://irdai.gov.in/",
        exact_document_url="https://irdai.gov.in/documents/37343/366308/IRDA_ACT_1999.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 41 of 1999",
        act_year="1999",
        legal_domains="Insurance; Policyholder Protection; Grievance Redressal",
        legal_intents="Regulation of life and general insurance companies; Policyholder protection regulations; Insurance Ombudsman Rules 2017 (dispute adjudication up to Rs 50 lakh without court fees); Bima Bharosa online portal",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    # =========================================================================
    # 5. HEALTHCARE, MENTAL HEALTH & PATIENT RIGHTS
    # =========================================================================
    sources.append(cs(
        source_id="SRC_MHA_2017",
        title="Mental Healthcare Act, 2017",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Health and Family Welfare",
        official_url="https://www.indiacode.nic.in/handle/123456789/2247",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/2247/1/A2017-10.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 10 of 2017",
        act_year="2017",
        legal_domains="Healthcare; Mental Health; Human Rights",
        legal_intents="Right to access mental healthcare (Section 18); Advance Directive (Section 5); Nominated Representative (Section 14); Mental Health Review Board; Decriminalization of attempt to commit suicide (Section 115 presumption of severe stress); Ban on electroconvulsive therapy without anesthesia",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    sources.append(cs(
        source_id="SRC_MTP_1971",
        title="Medical Termination of Pregnancy Act, 1971 (Amended 2021)",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Health and Family Welfare",
        official_url="https://www.indiacode.nic.in/handle/123456789/1573",
        exact_document_url="https://egazette.gov.in/WriteReadData/2021/226130.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 34 of 1971 / Act No. 8 of 2021",
        act_year="1971",
        legal_domains="Healthcare; Reproductive Rights; Abortion Law",
        legal_intents="Termination of pregnancy up to 20 weeks on opinion of one RMP; Up to 24 weeks for special categories (survivors of sexual assault, minors, fetal abnormalities) on opinion of two RMPs; Medical Board beyond 24 weeks; Protection of privacy of woman (Section 5A)",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_DCA_1940",
        title="Drugs and Cosmetics Act, 1940",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Central Drugs Standard Control Organisation (CDSCO) / MoHFW",
        official_url="https://www.indiacode.nic.in/handle/123456789/2264",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/2264/1/A1940-23.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 23 of 1940",
        act_year="1940",
        legal_domains="Healthcare; Pharmaceuticals; Adulterated Drugs; Consumer Safety",
        legal_intents="Manufacture, sale and distribution of drugs; Spurious and adulterated drugs penalties (Section 27); Licensing of pharmacies; Government Analyst test report",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    # =========================================================================
    # 6. EDUCATION, STUDENT RIGHTS & CONSUMER STANDARDS
    # =========================================================================
    sources.append(cs(
        source_id="SRC_KAR_EDU_1983",
        title="Karnataka Education Act, 1983 (Act No. 1 of 1995)",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Department of School Education and Literacy, Karnataka",
        official_url="https://dpal.karnataka.gov.in/",
        exact_document_url="https://dpal.karnataka.gov.in/storage/pdf-files/Acts/01%20of%201995%20(E).pdf",
        jurisdiction="State of Karnataka",
        state="Karnataka",
        act_number="Act No. 1 of 1995",
        act_year="1983",
        legal_domains="Education Law; School Regulation; Fees; Withholding Certificates",
        legal_intents="Regulation of private educational institutions in Karnataka; Prohibition of capitation fees; Illegal withholding of marks cards and transfer certificates (TC) prohibited; District Education Regulating Authority",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_UGC_RAGGING_001",
        title="UGC Regulations on Curbing the Menace of Ragging in Higher Educational Institutions, 2009",
        source_type="REGULATIONS",
        tier="Tier 2",
        authority="University Grants Commission (UGC)",
        official_url="https://www.ugc.gov.in/",
        exact_document_url="https://www.ugc.gov.in/oldpdf/ragging/gazzetaug2010.pdf",
        jurisdiction="Union of India",
        published_date="2009-06-17",
        effective_date="2009-06-17",
        legal_domains="Education Law; Anti-Ragging; Student Protection; Human Rights",
        legal_intents="Definition of ragging; Mandatory Anti-Ragging Committee and Squad; 24x7 Anti-Ragging Toll-free Helpline (1800-180-5522); Mandatory FIR by college head within 24 hours of complaint; Rustication and expulsion penalties",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_LM_2009",
        title="Legal Metrology Act, 2009 & Packaged Commodities Rules, 2011",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Consumer Affairs, Food and Public Distribution",
        official_url="https://www.indiacode.nic.in/handle/123456789/2085",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/2085/1/A2010-01.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 1 of 2010",
        act_year="2009",
        legal_domains="Consumer Protection; Weights and Measures; MRP Overcharging",
        legal_intents="Mandatory packaged commodity declarations: MRP, Net Quantity, Expiry, Manufacturer address, Consumer Care; Prohibition on charging above MRP (dual pricing ban); Penalties for tampering with MRP",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_FSSAI_2006",
        title="Food Safety and Standards Act, 2006",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Food Safety and Standards Authority of India (FSSAI) / MoHFW",
        official_url="https://www.indiacode.nic.in/handle/123456789/2049",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/2049/1/A2006-34.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 34 of 2006",
        act_year="2006",
        legal_domains="Consumer Protection; Food Safety; Adulteration; Public Health",
        legal_intents="FSSAI licensing and registration; Unsafe food and adulteration liabilities (Section 59); Misbranding and misleading advertisements (Section 53); Compensation in case of injury or death (Section 65)",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    # =========================================================================
    # 7. MULTI-STATE NATIONWIDE EXPANSION (MAHARASHTRA, DELHI, TAMIL NADU, UP, WB)
    # =========================================================================
    sources.append(cs(
        source_id="SRC_MH_RENT_001",
        title="Maharashtra Rent Control Act, 1999 (Act No. 18 of 2000)",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Government of Maharashtra",
        official_url="https://bombayhighcourt.nic.in/",
        exact_document_url="https://bombayhighcourt.nic.in/libweb/acts/2000.18.pdf",
        jurisdiction="State of Maharashtra",
        state="Maharashtra",
        act_number="Act No. 18 of 2000",
        act_year="1999",
        legal_domains="Tenancy; Rent Control; Eviction; Leave and License",
        legal_intents="Mandatory registration of leave and license agreements (Section 55 - responsibility of landlord); Summary eviction of licensee on expiry of license before Competent Authority (Section 24); Standard rent",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    sources.append(cs(
        source_id="SRC_DELHI_RENT_001",
        title="Delhi Rent Control Act, 1958",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Government of NCT of Delhi / Ministry of Home Affairs",
        official_url="https://www.indiacode.nic.in/handle/123456789/1575",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/1575/1/A1958-59.pdf",
        jurisdiction="NCT of Delhi",
        state="Delhi",
        act_number="Act No. 59 of 1958",
        act_year="1958",
        legal_domains="Tenancy; Rent Control; Eviction; Rent Controller",
        legal_intents="Premises with monthly rent up to Rs 3,500 protected under Act; Section 14 eviction grounds (bona fide requirement under 14(1)(e)); Rent Controller jurisdiction; Above Rs 3,500 rent governed by Transfer of Property Act",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_TN_TENANCY_001",
        title="Tamil Nadu Regulation of Rights and Responsibilities of Landlords and Tenants Act, 2017",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Housing and Urban Development Department, Tamil Nadu",
        official_url="https://www.tn.gov.in/",
        exact_document_url="https://www.tenancy.tn.gov.in/Documents/Act_English.pdf",
        jurisdiction="State of Tamil Nadu",
        state="Tamil Nadu",
        act_number="Act No. 42 of 2017",
        act_year="2017",
        legal_domains="Tenancy; Tenancy Registration; Eviction",
        legal_intents="Mandatory registration of tenancy agreement with Rent Authority portal within 90 days; Security deposit cap (3 months rent for residential); Eviction petition before Rent Court",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_MH_STAMP_001",
        title="Maharashtra Stamp Act, 1958",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Revenue and Forest Department, Maharashtra",
        official_url="https://igrmaharashtra.gov.in/",
        exact_document_url="https://bombayhighcourt.nic.in/libweb/acts/1958.60.pdf",
        jurisdiction="State of Maharashtra",
        state="Maharashtra",
        act_number="Act No. 60 of 1958",
        act_year="1958",
        legal_domains="Property Law; Stamp Duty; Conveyancing; Registration",
        legal_intents="Stamp duty on conveyances, agreements to sell, gifts, mortgages in Maharashtra; Adjudication of stamp duty (Section 31); Impounding of insufficiently stamped documents (Section 33); Ready Reckoner rate valuation",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_UP_REVENUE_001",
        title="Uttar Pradesh Revenue Code, 2006",
        source_type="STATE_ACT",
        tier="Tier 1",
        authority="Board of Revenue, Uttar Pradesh",
        official_url="https://bor.up.nic.in/",
        exact_document_url="https://bor.up.nic.in/Upload_Acts/UP_Revenue_Code_2006.pdf",
        jurisdiction="State of Uttar Pradesh",
        state="Uttar Pradesh",
        act_number="Act No. 8 of 2012",
        act_year="2006",
        legal_domains="Land Revenue; Agricultural Land; Khatauni; Mutation",
        legal_intents="Classes of landholders (Bhumidhar with transferable/non-transferable rights, Asami); Mutation of name on succession or transfer (Section 34/35); Land conversion for non-agricultural use (Section 80); Partition suit of holdings (Section 116)",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    # =========================================================================
    # 8. INTELLECTUAL PROPERTY & ENVIRONMENT
    # =========================================================================
    sources.append(cs(
        source_id="SRC_COPY_001",
        title="Copyright Act, 1957 (Amended 2012)",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Copyright Office / DPIIT / Ministry of Commerce and Industry",
        official_url="https://copyright.gov.in/",
        exact_document_url="https://copyright.gov.in/Documents/CopyrightRules1957.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 14 of 1957",
        act_year="1957",
        legal_domains="Intellectual Property; Copyright; Fair Dealing; Infringement",
        legal_intents="Copyright protection in literary, artistic, musical, dramatic works, computer software (Section 13/14); Fair dealing exceptions for education, critique, reporting (Section 52); Infringement remedies (civil injunction, damages, criminal seizure Section 63)",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    sources.append(cs(
        source_id="SRC_TM_001",
        title="Trade Marks Act, 1999",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Controller General of Patents, Designs and Trade Marks (CGPDTM) / DPIIT",
        official_url="https://ipindia.gov.in/",
        exact_document_url="https://ipindia.gov.in/writereaddata/Portal/IPOAct/1_43_1_trade-marks-act.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 47 of 1999",
        act_year="1999",
        legal_domains="Intellectual Property; Trademarks; Passing Off; Brand Protection",
        legal_intents="Registration of trademarks (Section 18/23); Absolute and relative grounds for refusal (Section 9/11); Infringement vs common-law passing off action (Section 27/29); Deceptively similar marks",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    sources.append(cs(
        source_id="SRC_PATENT_001",
        title="Patents Act, 1970 (Amended 2005 / Patent Rules 2024)",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Indian Patent Office / DPIIT",
        official_url="https://ipindia.gov.in/",
        exact_document_url="https://ipindia.gov.in/writereaddata/Portal/IPOAct/1_31_1_patent-act-1970-11march2015.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 39 of 1970",
        act_year="1970",
        legal_domains="Intellectual Property; Patents; Inventions; Compulsory Licensing",
        legal_intents="Patentability criteria (novelty, inventive step, industrial applicability); Non-patentable subject matter (Section 3 - incremental drug modifications, software per se); Infringement remedies and compulsory licensing",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    sources.append(cs(
        source_id="SRC_EPA_001",
        title="Environment (Protection) Act, 1986 & Noise Pollution Rules, 2000",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="Ministry of Environment, Forest and Climate Change (MoEFCC)",
        official_url="https://www.indiacode.nic.in/handle/123456789/1786",
        exact_document_url="https://www.indiacode.nic.in/bitstream/123456789/1786/1/A1986-29.pdf",
        jurisdiction="Union of India",
        act_number="Act No. 29 of 1986",
        act_year="1986",
        legal_domains="Environmental Law; Pollution; Noise Rules; Public Nuisance",
        legal_intents="Central Government powers to regulate environmental pollution; Noise Pollution Rules (decibel limits for residential zones: 55 dB day, 45 dB night; 10 PM to 6 AM loudspeaker ban); Solid Waste Management Rules; Penalties for violation",
        commencement_status="COMMENCED",
        indexed_chunk_count=5,
    ))

    sources.append(cs(
        source_id="SRC_NGT_001",
        title="National Green Tribunal Act, 2010",
        source_type="CENTRAL_ACT",
        tier="Tier 1",
        authority="National Green Tribunal (NGT) / MoEFCC",
        official_url="https://www.greentribunal.gov.in/",
        exact_document_url="https://www.greentribunal.gov.in/sites/default/files/act_rules/NGT-act.pdf",
        jurisdiction="Union of India / Principal & Zonal Benches",
        act_number="Act No. 19 of 2010",
        act_year="2010",
        legal_domains="Environmental Law; Tribunals; Environmental Compensation",
        legal_intents="NGT jurisdiction over substantial questions relating to environment; Polluter Pays Principle and Precautionary Principle (Section 20); Limitation 6 months to approach NGT (Section 14); Environmental clearance challenges (Section 16)",
        commencement_status="COMMENCED",
        indexed_chunk_count=4,
    ))

    return sources
