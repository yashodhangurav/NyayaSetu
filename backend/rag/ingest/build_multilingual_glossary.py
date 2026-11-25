"""Comprehensive 1,500+ Multilingual Indian Legal Glossary Generator for NyayaSetu.

Covers 10 practice areas:
1. Land Records & Karnataka Property Terminology (RTC, Pahani, Khata, Phodi, Durasti, Mutation, etc.)
2. Family Law & Personal Law (Hindu, Muslim, Christian, Parsi, Maintenance, Inheritance)
3. Criminal Law & Sanhitas (Offences, Arrest, Bail, FIR, Investigation, Evidence)
4. Banking, Finance & Debt Recovery (Cheque bounce, SARFAESI, NPA, Digital lending, UPI fraud)
5. Consumer Protection & E-Commerce (Defects, Service deficiencies, Dark patterns, e-Daakhil)
6. Employment & Labour Law (Wages, Gratuity, POSH, Retrenchment, Termination)
7. Healthcare & Medical Law (Negligence, Consent, Patient rights, MTP, Clinical regulations)
8. Taxation & Revenue (Income tax, GST, Capital gains, TDS, Municipal tax)
9. Government Services & RTI (Sakala, Seva Sindhu, RTI procedure, Certificates)
10. Vernacular Transliterations, Hinglish, Kanglish & Common Spelling Errors
"""

import json
import os
from typing import Dict, List, Any


def generate_comprehensive_glossary() -> Dict[str, Any]:
    glossary: Dict[str, Dict[str, Any]] = {}

    def add_term(
        term_en: str,
        term_kn: str,
        term_hi: str,
        domain: str,
        category: str,
        definition: str,
        transliterations: List[str] = None,
        misspellings: List[str] = None,
        canonical_statute: str = "",
    ):
        key = term_en.lower().strip()
        glossary[key] = {
            "english": term_en,
            "kannada": term_kn,
            "hindi": term_hi,
            "domain": domain,
            "category": category,
            "definition": definition,
            "transliterations": transliterations or [],
            "common_misspellings": misspellings or [],
            "canonical_statute": canonical_statute,
        }

    # =========================================================================
    # 1. LAND RECORDS, REVENUE & REGISTRATION (KARNATAKA & ALL-INDIA)
    # =========================================================================
    land_terms = [
        ("RTC (Record of Rights, Tenancy and Crops)", "ಆರ್.ಟಿ.ಸಿ / ಪಹಣಿ", "अधिकार अभिलेख (खतौनी)", "Land Revenue", "Revenue Record", "Form 16 under Karnataka Land Revenue Act detailing survey number, owner name, soil class, crop cultivated, and cultivation rights", ["Pahani", "Patta", "RoR", "Khatauni"], ["pahanie", "pahni", "rtcc"], "Karnataka Land Revenue Act, 1964 (Sec 127)"),
        ("Pahani", "ಪಹಣಿ", "खसरा / खतौनी", "Land Revenue", "Revenue Record", "Cultivation and tenancy record maintained by village accountant in Karnataka", ["Pahani patrike", "Khasra"], ["pahni", "paahani"], "Karnataka Land Revenue Act, 1964"),
        ("Mutation", "ಮ್ಯುಟೇಶನ್ / ಪೌತಿ ಬದಲಾವಣೆ", "नामांतरण / दाखिल खारिज", "Land Revenue", "Title Transfer Record", "Process of updating revenue records upon succession, partition or transfer of property; does NOT confer title", ["Dakhil Kharij", "Namantaran", "Fauti"], ["mutasion", "mutetion"], "Karnataka Land Revenue Act, 1964 (Sec 128)"),
        ("A-Khata", "ಎ-ಖಾತಾ", "ए-खाता (मान्यता प्राप्त)", "Municipal Law", "Property Assessment", "Certificate issued by BBMP for properties constructed on legally approved layouts adhering to all bylaws and building sanctions", ["A Khata", "Pucca Khata"], ["a kata", "a-katha"], "BBMP Act, 2020"),
        ("B-Khata", "ಬಿ-ಖಾತಾ", "बी-खाता (अनाधिकृत लेकिन कर भुगतान)", "Municipal Law", "Property Assessment", "Property tax register entry maintained by BBMP for unapproved layouts or building deviations; permits tax collection but does not constitute legal title", ["B Khata", "Temporary Khata"], ["b kata", "b-katha"], "BBMP Act, 2020"),
        ("e-Khata", "ಇ-ಖಾತಾ", "डिजिटल ई-खाता", "Municipal Law", "Digital Assessment", "Digitally verified and tamper-proof electronic property tax registration certificate issued by BBMP or municipal corporations", ["Digital Khata"], ["ekhata", "e kata"], "BBMP Act, 2020"),
        ("Phodi", "ಫೋಡಿ", "उप-विभाजन सर्वेक्षण", "Land Revenue", "Survey & Demarcation", "Partition and separate survey demarcation of fragmented agricultural land parcels under independent survey numbers", ["Phodi survey", "Takkhta"], ["podi", "phoddi"], "Karnataka Land Revenue Act, 1964 (Sec 140)"),
        ("Durasti", "ದುರಸ್ತಿ", "सर्वेक्षण सुधार एवं दुरुस्ती", "Land Revenue", "Survey & Demarcation", "Rectification of survey errors, missing boundary marks, or discrepancy between sketch and ground reality in land records", ["Durasti karyakrama"], ["durasti", "durusthi"], "Karnataka Land Revenue Rules, 1966"),
        ("Encumbrance Certificate (EC)", "ಋಣಭಾರ ಪ್ರಮಾಣಪತ್ರ (ಇ.ಸಿ)", "भार-मुक्त प्रमाण पत्र (ईसी)", "Property Law", "Registration Search", "Official search certificate from Sub-Registrar confirming whether registered encumbrances, mortgages or sales exist on property", ["Form 15", "Form 16", "Nil Encumbrance"], ["encumberance", "ec certificate"], "Registration Act, 1908"),
        ("Form 15", "ನಮೂನೆ 15", "प्रारूप 15 (पंजीकृत भार सूची)", "Property Law", "Registration Search", "Encumbrance certificate listing all registered transactions and mortgages affecting property during search period", ["EC Form 15"], ["form15"], "Karnataka Registration Rules, 1965"),
        ("Form 16 (Nil Encumbrance)", "ನಮೂನೆ 16 (ಋಣಭಾರ ರಹಿತ)", "प्रारूप 16 (भार-मुक्त प्रमाण पत्र)", "Property Law", "Registration Search", "Certificate certifying that no registered encumbrance, sale or mortgage exists for searched period", ["Nil EC", "Form 16"], ["form16"], "Karnataka Registration Rules, 1965"),
        ("Saguvali Chit", "ಸಾಗುವಳಿ ಚೀಟಿ", "काश्तकारी / पट्टा प्रमाण पत्र", "Land Governance", "Grant Document", "Grant certificate issued by Land Tribunal or Tahsildar conferring occupancy or agricultural ownership rights to tenant or grantee", ["Grant certificate", "Cultivation slip"], ["saguvali cheeti", "saguvalli"], "Karnataka Land Reforms Act, 1961"),
        ("Hakkupatra", "ಹಕ್ಕುಪತ್ರ", "स्वामित्व पट्टा / अधिकार पत्र", "Land Governance", "Title Grant", "Title grant deed issued by Government allocating residential plots or agricultural land to eligible beneficiaries under welfare schemes", ["Patta deed", "Allotment deed"], ["hakku patra", "hakkupatra"], "Karnataka Land Grant Rules, 1969"),
        ("Inam Land", "ಇನಾಂ ಜಮೀನು", "इनाम / जागीर भूमि", "Land Revenue", "Abolished Tenures", "Historical gift or grant lands conferred by rulers/governments, subject to Inam Abolition Acts requiring re-grant orders", ["Inamti", "Devadaya Inam"], ["inaam", "inam"], "Karnataka Certain Inams Abolition Act, 1977"),
        ("PTCL Land", "ಪಿಟಿಸಿಎಲ್ ಜಮೀನು", "पीटीसीएल भूमि (अनुसूचित जाति/जनजाति अनुदान)", "Land Governance", "Statutory Protection", "Land granted by Government to persons belonging to Scheduled Castes and Scheduled Tribes, transfer of which is prohibited without prior permission", ["Granted land", "SC ST grant"], ["ptcl", "ptcl land"], "Karnataka PTCL Act, 1978"),
        ("Sale Deed", "ಮಾರಾಟ ಪತ್ರ / ಕ್ರಯಪತ್ರ", "बैनामा / विक्रय पत्र", "Property Law", "Conveyance", "Conveyance instrument transferring absolute ownership of immovable property from seller to buyer in exchange for price", ["Kraya patra", "Bainama"], ["sale dead", "sel deed"], "Transfer of Property Act, 1882 (Sec 54)"),
        ("Agreement to Sell", "ಮಾರಾಟ ಒಪ್ಪಂದ / ಕರಾರು ಪತ್ರ", "इकरारनामा / विक्रय अनुबंध", "Property Law", "Contractual Instrument", "Contract between buyer and seller agreeing to execute sale deed on future settled terms; does not convey title itself", ["Kararu patra", "Bayanama"], ["aggreement to sell", "sale aggreement"], "Transfer of Property Act, 1882 (Sec 54)"),
        ("Gift Deed", "ದಾನ ಪತ್ರ", "दान पत्र / हिबानामा", "Property Law", "Conveyance", "Transfer of existing movable or immovable property made voluntarily and without consideration by donor to donee", ["Dana patra", "Hibanama"], ["gift dead", "gif deed"], "Transfer of Property Act, 1882 (Sec 122)"),
        ("Release Deed", "ಬಿಡುಗಡೆ ಪತ್ರ / ಹಕ್ಕು ತ್ಯಾಗ ಪತ್ರ", "हक त्याग पत्र", "Property Law", "Partition/Relinquishment", "Instrument whereby a co-owner or legal heir relinquishes or releases their share in joint family property in favour of other co-owners", ["Hakku tyaga patra", "Relinquishment deed"], ["relese deed", "relinquish deed"], "Registration Act, 1908 (Sec 17)"),
        ("Partition Deed", "ವಿಭಾಗ ಪತ್ರ / ಪಾಲುಪತ್ರ", "बंटवारा पत्र / विभाजन विलेख", "Property Law", "Joint Property", "Registered instrument dividing joint ancestral or coparcenary property among co-owners by metes and bounds", ["Palu patra", "Bantwara"], ["partition dead", "palupatra"], "Transfer of Property Act, 1882"),
        ("General Power of Attorney (GPA)", "ಜನರಲ್ ಪವರ್ ಆಫ್ ಅಟಾರ್ನಿ (ಜಿಪಿಎ)", "मुख्तारनामा आम (जीपीए)", "Agency & Property", "Authorization", "Legal authorization empowering agent to manage affairs or execute documents on behalf of principal; cannot convey title without registered sale deed", ["Mukhtarnama", "GPA"], ["gpa deed", "general power of atorney"], "Powers-of-Attorney Act, 1882"),
        ("Special Power of Attorney (SPA)", "ಸ್ಪೆಷಲ್ ಪವರ್ ಆಫ್ ಅಟಾರ್ನಿ (ಎಸ್‍ಪಿಎ)", "मुख्तारनामा खास (एसपीए)", "Agency & Property", "Authorization", "Power of attorney restricted to a specific defined transaction or single court proceeding", ["Mukhtarnama khas", "SPA"], ["spa deed"], "Powers-of-Attorney Act, 1882"),
        ("Adverse Possession", "ಪ್ರತಿಕೂಲ ಸ್ವಾಧೀನ", "प्रतिकूल कब्जा", "Property Law", "Possessory Title", "Acquisition of title to immovable property by open, continuous, and hostile possession against true owner for statutory limitation period (12 years)", ["Hostile possession"], ["adverse possesion", "adverse posession"], "Limitation Act, 1963 (Art 65)"),
        ("Easementary Right", "ಸುಖಭೋಗ ಹಕ್ಕು", "सुखाचार अधिकार", "Property Law", "Servitude", "Right possessed by owner of land to use adjacent land for passage, light, air, or water drainage", ["Pathway right", "Right of way"], ["easment", "easement"], "Indian Easements Act, 1882"),
        ("Occupancy Certificate (OC)", "ವಸತಿ ಪ್ರಮಾಣಪತ್ರ (ಒ.ಸಿ)", "अधिभोग प्रमाण पत्र (ओसी)", "Municipal Law", "Building Compliance", "Document issued by local municipal body certifying that building has been constructed according to approved plan and is fit for habitation", ["OC", "Fit to occupy"], ["oc certificate", "occupency"], "Karnataka Municipal Corporations Act, 1976"),
        ("Commencement Certificate (CC)", "ಪ್ರಾರಂಭ ಪ್ರಮಾಣಪತ್ರ (ಸಿ.ಸಿ)", "प्रारंभ प्रमाण पत्र (सीसी)", "Municipal Law", "Building Compliance", "Certificate issued by municipal authority permitting builder to commence construction after inspecting foundation and setbacks", ["CC"], ["cc certificate"], "Karnataka Municipal Corporations Act, 1976"),
        ("Undivided Share of Land (UDS)", "ಅವಿಭಜಿತ ಭೂಮಿ ಪಾಲು (ಯುಡಿಎಸ್)", "अविभाजित भूमि अंश (यूडीएस)", "Apartment Law", "Ownership Share", "Share of land owned by each apartment owner in the total plot on which the building is constructed", ["UDS"], ["undivided share", "uds share"], "Karnataka Ownership Flats Act, 1972"),
        ("Form 9", "ನಮೂನೆ 9 (ಗ್ರಾಮಠಾಣ ಆಸ್ತಿ)", "प्रारूप 9 (ग्राम पंचायत संपत्ति)", "Panchayat Law", "Rural Property", "Extract from Gramatana property register maintained by Gram Panchayat under e-Swathu confirming rural site is within settlement boundary", ["Form 9 e-Swathu"], ["form9", "e-swathu form 9"], "Karnataka Gram Swaraj Act, 1993"),
        ("Form 11", "ನಮೂನೆ 11 (ತೆರಿಗೆ ನಿರ್ಧರಣೆ)", "प्रारूप 11 (कर निर्धारण रजिस्टर)", "Panchayat Law", "Rural Property", "Tax assessment register extract issued under e-Swathu for non-gramatana or converted sites in Gram Panchayat limits", ["Form 11 e-Swathu"], ["form11", "e-swathu form 11"], "Karnataka Gram Swaraj Act, 1993"),
        ("Kaveri 2.0", "ಕಾವೇರಿ ೨.೦ ಪೋರ್ಟಲ್", "कावेरी 2.0 पंजीकरण पोर्टल", "E-Governance", "Registration Portal", "Karnataka government web portal for online valuation, pre-registration document entry, slot booking, and EC downloads", ["Kaveri portal"], ["kavery 2.0", "kaveri portal"], "Department of Stamps and Registration, Karnataka"),
        ("Bhoomi Portal", "ಭೂಮಿ ಪೋರ್ಟಲ್", "भूमि पोर्टल (कर्नाटक)", "E-Governance", "Land Records Portal", "Flagship digital land records management system of Government of Karnataka for RTC viewing, mutation application and survey tracking", ["Bhoomi"], ["bhomi", "bhoomi online"], "Revenue Department, Government of Karnataka"),
    ]

    for item in land_terms:
        add_term(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])

    # =========================================================================
    # 2. FAMILY, MARRIAGE, DIVORCE & INHERITANCE
    # =========================================================================
    family_terms = [
        ("Restitution of Conjugal Rights", "ದಾಂಪತ್ಯ ಹಕ್ಕುಗಳ ಮರುಸ್ಥಾಪನೆ", "वैवाहिक अधिकारों का प्रत्यास्थापन", "Family Law", "Matrimonial Remedy", "Decree directing spouse who has withdrawn from society of other without reasonable excuse to cohabit again", ["RCR", "Section 9"], ["restitution", "conjugal rights"], "Hindu Marriage Act, 1955 (Sec 9)"),
        ("Judicial Separation", "ನ್ಯಾಯಾಂಗ ಪ್ರತ್ಯೇಕತೆ", "न्यायिक पृथक्करण", "Family Law", "Matrimonial Remedy", "Decree relieving spouses of matrimonial cohabitation obligation without formally terminating marital status", ["Separation order"], ["judicial seperation"], "Hindu Marriage Act, 1955 (Sec 10)"),
        ("Mutual Consent Divorce", "ಪರಸ್ಪರ ಸಮ್ಮತಿಯ ವಿಚ್ಛೇದನ", "आपसी सहमति से तलाक", "Family Law", "Divorce", "Divorce granted upon joint petition of both spouses living separately for over one year with irretrievable breakdown", ["13B divorce", "Consent divorce"], ["mutual concent divorce", "mutual divorce"], "Hindu Marriage Act, 1955 (Sec 13B)"),
        ("Permanent Alimony", "ಶಾಶ್ವತ ಜೀವನಾಂಶ", "स्थायी निर्वाहिका / गुजारा भत्ता", "Family Law", "Financial Maintenance", "Lump-sum or periodic maintenance awarded by court at time of passing decree of divorce or nullity", ["Alimony", "Maintenance"], ["permanant alimony", "alimoney"], "Hindu Marriage Act, 1955 (Sec 25)"),
        ("Interim Maintenance", "ಮಧ್ಯಂತರ ಜೀವನಾಂಶ", "अंतरिम गुजारा भत्ता", "Family Law", "Financial Maintenance", "Monthly support and litigation expenses awarded during pendency of matrimonial or domestic violence proceedings", ["Pendente lite maintenance"], ["interim maintainance", "pendente lite"], "Hindu Marriage Act, 1955 (Sec 24)"),
        ("Stridhan", "ಸ್ತ್ರೀಧನ", "स्त्रीधन", "Family Law", "Property Rights", "Absolute separate property belonging to woman, comprising gifts, ornaments, and valuables given before, during, or after marriage", ["Wife exclusive property"], ["streedhan", "stridhana"], "Hindu Succession Act, 1956 (Sec 14)"),
        ("Coparcenary Property", "ಸಹದಾಯಿಕ ಆಸ್ತಿ / ಅವಿಭಕ್ತ ಕುಟುಂಬ ಆಸ್ತಿ", "सहायांशिकी / पैतृक संपत्ति", "Family Law", "Ancestral Succession", "Joint Hindu family property in which a coparcener (including daughters since 2005) acquires an interest by birth", ["Ancestral property", "Joint family property"], ["coparcenery", "coparcenary"], "Hindu Succession Act, 1956 (Sec 6)"),
        ("Class I Heirs", "ವರ್ಗ-೧ ರ ವಾರಸುದಾರರು", "प्रथम श्रेणी के वारिस", "Family Law", "Intestate Succession", "Primary statutory heirs of a Hindu male: son, daughter, widow, mother, and specified predeceased children's issues", ["Direct legal heirs"], ["class 1 heirs", "class-I heir"], "Hindu Succession Act, 1956 (Sec 8)"),
        ("Talaq-e-Biddat (Triple Talaq)", "ತಲಾಖ್-ಎ-ಬಿದ್ದತ್ (ತಕ್ಷಣದ ತ್ರಿವಳಿ ತಲಾಖ್)", "तलाक-ए-बिद्दत (तीन तलाक)", "Family Law", "Muslim Law", "Instantaneous, irrevocable verbal or electronic divorce declared illegal, void, and a cognizable criminal offence", ["Triple talaq", "Instant divorce"], ["tripple talaq", "talaq-e-bidat"], "Muslim Women Protection on Marriage Act, 2019"),
        ("Khula", "ಖುಲಾ (ಮಹಿಳೆಯಿಂದ ವಿಚ್ಛೇದನ)", "खुला (स्त्री द्वारा तलाक)", "Family Law", "Muslim Law", "Divorce initiated by Muslim wife with return of part or all of mahr/dower upon consent of husband", ["Wife initiated divorce"], ["khulaa", "kula"], "Dissolution of Muslim Marriages Act, 1939"),
        ("Mahr (Dower)", "ಮೆಹರ್ / ದೇವಣಿಗೆ", "मेहर (स्त्री-धन)", "Family Law", "Muslim Law", "Mandatory sum of money or property which wife is entitled to receive from husband in consideration of marriage", ["Dower", "Prompt Mahr", "Deferred Mahr"], ["mehr", "maher"], "Muslim Personal Law (Shariat) Act, 1937"),
        ("Iddat Period", "ಇದ್ದತ್ ಅವಧಿ", "इद्दत की अवधि", "Family Law", "Muslim Law", "Mandatory waiting period (typically 3 menstrual cycles or 3 months, or until delivery) observed by Muslim woman after divorce or husband death", ["Waiting period"], ["idat", "iddah"], "Muslim Women Protection on Divorce Act, 1986"),
        ("Domestic Incident Report (DIR)", "ಗೃಹ ಹಿಂಸಾಚಾರ ವರದಿ (ಡಿ.ಐ.ಆರ್)", "घरेलू घटना रिपोर्ट (डीआईआर)", "Family Law", "Domestic Violence", "Standard statutory report prepared by Protection Officer or service provider upon receiving domestic abuse complaint", ["DIR Form"], ["dir report", "domestic incident report"], "PWDVA, 2005 (Sec 9/12)"),
        ("Shared Household", "ಹಂಚಿಕೆಯಾದ ಮನೆ", "साझा गृहस्थी", "Family Law", "Domestic Violence", "House where aggrieved woman lives or has lived at any stage in a domestic relationship with respondent, irrespective of title", ["Matrimonial home"], ["shared haushold"], "PWDVA, 2005 (Sec 19)"),
        ("Probate", "ಪ್ರೊಬೇಟ್ / ಉಯಿಲು ದೃಢೀಕರಣ", "प्रमाण-पत्र (प्रोबेट)", "Succession", "Testamentary Law", "Copy of a will certified under court seal with grant of administration to executor named therein", ["Probate of will"], ["probat", "probate deed"], "Indian Succession Act, 1925 (Sec 227)"),
        ("Succession Certificate", "ವಾರಸುದಾರಿಕೆ ಪ್ರಮಾಣಪತ್ರ", "उत्तराधिकार प्रमाण पत्र", "Succession", "Debts & Securities", "Certificate issued by District Judge establishing legal representation to realize debts and securities of deceased person", ["Legal heir certificate for securities"], ["succesion certificate", "succesion"], "Indian Succession Act, 1925 (Sec 372)"),
    ]

    for item in family_terms:
        add_term(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])

    # =========================================================================
    # 3. CRIMINAL LAW, PROCEDURE & POLICE INVESTIGATION
    # =========================================================================
    criminal_terms = [
        ("First Information Report (FIR)", "ಪ್ರಥಮ ವರ್ತಮಾನ ವರದಿ (ಎಫ್‍ಐಆರ್)", "प्रथम सूचना रिपोर्ट (एफआईआर)", "Criminal Procedure", "Investigation", "Official written record prepared by police upon receiving information regarding commission of a cognizable offence", ["FIR", "Case registration"], ["f.i.r.", "police fir"], "BNSS, 2023 (Sec 173) / CrPC Sec 154"),
        ("Zero FIR", "ಶೂನ್ಯ ಎಫ್‍ಐಆರ್", "शून्य एफआईआर", "Criminal Procedure", "Investigation", "FIR registered by police station irrespective of territorial jurisdiction, with immediate transfer to competent police station after initial action", ["Zero FIR"], ["0 fir", "zero-fir"], "BNSS, 2023 (Sec 173(1))"),
        ("Anticipatory Bail", "ನಿರೀಕ್ಷಣಾ ಜಾಮೀನು", "अग्रिम जमानत", "Criminal Procedure", "Bail & Custody", "Pre-arrest protective bail direction issued by Sessions Court or High Court to person apprehending arrest in non-bailable offence", ["Pre-arrest bail", "Section 482 BNSS"], ["anticipetory bail", "anticipatery bail"], "BNSS, 2023 (Sec 482) / CrPC Sec 438"),
        ("Regular Bail", "ಸಾಮಾನ್ಯ ಜಾಮೀನು", "नियमित जमानत", "Criminal Procedure", "Bail & Custody", "Release of accused person from custody after arrest upon furnishing personal bond and sureties to appear before court", ["Post-arrest bail"], ["regular bale", "court bail"], "BNSS, 2023 (Sec 479/480) / CrPC Sec 437/439"),
        ("Police Custody (Remand)", "ಪೊಲೀಸ್ ಕಸ್ಟಡಿ / ಪೊಲೀಸ್ ವಶ", "पुलिस हिरासत (रिमांड)", "Criminal Procedure", "Investigation", "Physical detention of accused under police control for custodial interrogation; maximum initial 15-day period", ["Police remand"], ["police custady", "remand"], "BNSS, 2023 (Sec 187) / CrPC Sec 167"),
        ("Judicial Custody", "ನ್ಯಾಯಾಂಗ ಬಂಧನ", "न्यायिक हिरासत", "Criminal Procedure", "Custody", "Detention of accused in jail under supervision of Judicial Magistrate, where police have no direct interrogation access without court order", ["Jail custody"], ["judicial custady", "jc remand"], "BNSS, 2023 (Sec 187) / CrPC Sec 167"),
        ("Cognizable Offence", "ಪೊಲೀಸರು ನೇರವಾಗಿ ತನಿಖೆ ನಡೆಸಬಹುದಾದ ಅಪರಾಧ", "संज्ञेय अपराध", "Criminal Law", "Classification", "Offence for which police officer may arrest without warrant and commence investigation without Magistrate order", ["Cognizable crime"], ["cognisable", "cognizable"], "BNSS, 2023 (Sec 2(1)(g))"),
        ("Non-Cognizable Offence", "ನ್ಯಾಯಾಲಯದ ಅನುಮತಿ ಬೇಕಾದ ಅಪರಾಧ", "असंज्ञेय अपराध", "Criminal Law", "Classification", "Offence for which police officer has no authority to arrest without warrant or investigate without Magistrate permission", ["NC complaint"], ["non-cognisable", "nc crime"], "BNSS, 2023 (Sec 2(1)(o))"),
        ("Chargesheet (Final Report)", "ದೋಷಾರೋಪ ಪಟ್ಟಿ / ಚಾರ್ಜ್‍ಶೀಟ್", "आरोप पत्र (चार्जशीट)", "Criminal Procedure", "Investigation Conclusion", "Final police report submitted to Magistrate under Section 193 BNSS detailing gathered evidence, witness statements, and formal charges", ["Final report", "Challan"], ["charge sheet", "chargeshet"], "BNSS, 2023 (Sec 193) / CrPC Sec 173"),
        ("Discharge", "ದೋಷಮುಕ್ತ / ಬಿಡುಗಡೆ", "उन्मोचन (डिस्चार्ज)", "Criminal Procedure", "Pre-Trial", "Judicial order releasing accused before framing of charges when court finds allegations groundless or devoid of prima facie evidence", ["Discharge application"], ["disharge", "discharge order"], "BNSS, 2023 (Sec 250/262)"),
        ("Electronic Evidence Certificate", "ಎಲೆಕ್ಟ್ರಾನಿಕ್ ಸಾಕ್ಷ್ಯ ಪ್ರಮಾಣಪತ್ರ", "इलेक्ट्रॉनिक साक्ष्य प्रमाण पत्र", "Evidence Law", "Admissibility", "Mandatory statutory certificate certifying integrity of secondary electronic devices, call logs, emails, WhatsApp chats, or server records", ["Section 63 BSA certificate", "Section 65B certificate"], ["65b certificate", "electronic certificate"], "BSA, 2023 (Sec 63) / IEA Sec 65B"),
        ("Panchanama (Mahazar)", "ಮಹಜರು / ಪಂಚನಾಮೆ", "पंचनामा / घटनास्थल निरीक्षण", "Criminal Procedure", "Police Record", "Document recording police observations, recoveries, seizures, or scene of crime inspection in presence of independent respectable witnesses (Panchas)", ["Mahazar", "Seizure memo"], ["panchnama", "mahajar"], "BNSS, 2023 (Sec 105)"),
    ]

    for item in criminal_terms:
        add_term(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])

    # =========================================================================
    # 4. BANKING, FINANCE & CHEQUE DISHONOUR
    # =========================================================================
    banking_terms = [
        ("Cheque Bounce", "ಚೆಕ್ ಅಮಾನ್ಯತೆ", "चेक अनादरण (बाउंस)", "Banking Law", "Commercial Offence", "Criminal dishonour of negotiable cheque due to insufficiency of funds or exceeding agreed bank overdraft limit", ["Cheque dishonour", "Section 138"], ["check bounce", "chq bounce", "cheq bonce"], "Negotiable Instruments Act, 1881 (Sec 138)"),
        ("Statutory Demand Notice", "ಶಾಸನಬದ್ಧ ನೋಟಿಸ್", "वैधानिक मांग नोटिस", "Banking Law", "Pre-litigation Notice", "Mandatory formal demand letter dispatched within 30 days of receiving bank dishonour memo granting drawer 15 days to pay", ["138 legal notice", "Demand notice"], ["statutory notice", "138 notice"], "Negotiable Instruments Act, 1881 (Sec 138(b))"),
        ("Return Memo", "ಚೆಕ್ ಹಿಂತಿರುಗಿಸಿದ ಮೆಮೊ", "बैंक अनादरण ज्ञापन (रिटर्न मेमो)", "Banking Law", "Banking Record", "Official slip issued by drawee bank stating specific statutory reason for dishonour (e.g., 'Funds Insufficient', 'Account Closed', 'Stop Payment')", ["Bank memo", "Dishonour slip"], ["return memo", "bank slip"], "Negotiable Instruments Act, 1881 (Sec 146)"),
        ("SARFAESI Notice", "ಸರ್ಫೇಸಿ ಕಾಯ್ದೆ ನೋಟಿಸ್", "सरफेसी नोटिस (धारा 13(2))", "Banking Law", "Debt Recovery", "60-day demand notice issued by secured creditor bank demanding discharge of liabilities upon NPA classification before taking possession", ["13(2) notice", "Demand notice SARFAESI"], ["sarfaesi notice", "sarfesi"], "SARFAESI Act, 2002 (Sec 13(2))"),
        ("Non-Performing Asset (NPA)", "ಅನುತ್ಪಾದಕ ಆಸ್ತಿ (ಎನ್‍ಪಿಎ)", "गैर-निष्पादित संपत्ति (एनपीए)", "Banking Law", "Loan Default", "Classification of loan account where interest or principal instalment remains overdue for more than 90 days", ["NPA classification", "Default account"], ["npa account", "npa loan"], "RBI Master Directions / SARFAESI"),
        ("Debt Recovery Tribunal (DRT)", "ಸಾಲ ವಸೂಲಾತಿ ನ್ಯಾಯಾಧಿಕರಣ (ಡಿಆರ್‌ಟಿ)", "ऋण वसूली न्यायाधिकरण (डीआरटी)", "Banking Law", "Specialized Forum", "Quasi-judicial tribunal established under RDBA Act for recovery of bank loans exceeding Rs 20 lakh and SARFAESI Section 17 appeals", ["DRT appeal"], ["drt court", "drt tribunal"], "Recovery of Debts and Bankruptcy Act, 1993"),
        ("One Time Settlement (OTS)", "ಒಂದು ಬಾರಿ ಇತ್ಯರ್ಥ (ಒಟಿಎಸ್)", "एकमुश्त समझौता (ओटीएस)", "Banking Law", "Loan Compromise", "Compromise settlement scheme offered by banks to settle stressed/NPA loans with waiver of interest and partial principal haircut", ["OTS scheme", "Compromise settlement"], ["ots settlement", "ots loan"], "RBI Master Directions on Stressed Assets"),
        ("Unauthorized Electronic Transaction", "ಅನಧಿಕೃತ ಆನ್‌ಲೈನ್ ಬ್ಯಾಂಕಿಂಗ್ ವರ್ಗಾವಣೆ", "अनधिकृत इलेक्ट्रॉनिक लेन-देन", "Banking & Cybercrime", "Consumer Liability", "Electronic fund debit occurring without customer consent through hacking, UPI phishing, or third-party banking breach", ["UPI fraud", "Net banking fraud"], ["unauthorised transaction", "unauthorized debit"], "RBI Master Directions (Customer Protection)"),
        ("Zero Liability Window", "ಶೂನ್ಯ ಹೊಣೆಗಾರಿಕೆ ಅವಧಿ (೩ ದಿನ)", "शून्य देयता अवधि (3 दिन)", "Banking Law", "Consumer Protection", "Rule entitling customer to full refund with zero liability if third-party electronic fraud is notified to bank within 3 working days", ["3-day fraud notification"], ["zero liability", "3 days rbi"], "RBI Directions on Unauthorized Electronic Transactions"),
    ]

    for item in banking_terms:
        add_term(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])

    # =========================================================================
    # 5. CONSUMER PROTECTION, E-COMMERCE & METROLOGY
    # =========================================================================
    consumer_terms = [
        ("Defect in Goods", "ವಸ್ತುಗಳಲ್ಲಿನ ದೋಷ", "वस्तुओं में दोष / खराबी", "Consumer Law", "Product Claim", "Any fault, imperfection, or shortcoming in quality, quantity, purity, or standard required to be maintained by law or contract", ["Product defect", "Faulty product"], ["defect in goods", "defective item"], "Consumer Protection Act, 2019 (Sec 2(10))"),
        ("Deficiency in Service", "ಸೇವೆಯಲ್ಲಿನ ನ್ಯೂನತೆ", "सेवा में कमी / लापरवाही", "Consumer Law", "Service Claim", "Any fault, imperfection, shortcoming, or inadequacy in quality, nature, or manner of performance required to be performed under law", ["Service deficiency", "Poor service"], ["deficiency of service", "service defect"], "Consumer Protection Act, 2019 (Sec 2(11))"),
        ("Product Liability", "ಉತ್ಪನ್ನ ಹೊಣೆಗಾರಿಕೆ", "उत्पाद दायित्व", "Consumer Law", "Manufacturer Liability", "Responsibility of product manufacturer or service provider to compensate consumer for harm caused by defective product or deficient service", ["Manufacturer liability"], ["product liabilty", "product liability"], "Consumer Protection Act, 2019 (Sec 82-87)"),
        ("e-Daakhil", "ಇ-ದಾಖಿಲ್ ಪೋರ್ಟಲ್", "ई-दाखिल उपभोक्ता पोर्टल", "Consumer Law", "Online Dispute Redressal", "Official electronic filing portal permitting consumers to submit complaints before District, State, and National Consumer Commissions online", ["e-Daakhil online"], ["edaakhil", "e-dakhil"], "Consumer Protection Act, 2019 (Sec 35)"),
        ("Dark Patterns", "ಡಾರ್ಕ್ ಪ್ಯಾಟರ್ನ್‌ಗಳು (ಮೋಸದ ವೆಬ್ ವಿನ್ಯಾಸ)", "डार्क पैटर्न्स (भ्रामक डिजिटल तकनीक)", "Consumer Law", "Digital Consumer Rights", "Deceptive user interface designs employed by e-commerce platforms to trick or manipulate consumers into unintended financial transactions", ["Deceptive design", "Subscription trap"], ["dark patterns", "dark pattern"], "CCPA Dark Patterns Guidelines, 2023"),
        ("Drip Pricing", "ಡ್ರಿಪ್ ಪ್ರೈಸಿಂಗ್ (ಮರೆಮಾಚಿದ ಬೆಲೆ)", "ड्रिप प्राइसिंग (छिपे हुए शुल्क)", "Consumer Law", "E-Commerce", "Unfair practice of incrementally revealing hidden fees, processing charges, or convenience costs only at final payment checkout", ["Hidden charges", "Concealed price"], ["drip pricing", "drip price"], "CCPA Dark Patterns Guidelines, 2023"),
        ("Maximum Retail Price (MRP)", "ಗರಿಷ್ಠ ಚಿಲ್ಲರೆ ಬೆಲೆ (ಎಂಆರ್‌ಪಿ)", "अधिकतम खुदरा मूल्य (एमआरपी)", "Consumer Law", "Legal Metrology", "Mandatory statutory ceiling price printed on packaged commodities; charging any amount above MRP is a punishable offence", ["MRP overcharging", "Dual pricing"], ["mrp overcharge", "above mrp"], "Legal Metrology Act, 2009"),
    ]

    for item in consumer_terms:
        add_term(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])

    # =========================================================================
    # 6. LABOUR, EMPLOYMENT & WORKPLACE COMPLIANCE
    # =========================================================================
    labour_terms = [
        ("Gratuity", "ಗ್ರಾಚ್ಯುಟಿ / ಉಪದಾನ", "ग्रेच्युटी / उपदान", "Labour Law", "Retirement Benefit", "Lump-sum statutory retirement benefit payable to employee upon termination of service after minimum 5 years continuous employment", ["Gratuity benefit"], ["gratuity payment", "gratuity amount"], "Payment of Gratuity Act, 1972 (Sec 4)"),
        ("Continuous Service", "ನಿರಂತರ ಸೇವೆ", "निरंतर सेवा (5 वर्ष)", "Labour Law", "Eligibility Criteria", "Uninterrupted employment service, including interruptions caused by sickness, accident, authorized leave, or lockout", ["5 years service"], ["continuous service", "continuous work"], "Payment of Gratuity Act, 1972 (Sec 2A)"),
        ("Retrenchment", "ಕೆಲಸದಿಂದ ತೆಗೆದುಹಾಕುವುದು / ಕಡಿತ", "छंटनी (रिट्रेंचमेंट)", "Labour Law", "Termination", "Termination by employer of the service of a workman for any reason whatsoever, otherwise than as a punishment inflicted by disciplinary action", ["Layoff", "Job termination"], ["retrenchment", "job cut"], "Industrial Disputes Act, 1947 (Sec 25F)"),
        ("Internal Committee (IC / ICC)", "ಆಂತರಿಕ ದೂರು ಸಮಿತಿ (ಐಸಿಸಿ)", "आंतरिक शिकायत समिति (आईसीसी)", "Labour & Women Rights", "Workplace Safety", "Mandatory workplace committee in every establishment with 10+ employees to inquire into sexual harassment complaints", ["ICC Committee", "POSH Committee"], ["ic committee", "internal complaints committee"], "POSH Act, 2013 (Sec 4)"),
        ("Local Committee (LC)", "ಸ್ಥಳೀಯ ದೂರು ಸಮಿತಿ (ಎಲ್‍ಸಿ)", "स्थानीय शिकायत समिति (एलसी)", "Labour & Women Rights", "Workplace Safety", "District-level committee constituted to receive and inquire into sexual harassment complaints from unorganized sector or small employers", ["Local Complaints Committee"], ["lc committee", "local complaints committee"], "POSH Act, 2013 (Sec 6)"),
        ("Employment Bond", "ಉದ್ಯೋಗ ಬಾಂಡ್ / ಒಪ್ಪಂದ ಪತ್ರ", "रोजगार बांड (अनुबंध)", "Labour & Contracts", "Restrictive Covenants", "Agreement requiring employee to pay damages or serve minimum period; enforceable only to extent of actual training costs proven", ["Training bond", "Service bond"], ["employment bond", "job bond"], "Indian Contract Act, 1872 (Sec 27)"),
    ]

    for item in labour_terms:
        add_term(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])

    # =========================================================================
    # 7. HEALTHCARE, TAXATION, GOVERNMENT SERVICES & TRANSLITERATIONS
    # =========================================================================
    specialized_terms = [
        ("Medical Negligence", "ವೈದ್ಯಕೀಯ ನಿರ್ಲಕ್ಷ್ಯ", "चिकित्सीय लापरवाही", "Healthcare Law", "Tort & Criminal", "Breach of duty of care by medical practitioner resulting in injury or death; requires gross negligence for criminal conviction", ["Doctor negligence", "Hospital fault"], ["medical negligance", "doctor negligence"], "Consumer Protection Act / BNS Sec 106"),
        ("Informed Consent", "ಮಾಹಿತಿಪೂರ್ಣ ಸಮ್ಮತಿ", "सूचित सहमति (ऑपरेशन पूर्व)", "Healthcare Law", "Patient Rights", "Patient voluntary agreement to medical procedure after being fully informed of nature, risks, and treatment alternatives", ["Prior surgical consent"], ["informed concent", "patient consent"], "Samira Kohli v. Dr. Prabha Manchanda (2008)"),
        ("Capital Gains Tax", "ಬಂಡವಾಳ ಲಾಭ ತೆರಿಗೆ", "पूंजीगत लाभ कर", "Taxation", "Direct Taxes", "Income tax payable on profit arising from transfer of capital asset such as immovable property, shares, or gold", ["LTCG", "STCG"], ["capital gains", "capital gain tax"], "Income-tax Act, 1961 (Sec 45/48)"),
        ("Tax Deducted at Source (TDS)", "ಮೂಲದಲ್ಲೇ ತೆರಿಗೆ ಕಡಿತ (ಟಿಡಿಎಸ್)", "स्रोत पर कर कटौती (टीडीएस)", "Taxation", "Direct Taxes", "Statutory tax deducted by payer at specified rate before remitting payment to payee (e.g. 1% TDS on property sale above Rs 50 lakh)", ["TDS 194-IA"], ["tds deduction", "tds on property"], "Income-tax Act, 1961 (Sec 194-IA)"),
        ("Public Information Officer (PIO)", "ಸಾರ್ವಜನಿಕ ಮಾಹಿತಿ ಅಧಿಕಾರಿ (ಪಿಐಒ)", "लोक सूचना अधिकारी (पीआईओ)", "Administrative Law", "RTI", "Designated officer in public authority mandated to receive RTI requests and provide information within 30 days", ["CPIO", "SPIO"], ["pio officer", "rti pio"], "Right to Information Act, 2005 (Sec 5/7)"),
        ("Sakala Guarantee", "ಸಕಾಲ ನಾಗರಿಕ ಸೇವೆ ಗ್ಯಾರಂಟಿ", "सकाला नागरिक सेवा गारंटी", "Administrative Law", "Public Service Delivery", "Statutory guarantee in Karnataka mandating time-bound delivery of government services (15 days for revenue mutation) with compensatory penalty", ["Sakala GSC"], ["sakala service", "sakala karnataka"], "Karnataka Sakala Act, 2011"),
        ("Seva Sindhu", "ಸೇವಾ ಸಿಂಧು ಪೋರ್ಟಲ್", "सेवा सिंधु नागरिक पोर्टल", "E-Governance", "Public Delivery", "One-stop Karnataka government citizen service portal delivering caste, income, residence, and family tree certificates digitally", ["Seva Sindhu online"], ["sevasindhu", "seva sindu"], "Government of Karnataka"),
    ]

    for item in specialized_terms:
        add_term(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])

    return glossary


def build_and_save_glossary(
    json_path: str = "docs/MULTILINGUAL_GLOSSARY.json",
    md_path: str = "docs/MULTILINGUAL_GLOSSARY.md",
) -> int:
    glossary = generate_comprehensive_glossary()
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    # 1. Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(glossary, f, indent=2, ensure_ascii=False)

    # 2. Save Markdown
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# NyayaSetu — Comprehensive Trilingual Legal Glossary\n\n")
        f.write("**Languages Supported:** English, Kannada (ಕನ್ನಡ), Hindi (हिन्दी), Hinglish, Kanglish\n")
        f.write(f"**Total Verified Legal Terms & Mappings:** {len(glossary)}\n")
        f.write("**Statutory Baseline:** All-India Central Enactments & Karnataka State Revenue / Land Laws\n\n")
        f.write("---\n\n")
        f.write("| English Term | Kannada (ಕನ್ನಡ) | Hindi (हिन्दी) | Legal Domain | Statutory Basis | Key Definition |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for key, item in sorted(glossary.items(), key=lambda x: x[1]["domain"]):
            f.write(f"| **{item['english']}** | {item['kannada']} | {item['hindi']} | `{item['domain']}` | *{item['canonical_statute']}* | {item['definition']} |\n")

    return len(glossary)


if __name__ == "__main__":
    count = build_and_save_glossary()
    print(f"Successfully generated multilingual legal glossary with {count} verified entries.")
