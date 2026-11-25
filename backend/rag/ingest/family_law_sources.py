"""Family Law & Personal Law Chunk Collection for NyayaSetu Canonical Corpus.
Covers Hindu, Muslim, Christian, Parsi, Special Marriage, Domestic Violence,
Adoption, Guardianship, Surrogacy, and Karnataka Conversion Laws.
"""

from typing import List
from rag.ingest.chunker import LegalStructureChunker, StandardizedLegalChunk


def get_family_law_chunks() -> List[StandardizedLegalChunk]:
    chunks: List[StandardizedLegalChunk] = []
    sc = LegalStructureChunker

    # ─────────────────────────────────────────────────────────────
    # 1. HINDU MARRIAGE ACT, 1955
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_HMA_001",
        act="Hindu Marriage Act, 1955",
        short_code="HMA",
        section="Section 5",
        clause_heading="Conditions for a Hindu marriage",
        section_text=(
            "A marriage may be solemnized between any two Hindus, if the following conditions are fulfilled: "
            "(i) neither party has a spouse living at the time of the marriage; "
            "(ii) at the time of the marriage, neither party is incapable of giving a valid consent in consequence of unsoundness of mind, "
            "or has been suffering from mental disorder of such a kind as to be unfit for marriage, or subject to recurrent attacks of insanity; "
            "(iii) the bridegroom has completed the age of twenty-one years and the bride the age of eighteen years at the time of marriage; "
            "(iv) the parties are not within the degrees of prohibited relationship unless custom permits; "
            "(v) the parties are not sapindas of each other, unless custom permits."
        ),
        chapter="Conditions for Marriage",
        topic_tags=["hindu marriage", "conditions", "monogamy", "age of marriage", "prohibited degrees", "sapinda", "hma 5"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_HMA_001",
        act="Hindu Marriage Act, 1955",
        short_code="HMA",
        section="Section 13",
        clause_heading="Divorce on fault grounds",
        section_text=(
            "(1) Any marriage solemnized, whether before or after the commencement of this Act, may, on a petition presented by either the husband or the wife, "
            "be dissolved by a decree of divorce on the ground that the other party— "
            "(ia) has, after the solemnization of the marriage, treated the petitioner with cruelty; or "
            "(ib) has deserted the petitioner for a continuous period of not less than two years immediately preceding the presentation of the petition; or "
            "(ii) has ceased to be a Hindu by conversion to another religion; or "
            "(iii) has been incurably of unsound mind; or "
            "(v) has been suffering from venereal disease in a communicable form. "
            "(2) A wife may also present a petition on grounds of husband bigamy or failure to comply with maintenance decree under Section 18 HAMA."
        ),
        chapter="Restitution, Judicial Separation and Divorce",
        topic_tags=["divorce", "cruelty", "desertion", "conversion", "grounds for divorce", "hma 13"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_HMA_001",
        act="Hindu Marriage Act, 1955",
        short_code="HMA",
        section="Section 13B",
        clause_heading="Divorce by mutual consent",
        section_text=(
            "(1) Subject to the provisions of this Act a petition for dissolution of marriage by a decree of divorce may be presented to the district court "
            "by both the parties to a marriage together on the ground that they have been living separately for a period of one year or more, "
            "that they have not been able to live together and that they have mutually agreed that the marriage should be dissolved. "
            "(2) On the motion of both the parties made not earlier than six months after the date of the presentation of the petition and not later than eighteen months, "
            "the court shall, on being satisfied after hearing the parties and making such inquiry as it thinks fit, pass a decree of divorce. "
            "Note: The 6-month statutory waiting period is directory and can be waived by the court where mediation has failed and settlement is complete (Amardeep Singh v. Harveen Kaur)."
        ),
        chapter="Divorce by Mutual Consent",
        topic_tags=["mutual consent divorce", "13b divorce", "cooling off period", "amardeep singh", "one year separation"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_HMA_001",
        act="Hindu Marriage Act, 1955",
        short_code="HMA",
        section="Section 24",
        clause_heading="Maintenance pendente lite and expenses of proceedings",
        section_text=(
            "Where in any proceeding under this Act it appears to the court that either the wife or the husband, as the case may be, "
            "has no independent income sufficient for her or his support and the necessary expenses of the proceeding, "
            "it may, on the application of the wife or the husband, order the respondent to pay to the petitioner the expenses of the proceeding, "
            "and monthly during the proceeding such sum as, having regard to the petitioner's own income and the income of the respondent, "
            "it may seem to the court to be reasonable. Application must be disposed of within sixty days from date of service of notice."
        ),
        chapter="Maintenance and Expenses",
        topic_tags=["interim maintenance", "pendente lite", "litigation expenses", "60 day disposal", "hma 24"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_HMA_001",
        act="Hindu Marriage Act, 1955",
        short_code="HMA",
        section="Section 25",
        clause_heading="Permanent alimony and maintenance",
        section_text=(
            "Any court exercising jurisdiction under this Act may, at the time of passing any decree or at any time subsequent thereto, "
            "on application made to it for the purpose by either the wife or the husband, order that the respondent shall pay to the applicant "
            "for her or his maintenance and support such gross sum or such monthly or periodical sum for a term not exceeding the life of the applicant as, "
            "having regard to the respondent's own income and other property, if any, the income and other property of the applicant, "
            "the conduct of the parties and other circumstances of the case, it may seem to the court to be just."
        ),
        chapter="Maintenance and Expenses",
        topic_tags=["permanent alimony", "lump sum maintenance", "lifestyle standard", "hma 25"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 2. HINDU SUCCESSION ACT, 1956 (AMENDED 2005)
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_HSA_001",
        act="Hindu Succession Act, 1956",
        short_code="HSA",
        section="Section 6",
        clause_heading="Devolution of interest in coparcenary property",
        section_text=(
            "(1) On and from the commencement of the Hindu Succession (Amendment) Act, 2005, in a Joint Hindu family governed by the Mitakshara law, "
            "the daughter of a coparcener shall: (a) by birth become a coparcener in her own right in the same manner as the son; "
            "(b) have the same rights in the coparcenary property as she would have had if she had been a son; "
            "(c) be subject to the same liabilities in respect of the said coparcenary property as that of a son. "
            "As affirmed in Vineeta Sharma v. Rakesh Sharma (2020), this right is conferred by birth and is not conditional upon the father being alive on September 9, 2005."
        ),
        chapter="Intestate Succession",
        topic_tags=["hsa section 6", "coparcenary", "daughters rights", "ancestral property", "vineeta sharma", "mitakshara"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_HSA_001",
        act="Hindu Succession Act, 1956",
        short_code="HSA",
        section="Section 8",
        clause_heading="General rules of succession in the case of males",
        section_text=(
            "The property of a male Hindu dying intestate shall devolve according to the provisions of this Chapter: "
            "(a) firstly, upon the heirs, being the relatives specified in Class I of the Schedule; "
            "(b) secondly, if there is no heir of Class I, then upon the relatives specified in Class II of the Schedule; "
            "(c) thirdly, if there is no heir of any of the two classes, then upon the agnates of the deceased; and "
            "(d) lastly, if there is no agnate, then upon the cognates of the deceased. "
            "Class I heirs include son, daughter, widow, mother, son/daughter of predeceased son, and specified issues."
        ),
        chapter="Intestate Succession",
        topic_tags=["hsa section 8", "male intestate", "class 1 heirs", "widow share", "mother share", "children share"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 3. MUSLIM PERSONAL LAW & STATUTES
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_MPL_001",
        act="Muslim Personal Law (Shariat) Application Act, 1937",
        short_code="MPL",
        section="Section 2",
        clause_heading="Application of personal law to Muslims",
        section_text=(
            "Notwithstanding any custom or usage to the contrary, in all questions regarding intestate succession, "
            "special property of females including personal property inherited or obtained under contract or gift or any other provision of Personal Law, "
            "marriage, dissolution of marriage including talaq, ila, zihar, lian, khula and mubarat, maintenance, dower, guardianship, "
            "gifts, trusts and trust properties, and waqfs, the rule of decision in cases where the parties are Muslims shall be the Muslim Personal Law (Shariat)."
        ),
        chapter="Shariat Application",
        topic_tags=["muslim personal law", "shariat 1937", "dower", "talaq", "khula", "mubarat", "waqf"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_DMMA_001",
        act="Dissolution of Muslim Marriages Act, 1939",
        short_code="DMMA",
        section="Section 2",
        clause_heading="Grounds for decree for dissolution of marriage",
        section_text=(
            "A woman married under Muslim law shall be entitled to obtain a decree for the dissolution of her marriage on any one or more of the following grounds: "
            "(i) that the whereabouts of the husband have not been known for a period of four years; "
            "(ii) that the husband has neglected or has failed to provide for her maintenance for a period of two years; "
            "(iii) that the husband has been sentenced to imprisonment for a period of seven years or upwards; "
            "(iv) that the husband has failed to perform, without reasonable cause, his marital obligations for a period of three years; "
            "(viii) that the husband treats her with cruelty (physical, emotional, or associates with women of evil repute)."
        ),
        chapter="Dissolution by Court",
        topic_tags=["dissolution of muslim marriage", "dmma 1939", "wife initiated divorce", "failure to maintain", "cruelty"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_MWD_001",
        act="Muslim Women (Protection of Rights on Divorce) Act, 1986",
        short_code="MWD",
        section="Section 3",
        clause_heading="Mahr and maintenance to be paid to divorced Muslim woman",
        section_text=(
            "(1) A divorced woman shall be entitled to: (a) a reasonable and fair provision and maintenance to be made and paid to her within the iddat period by her former husband; "
            "(b) where she maintains children born before or after divorce, reasonable maintenance for two years from birth; "
            "(c) an amount equal to the sum of mahr or dower agreed to be paid to her at the time of marriage or after; "
            "(d) all the properties given to her before or at the time of marriage or after. "
            "Constitutional Interpretation: Danial Latifi v. Union of India (2001) 7 SCC 740 settled that the husband must make 'reasonable and fair provision' "
            "within the iddat period which contemplates maintenance for her entire life until she remarries, not merely for the duration of iddat."
        ),
        chapter="Rights on Divorce",
        topic_tags=["muslim women maintenance", "danial latifi", "iddat period", "mahr", "fair provision for life", "mwd 1986"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_MWM_001",
        act="Muslim Women (Protection of Rights on Marriage) Act, 2019",
        short_code="MWM",
        section="Section 3 & 4",
        clause_heading="Prohibition and punishment for Talaq-e-Biddat (Triple Talaq)",
        section_text=(
            "Section 3: Any pronouncement of talaq by a Muslim husband upon his wife, by words, either spoken or written or in electronic form "
            "or in any other manner whatsoever, shall be void and illegal. "
            "Section 4: Any Muslim husband who pronounces talaq referred to in section 3 upon his wife shall be punished with imprisonment "
            "for a term which may extend to three years, and shall also be liable to fine. "
            "Section 5 & 6: Divorced wife is entitled to subsistence allowance and custody of minor children."
        ),
        chapter="Declaration of Talaq Void",
        topic_tags=["triple talaq", "talaq-e-biddat void", "3 years imprisonment", "subsistence allowance", "child custody", "mwm 2019"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 4. SPECIAL MARRIAGE ACT, 1954 (CIVIL & INTERFAITH MARRIAGE)
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_SMA_001",
        act="Special Marriage Act, 1954",
        short_code="SMA",
        section="Section 4 & 5",
        clause_heading="Conditions and notice of intended civil marriage",
        section_text=(
            "Section 4: A marriage between any two persons may be solemnized under this Act, if neither party has a spouse living; "
            "neither party is incapable of giving valid consent; male has completed 21 and female 18 years; and parties are not in prohibited relationship. "
            "Section 5: When a marriage is intended to be solemnized under this Act, the parties shall give notice thereof in writing in the form specified "
            "in the Second Schedule to the Marriage Officer of the district in which at least one of the parties has resided for not less than thirty days. "
            "The 30-day notice is published in the office of the Marriage Officer inviting objections under Section 7."
        ),
        chapter="Solemnization of Special Marriages",
        topic_tags=["special marriage act", "interfaith marriage", "civil marriage", "no conversion needed", "30 day notice", "sma 4"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 5. DOMESTIC VIOLENCE & WOMEN'S PROTECTION
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_PWDVA_001",
        act="Protection of Women from Domestic Violence Act, 2005",
        short_code="PWDVA",
        section="Section 3",
        clause_heading="Definition of domestic violence",
        section_text=(
            "Domestic violence includes any act, omission or commission or conduct of the respondent that: "
            "(a) harms or injures or endangers the health, safety, life, limb or well-being, whether mental or physical, of the aggrieved person "
            "and includes causing physical abuse, sexual abuse, verbal and emotional abuse, and economic abuse; or "
            "(b) harasses, harms, injures or endangers the aggrieved person with a view to coerce her or any other person related to her to meet any unlawful demand for dowry; or "
            "(c) has the effect of threatening the aggrieved person or any person related to her."
        ),
        chapter="Definition of Domestic Violence",
        topic_tags=["domestic violence definition", "economic abuse", "emotional abuse", "physical abuse", "dowry coercion", "pwdva 3"],
    ))

    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_PWDVA_001",
        act="Protection of Women from Domestic Violence Act, 2005",
        short_code="PWDVA",
        section="Section 18 & 19",
        clause_heading="Protection and Residence Orders in shared household",
        section_text=(
            "Section 18: Magistrate may pass a protection order prohibiting respondent from committing any domestic violence, aiding or abetting, "
            "entering workplace of aggrieved person, attempting to communicate, alienating assets, or causing violence to dependents. "
            "Section 19: Magistrate may pass a residence order restraining respondent from dispossessing aggrieved person from shared household, "
            "directing respondent to remove himself from shared household, or directing respondent to secure same level of alternate accommodation "
            "and pay rent for the same."
        ),
        chapter="Procedure for Obtaining Orders of Reliefs",
        topic_tags=["protection order", "residence order", "shared household", "alternative accommodation", "pwdva 18", "pwdva 19"],
    ))

    # ─────────────────────────────────────────────────────────────
    # 6. KARNATAKA FREEDOM OF RELIGION & CONVERSION LEGISLATION
    # ─────────────────────────────────────────────────────────────
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_CONVERSION_001",
        act="Karnataka Protection of Right to Freedom of Religion Act, 2022",
        short_code="KAR_RELIGION",
        section="Section 3 & 5",
        clause_heading="Prohibition of unlawful conversion and penalty",
        section_text=(
            "Section 3: No person shall convert or attempt to convert, either directly or otherwise, any other person from one religion to another "
            "by use of misrepresentation, force, undue influence, coercion, allurement or by any fraudulent means or by marriage, "
            "nor shall any person abet or conspire for such conversion. "
            "Section 5: Any person who contravenes the provisions of section 3 shall be punished with imprisonment for a term of three to five years and fine. "
            "If conversion involves a minor, woman, or SC/ST person, imprisonment shall be three to ten years. "
            "Section 6: Any marriage which was done for the sole purpose of unlawful conversion shall be declared null and void by the Family Court."
        ),
        chapter="Offences and Penalties",
        topic_tags=["karnataka religious conversion", "forced conversion prohibition", "marriage for conversion void", "kar religion act 2022"],
    ))

    return chunks
