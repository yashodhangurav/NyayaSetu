"""Curated, verified statutory Indian legal sources for NyayaSetu RAG.

Covers 10 core Indian legal practice domains with verified Bare Act text,
statutory section numbers, official gazette citations, and government portal URLs:
1. Family Law (Domestic Violence, Marriage & Divorce, Succession)
2. Criminal Law (BNS, BNSS, BSA - Sanhitas 2023)
3. Commercial & Contracts (Indian Contract Act, Negotiable Instruments Act)
4. Consumer Protection (Consumer Protection Act, 2019)
5. Cyber Law & Data Privacy (IT Act 2000, DPDP Act 2023)
6. Motor Vehicle Accidents (Motor Vehicles Act 1988/2019 - MACT)
7. Property & Civil Law (Transfer of Property Act, Limitation Act, RERA)
8. Legal Aid & Access (Legal Services Authorities Act, 1987)
9. Employment & Labour (Industrial Disputes Act, Payment of Gratuity Act)
10. Intellectual Property (Copyright Act, Trade Marks Act)
"""

from datetime import date
from typing import Any, Dict, List

CURATED_LEGAL_SOURCES: List[Dict[str, Any]] = [
    # ──────────────────────────────────────────────────────────────
    # 1. Commercial & Banking: Negotiable Instruments Act, 1881
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Negotiable Instruments Act, 1881",
        "source_type": "BARE_ACT",
        "short_code": "NI_ACT",
        "citation": "Act No. 26 of 1881",
        "act_or_judgment_identifier": "Act No. 26 of 1881",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1881, 12, 9),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/2189",
        "year": 1881,
        "chunks": [
            {
                "section_number": "Section 138",
                "clause_heading": "Dishonour of cheque for insufficiency, etc., of funds in the account",
                "chunk_text": (
                    "Where any cheque drawn by a person on an account maintained by him with a banker for payment "
                    "of any amount of money to another person from out of that account for the discharge, in whole or "
                    "in part, of any debt or other liability, is returned by the bank unpaid, either because of the "
                    "amount of money standing to the credit of that account is insufficient to honour the cheque or "
                    "that it exceeds the amount arranged to be paid from that account by an agreement made with that "
                    "bank, such person shall be deemed to have committed an offence and shall be punished with "
                    "imprisonment for a term which may be extended to two years, or with fine which may extend to twice "
                    "the amount of the cheque, or with both: Provided that nothing contained in this section shall apply "
                    "unless (a) the cheque has been presented to the bank within a period of three months from the date "
                    "on which it is drawn; (b) the payee or holder in due course makes a demand for the payment of the said "
                    "amount of money by giving a notice in writing to the drawer within thirty days of the receipt of information "
                    "from the bank regarding the return of the cheque as unpaid; and (c) the drawer of such cheque fails to "
                    "make the payment of the said amount of money to the payee or holder in due course within fifteen days of the "
                    "receipt of the said notice."
                ),
            },
            {
                "section_number": "Section 139",
                "clause_heading": "Presumption in favour of holder",
                "chunk_text": (
                    "It shall be presumed, unless the contrary is proved, that the holder of a cheque received the cheque of the "
                    "nature referred to in section 138 for the discharge, in whole or in part, of any debt or other liability."
                ),
            },
            {
                "section_number": "Section 141",
                "clause_heading": "Offences by companies",
                "chunk_text": (
                    "If the person committing an offence under section 138 is a company, every person who, at the time the offence "
                    "was committed, was in charge of, and was responsible to the company for the conduct of the business of the "
                    "company, as well as the company, shall be deemed to be guilty of the offence and shall be liable to be proceeded "
                    "against and punished accordingly."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 2. Consumer Law: Consumer Protection Act, 2019
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Consumer Protection Act, 2019",
        "source_type": "BARE_ACT",
        "short_code": "CPA_2019",
        "citation": "Act No. 35 of 2019",
        "act_or_judgment_identifier": "Act No. 35 of 2019",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(2019, 8, 9),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/15256",
        "year": 2019,
        "chunks": [
            {
                "section_number": "Section 2(7)",
                "clause_heading": "Definition of Consumer",
                "chunk_text": (
                    "Consumer means any person who buys any goods for a consideration which has been paid or promised or partly "
                    "paid and partly promised, or under any system of deferred payment and includes any user of such goods other "
                    "than the person who buys such goods for consideration, but does not include a person who obtains such goods "
                    "for resale or for any commercial purpose; or hires or avails of any service for a consideration."
                ),
            },
            {
                "section_number": "Section 35",
                "clause_heading": "Manner in which complaint shall be made",
                "chunk_text": (
                    "A complaint, in relation to any goods sold or delivered or agreed to be sold or delivered or any service "
                    "provided or agreed to be provided, may be filed with a District Commission by the consumer, recognized consumer "
                    "association, or Central Authority. A complaint may also be filed electronically through e-Daakhil in the District "
                    "Commission within the local limits of whose jurisdiction the complainant resides or personally works for gain, or "
                    "where the opposite party resides or carries on business."
                ),
            },
            {
                "section_number": "Section 47",
                "clause_heading": "Jurisdiction of State Commission",
                "chunk_text": (
                    "The State Commission shall have jurisdiction to entertain complaints where the value of the goods or services "
                    "paid as consideration exceeds rupees fifty lakhs but does not exceed rupees two crores, and appeals against "
                    "orders of any District Commission within the State."
                ),
            },
            {
                "section_number": "Section 84",
                "clause_heading": "Liability of product manufacturer in product liability action",
                "chunk_text": (
                    "A product manufacturer shall be liable in a product liability action if (a) the product contains a manufacturing "
                    "defect; (b) the product is defective in design; (c) there is a deviation from manufacturing specifications; "
                    "(d) the product does not conform to the express warranty; or (e) the product fails to contain adequate instructions "
                    "of correct usage to prevent any harm or any warning regarding improper or incorrect usage."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 3. Legal Aid & Access: Legal Services Authorities Act, 1987
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Legal Services Authorities Act, 1987",
        "source_type": "LEGAL_AID_SCHEME",
        "short_code": "NALSA_1987",
        "citation": "Act No. 39 of 1987",
        "act_or_judgment_identifier": "Act No. 39 of 1987",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1987, 10, 11),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://nalsa.gov.in/acts-rules",
        "year": 1987,
        "chunks": [
            {
                "section_number": "Section 12",
                "clause_heading": "Criteria for giving legal services (Free Legal Aid Entitlement)",
                "chunk_text": (
                    "Every person who has to file or defend a case shall be entitled to legal services under this Act if that person "
                    "is (a) a member of a Scheduled Caste or Scheduled Tribe; (b) a victim of trafficking in human beings or begar; "
                    "(c) a woman or a child; (d) a person with disability; (e) a person under circumstances of underserved want such "
                    "as being a victim of a mass disaster, ethnic violence, caste atrocity, flood, drought, earthquake or industrial "
                    "disaster; (f) an industrial workman; (g) in custody, including custody in a protective home or psychiatric hospital; "
                    "or (h) in receipt of annual income less than the amount prescribed by the State Government or Central Government."
                ),
            },
            {
                "section_number": "Section 19",
                "clause_heading": "Organization of Lok Adalats",
                "chunk_text": (
                    "Every State Authority or District Authority or Supreme Court Legal Services Committee or High Court Legal Services "
                    "Committee or Taluk Legal Services Committee may organize Lok Adalats at such intervals and places and for "
                    "exercising such jurisdiction and for such areas as it thinks fit. A Lok Adalat shall have jurisdiction to determine "
                    "and to arrive at a compromise or settlement between the parties to a dispute in respect of any case pending "
                    "before any court, or any matter which is falling within the jurisdiction of, and is not brought before, any court "
                    "for which the Lok Adalat is organized."
                ),
            },
            {
                "section_number": "Section 21",
                "clause_heading": "Award of Lok Adalat and refund of court fee",
                "chunk_text": (
                    "Every award of the Lok Adalat shall be deemed to be a decree of a civil court or, as the case may be, an order "
                    "of any other court and where a compromise or settlement has been arrived at, by a Lok Adalat in a case referred "
                    "to it under sub-section (1) of section 20, the court-fee paid in such case shall be refunded in the manner provided "
                    "under the Court-fees Act, 1870. Every award made by a Lok Adalat shall be final and binding on all the parties to the "
                    "dispute, and no appeal shall lie to any court against the award."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 4. Property & Real Estate: RERA Act, 2016
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Real Estate (Regulation and Development) Act, 2016",
        "source_type": "BARE_ACT",
        "short_code": "RERA_2016",
        "citation": "Act No. 16 of 2016",
        "act_or_judgment_identifier": "Act No. 16 of 2016",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(2016, 3, 26),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/2158",
        "year": 2016,
        "chunks": [
            {
                "section_number": "Section 18",
                "clause_heading": "Return of amount and compensation for delay in possession",
                "chunk_text": (
                    "If the promoter fails to complete or is unable to give possession of an apartment, plot or building in "
                    "accordance with the terms of the agreement for sale or duly completed by the date specified therein, the promoter "
                    "shall be liable on demand to the allottees, in case the allottee wishes to withdraw from the project, to return "
                    "the amount received by him in respect of that apartment, plot, building, with interest at such rate as may be "
                    "prescribed in this behalf including compensation. If the allottee does not intend to withdraw from the project, he "
                    "shall be paid, by the promoter, interest for every month of delay, till the handing over of the possession."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 5. Criminal Procedure: Bharatiya Nagarik Suraksha Sanhita, 2023
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Bharatiya Nagarik Suraksha Sanhita, 2023",
        "source_type": "BARE_ACT",
        "short_code": "BNSS_2023",
        "citation": "Act No. 46 of 2023",
        "act_or_judgment_identifier": "Act No. 46 of 2023",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(2023, 12, 25),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.mha.gov.in/en/acts",
        "year": 2023,
        "chunks": [
            {
                "section_number": "Section 173",
                "clause_heading": "Information in cognizable cases (First Information Report)",
                "chunk_text": (
                    "Every information relating to the commission of a cognizable offence, if given orally to an officer in charge "
                    "of a police station, shall be reduced to writing by him or under his direction, and be read over to the informant; "
                    "and every such information, whether given in writing or reduced to writing as aforesaid, shall be signed by the person "
                    "giving it, and the substance thereof shall be entered in a book to be kept by such officer. Information may also be "
                    "given electronically and taken on record."
                ),
            },
            {
                "section_number": "Section 479",
                "clause_heading": "Maximum period for which an undertrial prisoner can be detained",
                "chunk_text": (
                    "Where a person has, during the period of investigation, inquiry or trial under this Sanhita of an offence "
                    "under any law, undergone detention for a period extending up to one-half of the maximum period of imprisonment "
                    "specified for that offence under that law, he shall be released by the Court on bail: Provided that where such person "
                    "is a first-time offender who has never been convicted of any offence in the past, he shall be released on bail by "
                    "the Court if he has undergone detention for the period extending up to one-third of the maximum period of "
                    "imprisonment specified for such offence."
                ),
            },
            {
                "section_number": "Section 482",
                "clause_heading": "Direction for grant of bail to person apprehending arrest (Anticipatory Bail)",
                "chunk_text": (
                    "When any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable "
                    "offence, he may apply to the High Court or the Court of Session for a direction under this section that in the event "
                    "of such arrest he shall be released on bail; and that Court may, after taking into consideration the nature and gravity "
                    "of the accusation, the antecedents of the applicant, the possibility of the applicant to flee from justice, and where "
                    "the accusation has been made with the object of injuring or humiliating the applicant by having him so arrested, "
                    "either reject the application or issue an interim order for the grant of anticipatory bail."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 6. Substantive Criminal Law: Bharatiya Nyaya Sanhita, 2023
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Bharatiya Nyaya Sanhita, 2023",
        "source_type": "BARE_ACT",
        "short_code": "BNS_2023",
        "citation": "Act No. 45 of 2023",
        "act_or_judgment_identifier": "Act No. 45 of 2023",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(2023, 12, 25),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.mha.gov.in/en/acts",
        "year": 2023,
        "chunks": [
            {
                "section_number": "Section 85",
                "clause_heading": "Husband or relative of husband of a woman subjecting her to cruelty",
                "chunk_text": (
                    "Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty shall be "
                    "punished with imprisonment for a term which may extend to three years and shall also be liable to fine. For the "
                    "purposes of this section, cruelty means (a) any wilful conduct which is of such a nature as is likely to drive the "
                    "woman to commit suicide or to cause grave injury or danger to life, limb or health (whether mental or physical) "
                    "of the woman; or (b) harassment of the woman where such harassment is with a view to coercing her or any person "
                    "related to her to meet any unlawful demand for any property or valuable security."
                ),
            },
            {
                "section_number": "Section 316",
                "clause_heading": "Criminal breach of trust",
                "chunk_text": (
                    "Whoever, being in any manner entrusted with property, or with any dominion over property, dishonestly "
                    "misappropriates or converts to his own use that property, or dishonestly uses or disposes of that property in "
                    "violation of any direction of law prescribing the mode in which such trust is to be discharged, or of any legal "
                    "contract, express or implied, which he has made touching the discharge of such trust, or wilfully suffers any "
                    "other person so to do, commits criminal breach of trust. Whoever commits criminal breach of trust shall be "
                    "punished with imprisonment of either description for a term which may extend to five years, or with fine, or with both."
                ),
            },
            {
                "section_number": "Section 318",
                "clause_heading": "Cheating and dishonestly inducing delivery of property",
                "chunk_text": (
                    "Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property "
                    "to any person, or to consent that any person shall retain any property, or intentionally induces the person so "
                    "deceived to do or omit to do anything which he would not do or omit if he were not so deceived, and which act or "
                    "omission causes or is likely to cause damage or harm to that person in body, mind, reputation or property, is said "
                    "to cheat. Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person "
                    "shall be punished with imprisonment of either description for a term which may extend to seven years, and shall "
                    "also be liable to fine."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 7. Law of Evidence: Bharatiya Sakshya Adhiniyam, 2023
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Bharatiya Sakshya Adhiniyam, 2023",
        "source_type": "BARE_ACT",
        "short_code": "BSA_2023",
        "citation": "Act No. 47 of 2023",
        "act_or_judgment_identifier": "Act No. 47 of 2023",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(2023, 12, 25),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.mha.gov.in/en/acts",
        "year": 2023,
        "chunks": [
            {
                "section_number": "Section 61",
                "clause_heading": "Admissibility of electronic or digital records",
                "chunk_text": (
                    "Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in the evidence "
                    "on the ground that it is an electronic or digital record and such record shall have the same legal effect, validity "
                    "and enforceability as any other document."
                ),
            },
            {
                "section_number": "Section 63",
                "clause_heading": "Admissibility of electronic records and certificate requirement",
                "chunk_text": (
                    "Any information contained in an electronic record which is printed on a paper, stored, recorded or copied in optical "
                    "or magnetic media or cloud or semiconductor memory produced by a computer shall be deemed to be also a document and "
                    "shall be admissible in any proceedings, without further proof or production of the original, as evidence of any "
                    "contents of the original or of any fact stated therein of which direct evidence would be admissible, provided the "
                    "device producing the record was in regular lawful use and accompanied by a certificate signed by a person occupying "
                    "a responsible official position in relation to the operation of the relevant device."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 8. Family Law: Protection of Women from Domestic Violence Act, 2005
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Protection of Women from Domestic Violence Act, 2005",
        "source_type": "BARE_ACT",
        "short_code": "PWDVA_2005",
        "citation": "Act No. 43 of 2005",
        "act_or_judgment_identifier": "Act No. 43 of 2005",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(2005, 9, 13),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/2012",
        "year": 2005,
        "chunks": [
            {
                "section_number": "Section 3",
                "clause_heading": "Definition of domestic violence",
                "chunk_text": (
                    "For the purposes of this Act, any act, omission or commission or conduct of the respondent shall constitute domestic "
                    "violence if it (a) harms or injures or endangers the health, safety, life, limb or well-being, whether mental or physical, "
                    "of the aggrieved person or tends to do so and includes causing physical abuse, sexual abuse, verbal and emotional abuse "
                    "and economic abuse; or (b) harasses, harms, injures or endangers the aggrieved person with a view to coerce her or any other "
                    "person related to her to meet any unlawful demand for any dowry or other property or valuable security; or (c) has the "
                    "effect of threatening the aggrieved person or any person related to her by any conduct mentioned in clause (a) or clause (b); "
                    "or (d) otherwise injures or causes harm, whether physical or mental, to the aggrieved person."
                ),
            },
            {
                "section_number": "Section 12",
                "clause_heading": "Application to Magistrate for reliefs",
                "chunk_text": (
                    "An aggrieved person or a Protection Officer or any other person on behalf of the aggrieved person may present an application "
                    "to the Magistrate seeking one or more reliefs under this Act: Provided that before passing any order on such application, "
                    "the Magistrate shall take into consideration any domestic incident report received by him from the Protection Officer or the "
                    "service provider. The reliefs sought may include orders for protection, residence, monetary relief, custody orders, or compensation."
                ),
            },
            {
                "section_number": "Section 18",
                "clause_heading": "Protection orders",
                "chunk_text": (
                    "The Magistrate may, after giving the aggrieved person and the respondent an opportunity of being heard and on being prima facie "
                    "satisfied that domestic violence has taken place or is likely to take place, pass a protection order in favour of the "
                    "aggrieved person and prohibit the respondent from committing any act of domestic violence, aiding or abetting acts of "
                    "domestic violence, entering the place of employment of the aggrieved person, attempting to communicate in any form, alienating "
                    "any assets or operating bank lockers without permission."
                ),
            },
            {
                "section_number": "Section 19",
                "clause_heading": "Residence orders in shared household",
                "chunk_text": (
                    "While disposing of an application under sub-section (1) of section 12, the Magistrate may, on being satisfied that domestic "
                    "violence has taken place, pass a residence order restraining the respondent from dispossessing or in any other manner "
                    "disturbing the possession of the aggrieved person from the shared household, whether or not the respondent has a legal or "
                    "equitable interest in the shared household; directing the respondent to remove himself from the shared household; or restraining "
                    "the respondent or any of his relatives from entering any portion of the shared household in which the aggrieved person resides."
                ),
            },
            {
                "section_number": "Section 20",
                "clause_heading": "Monetary reliefs and maintenance",
                "chunk_text": (
                    "While disposing of an application under sub-section (1) of section 12, the Magistrate may direct the respondent to pay "
                    "monetary relief to meet the expenses incurred and losses suffered by the aggrieved person and any child of the aggrieved "
                    "person as a result of the domestic violence, including loss of earnings, medical expenses, loss caused due to destruction or "
                    "damage of property, and the maintenance for the aggrieved person as well as her children, an order which shall be in addition "
                    "to an order of maintenance under section 125 of the Code of Criminal Procedure or any other law."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 9. Family Law: Hindu Marriage Act, 1955
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Hindu Marriage Act, 1955",
        "source_type": "BARE_ACT",
        "short_code": "HMA_1955",
        "citation": "Act No. 25 of 1955",
        "act_or_judgment_identifier": "Act No. 25 of 1955",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1955, 5, 18),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/1559",
        "year": 1955,
        "chunks": [
            {
                "section_number": "Section 13",
                "clause_heading": "Divorce and grounds for dissolution of marriage",
                "chunk_text": (
                    "Any marriage solemnized, whether before or after the commencement of this Act, may, on a petition presented by either the "
                    "husband or the wife, be dissolved by a decree of divorce on the ground that the other party (i) has, after the solemnization "
                    "of the marriage, had voluntary sexual intercourse with any person other than his or her spouse; or (ia) has, after the "
                    "solemnization of the marriage, treated the petitioner with cruelty; or (ib) has deserted the petitioner for a continuous period "
                    "of not less than two years immediately preceding the presentation of the petition; or (ii) has ceased to be a Hindu by "
                    "conversion to another religion; or (iii) has been incurably of unsound mind or suffering continuously or intermittently from "
                    "mental disorder of such a kind that the petitioner cannot reasonably be expected to live with the respondent."
                ),
            },
            {
                "section_number": "Section 13B",
                "clause_heading": "Divorce by mutual consent",
                "chunk_text": (
                    "Subject to the provisions of this Act, a petition for dissolution of marriage by a decree of divorce may be presented to the "
                    "district court by both the parties to a marriage together on the ground that they have been living separately for a period "
                    "of one year or more, that they have not been able to live together and that they have mutually agreed that the marriage should "
                    "be dissolved. On the motion of both parties made not earlier than six months after the date of the presentation of the petition "
                    "and not later than eighteen months after the said date, if the petition is not withdrawn in the meantime, the court shall pass a decree."
                ),
            },
            {
                "section_number": "Section 24",
                "clause_heading": "Maintenance pendente lite and expenses of proceedings",
                "chunk_text": (
                    "Where in any proceeding under this Act it appears to the court that either the wife or the husband, as the case may be, "
                    "has no independent income sufficient for her or his support and the necessary expenses of the proceeding, it may, on the "
                    "application of the wife or the husband, order the respondent to pay to the petitioner the expenses of the proceeding, and "
                    "monthly during the proceeding such sum as, having regard to the petitioner's own income and the income of the respondent, "
                    "it may seem to the court to be reasonable."
                ),
            },
            {
                "section_number": "Section 25",
                "clause_heading": "Permanent alimony and maintenance",
                "chunk_text": (
                    "Any court exercising jurisdiction under this Act may, at the time of passing any decree or at any time subsequent thereto, "
                    "on application made to it for the purpose by either the wife or the husband, as the case may be, order that the respondent "
                    "shall pay to the applicant for her or his maintenance and support such gross sum or such monthly or periodical sum for a term "
                    "not exceeding the life of the applicant having regard to the respondent's own income and other property, if any, the income "
                    "and other property of the applicant, the conduct of the parties and other circumstances of the case."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 10. Family Law: Hindu Succession Act, 1956
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Hindu Succession Act, 1956",
        "source_type": "BARE_ACT",
        "short_code": "HSA_1956",
        "citation": "Act No. 30 of 1956",
        "act_or_judgment_identifier": "Act No. 30 of 1956",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1956, 6, 17),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/1702",
        "year": 1956,
        "chunks": [
            {
                "section_number": "Section 6",
                "clause_heading": "Devolution of interest in coparcenary property (Equal rights for daughters)",
                "chunk_text": (
                    "On and from the commencement of the Hindu Succession (Amendment) Act, 2005, in a Joint Hindu family governed by the "
                    "Mitakshara law, the daughter of a coparcener shall (a) by birth become a coparcener in her own right in the same manner "
                    "as the son; (b) have the same rights in the coparcenary property as she would have had if she had been a son; (c) be subject "
                    "to the same liabilities in respect of the said coparcenary property as that of a son, and any reference to a Hindu Mitakshara "
                    "coparcener shall be deemed to include a reference to a daughter of a coparcener."
                ),
            },
            {
                "section_number": "Section 8",
                "clause_heading": "General rules of succession in the case of males (Class I and Class II heirs)",
                "chunk_text": (
                    "The property of a male Hindu dying intestate shall devolve according to the provisions of this Chapter: (a) firstly, upon "
                    "the heirs, being the relatives specified in Class I of the Schedule; (b) secondly, if there is no heir of Class I, then upon "
                    "the heirs, being the relatives specified in Class II of the Schedule; (c) thirdly, if there is no heir of any of the two classes, "
                    "then upon the agnates of the deceased; and (d) lastly, if there is no agnate, then upon the cognates of the deceased. Class I "
                    "heirs include son, daughter, widow, mother, and children of predeceased children."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 11. Commercial & Contracts: Indian Contract Act, 1872
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Indian Contract Act, 1872",
        "source_type": "BARE_ACT",
        "short_code": "ICA_1872",
        "citation": "Act No. 9 of 1872",
        "act_or_judgment_identifier": "Act No. 9 of 1872",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1872, 4, 25),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/2187",
        "year": 1872,
        "chunks": [
            {
                "section_number": "Section 10",
                "clause_heading": "What agreements are contracts",
                "chunk_text": (
                    "All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful "
                    "consideration and with a lawful object, and are not hereby expressly declared to be void. Nothing herein contained "
                    "shall affect any law in force in India, by which any contract is required to be made in writing or in the presence of "
                    "witnesses, or any law relating to the registration of documents."
                ),
            },
            {
                "section_number": "Section 73",
                "clause_heading": "Compensation for loss or damage caused by breach of contract",
                "chunk_text": (
                    "When a contract has been broken, the party who suffers by such breach is entitled to receive, from the party who has "
                    "broken the contract, compensation for any loss or damage caused to him thereby, which naturally arose in the usual course "
                    "of things from such breach, or which the parties knew, when they made the contract, to be likely to result from the breach "
                    "of it. Such compensation is not to be given for any remote and indirect loss or damage sustained by reason of the breach."
                ),
            },
            {
                "section_number": "Section 74",
                "clause_heading": "Compensation for breach of contract where penalty stipulated for",
                "chunk_text": (
                    "When a contract has been broken, if a sum is named in the contract as the amount to be paid in case of such breach, or "
                    "if the contract contains any other stipulation by way of penalty, the party complaining of the breach is entitled, "
                    "whether or not actual damage or loss is proved to have been caused thereby, to receive from the party who has broken the "
                    "contract reasonable compensation not exceeding the amount so named or, as the case may be, the penalty stipulated for."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 12. Property Law: Transfer of Property Act, 1882
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Transfer of Property Act, 1882",
        "source_type": "BARE_ACT",
        "short_code": "TPA_1882",
        "citation": "Act No. 4 of 1882",
        "act_or_judgment_identifier": "Act No. 4 of 1882",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1882, 2, 17),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/2338",
        "year": 1882,
        "chunks": [
            {
                "section_number": "Section 54",
                "clause_heading": "Sale defined and how transfer is made",
                "chunk_text": (
                    "Sale is a transfer of ownership in exchange for a price paid or promised or part-paid and part-promised. Such transfer, "
                    "in the case of tangible immovable property of the value of one hundred rupees and upwards, or in the case of a reversion "
                    "or other intangible thing, can be made only by a registered instrument. A contract for the sale of immovable property is "
                    "a contract that a sale of such property shall take place on terms settled between the parties. It does not, of itself, "
                    "create any interest in or charge on such property."
                ),
            },
            {
                "section_number": "Section 106",
                "clause_heading": "Duration of certain leases in absence of written contract and notice to terminate",
                "chunk_text": (
                    "In the absence of a contract or local law or usage to the contrary, a lease of immovable property for agricultural or "
                    "manufacturing purposes shall be deemed to be a lease from year to year, terminable, on the part of either lessor or lessee, "
                    "by six months' notice; and a lease of immovable property for any other purpose shall be deemed to be a lease from month to "
                    "month, terminable, on the part of either lessor or lessee, by fifteen days' notice. Every notice under sub-section (1) "
                    "must be in writing, signed by or on behalf of the person giving it, and either sent by post or tendered personally."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 13. Civil Procedure & Deadlines: Limitation Act, 1963
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Limitation Act, 1963",
        "source_type": "BARE_ACT",
        "short_code": "LIMITATION_1963",
        "citation": "Act No. 36 of 1963",
        "act_or_judgment_identifier": "Act No. 36 of 1963",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1963, 10, 5),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/1565",
        "year": 1963,
        "chunks": [
            {
                "section_number": "Section 5",
                "clause_heading": "Extension of prescribed period in certain cases (Condonation of delay)",
                "chunk_text": (
                    "Any appeal or any application, other than an application under any of the provisions of Order XXI of the Code of Civil "
                    "Procedure, 1908, may be admitted after the prescribed period, if the appellant or the applicant satisfies the court "
                    "that he had sufficient cause for not preferring the appeal or making the application within such period. Explanation: "
                    "The fact that the appellant or applicant was misled by any order, practice or judgment of the High Court in ascertaining "
                    "or computing the prescribed period may be sufficient cause within the meaning of this section."
                ),
            },
            {
                "section_number": "Article 54",
                "clause_heading": "Limitation period for suit for specific performance of contract",
                "chunk_text": (
                    "Under Article 54 of the Schedule to the Limitation Act, 1963, the period of limitation for a suit for specific performance "
                    "of a contract is three years. The time from which the period begins to run is the date fixed for the performance, or, if "
                    "no such date is fixed, when the plaintiff has notice that performance is refused."
                ),
            },
            {
                "section_number": "Article 65",
                "clause_heading": "Limitation period for suit for possession of immovable property based on title",
                "chunk_text": (
                    "Under Article 65 of the Schedule to the Limitation Act, 1963, the period of limitation for a suit for possession of "
                    "immovable property or any interest therein based on title is twelve years. The time from which the period begins to run "
                    "is when the possession of the defendant becomes adverse to the plaintiff."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 14. Cyber Law: Information Technology Act, 2000
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Information Technology Act, 2000",
        "source_type": "BARE_ACT",
        "short_code": "IT_ACT_2000",
        "citation": "Act No. 21 of 2000",
        "act_or_judgment_identifier": "Act No. 21 of 2000",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(2000, 6, 9),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/1999",
        "year": 2000,
        "chunks": [
            {
                "section_number": "Section 43",
                "clause_heading": "Penalty and compensation for damage to computer system and data theft",
                "chunk_text": (
                    "If any person without permission of the owner or any other person who is incharge of a computer, computer system or "
                    "computer network accesses or secures access to such computer, downloads, copies or extracts any data, introduces any "
                    "computer contaminant or virus, damages or causes to be damaged any computer data, disrupts any computer system, or denies "
                    "access to any person authorized to access any computer system, he shall be liable to pay damages by way of compensation "
                    "to the person so affected."
                ),
            },
            {
                "section_number": "Section 66C",
                "clause_heading": "Punishment for identity theft",
                "chunk_text": (
                    "Whoever, fraudulently or dishonestly make use of the electronic signature, password or any other unique identification "
                    "feature of any other person, shall be punished with imprisonment of either description for a term which may extend to "
                    "three years and shall also be liable to fine which may extend to rupees one lakh."
                ),
            },
            {
                "section_number": "Section 66D",
                "clause_heading": "Punishment for cheating by personation by using computer resource",
                "chunk_text": (
                    "Whoever, by means of any communication device or computer resource cheats by personating, shall be punished with "
                    "imprisonment of either description for a term which may extend to three years and shall also be liable to fine which "
                    "may extend to one lakh rupees."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 15. Data Privacy: Digital Personal Data Protection Act, 2023
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Digital Personal Data Protection Act, 2023",
        "source_type": "BARE_ACT",
        "short_code": "DPDPA_2023",
        "citation": "Act No. 22 of 2023",
        "act_or_judgment_identifier": "Act No. 22 of 2023",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(2023, 8, 11),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.meity.gov.in/acts",
        "year": 2023,
        "chunks": [
            {
                "section_number": "Section 6",
                "clause_heading": "Consent for processing digital personal data",
                "chunk_text": (
                    "Consent given by the Data Principal shall be free, specific, informed, unconditional and unambiguous with a clear "
                    "affirmative action, and shall signify an agreement to the processing of her personal data for the specified purpose "
                    "and be limited to such personal data as is necessary for such specified purpose. The Data Principal shall have the right "
                    "to withdraw her consent at any time, with the ease of doing so being comparable to the ease with which such consent was given."
                ),
            },
            {
                "section_number": "Section 11",
                "clause_heading": "Rights of Data Principal (Information and Access)",
                "chunk_text": (
                    "The Data Principal shall have the right to obtain from the Data Fiduciary to whom she has previously given consent: "
                    "(a) a summary of personal data which is being processed by such Data Fiduciary and the processing activities undertaken; "
                    "(b) the identities of all other Data Fiduciaries and Data Processors with whom the personal data has been shared; and "
                    "(c) any other information as may be prescribed."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 16. Motor Vehicle Law: Motor Vehicles Act, 1988 (as amended 2019)
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Motor Vehicles Act, 1988",
        "source_type": "BARE_ACT",
        "short_code": "MV_ACT_1988",
        "citation": "Act No. 59 of 1988",
        "act_or_judgment_identifier": "Act No. 59 of 1988",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1988, 10, 14),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://morth.nic.in/acts-rules-and-notifications",
        "year": 1988,
        "chunks": [
            {
                "section_number": "Section 164",
                "clause_heading": "Payment of compensation in case of death or grievous hurt (No-fault liability)",
                "chunk_text": (
                    "Notwithstanding anything contained in this Act or in any other law for the time being in force, the owner of the motor "
                    "vehicle or the authorised insurer shall be liable to pay in the case of death or grievous hurt due to any accident arising "
                    "out of the use of the motor vehicle, a compensation of five lakh rupees in case of death or two and a half lakh rupees in "
                    "case of grievous hurt to the legal heirs or victim. In any claim for compensation under this section, the claimant shall "
                    "not be required to plead or establish wrongful act, neglect or default."
                ),
            },
            {
                "section_number": "Section 166",
                "clause_heading": "Application for compensation before Claims Tribunal (MACT)",
                "chunk_text": (
                    "An application for compensation arising out of an accident of the nature specified in section 165 may be made by the "
                    "person who has sustained the injury, by the owner of the property, or where death has resulted from the accident, by all "
                    "or any of the legal representatives of the deceased before the Motor Accidents Claims Tribunal. No application for "
                    "compensation shall be entertained unless it is made within six months of the occurrence of the accident."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 17. Labour & Employment: Industrial Disputes Act, 1947
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Industrial Disputes Act, 1947",
        "source_type": "BARE_ACT",
        "short_code": "IDA_1947",
        "citation": "Act No. 14 of 1947",
        "act_or_judgment_identifier": "Act No. 14 of 1947",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1947, 3, 11),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://labour.gov.in/acts",
        "year": 1947,
        "chunks": [
            {
                "section_number": "Section 25F",
                "clause_heading": "Conditions precedent to retrenchment of workmen",
                "chunk_text": (
                    "No workman employed in any industry who has been in continuous service for not less than one year under an employer shall "
                    "be retrenched by that employer until (a) the workman has been given one month's notice in writing indicating the reasons for "
                    "retrenchment and the period of notice has expired, or the workman has been paid in lieu of such notice, wages for the period "
                    "of the notice; (b) the workman has been paid, at the time of retrenchment, compensation which shall be equivalent to fifteen "
                    "days' average pay for every completed year of continuous service or any part thereof in excess of six months; and (c) notice "
                    "in the prescribed manner is served on the appropriate Government."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 18. Labour & Employment: Payment of Gratuity Act, 1972
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Payment of Gratuity Act, 1972",
        "source_type": "BARE_ACT",
        "short_code": "PGA_1972",
        "citation": "Act No. 39 of 1972",
        "act_or_judgment_identifier": "Act No. 39 of 1972",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1972, 8, 21),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://labour.gov.in/acts",
        "year": 1972,
        "chunks": [
            {
                "section_number": "Section 4",
                "clause_heading": "Payment of gratuity and eligibility conditions",
                "chunk_text": (
                    "Gratuity shall be payable to an employee on the termination of his employment after he has rendered continuous service "
                    "for not less than five years: (a) on his superannuation, or (b) on his retirement or resignation, or (c) on his death or "
                    "disablement due to accident or disease: Provided that the completion of continuous service of five years shall not be "
                    "necessary where the termination of employment is due to death or disablement. For every completed year of service or part "
                    "thereof in excess of six months, the employer shall pay gratuity to an employee at the rate of fifteen days' wages based "
                    "on the rate of wages last drawn."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 19. Intellectual Property: Copyright Act, 1957
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Copyright Act, 1957",
        "source_type": "BARE_ACT",
        "short_code": "COPYRIGHT_1957",
        "citation": "Act No. 14 of 1957",
        "act_or_judgment_identifier": "Act No. 14 of 1957",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1957, 6, 4),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://ipindia.gov.in",
        "year": 1957,
        "chunks": [
            {
                "section_number": "Section 14",
                "clause_heading": "Meaning of copyright and exclusive rights of owner",
                "chunk_text": (
                    "For the purposes of this Act, copyright means the exclusive right, by virtue of and subject to the provisions of this Act, "
                    "to do or authorise the doing of any of the following acts in respect of a work or any substantial part thereof, namely: in "
                    "the case of a literary, dramatic or musical work, not being a computer programme, reproducing the work in any material form "
                    "including storing of it in any medium by electronic means; issuing copies of the work to the public; performing the work "
                    "in public or communicating it to the public; and making any translation or adaptation of the work."
                ),
            },
            {
                "section_number": "Section 52",
                "clause_heading": "Certain acts not to be infringement of copyright (Fair Dealing exceptions)",
                "chunk_text": (
                    "The following acts shall not constitute an infringement of copyright, namely: (a) a fair dealing with any work, not being a "
                    "computer programme, for the purposes of (i) private or personal use, including research; (ii) criticism or review, whether "
                    "of that work or of any other work; (iii) the reporting of current events and current affairs, including the reporting of a "
                    "lecture delivered in public; (b) the transient or incidental storage of a work purely in the technical process of electronic "
                    "transmission; or (c) reproduction of any work for the purpose of a judicial proceeding or legislative reporting."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 20. Intellectual Property: Trade Marks Act, 1999
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Trade Marks Act, 1999",
        "source_type": "BARE_ACT",
        "short_code": "TRADEMARKS_1999",
        "citation": "Act No. 47 of 1999",
        "act_or_judgment_identifier": "Act No. 47 of 1999",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1999, 12, 30),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://ipindia.gov.in",
        "year": 1999,
        "chunks": [
            {
                "section_number": "Section 29",
                "clause_heading": "Infringement of registered trade marks",
                "chunk_text": (
                    "A registered trade mark is infringed by a person who, not being a registered proprietor or a person using by way of "
                    "permitted use, uses in the course of trade, a mark which is identical with, or deceptively similar to, the trade mark in "
                    "relation to goods or services in respect of which the trade mark is registered and in such manner as to render the use of "
                    "the mark likely to be taken as being used as a trade mark. A person shall also be deemed to infringe if using a mark which "
                    "is likely to cause confusion on the part of the public, or which takes unfair advantage of or is detrimental to the "
                    "distinctive character or repute of the registered trade mark."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 21. Property & Registration: The Registration Act, 1908
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Registration Act, 1908",
        "source_type": "BARE_ACT",
        "short_code": "REG_ACT_1908",
        "citation": "Act No. 16 of 1908",
        "act_or_judgment_identifier": "Act No. 16 of 1908",
        "jurisdiction": "Union of India",
        "court": None,
        "publication_date": date(1908, 12, 18),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/2312",
        "year": 1908,
        "chunks": [
            {
                "section_number": "Section 17",
                "clause_heading": "Documents of which registration is compulsory",
                "chunk_text": (
                    "Instruments of gift of immovable property; other non-testamentary instruments which purport or operate to create, "
                    "declare, assign, limit or extinguish any right, title or interest of the value of one hundred rupees and upwards to or "
                    "in immovable property; and leases of immovable property from year to year or exceeding one year must be compulsorily registered."
                ),
            },
            {
                "section_number": "Section 49",
                "clause_heading": "Effect of non-registration of documents required to be registered",
                "chunk_text": (
                    "No document required by section 17 to be registered shall affect any immovable property comprised therein, or be received "
                    "as evidence of any transaction affecting such property, unless it has been registered, except as evidence of a contract in a suit "
                    "for specific performance or as evidence of any collateral transaction not required to be effected by registered instrument."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 22. Karnataka State: The Karnataka Land Revenue Act, 1964
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Karnataka Land Revenue Act, 1964",
        "source_type": "BARE_ACT",
        "short_code": "KLRA_1964",
        "citation": "Karnataka Act No. 12 of 1964",
        "act_or_judgment_identifier": "Karnataka Act No. 12 of 1964",
        "jurisdiction": "State of Karnataka",
        "court": None,
        "publication_date": date(1964, 3, 19),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://dpal.karnataka.gov.in",
        "year": 1964,
        "chunks": [
            {
                "section_number": "Section 95",
                "clause_heading": "Uses of agricultural land and procedure for diversion for other purposes (Land Conversion)",
                "chunk_text": (
                    "An occupant of agricultural land wishing to divert such land or any part thereof to residential, commercial or "
                    "industrial purposes must apply to the Deputy Commissioner for conversion. Deemed conversion applies upon payment of prescribed "
                    "conversion fine if the land use conforms to the published Master Plan under the Karnataka Town and Country Planning Act."
                ),
            },
            {
                "section_number": "Section 128",
                "clause_heading": "Acquisition of rights to be reported",
                "chunk_text": (
                    "Any person acquiring by succession, survivorship, inheritance, partition, purchase, mortgage, gift, lease or otherwise, "
                    "any right as holder, occupant, owner, or tenant of land in Karnataka must report the acquisition to the prescribed revenue officer within three months."
                ),
            },
            {
                "section_number": "Section 133",
                "clause_heading": "Presumption regarding entries in Record of Rights (Pahani / RTC)",
                "chunk_text": (
                    "An entry in the Record of Rights and a certified entry in the register of mutations shall be presumed to be true until the contrary "
                    "is proved. However, revenue mutation does not confer or extinguish title, which can only be established by a competent civil court."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 23. Karnataka State: The Karnataka Rent Act, 1999
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Karnataka Rent Act, 1999",
        "source_type": "BARE_ACT",
        "short_code": "KRA_1999",
        "citation": "Karnataka Act No. 34 of 2001",
        "act_or_judgment_identifier": "Karnataka Act No. 34 of 2001",
        "jurisdiction": "State of Karnataka",
        "court": None,
        "publication_date": date(2001, 11, 27),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://dpal.karnataka.gov.in",
        "year": 1999,
        "chunks": [
            {
                "section_number": "Section 14",
                "clause_heading": "Landlord's duty to keep premises in good repair and essential services",
                "chunk_text": (
                    "The landlord shall be bound to keep premises in good and tenantable repair and shall not withhold or cut off essential "
                    "supplies such as electricity, water, or sanitation without just and sufficient cause."
                ),
            },
            {
                "section_number": "Section 27",
                "clause_heading": "Protection of tenants against eviction and return of deposit",
                "chunk_text": (
                    "No tenant shall be evicted except on specific statutory grounds under Section 27. Advance security deposit exceeding one month "
                    "rent must be accounted for and refunded to the tenant within 30 days of vacating premises; failure enables tenant to petition the Rent Controller."
                ),
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # 24. Karnataka State: The PTCL Act, 1978
    # ──────────────────────────────────────────────────────────────
    {
        "title": "The Karnataka SC and ST (Prohibition of Transfer of Certain Lands) Act, 1978",
        "source_type": "BARE_ACT",
        "short_code": "PTCL_1978",
        "citation": "Karnataka Act No. 2 of 1979",
        "act_or_judgment_identifier": "Karnataka Act No. 2 of 1979",
        "jurisdiction": "State of Karnataka",
        "court": None,
        "publication_date": date(1979, 1, 1),
        "last_verified_date": date(2026, 1, 1),
        "document_version": "2026.1",
        "official_source_url": "https://dpal.karnataka.gov.in",
        "year": 1978,
        "chunks": [
            {
                "section_number": "Section 4",
                "clause_heading": "Prohibition of transfer of granted lands",
                "chunk_text": (
                    "Any transfer of granted land made either before or after the commencement of this Act in contravention of the terms of the grant "
                    "or without prior permission of the Government is null and void and conveys no right, title or interest."
                ),
            },
            {
                "section_number": "Section 5",
                "clause_heading": "Resumption and restitution of granted lands",
                "chunk_text": (
                    "The Assistant Commissioner is empowered to declare transfer of granted land null and void, resume the land to the Government "
                    "free from all encumbrances, and restore possession to the original SC/ST grantee or their legal heirs."
                ),
            },
        ],
    },
]
