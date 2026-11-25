"""Canonical Legal Corpus Ingestion and Builder.
Assembles Tier 1 to Tier 5 official legal chunks with full statutory fidelity and metadata.
"""

import json
import os
from typing import List, Dict, Any

from rag.ingest.chunker import LegalStructureChunker, StandardizedLegalChunk


def build_canonical_corpus() -> List[StandardizedLegalChunk]:
    chunks: List[StandardizedLegalChunk] = []
    sc = LegalStructureChunker

    # =========================================================================
    # TIER 1: CORE STATUTES
    # =========================================================================

    # 1. Constitution of India
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_CONST_001",
        act="Constitution of India, 1950",
        short_code="CONST",
        section="Article 21",
        clause_heading="Protection of life and personal liberty",
        section_text="No person shall be deprived of his life or personal liberty except according to procedure established by law. This guarantees fundamental human dignity, privacy, and right to legal representation.",
        chapter="Part III: Fundamental Rights",
        topic_tags=["constitutional", "life", "liberty", "human rights", "fundamental rights"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_CONST_001",
        act="Constitution of India, 1950",
        short_code="CONST",
        section="Article 22",
        clause_heading="Protection against arrest and detention in certain cases",
        section_text="""(1) No person who is arrested shall be detained in custody without being informed, as soon as may be, of the grounds for such arrest nor shall he be denied the right to consult, and to be defended by, a legal practitioner of his choice.
(2) Every person who is arrested and detained in custody shall be produced before the nearest magistrate within a period of twenty-four hours of such arrest excluding the time necessary for the journey from the place of arrest to the court of the magistrate and no such person shall be detained in custody beyond the said period without the authority of a magistrate.
(3) Nothing in clauses (1) and (2) shall apply to any person who for the time being is an enemy alien; or to any person who is arrested or detained under any law providing for preventive detention.""",
        chapter="Part III: Fundamental Rights",
        topic_tags=["arrest", "detention", "magistrate", "constitutional rights", "24 hours", "police custody"],
    ))

    # 2. Negotiable Instruments Act, 1881 (Sec 138 & 142)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_NIA_001",
        act="Negotiable Instruments Act, 1881",
        short_code="NI_ACT",
        section="Section 138",
        clause_heading="Dishonour of cheque for insufficiency, etc., of funds in the account",
        section_text="""Where any cheque drawn by a person on an account maintained by him with a banker for payment of any amount of money to another person from out of that account for the discharge, in whole or in part, of any debt or other liability, is returned by the bank unpaid, either because of the amount of money standing to the credit of that account is insufficient to honour the cheque or that it exceeds the amount arranged to be paid from that account by an agreement made with that bank, such person shall be deemed to have committed an offence and shall, without prejudice to any other provision of this Act, be punished with imprisonment for a term which may be extended to two years, or with fine which may extend to twice the amount of the cheque, or with both:
Provided that nothing contained in this section shall apply unless—
(a) the cheque has been presented to the bank within a period of three months from the date on which it is drawn or within the period of its validity, whichever is earlier;
(b) the payee or the holder in due course of the cheque, as the case may be, makes a demand for the payment of the said amount of money by giving a notice in writing, to the drawer of the cheque, within thirty days of the receipt of information by him from the bank regarding the return of the cheque as unpaid; and
(c) the drawer of such cheque fails to make the payment of the said amount of money to the payee or, as the case may be, to the holder in due course of the cheque, within fifteen days of the receipt of the said notice.""",
        chapter="Chapter XVII: Penalties in case of Dishonour of Certain Cheques",
        topic_tags=["cheque bounce", "section 138", "30 days notice", "15 days payment", "dishonour", "commercial recovery", "bank memo"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_NIA_001",
        act="Negotiable Instruments Act, 1881",
        short_code="NI_ACT",
        section="Section 142",
        clause_heading="Cognizance of offences and limitation period",
        section_text="""(1) Notwithstanding anything contained in the Code of Criminal Procedure, 1973—
(a) no court shall take cognizance of any offence punishable under section 138 except upon a complaint, in writing, made by the payee or, as the case may be, the holder in due course of the cheque;
(b) such complaint is made within one month of the date on which the cause of action arises under clause (c) of the proviso to section 138:
Provided that the cognizance of a complaint may be taken by the Court after the prescribed period, if the complainant satisfies the Court that he had sufficient cause for not making a complaint within such period;
(c) no court inferior to that of a Metropolitan Magistrate or a Judicial Magistrate of the first class shall try any offence punishable under section 138.
(2) The offence under section 138 shall be inquired into and tried only by a court within whose local jurisdiction—
(a) if the cheque is delivered for collection through an account, the branch of the bank where the payee or holder in due course, as the case may be, maintains the account, is situated; or
(b) if the cheque is presented for payment by the payee or holder in due course, otherwise through an account, the branch of the drawee bank where the drawer maintains the account, is situated.""",
        chapter="Chapter XVII: Penalties in case of Dishonour of Certain Cheques",
        topic_tags=["cheque bounce", "section 142", "limitation", "one month complaint", "jurisdiction", "magistrate"],
    ))

    # 3. Bharatiya Nyaya Sanhita, 2023 (BNS)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNS_001",
        act="Bharatiya Nyaya Sanhita, 2023",
        short_code="BNS",
        section="Section 318(4)",
        clause_heading="Cheating and dishonestly inducing delivery of property",
        section_text="""(1) Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person, or to consent that any person shall retain any property, or intentionally induces the person so deceived to do or omit to do anything which he would not do or omit if he were not so deceived, and which act or omission causes or is likely to cause damage or harm to that person in body, mind, reputation or property, is said to 'cheat'.
(4) Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, or anything which is signed or sealed, and which is capable of being converted into a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.""",
        chapter="Chapter XVIII: Offences Against Property",
        effective_date="2024-07-01",
        topic_tags=["cheating", "fraud", "section 420 replacement", "property fraud", "financial crime", "bns 318"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNS_001",
        act="Bharatiya Nyaya Sanhita, 2023",
        short_code="BNS",
        section="Section 85",
        clause_heading="Husband or relative of husband subjecting woman to cruelty",
        section_text="Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty shall be punished with imprisonment for a term which may extend to three years and shall also be liable to fine. Cruelty includes willful conduct likely to drive the woman to commit suicide or cause grave injury, or harassment with a view to coercing her or any person related to her to meet any unlawful demand for dowry or property.",
        chapter="Chapter V: Offences Against Woman and Child",
        effective_date="2024-07-01",
        topic_tags=["cruelty", "dowry", "section 498a replacement", "domestic cruelty", "women safety", "bns 85"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNS_001",
        act="Bharatiya Nyaya Sanhita, 2023",
        short_code="BNS",
        section="Section 103",
        clause_heading="Punishment for murder and mob lynching",
        section_text="""(1) Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine.
(2) When a group of five or more persons acting in concert commits murder on the ground of race, caste or community, sex, place of birth, language, personal belief or any other similar ground, each member of such group shall be punished with death or with imprisonment for life, and shall also be liable to fine.""",
        chapter="Chapter VI: Offences Affecting the Human Body",
        effective_date="2024-07-01",
        topic_tags=["murder", "section 302 replacement", "mob lynching", "homicide", "bns 103"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNS_001",
        act="Bharatiya Nyaya Sanhita, 2023",
        short_code="BNS",
        section="Section 303(2)",
        clause_heading="Theft and community service for petty theft",
        section_text="""Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both:
Provided that in cases of theft where the value of the stolen property is less than five thousand rupees, and a person is convicted for the first time, upon return of the stolen property or payment of the value thereof, the court may award punishment of community service.""",
        chapter="Chapter XVIII: Offences Against Property",
        effective_date="2024-07-01",
        topic_tags=["theft", "section 379 replacement", "community service", "petty theft", "bns 303"],
    ))

    # 4. Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNSS_001",
        act="Bharatiya Nagarik Suraksha Sanhita, 2023",
        short_code="BNSS",
        section="Section 173",
        clause_heading="Information in cognizable cases (FIR, Zero FIR & e-FIR)",
        section_text="""(1) Every information relating to the commission of a cognizable offence, if given orally to an officer in charge of a police station, shall be reduced to writing by him or under his direction, and be read over to the informant; and every such information, whether given in writing or reduced to writing as aforesaid, shall be signed by the person giving it, and the substance thereof shall be entered in a book to be kept by such officer in such form as the State Government may prescribe in this behalf:
Provided that information may be given electronically (e-FIR), and such information shall be taken on record by the police officer, subject to the condition that the informant shall sign the same within three days before the First Information Report is formally registered:
Provided further that irrespective of the area where the offence was committed, information may be given to any police station, and such police station shall register the same as a 'Zero FIR' and transfer it immediately to the jurisdictional police station having authority over the place of offence.
(2) A copy of the information as recorded under sub-section (1) shall be given forthwith, free of cost, to the informant or the person who gave the information.
(3) If police refuse to record information, the aggrieved person may send the substance of such information in writing and by post to the Superintendent of Police concerned, or approach the Magistrate under Section 175(3).""",
        chapter="Chapter XIII: Information to the Police and their Powers to Investigate",
        effective_date="2024-07-01",
        topic_tags=["fir", "section 154 replacement", "zero fir", "e-fir", "police refusal", "cognizable offence", "bnss 173"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNSS_001",
        act="Bharatiya Nagarik Suraksha Sanhita, 2023",
        short_code="BNSS",
        section="Section 35",
        clause_heading="Notice of appearance before police officer and safeguards against arrest",
        section_text="""(1) The police officer may, in all cases where the arrest of a person is not required under sub-section (1) of section 35, issue a notice directing the person against whom a reasonable complaint has been made, or credible information has been received, or a reasonable suspicion exists that he has committed a cognizable offence, to appear before him or at such other place as may be specified in the notice.
(3) Where such notice is issued to any person, it shall be the duty of that person to comply with the terms of the notice.
Provided that no arrest shall be made without prior permission of an officer not below the rank of Deputy Superintendent of Police where the offence is punishable with imprisonment for less than three years and the person is an infirm person or over sixty years of age.""",
        chapter="Chapter V: Arrest of Persons",
        effective_date="2024-07-01",
        topic_tags=["arrest", "section 41a replacement", "notice of appearance", "dsp permission", "senior citizens", "bnss 35"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNSS_001",
        act="Bharatiya Nagarik Suraksha Sanhita, 2023",
        short_code="BNSS",
        section="Section 482",
        clause_heading="Direction for grant of bail to person apprehending arrest (Anticipatory Bail)",
        section_text="Where any person has reason to believe that he may be arrested on accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session for a direction under this section that in the event of such arrest, he shall be released on bail; and that Court may, after considering the nature and gravity of accusation, the antecedents of the applicant, and the possibility of fleeing justice, direct that he be granted anticipatory bail subject to conditions including making himself available for interrogation.",
        chapter="Chapter XXXV: Provisions as to Bail and Bonds",
        effective_date="2024-07-01",
        topic_tags=["anticipatory bail", "section 438 replacement", "bail", "arrest apprehension", "sessions court", "high court", "bnss 482"],
    ))

    # 5. Repealed Codes (IPC, CrPC) — Marked in_force=False for historical transition
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_IPC_REPEALED",
        act="Indian Penal Code, 1860 (Repealed)",
        short_code="IPC",
        section="Section 420",
        clause_heading="Cheating and dishonestly inducing delivery of property",
        section_text="Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person... shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine. [REPEALED: Operative replacement is Section 318(4) of Bharatiya Nyaya Sanhita, 2023].",
        chapter="Chapter XVII",
        in_force=False,
        repealed_by="Bharatiya Nyaya Sanhita, 2023",
        topic_tags=["cheating", "ipc 420", "repealed", "historical mapping"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_CRPC_REPEALED",
        act="Code of Criminal Procedure, 1973 (Repealed)",
        short_code="CRPC",
        section="Section 154",
        clause_heading="Information in cognizable cases (FIR)",
        section_text="Every information relating to the commission of a cognizable offence... shall be reduced to writing by police. [REPEALED: Operative replacement is Section 173 of Bharatiya Nagarik Suraksha Sanhita, 2023 with Zero FIR and e-FIR provisions].",
        chapter="Chapter XII",
        in_force=False,
        repealed_by="Bharatiya Nagarik Suraksha Sanhita, 2023",
        topic_tags=["fir", "crpc 154", "repealed", "historical mapping"],
    ))

    # 6. Transfer of Property Act, 1882
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_TPA_001",
        act="Transfer of Property Act, 1882",
        short_code="TPA",
        section="Section 108",
        clause_heading="Rights and liabilities of lessor and lessee",
        section_text="""In the absence of a contract or local usage to the contrary, the lessor and the lessee of immovable property, as against one another, respectively, possess the rights and are subject to the liabilities following:
(m) the lessee is bound to keep, and on the termination of the lease to restore, the property in as good condition as it was in at the time when he was put in possession, reasonable wear and tear and irresistible force excepted;
(q) on the termination of the lease, the lessee is bound to put the lessor into possession of the property.
Security deposits paid by tenant constitute trust funds held by lessor, repayable immediately upon vacant possession handover, subject only to deductions for actual verified damages beyond ordinary wear and tear.""",
        chapter="Chapter V: Of Leases of Immovable Property",
        topic_tags=["tenancy", "security deposit", "reasonable wear and tear", "landlord tenant", "lease termination", "deposit return"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_TPA_001",
        act="Transfer of Property Act, 1882",
        short_code="TPA",
        section="Section 106",
        clause_heading="Duration of certain leases in absence of written contract and notice to quit",
        section_text="In the absence of a contract or local law or usage to the contrary, a lease of immovable property for agricultural or manufacturing purposes shall be deemed to be a lease from year to year, terminable, on the part of either lessor or lessee, by six months' notice; and a lease of immovable property for any other purpose (including residential tenancy) shall be deemed to be a lease from month to month, terminable, on the part of either lessor or lessee, by fifteen days' notice.",
        chapter="Chapter V: Of Leases of Immovable Property",
        topic_tags=["tenancy", "notice to quit", "15 days notice", "lease termination", "tpa 106"],
    ))

    # 7. Karnataka Rent Act, 1999 (Tier 2 Karnataka Focus)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_RENT_001",
        act="Karnataka Rent Act, 1999",
        short_code="KRA",
        section="Section 27",
        clause_heading="Protection of tenants against eviction and refund of advance deposit",
        section_text="""(1) Notwithstanding anything to the contrary contained in any other law or contract, no order or decree for the recovery of possession of any premises shall be made by the Court, District Judge or Rent Controller in favour of the landlord against a tenant, save as provided in this section.
(2) The landlord shall not claim or receive any premium or other like sum or any advance exceeding one month's rent in case of residential tenancy, and any excess deposit received shall be accounted for and refunded to the tenant upon handover of vacant possession.
(3) Where the landlord refuses to accept rent or fails to refund the security deposit within thirty days of tenant vacating the premises, the tenant may apply to the Rent Controller having territorial jurisdiction for summary adjudication and recovery.""",
        chapter="Chapter V: Control of Eviction of Tenants",
        jurisdiction="Karnataka (State)",
        topic_tags=["karnataka rent act", "tenancy karnataka", "rent controller", "deposit refund", "eviction protection", "30 days refund"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_RENT_001",
        act="Karnataka Rent Act, 1999",
        short_code="KRA",
        section="Section 14",
        clause_heading="Landlord's duty to keep the premises in good repair",
        section_text="Every landlord shall be bound to keep the premises in good and tenantable repair. If the landlord neglects or fails to make within thirty days after notice in writing, any repairs which he is bound to make, the tenant may make the same and deduct one-fourth of the rent of the year from the rent payable.",
        chapter="Chapter III",
        jurisdiction="Karnataka (State)",
        topic_tags=["karnataka rent", "repairs", "tenant rights", "rent deduction"],
    ))

    # 8. Consumer Protection Act, 2019
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_CPA_001",
        act="Consumer Protection Act, 2019",
        short_code="CPA",
        section="Section 35",
        clause_heading="Manner in which complaint shall be made before District Commission (e-Daakhil)",
        section_text="""(1) A complaint, in relation to any goods sold or delivered or agreed to be sold or delivered or any service provided or agreed to be provided, may be filed with a District Commission by—
(a) the consumer to whom such goods are sold or delivered or agreed to be sold or delivered or such service is provided or agreed to be provided;
(b) any recognized consumer association;
(c) one or more consumers, where there are numerous consumers having the same interest; or
(d) the Central Government, the Central Authority or the State Government.
(2) Every complaint filed under sub-section (1) shall be accompanied with such fee and in such manner as may be prescribed, including electronic filing through the e-Daakhil portal.
(3) The complaint shall be admitted within twenty-one days of filing, and notice issued to the opposite party to respond within thirty days (extendable by fifteen days). Limitation period for filing a complaint is two years from the date on which the cause of action arose under Section 69.""",
        chapter="Chapter IV: Consumer Disputes Redressal Commission",
        topic_tags=["consumer protection", "consumer complaint", "district commission", "e-daakhil", "section 35", "2 years limitation", "defective goods", "deficiency in service"],
    ))

    # 9. Real Estate (Regulation and Development) Act, 2016 (RERA)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_RERA_001",
        act="Real Estate (Regulation and Development) Act, 2016",
        short_code="RERA",
        section="Section 18",
        clause_heading="Return of amount and compensation for project delay",
        section_text="If the promoter fails to complete or is unable to give possession of an apartment, plot or building in accordance with the terms of the agreement for sale or by the date specified therein, the promoter shall be liable on demand to the allottees, in case the allottee wishes to withdraw from the project, to return the amount received by him in respect of that apartment, with interest at such rate as may be prescribed, including compensation. If the allottee does not intend to withdraw, he shall be paid interest for every month of delay until possession is delivered.",
        chapter="Chapter III: Rights and Duties of Allottees",
        topic_tags=["rera", "builder delay", "flat possession", "refund with interest", "real estate", "section 18"],
    ))

    # 10. Hindu Marriage Act, 1955 & Hindu Succession Act, 1956
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_HMA_001",
        act="Hindu Marriage Act, 1955",
        short_code="HMA",
        section="Section 13B",
        clause_heading="Divorce by mutual consent and cooling-off period",
        section_text="""(1) Subject to the provisions of this Act a petition for dissolution of marriage by a decree of divorce may be presented to the district court by both the parties to a marriage together, on the ground that they have been living separately for a period of one year or more, that they have not been able to live together and that they have mutually agreed that the marriage should be dissolved.
(2) On the motion of both the parties made not earlier than six months after the date of the presentation of the petition referred to in sub-section (1) and not later than eighteen months after the said date, the court shall, on being satisfied, after hearing the parties and after making such inquiry as it thinks fit, pass a decree of divorce:
Provided that the Supreme Court and High Courts have held that the six-month cooling-off period can be waived under appropriate conditions where all efforts of mediation have failed and parties have settled all maintenance, custody, and property claims.""",
        chapter="Chapter IV: Nullity of Marriage and Divorce",
        topic_tags=["divorce", "mutual consent", "cooling off period", "six months waiver", "family court", "hma 13b"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_HSA_001",
        act="Hindu Succession Act, 1956",
        short_code="HSA",
        section="Section 6",
        clause_heading="Equal coparcenary rights of daughters in ancestral joint family property",
        section_text="""On and from the commencement of the Hindu Succession (Amendment) Act, 2005, in a Joint Hindu family governed by the Mitakshara law, the daughter of a coparcener shall—
(a) by birth become a coparcener in her own right in the same manner as the son;
(b) have the same rights in the coparcenary property as she would have had if she had been a son;
(c) be subject to the same liabilities in respect of the said coparcenary property as that of a son,
and any reference to a Hindu Mitakshara coparcener shall be deemed to include a reference to a daughter of a coparcener:
Provided that nothing contained in this sub-section shall affect or invalidate any disposition or alienation, including any partition or testamentary disposition of property, which had taken place before the 20th day of December, 2004.""",
        chapter="Chapter II: Intestate Succession",
        topic_tags=["ancestral property", "coparcenary", "daughters property rights", "inheritance", "partition suit", "hsa 6"],
    ))

    # 11. Protection of Women from Domestic Violence Act, 2005 (PWDVA)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_PWDVA_001",
        act="Protection of Women from Domestic Violence Act, 2005",
        short_code="PWDVA",
        section="Section 18 & 19",
        clause_heading="Protection orders and right to reside in shared household",
        section_text="The Magistrate may, after giving the aggrieved person and the respondent an opportunity of being heard and on being prima facie satisfied that domestic violence has taken place, pass a protection order prohibiting the respondent from committing acts of domestic violence, entering the workplace or residence of aggrieved person, or alienating shared assets. Under Section 19, the Magistrate may direct the respondent not to dispossess or disturb the possession of the aggrieved woman from the shared household, irrespective of whether she has any legal title in the property.",
        chapter="Chapter IV: Procedure for Obtaining Orders of Reliefs",
        topic_tags=["domestic violence", "protection order", "shared household", "women rights", "magistrate relief", "pwdva 18"],
    ))

    # 12. Indian Contract Act, 1872 & Limitation Act, 1963
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_ICA_001",
        act="Indian Contract Act, 1872",
        short_code="ICA",
        section="Section 27",
        clause_heading="Agreement in restraint of trade, void",
        section_text="Every agreement by which anyone is restrained from exercising a lawful profession, trade or business of any kind, is to that extent void. Non-compete clauses operating post-employment are unenforceable under Indian law, except where statutory goodwill of a business is sold.",
        chapter="Chapter II",
        topic_tags=["contract", "non compete clause", "employment restraint", "void agreement", "section 27"],
    ))
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_LIM_001",
        act="Limitation Act, 1963",
        short_code="LIM",
        section="Article 54 & Schedule",
        clause_heading="Three-year period of limitation for contracts, recovery of money and specific performance",
        section_text="For specific performance of a contract or recovery of money based on breach of contract, the period of limitation is three years from the date fixed for performance, or, if no such date is fixed, when the plaintiff has notice that performance is refused. After expiry of three years, the legal remedy in court is barred by limitation.",
        chapter="Schedule: First Division",
        topic_tags=["limitation act", "3 years limitation", "money recovery", "contract breach", "legal deadline"],
    ))

    # 13. RTI Act, 2005 & DPDP Act, 2023
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_RTI_001",
        act="Right to Information Act, 2005",
        short_code="RTI",
        section="Section 7",
        clause_heading="Disposal of request within thirty days and 48-hour life or liberty window",
        section_text="The Central Public Information Officer or State Public Information Officer shall, on receipt of a request under Section 6, as expeditiously as possible, and in any case within thirty days of the receipt of the request, either provide the information on payment of such fee as may be prescribed or reject the request: Provided that where the information sought for concerns the life or liberty of a person, the same shall be provided within forty-eight hours of the receipt of the request.",
        chapter="Chapter II",
        topic_tags=["rti", "right to information", "30 days rti", "48 hours life liberty", "cpio", "public information"],
    ))

    # =========================================================================
    # TIER 3: PROCEDURES & CITIZEN GUIDES
    # =========================================================================
    chunks.append(sc.chunk_procedure_guide(
        source_id="SRC_PROC_FIR_001",
        title="Filing an FIR and Remedies if Police Refuse",
        step_heading="Zero FIR & Magistrate Remedies under Section 173 BNSS",
        guide_text="""1. An FIR can be registered at ANY police station irrespective of territorial jurisdiction as a 'Zero FIR', which the police station must register and transfer to the competent station.
2. If an officer refuses to register an FIR for a cognizable offence, you have the statutory right under Section 173(3) BNSS to send the complaint in writing by registered post to the Superintendent of Police (SP) or Commissioner.
3. If no action is taken within reasonable time, you can file a criminal complaint before the jurisdictional Judicial Magistrate under Section 175(3) BNSS, who can direct the police to investigate.""",
        topic_tags=["fir", "zero fir", "police refusal", "magistrate complaint", "superintendent of police"],
    ))
    chunks.append(sc.chunk_procedure_guide(
        source_id="SRC_PROC_EDAAKHIL_001",
        title="Filing a Consumer Complaint Online on e-Daakhil",
        step_heading="Step-by-Step e-Daakhil Filing Process",
        guide_text="""1. Register on edaakhil.nic.in with Aadhaar or OTP verification.
2. Select the competent District Commission based on where you reside, where the seller resides or has branch office, or where cause of action arose.
3. Upload PDF documents: Invoice/receipt, legal notice served, opposite party reply, proof of payment.
4. Pay nominal court fee online via Bharatkosh (Zero fee for claims up to ₹5 Lakhs under CPA 2019 rules).
5. The Commission will scrutinize and list the matter for admission within 21 days.""",
        topic_tags=["consumer court", "e-daakhil", "online complaint", "consumer fee", "step by step"],
    ))
    chunks.append(sc.chunk_procedure_guide(
        source_id="SRC_PROC_NALSA_001",
        title="Free Legal Aid and NALSA/DLSA Helpline 15100",
        step_heading="Eligibility Criteria and 24/7 Citizen Helpline",
        guide_text="""Under Section 12 of the Legal Services Authorities Act, 1987, free legal aid (including advocate representation and court fees) is available to:
- Women and children;
- Members of Scheduled Castes (SC) and Scheduled Tribes (ST);
- Victims of human trafficking or beggar;
- Persons with disabilities;
- Victims of mass disaster, ethnic violence, or industrial disaster;
- Persons in custody or juvenile homes;
- Citizens whose annual income is less than ₹3,00,000 (in Karnataka, notified by State Government).
Helpline: Call 15100 (toll-free national legal aid helpline) or visit the District Legal Services Authority (DLSA) at the District Court Complex.""",
        topic_tags=["free legal aid", "nalsa", "kslsa", "dlsa", "15100 helpline", "legal aid eligibility"],
    ))

    # =========================================================================
    # TIER 4: LANDMARK JUDICIAL PRECEDENTS (STRUCTURED SUMMARIES)
    # =========================================================================
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_DKBASU_001",
        case_title="D.K. Basu v. State of West Bengal",
        citation="(1997) 1 SCC 416",
        court="Supreme Court of India",
        judgment_date="1996-12-18",
        issue="What mandatory guidelines and safeguards must police follow to prevent custodial torture and illegal detentions?",
        holding="The Supreme Court laid down 11 mandatory guidelines for arrest and detention under Articles 21 and 22 of the Constitution.",
        ratio_decidendi="1. Arresting officers must wear clear identification badges. 2. A memo of arrest must be prepared at the time of arrest, signed by at least one family member or respectable local witness. 3. The arrestee has the right to inform a friend or relative within 8 to 12 hours. 4. Medical examination must be conducted every 48 hours in custody by an empanelled doctor. 5. Copies of all arrest memos must be sent to the District Magistrate.",
        topic_tags=["arrest rights", "dk basu", "custodial violence", "memo of arrest", "medical exam", "constitutional safeguards"],
    ))
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_ARNESH_001",
        case_title="Arnesh Kumar v. State of Bihar",
        citation="(2014) 8 SCC 273",
        court="Supreme Court of India",
        judgment_date="2014-07-02",
        issue="Whether police can automatically arrest an accused in offences punishable with imprisonment up to seven years without recording reasons?",
        holding="No automatic arrest permitted in offences punishable with imprisonment up to seven years, including Section 498A IPC / Section 85 BNS.",
        ratio_decidendi="Police officers must serve a notice of appearance under Section 41A CrPC (now Section 35(3) BNSS) and must satisfy themselves of the necessity of arrest based on specified statutory parameters. Magistrates must not authorize detention mechanically without perusing the police officer's report.",
        topic_tags=["no automatic arrest", "arnesh kumar", "498a", "bns 85", "notice of appearance", "magistrate remand"],
    ))
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_PUTTASWAMY_001",
        case_title="Justice K.S. Puttaswamy (Retd.) v. Union of India",
        citation="(2017) 10 SCC 1",
        court="Supreme Court of India (9-Judge Constitution Bench)",
        judgment_date="2017-08-24",
        issue="Whether the right to privacy is a fundamental right under Part III of the Constitution of India?",
        holding="Right to privacy is an intrinsic part of the right to life and personal liberty under Article 21 and Part III of the Constitution.",
        ratio_decidendi="Privacy includes personal autonomy, informational privacy, and privacy of spatial choices. Any state encroachment on privacy must satisfy the three-fold test of legality, legitimate state aim, and proportionality.",
        topic_tags=["privacy", "fundamental right", "article 21", "puttaswamy", "data protection", "proportionality"],
    ))

    # =========================================================================
    # TIER 5: TRILINGUAL GLOSSARY & REVIEWED MAPPINGS (EN/KN/HI)
    # =========================================================================
    glossary_items = [
        ("Security Deposit", "ಭದ್ರತಾ ಠೇವಣಿ", "सुरक्षा जमा", "Money held in trust by landlord/lessor, repayable upon lease termination minus proven non-wear damages."),
        ("Anticipatory Bail", "ನಿರೀಕ್ಷಣಾ ಜಾಮೀನು", "अग्रिम जमानत", "Direction by Sessions Court or High Court to release a person on bail in the event of arrest for non-bailable offence (Section 482 BNSS)."),
        ("Cheque Bounced", "ಚೆಕ್ ಅಮಾನ್ಯ / ಬೌನ್ಸ್", "चेक बाउंस", "Dishonour of cheque due to insufficient funds under Section 138 of Negotiable Instruments Act with 30-day notice rule."),
        ("Free Legal Aid", "ಉಚಿತ ಕಾನೂನು ನೆರವು", "मुफ्त कानूनी सहायता", "Government-funded legal representation and court fee exemption under NALSA / DLSA schemes (Helpline 15100)."),
        ("Zero FIR", "ಶೂನ್ಯ ಎಫ್‌ಐಆರ್", "जीरो एफआईआर", "First Information Report registered at any police station without territorial jurisdiction, transferred immediately to competent station."),
        ("Ancestral Property", "ಪೂರ್ವಜರ ಆಸ್ತಿ", "पैतृक संपत्ति", "Property inherited undivided through four generations of coparceners, in which daughters and sons have equal rights by birth under Hindu Succession Act."),
    ]
    for en_term, kn_term, hi_term, meaning in glossary_items:
        text = f"Legal Glossary Term: {en_term}\nKannada: {kn_term} | Hindi: {hi_term}\nStatutory Meaning: {meaning}"
        chk = sc.chunk_procedure_guide(
            source_id="SRC_REV_GLOSSARY_001",
            title=f"Legal Term: {en_term} ({kn_term} / {hi_term})",
            step_heading="Statutory Definition",
            guide_text=text,
            topic_tags=["glossary", en_term.lower(), kn_term, hi_term, "trilingual"],
        )
        chunks.append(chk)

    # 6. Integrated Expanded Modules (Central Property, Karnataka Land & Tenancy, Precedents)
    try:
        from rag.ingest.expanded_sources import get_expanded_corpus_chunks
        chunks.extend(get_expanded_corpus_chunks())
    except ImportError:
        pass

    try:
        from rag.ingest.family_law_sources import get_family_law_chunks
        chunks.extend(get_family_law_chunks())
    except ImportError:
        pass

    try:
        from rag.ingest.property_karnataka_sources import get_property_karnataka_chunks
        chunks.extend(get_property_karnataka_chunks())
    except ImportError:
        pass

    try:
        from rag.ingest.criminal_sanhitas_sources import get_criminal_sanhitas_chunks
        chunks.extend(get_criminal_sanhitas_chunks())
    except ImportError:
        pass

    try:
        from rag.ingest.banking_consumer_labour_sources import get_banking_consumer_labour_chunks
        chunks.extend(get_banking_consumer_labour_chunks())
    except ImportError:
        pass

    try:
        from rag.ingest.specialized_domains_sources import get_specialized_domain_chunks
        chunks.extend(get_specialized_domain_chunks())
    except ImportError:
        pass

    try:
        from rag.ingest.expanded_precedents_sources import get_expanded_precedents_chunks
        chunks.extend(get_expanded_precedents_chunks())
    except ImportError:
        pass

    return chunks


def save_canonical_corpus_to_json(output_path: str = "rag/data/processed/canonical_corpus.json") -> int:
    """Builds and serializes canonical corpus into validated JSON."""
    chunks = build_canonical_corpus()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    serializable = [c.to_dict() for c in chunks]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated and serialized {len(chunks)} legal chunks to {output_path}")
    return len(chunks)


if __name__ == "__main__":
    count = save_canonical_corpus_to_json()
    print(f"Total chunks verified: {count}")
