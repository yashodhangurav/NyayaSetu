"""Expanded authoritative statutory provisions, state laws, guides, and precedents.
Provides modular legal chunk collections for canonical corpus builder.
"""

from typing import List
from rag.ingest.chunker import LegalStructureChunker, StandardizedLegalChunk


def get_expanded_corpus_chunks() -> List[StandardizedLegalChunk]:
    chunks: List[StandardizedLegalChunk] = []
    sc = LegalStructureChunker

    # =========================================================================
    # 1. CENTRAL PROPERTY, REAL ESTATE & CIVIL STATUTES
    # =========================================================================

    # Transfer of Property Act, 1882 - Section 54 (Sale)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_TPA_001",
        act="Transfer of Property Act, 1882",
        short_code="TPA",
        section="Section 54",
        clause_heading="Sale defined and transfer how effected",
        section_text=(
            "Sale is a transfer of ownership in exchange for a price paid or promised or part-paid and part-promised. "
            "Such transfer, in the case of tangible immovable property of the value of one hundred rupees and upwards, "
            "or in the case of a reversion or other intangible thing, can be made only by a registered instrument. "
            "A contract for the sale of immovable property is a contract that a sale of such property shall take place "
            "on terms settled between the parties. It does not, of itself, create any interest in or charge on such property."
        ),
        chapter="Chapter III: Of Sales of Immovable Property",
        topic_tags=["sale deed", "property sale", "registered instrument", "tpa 54", "ownership transfer", "agreement to sell"],
    ))

    # Transfer of Property Act, 1882 - Section 53A (Part Performance)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_TPA_001",
        act="Transfer of Property Act, 1882",
        short_code="TPA",
        section="Section 53A",
        clause_heading="Doctrine of Part Performance",
        section_text=(
            "Where any person contracts to transfer for consideration any immovable property by writing signed by him, "
            "and the transferee has, in part performance of the contract, taken possession of the property or any part thereof, "
            "or being already in possession, continues in possession in part performance of the contract and has done some act "
            "in furtherance of the contract, and the transferee has performed or is willing to perform his part of the contract, "
            "then the transferor is debarred from enforcing against the transferee any right in respect of the property, "
            "other than a right expressly provided by the terms of the contract. Section 17(1A) of the Registration Act mandates "
            "registration of documents containing contract for transfer of immovable property for the purpose of Section 53A."
        ),
        chapter="Chapter II",
        topic_tags=["part performance", "section 53a", "possession", "tpa 53a", "registration requirement"],
    ))

    # Transfer of Property Act, 1882 - Section 58 (Mortgages)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_TPA_001",
        act="Transfer of Property Act, 1882",
        short_code="TPA",
        section="Section 58",
        clause_heading="Mortgage, mortgagor, mortgagee, and types of mortgages",
        section_text=(
            "A mortgage is the transfer of an interest in specific immovable property for the purpose of securing the payment "
            "of money advanced or to be advanced by way of loan, an existing or future debt, or the performance of an engagement "
            "which may give rise to a pecuniary liability. The principal types include simple mortgage, mortgage by conditional sale, "
            "usufructuary mortgage, English mortgage, mortgage by deposit of title-deeds (equitable mortgage), and anomalous mortgage."
        ),
        chapter="Chapter IV: Of Mortgages of Immovable Property and Charges",
        topic_tags=["mortgage", "tpa 58", "loan security", "equitable mortgage", "title deed deposit", "simple mortgage"],
    ))

    # Transfer of Property Act, 1882 - Section 122 (Gift)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_TPA_001",
        act="Transfer of Property Act, 1882",
        short_code="TPA",
        section="Section 122",
        clause_heading="Gift defined and acceptance",
        section_text=(
            "Gift is the transfer of certain existing movable or immovable property made voluntarily and without consideration, "
            "by one person, called the donor, to another, called the donee, and accepted by or on behalf of the donee. "
            "Such acceptance must be made during the lifetime of the donor and while he is still capable of giving. "
            "Under Section 123, transfer of immovable property by gift must be effected by a registered instrument signed by "
            "or on behalf of the donor, and attested by at least two witnesses."
        ),
        chapter="Chapter VII: Of Gifts",
        topic_tags=["gift deed", "tpa 122", "voluntary transfer", "two witnesses", "compulsory registration"],
    ))

    # Registration Act, 1908 - Section 17 & 49
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_REG_001",
        act="Registration Act, 1908",
        short_code="REG_ACT",
        section="Section 17",
        clause_heading="Documents of which registration is compulsory",
        section_text=(
            "The following documents shall be registered: (a) instruments of gift of immovable property; "
            "(b) other non-testamentary instruments which purport or operate to create, declare, assign, limit or extinguish, "
            "whether in present or in future, any right, title or interest of the value of one hundred rupees and upwards, "
            "to or in immovable property; (c) non-testamentary instruments which acknowledge receipt of consideration; "
            "(d) leases of immovable property from year to year, or for any term exceeding one year, or reserving a yearly rent; "
            "(1A) documents containing contracts to transfer for consideration immovable property for Section 53A TPA purposes."
        ),
        chapter="Part III: Of Registerable Documents",
        topic_tags=["registration", "section 17", "compulsory registration", "sale deed", "lease over one year", "gift deed"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_REG_001",
        act="Registration Act, 1908",
        short_code="REG_ACT",
        section="Section 49",
        clause_heading="Effect of non-registration of documents required to be registered",
        section_text=(
            "No document required by Section 17 or by any provision of the Transfer of Property Act to be registered shall "
            "affect any immovable property comprised therein, or confer any power to adopt, or be received as evidence of any "
            "transaction affecting such property, unless it has been registered: Provided that an unregistered document affecting "
            "immovable property may be received as evidence of a contract in a suit for specific performance under the Specific Relief Act "
            "or as evidence of any collateral transaction not required to be effected by registered instrument."
        ),
        chapter="Part X: Of the Effects of Registration and Non-Registration",
        topic_tags=["unregistered document", "section 49", "collateral evidence", "inadmissible title", "specific performance evidence"],
    ))

    # Indian Easements Act, 1882 - Section 4 & 15
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_EAS_001",
        act="Indian Easements Act, 1882",
        short_code="EAS_ACT",
        section="Section 4 & 15",
        clause_heading="Easement defined and acquisition of right of way by prescription",
        section_text=(
            "An easement is a right which the owner or occupier of certain land possesses, as such, for the beneficial enjoyment "
            "of that land, to do and continue to do something, or to prevent and continue to prevent something being done, in or upon, "
            "or in respect of, certain other land not his own. Under Section 15, where the access and use of light or air, or right of way "
            "or other easement has been peaceably and openly enjoyed by any person claiming title thereto, as an easement and as of right, "
            "without interruption, and for twenty years, the right to such access and use shall be absolute and indefeasible. "
            "When the property belongs to the Government, the period of prescription is thirty years."
        ),
        chapter="Chapter I & II",
        topic_tags=["easement", "right of way", "pathway", "prescription", "20 years continuous use", "easements act"],
    ))

    # Specific Relief Act, 1963 - Section 6, 10, 34, 38
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_SRA_001",
        act="Specific Relief Act, 1963",
        short_code="SRA",
        section="Section 6",
        clause_heading="Suit by person dispossessed of immovable property without due process",
        section_text=(
            "If any person is dispossessed without his consent of immovable property otherwise than in due course of law, "
            "he or any person through whom he has been in possession or any person claiming through him may, by suit, recover possession "
            "thereof, notwithstanding any other title that may be set up in such suit. No suit under this section shall be brought "
            "after the expiry of six months from the date of dispossession, or against the Government. No appeal shall lie from any order "
            "or decree passed in any suit instituted under this section, nor shall any review of any such order or decree be allowed."
        ),
        chapter="Part II: Specific Relief",
        topic_tags=["dispossession", "section 6 sra", "summary possession", "six months limitation", "forcible eviction"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_SRA_001",
        act="Specific Relief Act, 1963",
        short_code="SRA",
        section="Section 34 & 38",
        clause_heading="Discretion of court as to declaration of status or right and perpetual injunction",
        section_text=(
            "Under Section 34, any person entitled to any legal character, or to any right as to any property, may institute a suit "
            "against any person denying, or interested to deny, his title to such character or right, and the court may in its discretion "
            "make therein a declaration that he is so entitled, and the plaintiff need not in such suit ask for any further relief: "
            "Provided that no court shall make any such declaration where the plaintiff, being able to seek further relief than a mere declaration "
            "of title, omits to do so. Under Section 38, a perpetual injunction may be granted to the plaintiff to prevent the breach of an "
            "obligation or where the defendant invades or threatens to invade the plaintiff's right to, or enjoyment of, property."
        ),
        chapter="Part II: Specific Relief",
        topic_tags=["declaration of title", "section 34 sra", "perpetual injunction", "section 38", "property stay", "cloud on title"],
    ))

    # Limitation Act, 1963 - Article 65 & Section 5
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_LIM_001",
        act="Limitation Act, 1963",
        short_code="LIM",
        section="Article 65 & Section 5",
        clause_heading="Twelve-year limitation for possession based on title and adverse possession; Condonation of delay",
        section_text=(
            "Under Article 65 of the Schedule to the Limitation Act, 1963, the period of limitation for a suit for possession of immovable property "
            "or any interest therein based on title is twelve years. The limitation begins to run when the possession of the defendant becomes "
            "adverse to the plaintiff. For suits against the Government, the limitation period is thirty years under Article 112. "
            "Under Section 5, any appeal or application (other than an execution application under Order XXI CPC) may be admitted after the prescribed "
            "period if the appellant or applicant satisfies the court that he had sufficient cause for not preferring the appeal or application within time."
        ),
        chapter="Limitation Act Provisions",
        topic_tags=["adverse possession", "article 65", "12 years limitation", "section 5", "condonation of delay", "title suit"],
    ))

    # Real Estate (Regulation and Development) Act, 2016 (RERA) - Section 11 & 14
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_RERA_001",
        act="Real Estate (Regulation and Development) Act, 2016",
        short_code="RERA",
        section="Section 11 & 14",
        clause_heading="Functions and duties of promoter and adherence to sanctioned plans; 5-year defect liability",
        section_text=(
            "Under Section 11, the promoter shall create a web page on the RERA authority website and enter project details including "
            "quarterly updates of list and number of apartments booked, approvals taken and pending, and quarterly status of the project. "
            "Under Section 14, the proposed project shall be developed and completed by the promoter in accordance with the sanctioned plans, "
            "layout plans and specifications approved by competent authorities. Any structural defect or any other defect in workmanship, "
            "quality or provision of services brought to the notice of the promoter within a period of five years from the date of handing over "
            "possession must be rectified by the promoter without further charge within thirty days."
        ),
        chapter="Chapter III: Rights and Duties of Allottees",
        topic_tags=["rera promoter", "section 14", "sanctioned plan", "5 years defect liability", "structural defect", "k-rera"],
    ))

    # SARFAESI Act, 2002 - Section 13
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_SARFAESI_001",
        act="Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002",
        short_code="SARFAESI",
        section="Section 13",
        clause_heading="Enforcement of security interest without court intervention and 60 days demand notice",
        section_text=(
            "Notwithstanding anything contained in Section 69 or Section 69A of the Transfer of Property Act, 1882, any security interest "
            "created in favour of any secured creditor may be enforced, without the intervention of the court or tribunal, by such creditor. "
            "Where any borrower makes any default in repayment of secured debt and his account is classified by the secured creditor as a non-performing asset (NPA), "
            "the secured creditor may require the borrower by notice in writing to discharge in full his liabilities within sixty days from the date of notice. "
            "If the borrower fails to comply, the creditor may take possession of the secured assets under Section 13(4) or take over management."
        ),
        chapter="Chapter III: Enforcement of Security Interest",
        topic_tags=["sarfaesi", "section 13", "60 days demand notice", "npa recovery", "bank auction", "drt appeal"],
    ))

    # =========================================================================
    # 2. KARNATAKA STATE SPECIFIC LAND REVENUE, REFORMS & HOUSING LAWS
    # =========================================================================

    # Karnataka Land Revenue Act, 1964 - Section 95 (Conversion)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_LRA_001",
        act="Karnataka Land Revenue Act, 1964",
        short_code="KLRA",
        section="Section 95",
        clause_heading="Uses of agricultural land and procedure for diversion for other purposes (Land Conversion)",
        section_text=(
            "An occupant of land assessed or held for the purpose of agriculture is entitled by himself, his servants, tenants, agents or "
            "other legal representatives, to erect farm buildings, construct wells or tanks, or make other improvements for better cultivation. "
            "If any occupant wishes to divert such land or any part thereof to any other purpose (commercial, industrial, or residential), "
            "he shall apply for permission to the Deputy Commissioner. Under recent Karnataka amendments, deemed conversion applies upon submission "
            "of self-declaration and payment of prescribed conversion fine if consistent with the Master Plan published under the Karnataka Town "
            "and Country Planning Act, 1961."
        ),
        chapter="Chapter VIII: Grant, Use and Relinquishment of Unalienated Land",
        jurisdiction="Karnataka (State)",
        topic_tags=["karnataka land revenue act", "section 95", "land conversion", "dc conversion", "agricultural to residential", "bhoomi conversion"],
    ))

    # Karnataka Land Revenue Act, 1964 - Section 128 & 133 (Mutation & RTC Presumption)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_LRA_001",
        act="Karnataka Land Revenue Act, 1964",
        short_code="KLRA",
        section="Section 128 & 133",
        clause_heading="Acquisition of rights to be reported; Presumption of correctness of Record of Rights (Pahani / RTC)",
        section_text=(
            "Under Section 128, any person acquiring by succession, survivorship, inheritance, partition, purchase, mortgage, gift, lease "
            "or otherwise, any right as holder, occupant, owner, mortgagee, landlord or tenant of land situated in Karnataka shall report orally "
            "or in writing his acquisition of such right to the prescribed revenue officer (Tahsildar / Revenue Inspector) within three months. "
            "Under Section 133, an entry in the Record of Rights and a certified entry in the register of mutations shall be presumed to be true "
            "until the contrary is proved or a new entry is lawfully substituted. However, revenue mutation does not confer or extinguish judicial title."
        ),
        chapter="Chapter XI: Record of Rights",
        jurisdiction="Karnataka (State)",
        topic_tags=["rtc", "pahani", "mutation", "section 128", "section 133", "record of rights", "bhoomi mutation", "presumption of rtc"],
    ))

    # Karnataka Land Reforms Act, 1961 - Section 79A/B & 132
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_LREFORMS_001",
        act="Karnataka Land Reforms Act, 1961",
        short_code="KLREFORMS",
        section="Section 79A, 79B & 132",
        clause_heading="Regulation of agricultural land acquisition and bar of jurisdiction of civil courts",
        section_text=(
            "Sections 79A (income limit for acquisition of agricultural land) and 79B (prohibition on holding agricultural land by non-agriculturists) "
            "of the Karnataka Land Reforms Act, 1961 were omitted by Karnataka Act No. 29 of 2020. Non-agriculturists and Indian citizens are permitted "
            "to purchase agricultural land in Karnataka subject to ceiling limits under Section 63. Under Section 132, no civil court shall have "
            "jurisdiction to settle, decide or deal with any question which is by or under this Act required to be settled, decided or dealt with by "
            "the Land Tribunal, Deputy Commissioner or Assistant Commissioner."
        ),
        chapter="Karnataka Land Reforms",
        jurisdiction="Karnataka (State)",
        topic_tags=["karnataka land reforms", "section 79a", "section 79b", "agricultural land purchase", "ceiling limits", "tribunal jurisdiction"],
    ))

    # Karnataka PTCL Act, 1978 - Section 4 & 5
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_PTCL_001",
        act="Karnataka Scheduled Castes and Scheduled Tribes (Prohibition of Transfer of Certain Lands) Act, 1978",
        short_code="PTCL",
        section="Section 4 & 5",
        clause_heading="Prohibition of transfer of granted land to SC/ST persons and resumption by Assistant Commissioner",
        section_text=(
            "Under Section 4, any transfer of granted land made either before or after the commencement of this Act, in contravention of the terms "
            "of the grant or the law providing for such grant, or without prior permission of the State Government, is null and void and no right, "
            "title or interest in such land shall be conveyed. Under Section 5, the Assistant Commissioner may, on application by any interested person "
            "or on information, declare the transfer of granted land null and void, resume the land to the State Government free from all encumbrances, "
            "and restore it to the original grantee or his legal heirs."
        ),
        chapter="PTCL Act Provisions",
        jurisdiction="Karnataka (State)",
        topic_tags=["ptcl act", "sc st granted land", "section 4", "section 5", "resumption of land", "assistant commissioner", "null and void transfer"],
    ))

    # Karnataka Land Grabbing Prohibition Act, 2011 - Section 3 & 4
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_LANDGRAB_001",
        act="Karnataka Land Grabbing Prohibition Act, 2011",
        short_code="KLGPA",
        section="Section 3 & 4",
        clause_heading="Prohibition of land grabbing and Special Court jurisdiction",
        section_text=(
            "Land grabbing of any land belonging to the Government, local authority, religious or charitable institution or Wakf is declared unlawful. "
            "Any person who commits or abets land grabbing shall be punished with imprisonment for a term not less than one year which may extend "
            "to three years and with fine up to twenty-five thousand rupees. Special Courts constituted under Section 7 have exclusive jurisdiction "
            "to try offences and determine civil disputes relating to alleged government and public land grabbing."
        ),
        chapter="Land Grabbing Prohibition",
        jurisdiction="Karnataka (State)",
        topic_tags=["land grabbing", "karnataka land grabbing act", "special court", "government land encroachment", "criminal penalty"],
    ))

    # Karnataka Apartment Ownership Act, 1972 - Section 5 & 10
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_APT_001",
        act="Karnataka Apartment Ownership Act, 1972",
        short_code="KAOA",
        section="Section 5 & 10",
        clause_heading="Status of apartments, undivided interest in common areas and Deed of Declaration",
        section_text=(
            "Each apartment owner shall be entitled to an undivided interest in the common areas and facilities in the percentage expressed in the "
            "Deed of Declaration. Such percentage cannot be altered without the consent of all apartment owners expressed in an amended Declaration. "
            "Common areas and facilities shall remain undivided, and no apartment owner or other person may bring any action for partition or division "
            "of any part thereof. Apartment Owners Associations manage maintenance, sinking funds, and compliance under registered bye-laws."
        ),
        chapter="Apartment Ownership",
        jurisdiction="Karnataka (State)",
        topic_tags=["apartment ownership", "kaoa 1972", "undivided share", "uds", "deed of declaration", "apartment association", "common areas"],
    ))

    # =========================================================================
    # 3. PROCEDURES, PORTALS & CITIZEN GUIDES
    # =========================================================================

    chunks.append(sc.chunk_procedure_guide(
        source_id="SRC_PROC_BHOOMI_001",
        title="Bhoomi Karnataka Land Portal: Extracting RTC / Pahani and Mutation Status",
        step_heading="Online Verification of Record of Rights and Mutation Register",
        guide_text=(
            "1. Visit the official Karnataka Bhoomi portal (bhoomi.karnataka.gov.in).\n"
            "2. Navigate to 'View RTC Information' and enter District, Taluk, Hobli, Village, and Survey Number.\n"
            "3. Verify Column 9 (Owner Name), Column 10 (Extent of land in Acres/Guntas), Column 11 (Khata Number), and Column 12 (Liabilities/Mortgages/Court stays).\n"
            "4. Check 'Mutation Status' to track pending or disputed mutation entries filed after purchase, inheritance (Pouthi Khata), or partition.\n"
            "5. Certified electronic RTC copies with digital signature can be downloaded upon paying ₹15 fee."
        ),
        topic_tags=["bhoomi", "rtc download", "pahani", "mutation status", "survey number", "karnataka revenue portal"],
    ))

    chunks.append(sc.chunk_procedure_guide(
        source_id="SRC_PROC_KAVERI_001",
        title="Kaveri 2.0 Karnataka Property Registration and Encumbrance Certificate (EC)",
        step_heading="Encumbrance Certificate (Form 15 & 16) and Online Deed Verification",
        guide_text=(
            "1. Access Kaveri 2.0 (kaveri.karnataka.gov.in) maintained by the Department of Stamps and Registration.\n"
            "2. Search Encumbrance Certificate (EC): Select property jurisdiction, village, survey number/site number, and search window (minimum 15 to 30 years recommended).\n"
            "3. Form 15 lists all registered transactions, mortgages, court attachments, and lease deeds during the searched period.\n"
            "4. Form 16 (Nil Encumbrance) certifies that no registered encumbrance was found in the register for the queried period.\n"
            "5. For registration: Upload draft sale deed, calculate valuation/stamp duty, book SRO appointment slot, and verify biometric Aadhaar e-KYC."
        ),
        topic_tags=["kaveri 2.0", "encumbrance certificate", "ec search", "form 15", "form 16", "stamp duty", "sro registration"],
    ))

    chunks.append(sc.chunk_procedure_guide(
        source_id="SRC_PROC_SAKALA_001",
        title="Karnataka Sakala Services Act, 2011: Guaranteed Citizen Delivery Timelines",
        step_heading="Statutory Timelines for Revenue and Municipal Services",
        guide_text=(
            "The Karnataka Guarantee of Services to Citizens Act (Sakala) mandates fixed timelines for citizen services:\n"
            "- Issuance of computerized RTC / Pahani: Same day / 3 working days.\n"
            "- Mutation entry based on registered sale deed: 30 working days.\n"
            "- Pouthi (Inheritance) mutation: 45 working days.\n"
            "- Land Conversion under Section 95 KLRA: 60 days (or deemed approved under master plan).\n"
            "- If the designated officer fails to provide service within the stipulated time, the citizen receives daily compensation "
            "deducted from the defaulting officer's salary via Sakala GSC number tracking."
        ),
        topic_tags=["sakala", "service guarantee", "karnataka timelines", "rtc timeline", "mutation timeline", "citizen charter"],
    ))

    # =========================================================================
    # 4. LANDMARK JUDICIAL PRECEDENTS (EXPANDED PROPERTY & CRIMINAL JURISPRUDENCE)
    # =========================================================================

    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_SURAJLAMP_001",
        case_title="Suraj Lamp & Industries Pvt. Ltd. v. State of Haryana",
        citation="(2012) 1 SCC 656",
        court="Supreme Court of India",
        judgment_date="2011-10-11",
        issue="Whether sale of immovable property through General Power of Attorney (GPA), Agreement to Sell (SA), and Living Will transfers valid title?",
        holding="Immovable property can be legally and lawfully transferred only by a registered deed of conveyance. SA/GPA/WILL transactions do not convey any title nor do they create any interest in immovable property.",
        ratio_decidendi="A Power of Attorney is not an instrument of transfer in regard to any right, title or interest in an immovable property. GPA transactions cannot be recognized as deeds of title or transfer by courts or registration authorities. Such transactions do not satisfy the mandatory requirements of Section 54 of the Transfer of Property Act or Section 17 of the Registration Act.",
        topic_tags=["suraj lamp", "gpa sale", "agreement to sell", "power of attorney", "registered deed required", "property title"],
    ))

    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_VINEETA_001",
        case_title="Vineeta Sharma v. Rakesh Sharma",
        citation="(2020) 9 SCC 1",
        court="Supreme Court of India (3-Judge Bench)",
        judgment_date="2020-08-11",
        issue="Whether the daughter's right to coparcenary property under Section 6 of the Hindu Succession Act, 1956 is conditional on the coparcener father being alive on September 9, 2005?",
        holding="Daughters have coparcenary rights by birth in ancestral property under amended Section 6 of the Hindu Succession Act, 1956, regardless of whether the coparcener father was alive on September 9, 2005.",
        ratio_decidendi="The rights conferred on daughters under Section 6 are born out of coparcenary status acquired by birth. The amendment operates on existing coparcenaries and has retroactive effect. A daughter is entitled to an equal share in coparcenary property identical to that of a son, except where a formal partition was registered before December 20, 2004.",
        topic_tags=["vineeta sharma", "ancestral property", "daughter coparcenary", "hindu succession act", "section 6", "equal inheritance"],
    ))

    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_JITENDRA_001",
        case_title="Jitendra Singh v. State of Madhya Pradesh",
        citation="(2021) SCC OnLine SC 802",
        court="Supreme Court of India",
        judgment_date="2021-09-06",
        issue="Whether mutation entry in revenue records confers ownership, title, or proprietary rights over immovable property?",
        holding="Mutation entry in revenue records does not confer title, ownership, or proprietary rights upon any individual; revenue records exist solely for fiscal tax collection purposes.",
        ratio_decidendi="It is settled law that mutation of property in the revenue records does not create or extinguish title nor has it any presumptive value on title. If there is any dispute regarding title, the parties must approach the competent Civil Court for declaration of title under Section 34 of the Specific Relief Act.",
        topic_tags=["jitendra singh", "mutation not title", "revenue records", "khata not ownership", "fiscal purpose", "civil suit for title"],
    ))

    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_RAVINDER_001",
        case_title="Ravinder Kaur Grewal v. Manjit Kaur",
        citation="(2019) 8 SCC 729",
        court="Supreme Court of India (3-Judge Bench)",
        judgment_date="2019-08-07",
        issue="Whether a plea of adverse possession under Article 65 of the Limitation Act, 1963 can be used as a sword by the plaintiff to seek declaration of title?",
        holding="Adverse possession can be used as a sword by a plaintiff to declare title, not merely as a shield of defense.",
        ratio_decidendi="When a squatter or possessor has been in open, continuous, and hostile possession of immovable property for more than twelve years extinguishing the owner's title under Section 27 and Article 65 of the Limitation Act, he acquires a perfected title by adverse possession and can maintain an affirmative suit for declaration of title and perpetual injunction.",
        topic_tags=["adverse possession", "ravinder kaur grewal", "article 65", "12 years hostile possession", "sword of adverse possession"],
    ))

    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_ANATHULA_001",
        case_title="Anathula Sudhakar v. P. Buchi Reddy",
        citation="(2008) 4 SCC 594",
        court="Supreme Court of India",
        judgment_date="2008-03-25",
        issue="Under what circumstances is a bare suit for injunction maintainable, and when must a plaintiff file a comprehensive suit for declaration of title?",
        holding="Where a cloud is raised over the plaintiff's title and he is not in possession, or where title is seriously disputed, a suit for bare injunction is not maintainable; the remedy is a suit for declaration of title with consequential relief.",
        ratio_decidendi="1. Where plaintiff's title is not in dispute or under cloud, but his peaceful possession is threatened, a suit for bare permanent injunction lies. 2. Where title is disputed or clouded, plaintiff must sue for declaration of title and injunction. 3. Where plaintiff is not in possession, he must sue for declaration of title and recovery of possession.",
        topic_tags=["anathula sudhakar", "injunction vs declaration", "cloud on title", "bare injunction", "possession suit"],
    ))

    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_LALITA_001",
        case_title="Lalita Kumari v. Government of Uttar Pradesh",
        citation="(2014) 2 SCC 1",
        court="Supreme Court of India (5-Judge Constitution Bench)",
        judgment_date="2013-11-12",
        issue="Whether a police officer is bound to register a First Information Report (FIR) upon receiving information relating to the commission of a cognizable offence?",
        holding="Registration of FIR is mandatory under Section 154 of the Code of Criminal Procedure (now Section 173 BNSS) if the information discloses commission of a cognizable offence.",
        ratio_decidendi="Police officers have no discretion to refuse registration of an FIR if a cognizable offence is disclosed. Preliminary inquiry is permissible only in limited categories such as medical negligence, corruption, matrimonial/family disputes, or commercial disputes, and such inquiry must be concluded within 7 to 14 days.",
        topic_tags=["lalita kumari", "mandatory fir", "cognizable offence", "police duty", "preliminary inquiry", "section 173 bnss"],
    ))

    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_RAJNESH_001",
        case_title="Rajnesh v. Neha",
        citation="(2021) 2 SCC 324",
        court="Supreme Court of India",
        judgment_date="2020-11-04",
        issue="What uniform guidelines and criteria govern the award of interim and final maintenance across matrimonial proceedings in India?",
        holding="The Supreme Court framed uniform national guidelines and made the submission of an Affidavit of Assets and Liabilities mandatory for both parties in all matrimonial maintenance proceedings.",
        ratio_decidendi="To eliminate delays and false financial claims, both spouses must file a standardized Disclosure Affidavit detailing all assets, liabilities, bank accounts, IT returns, and lifestyle standards. Maintenance is payable from the date of filing the application.",
        topic_tags=["rajnesh v neha", "maintenance", "affidavit of assets", "interim maintenance", "matrimonial disputes", "pwdva maintenance"],
    ))

    # =========================================================================
    # 5. EXPANDED PROPERTY & LAND GLOSSARY ENTRIES
    # =========================================================================
    glossary_items = [
        ("Pahani / RTC", "ಪಹಣಿ / ಆರ್‌ಟಿಸಿ", "खतौनी / पहानी", "Record of Rights, Tenancy and Crops extract issued under Karnataka Land Revenue Act Section 133 containing survey number, owner details, soil type, and encumbrances."),
        ("Mutation (Pouthi Khata)", "ನಾಮಾಂತರ / ಪೌತಿ ಖಾತಾ", "दाखिल खारिज / नामांतरण", "Administrative recording of transfer or succession of title in the revenue register for tax assessment; does not create judicial title."),
        ("A-Khata / B-Khata", "ಎ-ಖಾತಾ / ಬಿ-ಖಾತಾ", "ए-खाता / बी-खाता", "Bangalore municipal property register: A-Khata signifies fully approved sanctioned layout; B-Khata is a tax-assessment register for unauthorized or unapproved layouts."),
        ("Encumbrance Certificate (EC)", "ಭಾರಮುಕ್ತ ಪ್ರಮಾಣಪತ್ರ", "भारमुक्त प्रमाण पत्र", "Certificate from the Sub-Registrar showing all registered deeds, charges, mortgages, and attachments on an immovable property over a specified timeline."),
        ("Adverse Possession", "ಪ್ರತಿಕೂಲ ಸ್ವಾಧೀನ", "प्रतिकूल कब्जा", "Acquisition of title to immovable property through open, continuous, and hostile possession without permission for over 12 years under Limitation Act Article 65."),
        ("Phodi / Durasti", "ಫೋಡಿ / ದುರಸ್ತಿ", "हदबंदी / दुरुस्ती", "Official revenue survey and sub-division of survey land granting individual unshared survey numbers and sketch maps to joint owners in Karnataka."),
    ]
    for en_term, kn_term, hi_term, meaning in glossary_items:
        text = f"Legal Glossary Term: {en_term}\nKannada: {kn_term} | Hindi: {hi_term}\nStatutory Meaning: {meaning}"
        chk = sc.chunk_procedure_guide(
            source_id="SRC_REV_GLOSSARY_002",
            title=f"Legal Term: {en_term} ({kn_term} / {hi_term})",
            step_heading="Statutory Definition",
            guide_text=text,
            topic_tags=["glossary", en_term.lower(), kn_term, hi_term, "property terminology", "trilingual"],
        )
        chunks.append(chk)

    return chunks
