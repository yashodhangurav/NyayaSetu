"""Comprehensive Property, Real Estate & Karnataka Land Governance Chunks.
Covers Conveyancing, Registration, Adverse Possession, Karnataka Land Revenue,
Mutation, RTC/Pahani, Khata (A/B), PTCL, KOFA, BBMP, and FEMA NRI Property Rules.
"""

from typing import List
from rag.ingest.chunker import LegalStructureChunker, StandardizedLegalChunk


def get_property_karnataka_chunks() -> List[StandardizedLegalChunk]:
    chunks: List[StandardizedLegalChunk] = []
    sc = LegalStructureChunker

    # ─────────────────────────────────────────────────────────────
    # 1. CONVEYANCING & SPECIFIC RELIEF
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_REG_001",
        act="Registration Act, 1908",
        short_code="REG",
        section="Section 17 & 49",
        clause_heading="Documents compulsorily registrable and effect of non-registration",
        section_text=(
            "Section 17: Documents of which registration is compulsory include instruments of gift of immovable property, "
            "other non-testamentary instruments which purport or operate to create, declare, assign, limit or extinguish any right, title or interest "
            "of the value of one hundred rupees and upwards in immovable property, and leases exceeding one year. "
            "Section 49: No document required by section 17 to be registered shall affect any immovable property comprised therein, "
            "or be received as evidence of any transaction affecting such property, unless it has been registered."
        ),
        chapter="Of Registrable Documents",
        topic_tags=["compulsory registration", "unregistered deed invalid", "section 17", "section 49", "title evidence"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_POA_001",
        act="Powers-of-Attorney Act, 1882",
        short_code="POA",
        section="Section 2",
        clause_heading="Execution under power-of-attorney and limitation on title transfer",
        section_text=(
            "The donee of a power-of-attorney may, if he thinks fit, execute or do any assurance, instrument or thing in and with his own name "
            "and signature by the authority of the donor. "
            "Supreme Court Principle (Suraj Lamp v. State of Haryana (2012) 1 SCC 656): A General Power of Attorney (GPA) is merely an agency authorization. "
            "A GPA, Agreement to Sell, or Living Will does NOT transfer title or create ownership interest in immovable property. "
            "Ownership can be transferred solely through a duly stamped and registered Deed of Conveyance (Sale Deed) under TPA Section 54."
        ),
        chapter="General Powers of Attorney",
        topic_tags=["power of attorney", "gpa sale invalid", "suraj lamp", "title transfer requirement", "poa 1882"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_SRA_001",
        act="Specific Relief Act, 1963",
        short_code="SRA",
        section="Section 5 & 6",
        clause_heading="Recovery of specific immovable property and summary suit",
        section_text=(
            "Section 5: A person entitled to the possession of specific immovable property may recover it in the manner provided by the Code of Civil Procedure, 1908. "
            "Section 6: If any person is dispossessed without his consent of immovable property otherwise than in due course of law, "
            "he or any person claiming through him may, by suit, recover possession thereof, notwithstanding any other title that may be set up in such suit. "
            "Limitation: Suit under Section 6 must be brought within six months from the date of dispossession, and no suit lies against the Government."
        ),
        chapter="Recovering Possession of Property",
        topic_tags=["recovery of possession", "summary suit section 6", "6 month limitation", "illegal dispossession", "sra 5", "sra 6"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_SRA_001",
        act="Specific Relief Act, 1963",
        short_code="SRA",
        section="Section 34 & 38",
        clause_heading="Discretion of court as to declaration of status or right and perpetual injunction",
        section_text=(
            "Section 34: Any person entitled to any legal character, or to any right as to any property, may institute a suit against any person "
            "denying, or interested to deny, his title to such character or right, and the court may make therein a declaration that he is so entitled. "
            "Provided that no court shall make any such declaration where the plaintiff, being able to seek further relief (possession), omits to do so. "
            "Section 38: Perpetual injunction may be granted to prevent the breach of an obligation existing in favor of the applicant. "
            "Ruling (Anathula Sudhakar v. P. Buchi Reddy): Where plaintiff title is in dispute or under cloud and he is not in possession, "
            "suit for bare injunction does not lie; suit must be filed for declaration of title with consequential recovery of possession."
        ),
        chapter="Declaratory Decrees & Injunctions",
        topic_tags=["declaration of title", "perpetual injunction", "anathula sudhakar", "cloud on title", "bare injunction not maintainable"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 2. KARNATAKA LAND REVENUE & REVENUE RECORDS
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_KLR_001",
        act="Karnataka Land Revenue Act, 1964",
        short_code="KLR",
        section="Section 95",
        clause_heading="Uses of agricultural land and procedure for diversion for non-agricultural purpose",
        section_text=(
            "(1) An occupant of land assessed or held for the purpose of agriculture is entitled by himself, his servants, tenants, agents, or other legal representatives "
            "to erect farm buildings, construct wells or tanks, or make any other improvements thereon for the better cultivation of the land. "
            "(2) If any occupant of land assessed or held for agriculture wishes to divert such land or any part thereof to any other purpose (residential, commercial, industrial), "
            "he shall apply for permission to the Deputy Commissioner who may, subject to the provisions of this section and rules made thereunder, grant permission on terms. "
            "Where master plan exists under Karnataka Town and Country Planning Act, conversion operates under simplified deemed approval upon payment of statutory conversion fees."
        ),
        chapter="Use of Land and Revenue Exemptions",
        topic_tags=["land conversion", "section 95 klr", "agricultural to residential", "deputy commissioner conversion", "conversion fee"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_KLR_001",
        act="Karnataka Land Revenue Act, 1964",
        short_code="KLR",
        section="Section 127 & 128",
        clause_heading="Record of rights (RTC/Pahani) and acquisition of rights to be reported",
        section_text=(
            "Section 127: A Record of Rights (Pahani / RTC Form 16) shall be maintained in every village containing survey numbers, area, names of holders, "
            "cultivators, nature of tenure, rent, liabilities, and government water cess. "
            "Section 128: Any person acquiring by succession, survivorship, inheritance, partition, purchase, gift or otherwise, any right as holder, occupant, "
            "or mortgagee of land shall report orally or in writing his acquisition of such right to the village accountant within three months from date of acquisition. "
            "If acquired under registered deed, Sub-Registrar automatically transmits intimation (J-Slip) to Revenue authorities on Bhoomi."
        ),
        chapter="Record of Rights",
        topic_tags=["rtc pahani", "form 16", "section 128 klr", "reporting acquisition", "bhoomi j-slip", "3 month reporting"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_KLR_001",
        act="Karnataka Land Revenue Act, 1964",
        short_code="KLR",
        section="Section 129 & 136",
        clause_heading="Registration of mutations and appeal against revenue orders",
        section_text=(
            "Section 129: The Village Accountant enters every report in a register of mutations and posts a copy in the chavadi inviting objections within thirty days. "
            "If contested, the matter is registered in the register of disputed cases (Form 12) and enquired into by the Tahsildar. "
            "Section 136: Any person aggrieved by an entry or mutation order of the Tahsildar may prefer an appeal to the Assistant Commissioner within sixty days (Sec 136(2)). "
            "The Deputy Commissioner may call for records and examine legality under revision powers (Sec 136(3)). "
            "Legal Nature: Supreme Court settled (Jitendra Singh (2021)) that mutation entries in revenue records are for fiscal taxation purposes only; "
            "they do NOT confer or extinguish title. Title disputes belong exclusively to Civil Courts."
        ),
        chapter="Record of Rights",
        topic_tags=["mutation entry", "form 12 disputed mutation", "section 136(2) appeal", "ac revenue", "jitendra singh", "mutation is not title"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_KLR_001",
        act="Karnataka Land Revenue Act, 1964",
        short_code="KLR",
        section="Section 140",
        clause_heading="Determination of village and field boundaries (Phodi and Durasti)",
        section_text=(
            "The boundaries of villages and fields shall be determined and demarcated with boundary marks by survey officers. "
            "Where a survey number is sub-divided (partition or sale of fraction of agricultural holding), a Phodi survey must be conducted "
            "to carve out independent Hissa numbers and prepare a sub-division survey sketch (Tippani). "
            "Durasti is the official revenue process of rectifying boundary anomalies or missing boundary stones to match ground possession with land records."
        ),
        chapter="Boundaries and Boundary Marks",
        topic_tags=["phodi survey", "durasti", "boundary demarcation", "hissa number", "tippani sketch", "klr 140"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 3. KARNATAKA PTCL ACT (GRANTED LANDS)
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_PTCL_001",
        act="Karnataka SC & ST (Prohibition of Transfer of Certain Lands) Act, 1978",
        short_code="KAR_PTCL",
        section="Section 4 & 5",
        clause_heading="Prohibition of transfer of granted lands and resumption by Assistant Commissioner",
        section_text=(
            "Section 4: (1) Notwithstanding anything in any law, agreement, contract or instrument, any transfer of granted land made either before or after "
            "the commencement of this Act, in contravention of the terms of grant or without previous permission of the Government, shall be null and void "
            "and no right, title or interest in such land shall be conveyed or deemed ever to have conveyed by such transfer. "
            "Section 5: The Assistant Commissioner may, on application by any interested person or on information, by order declare transfer void, "
            "evict the purchaser, resume the granted land to Government, and restore it to the original grantee or their legal heirs. "
            "Limitation: Supreme Court held in Nekkanti Rama Lakshmi (2020) that PTCL restoration must be initiated within a reasonable time (typically 10-15 years); "
            "inordinate unexplained delay of decades disentitles resumption."
        ),
        chapter="Prohibition and Resumption",
        topic_tags=["ptcl act", "sc st granted land", "void alienation", "resumption by ac", "nekkanti rama lakshmi", "reasonable period limitation"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 4. BBMP ACT, 2020 (BENGALURU MUNICIPAL KHATA & BUILDING BYLAWS)
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_BBMP_001",
        act="Bruhat Bengaluru Mahanagara Palike Act, 2020",
        short_code="BBMP",
        section="Section 144 & 313",
        clause_heading="Property tax self-assessment and unauthorized building regulation",
        section_text=(
            "Section 144: Property tax is levied on all lands and buildings within BBMP limits on the basis of Unit Area Value (UAV) under Self-Assessment Scheme (SAS). "
            "A-Khata is issued for properties in layouts approved by BDA, BMRDA, or BBMP with converted land. "
            "B-Khata is an entry in the property tax collection register maintained under Section 108A KMC Act / BBMP Act for properties with building deviations, "
            "unapproved layouts, or un-converted revenue sites; B-Khata acknowledges payment of property tax but does NOT grant building sanction or legal title. "
            "Section 313 & 321: Building construction without prior sanction or in violation of building bylaws is subject to provisional notice, confirmation order, "
            "and demolition, and no Occupancy Certificate shall be issued for deviated structures."
        ),
        chapter="Taxation and Regulation of Buildings",
        topic_tags=["a-khata", "b-khata", "bbmp property tax", "sas return", "building deviation", "occupancy certificate", "bbmp 2020"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 5. KARNATAKA OWNERSHIP FLATS ACT, 1972 (APARTMENT GOVERNANCE)
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_KOFA_001",
        act="Karnataka Ownership Flats Act, 1972",
        short_code="KOFA",
        section="Section 10 & 11",
        clause_heading="Formation of co-operative society or association and conveyance of title",
        section_text=(
            "Section 10: As soon as a minimum number of persons required, or sixty percent of flat purchasers, have taken possession of flats, "
            "the promoter shall submit an application to the Registrar for registration of the organization of flat owners as a co-operative housing society "
            "or an association of flat owners under the Karnataka Apartment Ownership Act, 1972. "
            "Section 11: A promoter shall take all necessary steps to complete his title and execute a conveyance deed transferring the land, common areas, "
            "and undivided share in favour of the registered association of flat owners within the prescribed period."
        ),
        chapter="Management and Transfer of Ownership",
        topic_tags=["kofa 1972", "apartment association", "common area handover", "undivided share", "uds conveyance", "promoter duty"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 6. GRAM PANCHAYAT e-SWATHU (FORM 9 & FORM 11)
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_GRAM_001",
        act="Karnataka Gram Swaraj and Panchayat Raj Act, 1993",
        short_code="KAR_PANCHAYAT",
        section="Section 199",
        clause_heading="Property tax levy in Gram Panchayat limits and e-Swathu system",
        section_text=(
            "Gram Panchayats levy property tax on buildings and lands situated within their territorial jurisdiction. "
            "Under the Government of Karnataka e-Swathu software system, two statutory digital forms are generated: "
            "1. Form 9: Extract from the Village Site Property Register (Gramathana property), certifying the plot is situated inside original settlement limits. "
            "2. Form 11: Extract from the Property Tax Demand and Collection Register for properties situated outside old gramathana that have valid conversion orders. "
            "Mandate: Sub-Registrars in Karnataka are strictly barred from registering any deed of transfer of rural site without a digitally verified Form 9 and Form 11."
        ),
        chapter="Panchayat Taxation",
        topic_tags=["e-swathu", "form 9", "form 11", "gramathana site", "rural property registration", "panchayat property tax"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 7. FEMA REGULATIONS CONCERNING NRI IMMOVABLE PROPERTY
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_FEMA_PROP_001",
        act="FEMA (Acquisition and Transfer of Immovable Property in India) Regulations, 2018",
        short_code="FEMA_PROP",
        section="Regulation 3 & 4",
        clause_heading="Acquisition and transfer of property in India by NRI and OCI",
        section_text=(
            "Regulation 3: A Non-Resident Indian (NRI) or an Overseas Citizen of India (OCI) may acquire any immovable property in India "
            "other than agricultural land, farm house, or plantation property. "
            "Payment for acquisition must be made out of funds received in India through normal banking channels by inward remittance "
            "or debit to NRE/FCNR(B)/NRO account of the person. "
            "Regulation 4: An NRI or OCI may transfer any immovable property in India to a person resident in India, or transfer non-agricultural property "
            "to an NRI or OCI. Sale proceeds may be repatriated abroad up to USD 1,000,000 per financial year subject to payment of applicable capital gains taxes."
        ),
        chapter="NRI Property Acquisition",
        topic_tags=["nri property in india", "oci property purchase", "agricultural land ban nri", "repatriation 1 million usd", "fema property 2018"],
    ))

    return chunks
