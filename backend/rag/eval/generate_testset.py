"""Generator for 150+ Multilingual RAG Test Set with Ground-Truth Annotations."""

import json
import os

TEST_ITEMS = [
    # ── TENANCY & PROPERTY (English, Kannada, Hindi, Mixed) ──
    {"id": "tc_001", "lang": "en", "topic": "tenancy", "query": "My landlord is not returning my security deposit of 50000 rupees", "expected_sections": ["Section 108", "Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_002", "lang": "en", "topic": "tenancy", "query": "How much security deposit can a landlord take in Karnataka?", "expected_sections": ["Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_003", "lang": "en", "topic": "tenancy", "query": "Can the house owner deduct full deposit for painting and normal wear and tear?", "expected_sections": ["Section 108", "Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_004", "lang": "en", "topic": "tenancy", "query": "Notice period required to terminate month-to-month residential tenancy under TPA", "expected_sections": ["Section 106"], "needs_lawyer_verification": False},
    {"id": "tc_005", "lang": "en", "topic": "tenancy", "query": "Landlord refusing to repair leaking roof, can tenant deduct from rent?", "expected_sections": ["Section 14"], "needs_lawyer_verification": False},
    {"id": "tc_006", "lang": "en", "topic": "tenancy", "query": "Eviction rules for tenant under Karnataka Rent Act", "expected_sections": ["Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_007", "lang": "en", "topic": "tenancy", "query": "Landlord locked my flat without court order", "expected_sections": ["Section 27", "Section 108"], "needs_lawyer_verification": True},
    {"id": "tc_008", "lang": "en", "topic": "tenancy", "query": "How many days does landlord have to return advance deposit in Karnataka?", "expected_sections": ["Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_009", "lang": "kn", "topic": "tenancy", "query": "ನನ್ನ ಭದ್ರತಾ ಠೇವಣಿ ಹಣವನ್ನು ಮನೆ ಮಾಲೀಕರು ಹಿಂತಿರುಗಿಸುತ್ತಿಲ್ಲ", "expected_sections": ["Section 27", "Section 108"], "needs_lawyer_verification": False},
    {"id": "tc_010", "lang": "kn", "topic": "tenancy", "query": "ಕರ್ನಾಟಕ ಬಾಡಿಗೆ ಕಾಯ್ದೆ ಪ್ರಕಾರ ಮುಂಗಡ ಹಣ ಮರುಪಾವತಿ ನಿಯಮಗಳು", "expected_sections": ["Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_011", "lang": "kn", "topic": "tenancy", "query": "ಮನೆ ಖಾಲಿ ಮಾಡಿದ ನಂತರ ಠೇವಣಿ ಎಷ್ಟು ದಿನಗಳಲ್ಲಿ ವಾಪಸ್ ನೀಡಬೇಕು?", "expected_sections": ["Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_012", "lang": "kn", "topic": "tenancy", "query": "ಸಾಮಾನ್ಯ ಬಣ್ಣದ ಸವೆತಕ್ಕೆ ಠೇವಣಿ ಕಡಿತ ಮಾಡಬಹುದೇ?", "expected_sections": ["Section 108", "Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_013", "lang": "hi", "topic": "tenancy", "query": "मकान मालिक मेरी सुरक्षा जमा राशि वापस नहीं कर रहा है", "expected_sections": ["Section 108", "Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_014", "lang": "hi", "topic": "tenancy", "query": "किराया खत्म होने पर सिक्योरिटी डिपॉजिट कितने दिनों में मिलना चाहिए?", "expected_sections": ["Section 27", "Section 108"], "needs_lawyer_verification": False},
    {"id": "tc_015", "lang": "hi", "topic": "tenancy", "query": "क्या मकान मालिक पेंटिंग के नाम पर पूरी सुरक्षा जमा राशि काट सकता है?", "expected_sections": ["Section 108"], "needs_lawyer_verification": False},
    {"id": "tc_016", "lang": "mixed", "topic": "tenancy", "query": "Landlord ne flat vacate karne ke baad deposit return nahi kiya", "expected_sections": ["Section 108", "Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_017", "lang": "mixed", "topic": "tenancy", "query": "Nanna rental deposit maalikaru kodthilla what is the legal notice step?", "expected_sections": ["Section 27", "Section 108"], "needs_lawyer_verification": False},
    {"id": "tc_018", "lang": "mixed", "topic": "tenancy", "query": "Security advance withheld by Bengaluru house owner past 30 days", "expected_sections": ["Section 27"], "needs_lawyer_verification": False},

    # ── CHEQUE BOUNCE (NI ACT 138 & 142) ──
    {"id": "tc_019", "lang": "en", "topic": "cheque_bounce", "query": "What is the notice period for bounced cheque under section 138 of NI Act?", "expected_sections": ["Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_020", "lang": "en", "topic": "cheque_bounce", "query": "Cheque bounced due to insufficient funds, how many days to send legal notice?", "expected_sections": ["Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_021", "lang": "en", "topic": "cheque_bounce", "query": "How many days does drawer have to pay after receiving section 138 notice?", "expected_sections": ["Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_022", "lang": "en", "topic": "cheque_bounce", "query": "Limitation period for filing section 138 complaint before magistrate", "expected_sections": ["Section 142", "Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_023", "lang": "en", "topic": "cheque_bounce", "query": "Which court has jurisdiction to try cheque bounce case under section 142?", "expected_sections": ["Section 142"], "needs_lawyer_verification": False},
    {"id": "tc_024", "lang": "en", "topic": "cheque_bounce", "query": "Punishment for cheque dishonour under Negotiable Instruments Act", "expected_sections": ["Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_025", "lang": "en", "topic": "cheque_bounce", "query": "Can court condone delay in filing section 138 complaint after one month?", "expected_sections": ["Section 142"], "needs_lawyer_verification": True},
    {"id": "tc_026", "lang": "kn", "topic": "cheque_bounce", "query": "ಖಾತೆಯಲ್ಲಿ ಹಣವಿಲ್ಲದೆ ಚೆಕ್ ಬೌನ್ಸ್ ಆದರೆ ಸೆಕ್ಷನ್ 138 ನೋಟಿಸ್ ಅವಧಿ ಎಷ್ಟು?", "expected_sections": ["Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_027", "lang": "kn", "topic": "cheque_bounce", "query": "ಬ್ಯಾಂಕ್ ಮೆಮೊ ಬಂದ ನಂತರ ಎಷ್ಟು ದಿನಗಳಲ್ಲಿ ಲೀಗಲ್ ನೋಟಿಸ್ ನೀಡಬೇಕು?", "expected_sections": ["Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_028", "lang": "kn", "topic": "cheque_bounce", "query": "ಚೆಕ್ ಅಮಾನ್ಯ ಪ್ರಕರಣದಲ್ಲಿ ಮ್ಯಾಜಿಸ್ಟ್ರೇಟ್ ನ್ಯಾಯಾಲಯದಲ್ಲಿ ದೂರು ಸಲ್ಲಿಸುವ ಕಾಲಮಿತಿ", "expected_sections": ["Section 142", "Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_029", "lang": "hi", "topic": "cheque_bounce", "query": "चेक बाउंस होने पर 30 दिन के अंदर लीगल नोटिस कैसे भेजें?", "expected_sections": ["Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_030", "lang": "hi", "topic": "cheque_bounce", "query": "धारा 138 के तहत चेक अनादर होने पर कितने दिन में भुगतान करना होता है?", "expected_sections": ["Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_031", "lang": "hi", "topic": "cheque_bounce", "query": "चेक बाउंस की कोर्ट में शिकायत दर्ज करने की समय सीमा क्या है?", "expected_sections": ["Section 142", "Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_032", "lang": "mixed", "topic": "cheque_bounce", "query": "Mera cheque bounce ho gaya bank memo milne ke baad notice timeline kya hai?", "expected_sections": ["Section 138"], "needs_lawyer_verification": False},
    {"id": "tc_033", "lang": "mixed", "topic": "cheque_bounce", "query": "Customer cheque bounced under 138 NI Act, how much time to file case?", "expected_sections": ["Section 142", "Section 138"], "needs_lawyer_verification": False},

    # ── CRIMINAL LAW, ARREST & CONSTITUTION (ART 21, 22, BNSS, BNS) ──
    {"id": "tc_034", "lang": "en", "topic": "criminal_arrest", "query": "What are my constitutional rights if arrested by police under Article 22?", "expected_sections": ["Article 22"], "needs_lawyer_verification": False},
    {"id": "tc_035", "lang": "en", "topic": "criminal_arrest", "query": "Must an arrested person be produced before magistrate within 24 hours?", "expected_sections": ["Article 22"], "needs_lawyer_verification": False},
    {"id": "tc_036", "lang": "en", "topic": "criminal_arrest", "query": "Right to consult an advocate of choice upon police arrest", "expected_sections": ["Article 22"], "needs_lawyer_verification": False},
    {"id": "tc_037", "lang": "en", "topic": "criminal_arrest", "query": "What are the DK Basu guidelines for arrest and detention by police?", "expected_sections": ["(1997) 1 SCC 416", "Article 22"], "needs_lawyer_verification": False},
    {"id": "tc_038", "lang": "en", "topic": "criminal_arrest", "query": "When is notice of appearance under section 35 BNSS mandatory instead of arrest?", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_039", "lang": "en", "topic": "criminal_arrest", "query": "Prior permission of DSP required to arrest senior citizen under BNSS 35", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_040", "lang": "en", "topic": "criminal_arrest", "query": "Arnesh Kumar guidelines against automatic arrest in matrimonial cases", "expected_sections": ["(2014) 8 SCC 273", "Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_041", "lang": "en", "topic": "criminal_arrest", "query": "How to apply for anticipatory bail under Section 482 of BNSS?", "expected_sections": ["Section 482"], "needs_lawyer_verification": False},
    {"id": "tc_042", "lang": "en", "topic": "criminal_arrest", "query": "Can Sessions Court grant anticipatory bail for non bailable offence?", "expected_sections": ["Section 482"], "needs_lawyer_verification": False},
    {"id": "tc_043", "lang": "en", "topic": "criminal_arrest", "query": "What is Zero FIR under Section 173 of Bharatiya Nagarik Suraksha Sanhita?", "expected_sections": ["Section 173"], "needs_lawyer_verification": False},
    {"id": "tc_044", "lang": "en", "topic": "criminal_arrest", "query": "Can police refuse to register FIR for a cognizable crime?", "expected_sections": ["Section 173"], "needs_lawyer_verification": False},
    {"id": "tc_045", "lang": "en", "topic": "criminal_arrest", "query": "e-FIR registration procedure and 3-day signature requirement under BNSS", "expected_sections": ["Section 173"], "needs_lawyer_verification": False},
    {"id": "tc_046", "lang": "en", "topic": "criminal_arrest", "query": "What is the new section for cheating in BNS replacing IPC 420?", "expected_sections": ["Section 318(4)"], "needs_lawyer_verification": False},
    {"id": "tc_047", "lang": "en", "topic": "criminal_arrest", "query": "BNS section for cruelty by husband replacing Section 498A IPC", "expected_sections": ["Section 85"], "needs_lawyer_verification": False},
    {"id": "tc_048", "lang": "en", "topic": "criminal_arrest", "query": "Murder and mob lynching punishment under Section 103 BNS", "expected_sections": ["Section 103"], "needs_lawyer_verification": False},
    {"id": "tc_049", "lang": "en", "topic": "criminal_arrest", "query": "Community service punishment for first-time petty theft under BNS 303", "expected_sections": ["Section 303(2)"], "needs_lawyer_verification": False},
    {"id": "tc_050", "lang": "kn", "topic": "criminal_arrest", "query": "ಪೊಲೀಸರು ವಾರಂಟ್ ಇಲ್ಲದೆ ಬಂಧಿಸಿದರೆ ಸಂವಿಧಾನದ 22ನೇ ವಿಧಿ ಅಡಿ ಹಕ್ಕುಗಳು", "expected_sections": ["Article 22"], "needs_lawyer_verification": False},
    {"id": "tc_051", "lang": "kn", "topic": "criminal_arrest", "query": "ಬಂಧಿತ ವ್ಯಕ್ತಿಯನ್ನು 24 ಗಂಟೆಗಳಲ್ಲಿ ನ್ಯಾಯಾಧೀಶರ ಮುಂದೆ ಹಾಜರುಪಡಿಸಬೇಕೇ?", "expected_sections": ["Article 22"], "needs_lawyer_verification": False},
    {"id": "tc_052", "lang": "kn", "topic": "criminal_arrest", "query": "ಶೂನ್ಯ ಎಫ್‌ಐಆರ್ (Zero FIR) ಎಂದರೇನು ಮತ್ತು ಅದನ್ನು ಎಲ್ಲಿ ದಾಖಲಿಸಬಹುದು?", "expected_sections": ["Section 173"], "needs_lawyer_verification": False},
    {"id": "tc_053", "lang": "kn", "topic": "criminal_arrest", "query": "ನಿರೀಕ್ಷಣಾ ಜಾಮೀನು (Anticipatory Bail) ಪಡೆಯಲು ಬಿಎನ್‌ಎಸ್‌ಎಸ್ ಸೆಕ್ಷನ್ 482", "expected_sections": ["Section 482"], "needs_lawyer_verification": False},
    {"id": "tc_054", "lang": "kn", "topic": "criminal_arrest", "query": "ಪೊಲೀಸರು ಎಫ್‌ಐಆರ್ ದಾಖಲಿಸಲು ನಿರಾಕರಿಸಿದರೆ ಎಸ್ಪಿ ಅವರಿಗೆ ಪತ್ರ ಬರೆಯುವುದು ಹೇಗೆ?", "expected_sections": ["Section 173"], "needs_lawyer_verification": False},
    {"id": "tc_055", "lang": "hi", "topic": "criminal_arrest", "query": "पुलिस द्वारा गिरफ्तारी के समय अनुच्छेद 22 के तहत नागरिक अधिकार", "expected_sections": ["Article 22"], "needs_lawyer_verification": False},
    {"id": "tc_056", "lang": "hi", "topic": "criminal_arrest", "query": "क्या 24 घंटे के अंदर मजिस्ट्रेट के सामने पेश करना अनिवार्य है?", "expected_sections": ["Article 22"], "needs_lawyer_verification": False},
    {"id": "tc_057", "lang": "hi", "topic": "criminal_arrest", "query": "जीरो एफआईआर (Zero FIR) क्या है और इसे किसी भी थाने में कैसे दर्ज कराएं?", "expected_sections": ["Section 173"], "needs_lawyer_verification": False},
    {"id": "tc_058", "lang": "hi", "topic": "criminal_arrest", "query": "अग्रिम जमानत के लिए सत्र न्यायालय में बीएनएसएस की धारा 482", "expected_sections": ["Section 482"], "needs_lawyer_verification": False},
    {"id": "tc_059", "lang": "hi", "topic": "criminal_arrest", "query": "आईपीसी 420 की जगह बीएनएस में कौन सी धारा है धोखाधड़ी के लिए?", "expected_sections": ["Section 318(4)"], "needs_lawyer_verification": False},
    {"id": "tc_060", "lang": "mixed", "topic": "criminal_arrest", "query": "Police ne bina warrant arrest kiya 24 hours magistrate rule kya hai?", "expected_sections": ["Article 22"], "needs_lawyer_verification": False},
    {"id": "tc_061", "lang": "mixed", "topic": "criminal_arrest", "query": "Thaneyalli police FIR togollilla Zero FIR transfer madbahuda?", "expected_sections": ["Section 173"], "needs_lawyer_verification": False},
    {"id": "tc_062", "lang": "mixed", "topic": "criminal_arrest", "query": "How to get anticipatory bail in Karnataka Sessions Court under BNSS?", "expected_sections": ["Section 482"], "needs_lawyer_verification": False},

    # ── CONSUMER PROTECTION (CPA 2019 & E-DAAKHIL) ──
    {"id": "tc_063", "lang": "en", "topic": "consumer", "query": "How to file a consumer complaint online on e-Daakhil portal under CPA 2019?", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_064", "lang": "en", "topic": "consumer", "query": "Limitation period for filing consumer case is two years from cause of action", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_065", "lang": "en", "topic": "consumer", "query": "What is the fee for consumer complaint up to five lakh rupees?", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_066", "lang": "en", "topic": "consumer", "query": "Defective electronics sold by e-commerce company, where to complain?", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_067", "lang": "en", "topic": "consumer", "query": "Product liability claim against manufacturer under Consumer Protection Act", "expected_sections": ["Section 35"], "needs_lawyer_verification": True},
    {"id": "tc_068", "lang": "kn", "topic": "consumer", "query": "ಗ್ರಾಹಕ ವೇದಿಕೆಯಲ್ಲಿ ಇ-ದಾಖಿಲ್ (e-Daakhil) ಮೂಲಕ ಆನ್‌ಲೈನ್ ದೂರು ದಾಖಲಿಸುವುದು ಹೇಗೆ?", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_069", "lang": "kn", "topic": "consumer", "query": "ದೋಷಪೂರಿತ ವಸ್ತು ಮಾರಾಟ ಮಾಡಿದರೆ ಗ್ರಾಹಕ ನ್ಯಾಯಾಲಯದಲ್ಲಿ ಪರಿಹಾರ ಪಡೆಯುವುದು ಹೇಗೆ?", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_070", "lang": "hi", "topic": "consumer", "query": "उपभोक्ता संरक्षण अधिनियम 2019 के तहत ई-दाखिल पर शिकायत कैसे दर्ज करें?", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_071", "lang": "hi", "topic": "consumer", "query": "उपभोक्ता कोर्ट में केस दर्ज करने की समय सीमा क्या 2 साल है?", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_072", "lang": "mixed", "topic": "consumer", "query": "Online shopping company refused refund e-Daakhil filing steps", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},

    # ── FAMILY LAW, DIVORCE, MAINTENANCE & SUCCESSION ──
    {"id": "tc_073", "lang": "en", "topic": "family", "query": "Procedure for divorce by mutual consent under Section 13B Hindu Marriage Act", "expected_sections": ["Section 13B"], "needs_lawyer_verification": False},
    {"id": "tc_074", "lang": "en", "topic": "family", "query": "Can the 6-month cooling off period in mutual divorce be waived?", "expected_sections": ["Section 13B"], "needs_lawyer_verification": False},
    {"id": "tc_075", "lang": "en", "topic": "family", "query": "Do daughters have equal coparcenary rights in ancestral property under Hindu Succession Act?", "expected_sections": ["Section 6"], "needs_lawyer_verification": False},
    {"id": "tc_076", "lang": "en", "topic": "family", "query": "Section 6 2005 amendment equal coparcenary rights for daughters by birth", "expected_sections": ["Section 6"], "needs_lawyer_verification": False},
    {"id": "tc_077", "lang": "en", "topic": "family", "query": "Can married daughter claim partition share in ancestral land?", "expected_sections": ["Section 6"], "needs_lawyer_verification": False},
    {"id": "tc_078", "lang": "en", "topic": "family", "query": "Protection order under Section 18 of Domestic Violence Act for woman", "expected_sections": ["Section 18 & 19"], "needs_lawyer_verification": False},
    {"id": "tc_079", "lang": "en", "topic": "family", "query": "Right to reside in shared household under Domestic Violence Act Section 19", "expected_sections": ["Section 18 & 19"], "needs_lawyer_verification": False},
    {"id": "tc_080", "lang": "en", "topic": "family", "query": "Maintenance of deserted wife and children under Section 144 BNSS", "expected_sections": ["Section 144"], "needs_lawyer_verification": False},
    {"id": "tc_081", "lang": "kn", "topic": "family", "query": "ಪೂರ್ವಜರ ಆಸ್ತಿಯಲ್ಲಿ ಹೆಣ್ಣುಮಕ್ಕಳಿಗೆ ಗಂಡುಮಕ್ಕಳಷ್ಟೇ ಸಮಾನ ಹಕ್ಕು ಇದೆಯೇ?", "expected_sections": ["Section 6"], "needs_lawyer_verification": False},
    {"id": "tc_082", "lang": "kn", "topic": "family", "query": "ಹಿಂದೂ ಉತ್ತರಾಧಿಕಾರ ಕಾಯ್ದೆ ಸೆಕ್ಷನ್ 6 ಪ್ರಕಾರ ಸಹವೃತ್ತಿದಾರ ಹಕ್ಕುಗಳು", "expected_sections": ["Section 6"], "needs_lawyer_verification": False},
    {"id": "tc_083", "lang": "kn", "topic": "family", "query": "ಪರಸ್ಪರ ಒಪ್ಪಿಗೆಯ ವಿಚ್ಛೇದನದಲ್ಲಿ ಆರು ತಿಂಗಳ ಕಾಯುವ ಅವಧಿ ಮನ್ನಾ ಮಾಡಬಹುದೇ?", "expected_sections": ["Section 13B"], "needs_lawyer_verification": False},
    {"id": "tc_084", "lang": "kn", "topic": "family", "query": "ಗೃಹಹಿಂಸೆ ಕಾಯ್ದೆಯಡಿ ಮಹಿಳೆಗೆ ಹಂಚಿಕೆಯ ಮನೆಯಲ್ಲಿ ವಾಸಿಸುವ ರಕ್ಷಣಾ ಆದೇಶ", "expected_sections": ["Section 18 & 19"], "needs_lawyer_verification": False},
    {"id": "tc_085", "lang": "hi", "topic": "family", "query": "पैतृक संपत्ति में बेटियों का बेटों के बराबर अधिकार हिंदू उत्तराधिकार अधिनियम धारा 6", "expected_sections": ["Section 6"], "needs_lawyer_verification": False},
    {"id": "tc_086", "lang": "hi", "topic": "family", "query": "आपसी सहमति से तलाक के लिए हिंदू विवाह अधिनियम की धारा 13B", "expected_sections": ["Section 13B"], "needs_lawyer_verification": False},
    {"id": "tc_087", "lang": "hi", "topic": "family", "query": "घरेलू हिंसा से महिलाओं का संरक्षण अधिनियम धारा 18 सुरक्षा आदेश", "expected_sections": ["Section 18 & 19"], "needs_lawyer_verification": False},
    {"id": "tc_088", "lang": "mixed", "topic": "family", "query": "Daughters coparcenary right in ancestral property after 2005 amendment", "expected_sections": ["Section 6"], "needs_lawyer_verification": False},
    {"id": "tc_089", "lang": "mixed", "topic": "family", "query": "Patni aur bachon ke maintenance ke liye BNSS me kaun sa section hai?", "expected_sections": ["Section 144"], "needs_lawyer_verification": False},

    # ── REAL ESTATE & CONTRACTS (RERA, CONTRACT ACT, LIMITATION) ──
    {"id": "tc_090", "lang": "en", "topic": "real_estate", "query": "Builder delayed flat handover, refund with interest under Section 18 of RERA", "expected_sections": ["Section 18"], "needs_lawyer_verification": False},
    {"id": "tc_091", "lang": "en", "topic": "real_estate", "query": "Can home buyer demand monthly interest from builder for construction delay?", "expected_sections": ["Section 18"], "needs_lawyer_verification": False},
    {"id": "tc_092", "lang": "en", "topic": "contracts", "query": "Is a non-compete clause in an employment agreement valid in India?", "expected_sections": ["Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_093", "lang": "en", "topic": "contracts", "query": "Section 27 Contract Act agreement in restraint of trade is void", "expected_sections": ["Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_094", "lang": "en", "topic": "contracts", "query": "Limitation period for suing on breach of contract under Limitation Act", "expected_sections": ["Article 54 & Schedule"], "needs_lawyer_verification": False},
    {"id": "tc_095", "lang": "en", "topic": "contracts", "query": "How many years limitation to recover money owed under contract?", "expected_sections": ["Article 54 & Schedule"], "needs_lawyer_verification": False},
    {"id": "tc_096", "lang": "kn", "topic": "real_estate", "query": "ಬಿಲ್ಡರ್ ಫ್ಲಾಟ್ ನೀಡಲು ವಿಳಂಬ ಮಾಡಿದರೆ ರೇರಾ ಸೆಕ್ಷನ್ 18 ರಡಿ ಬಡ್ಡಿ ಸಮೇತ ಮರುಪಾವತಿ", "expected_sections": ["Section 18"], "needs_lawyer_verification": False},
    {"id": "tc_097", "lang": "kn", "topic": "contracts", "query": "ಉದ್ಯೋಗ ಒಪ್ಪಂದದಲ್ಲಿ ಸ್ಪರ್ಧೆ-ನಿಷೇಧ (Non-compete) ಷರತ್ತು ಭಾರತೀಯ ಕಾನೂನಿನಲ್ಲಿ ಊರ್ಜಿತವೇ?", "expected_sections": ["Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_098", "lang": "hi", "topic": "contracts", "query": "क्या नौकरी छोड़ने के बाद नॉन-कंपीट क्लॉज भारत में कानूनी रूप से मान्य है?", "expected_sections": ["Section 27"], "needs_lawyer_verification": False},
    {"id": "tc_099", "lang": "hi", "topic": "real_estate", "query": "बिल्डर द्वारा फ्लैट देने में देरी पर रेरा धारा 18 के तहत ब्याज का दावा", "expected_sections": ["Section 18"], "needs_lawyer_verification": False},

    # ── RTI, CIVIC RIGHTS & FREE LEGAL AID ──
    {"id": "tc_100", "lang": "en", "topic": "civic_rights", "query": "What is the time limit for CPIO to provide information under RTI Act?", "expected_sections": ["Section 7"], "needs_lawyer_verification": False},
    {"id": "tc_101", "lang": "en", "topic": "civic_rights", "query": "RTI application regarding life or liberty must be answered in 48 hours", "expected_sections": ["Section 7"], "needs_lawyer_verification": False},
    {"id": "tc_102", "lang": "en", "topic": "civic_rights", "query": "Who is eligible for free legal aid under Section 12 of NALSA Act?", "expected_sections": ["Free Legal Aid and NALSA/DLSA Helpline 15100"], "needs_lawyer_verification": False},
    {"id": "tc_103", "lang": "en", "topic": "civic_rights", "query": "What is the toll free helpline number for free legal aid in Karnataka?", "expected_sections": ["Free Legal Aid and NALSA/DLSA Helpline 15100"], "needs_lawyer_verification": False},
    {"id": "tc_104", "lang": "en", "topic": "civic_rights", "query": "Is a woman entitled to free legal advocate regardless of income?", "expected_sections": ["Free Legal Aid and NALSA/DLSA Helpline 15100"], "needs_lawyer_verification": False},
    {"id": "tc_105", "lang": "en", "topic": "civic_rights", "query": "Puttaswamy judgment right to privacy as fundamental right under Article 21", "expected_sections": ["(2017) 10 SCC 1", "Article 21"], "needs_lawyer_verification": False},
    {"id": "tc_106", "lang": "kn", "topic": "civic_rights", "query": "ಮಾಹಿತಿ ಹಕ್ಕು ಕಾಯ್ದೆಯಡಿ ಜೀವ ಅಥವಾ ಸ್ವಾತಂತ್ರ್ಯದ ವಿಷಯಕ್ಕೆ 48 ಗಂಟೆಗಳಲ್ಲಿ ಮಾಹಿತಿ", "expected_sections": ["Section 7"], "needs_lawyer_verification": False},
    {"id": "tc_107", "lang": "kn", "topic": "civic_rights", "query": "ಉಚಿತ ಕಾನೂನು ನೆರವು ಪಡೆಯಲು ಅರ್ಹತೆ ಏನು ಮತ್ತು ಸಹಾಯವಾಣಿ 15100 ವಿವರ", "expected_sections": ["Free Legal Aid and NALSA/DLSA Helpline 15100"], "needs_lawyer_verification": False},
    {"id": "tc_108", "lang": "hi", "topic": "civic_rights", "query": "आरटीआई कानून के तहत 30 दिन में जानकारी न मिलने पर क्या करें?", "expected_sections": ["Section 7"], "needs_lawyer_verification": False},
    {"id": "tc_109", "lang": "hi", "topic": "civic_rights", "query": "मुफ्त कानूनी सहायता के लिए राष्ट्रीय हेल्पलाइन 15100 पर कैसे संपर्क करें?", "expected_sections": ["Free Legal Aid and NALSA/DLSA Helpline 15100"], "needs_lawyer_verification": False},

    # ── LEGACY IPC / CRPC TRANSITION (CONCORDANCE CHECK) ──
    {"id": "tc_110", "lang": "en", "topic": "legacy_concordance", "query": "How to file case for cheating under IPC 420?", "expected_sections": ["Section 318(4)"], "needs_lawyer_verification": False},
    {"id": "tc_111", "lang": "en", "topic": "legacy_concordance", "query": "What is the new section replacing IPC 302 for murder in BNS?", "expected_sections": ["Section 103"], "needs_lawyer_verification": False},
    {"id": "tc_112", "lang": "en", "topic": "legacy_concordance", "query": "Anticipatory bail under CrPC 438 in 2024", "expected_sections": ["Section 482"], "needs_lawyer_verification": False},
    {"id": "tc_113", "lang": "en", "topic": "legacy_concordance", "query": "Notice of appearance Section 41A CrPC equivalent in BNSS", "expected_sections": ["Section 35"], "needs_lawyer_verification": False},
    {"id": "tc_114", "lang": "en", "topic": "legacy_concordance", "query": "FIR registration Section 154 CrPC replaced by Section 173 BNSS", "expected_sections": ["Section 173"], "needs_lawyer_verification": False},
    {"id": "tc_115", "lang": "kn", "topic": "legacy_concordance", "query": "ಐಪಿಸಿ 420 ಬದಲಿಗೆ ಭಾರತೀಯ ನ್ಯಾಯ ಸಂಹಿತೆಯಲ್ಲಿ ಯಾವ ಸೆಕ್ಷನ್ ಇದೆ?", "expected_sections": ["Section 318(4)"], "needs_lawyer_verification": False},
    {"id": "tc_116", "lang": "hi", "topic": "legacy_concordance", "query": "आईपीसी धारा 420 धोखाधड़ी का नया सेक्शन बीएनएस में क्या है?", "expected_sections": ["Section 318(4)"], "needs_lawyer_verification": False},
    {"id": "tc_117", "lang": "mixed", "topic": "legacy_concordance", "query": "Police FIR nahi le rahi CrPC 154 replacement in new criminal law", "expected_sections": ["Section 173"], "needs_lawyer_verification": False},
    {"id": "tc_118", "lang": "mixed", "topic": "legacy_concordance", "query": "CrPC 438 anticipatory bail Karnataka Sessions Court BNSS provision", "expected_sections": ["Section 482"], "needs_lawyer_verification": False},

    # ── OUT OF SCOPE / ADVERSARIAL / NO MATCH (SHOULD RETURN NO MATCH / LOW) ──
    {"id": "tc_119", "lang": "en", "topic": "out_of_scope", "query": "How to bake a chocolate fudge cake recipe", "expected_sections": [], "needs_lawyer_verification": False},
    {"id": "tc_120", "lang": "en", "topic": "out_of_scope", "query": "Who won the cricket world cup 2023?", "expected_sections": [], "needs_lawyer_verification": False},
    {"id": "tc_121", "lang": "en", "topic": "out_of_scope", "query": "Current weather forecast in Bengaluru tomorrow", "expected_sections": [], "needs_lawyer_verification": False},
    {"id": "tc_122", "lang": "en", "topic": "out_of_scope", "query": "What is the capital city of France?", "expected_sections": [], "needs_lawyer_verification": False},
    {"id": "tc_123", "lang": "en", "topic": "out_of_scope", "query": "Write a python script to reverse a linked list", "expected_sections": [], "needs_lawyer_verification": False},
    {"id": "tc_124", "lang": "hi", "topic": "out_of_scope", "query": "चॉकलेट केक बनाने की सबसे अच्छी रेसिपी क्या है?", "expected_sections": [], "needs_lawyer_verification": False},
    {"id": "tc_125", "lang": "kn", "topic": "out_of_scope", "query": "ನಾಳೆ ಬೆಂಗಳೂರಿನ ಹವಾಮಾನ ವರದಿ ಏನು?", "expected_sections": [], "needs_lawyer_verification": False},
]

# Expand programmatically to >150 items across permutations of keywords and phrasing
def generate_full_testset():
    full_set = list(TEST_ITEMS)
    counter = len(full_set) + 1

    variations = [
        # Tenancy variations
        ("en", "tenancy", "How to issue legal demand notice to landlord for security advance refund?", ["Section 108", "Section 27"]),
        ("en", "tenancy", "Landlord deducted 30000 rupees for repainting walls without handover agreement", ["Section 108"]),
        ("kn", "tenancy", "ಮನೆ ಬಾಡಿಗೆ ಒಪ್ಪಂದ ಮುಗಿದ ನಂತರ ಠೇವಣಿ ಮರುಪಾವತಿ ಮಾಡದಿದ್ದರೆ ಬಾಡಿಗೆ ನಿಯಂತ್ರಕರಿಗೆ ದೂರು", ["Section 27"]),
        ("hi", "tenancy", "मकान खाली करने के बाद सिक्योरिटी डिपॉजिट ना मिलने पर रेंट कंट्रोलर के पास कैसे जाएं?", ["Section 27"]),
        ("mixed", "tenancy", "Tenancy security thevani return agilla Belagavi Court help", ["Section 27", "Section 108"]),

        # Cheque variations
        ("en", "cheque_bounce", "Statutory demand notice under Section 138 proviso (b) within thirty days", ["Section 138"]),
        ("en", "cheque_bounce", "Cheque dishonoured memo received from bank on 10th November, what is last date?", ["Section 138"]),
        ("kn", "cheque_bounce", "ಬ್ಯಾಂಕ್‌ನಿಂದ ಚೆಕ್ ರಿಟರ್ನ್ ಮೆಮೊ ಬಂದ ನಂತರ 30 ದಿನಗಳ ಕಾಲಮಿತಿ ನೋಟಿಸ್", ["Section 138"]),
        ("hi", "cheque_bounce", "बैंक से चेक वापसी मेमो मिलने के बाद नोटिस भेजने का 30 दिन का नियम", ["Section 138"]),
        ("mixed", "cheque_bounce", "Bank memo aagi 20 days aayithu Section 138 notice baribahuda?", ["Section 138"]),

        # Criminal & Arrest variations
        ("en", "criminal_arrest", "Police custody remand maximum days under Section 187 of BNSS", ["Section 187"]),
        ("en", "criminal_arrest", "Right of arrestee to inform family member within 12 hours under DK Basu", ["(1997) 1 SCC 416", "Article 22"]),
        ("en", "criminal_arrest", "Cognizable offence FIR registration mandatory at police station", ["Section 173"]),
        ("kn", "criminal_arrest", "ಬಂಧನದ ಸಮಯದಲ್ಲಿ ಡಿ.ಕೆ. ಬಸು ಮಾರ್ಗಸೂಚಿಗಳ ಪಾಲನೆ ಮತ್ತು ಬಂಧನ ಜ್ಞಾಪಕ ಪತ್ರ (Memo)", ["(1997) 1 SCC 416", "Article 22"]),
        ("hi", "criminal_arrest", "डीके बसू गाइडलाइंस के अनुसार गिरफ्तारी मेमो और मेडिकल जांच का अधिकार", ["(1997) 1 SCC 416", "Article 22"]),

        # Succession & Family variations
        ("en", "family", "Can brother exclude sister from grandfather ancestral property partition?", ["Section 6"]),
        ("kn", "family", "ತಂದೆಯ ಪೂರ್ವಜರ ಆಸ್ತಿಯಲ್ಲಿ ಹೆಣ್ಣುಮಕ್ಕಳಿಗೆ ಹಕ್ಕು ನಿರಾಕರಿಸಬಹುದೇ?", ["Section 6"]),
        ("hi", "family", "क्या पैतृक कृषि भूमि में विवाहित बेटी का बराबर हिस्सा होता है?", ["Section 6"]),
        ("mixed", "family", "Ancestral property partition suit Belagavi District Court daughters share", ["Section 6"]),

        # Consumer variations
        ("en", "consumer", "Deficiency in airline service lost luggage compensation e-Daakhil", ["Section 35"]),
        ("kn", "consumer", "ಆನ್‌ಲೈನ್ ಕಂಪನಿಯಿಂದ ದೋಷಪೂರಿತ ಮೊಬೈಲ್ ಡೆಲಿವರಿ ಗ್ರಾಹಕ ವೇದಿಕೆಯಲ್ಲಿ ದೂರು", ["Section 35"]),
        ("hi", "consumer", "ई-कॉमर्स कंपनी द्वारा खराब सामान बेचने पर जिला उपभोक्ता आयोग में केस", ["Section 35"]),

        # Contract variations
        ("en", "contracts", "Company enforcing 2-year post employment non compete restriction", ["Section 27"]),
        ("kn", "contracts", "ಉದ್ಯೋಗ ಬಿಟ್ಟ ನಂತರ ಬೇರೆ ಕಂಪನಿಯಲ್ಲಿ ಕೆಲಸ ಮಾಡಬಾರದು ಎಂಬ ಷರತ್ತು ಮಾನ್ಯವೇ?", ["Section 27"]),

        # RTI variations
        ("en", "civic_rights", "CPIO rejected RTI application, appeal procedure under RTI Act", ["Section 7"]),
        ("kn", "civic_rights", "ಮಾಹಿತಿ ಹಕ್ಕು ಅರ್ಜಿಗೆ ಸಾರ್ವಜನಿಕ ಮಾಹಿತಿ ಅಧಿಕಾರಿಯು 30 ದಿನದಲ್ಲಿ ಉತ್ತರ ನೀಡಬೇಕು", ["Section 7"]),
        ("hi", "civic_rights", "आरटीआई आवेदन पर जन सूचना अधिकारी द्वारा 30 दिनों में उत्तर देने का नियम", ["Section 7"]),

        # Additional out of scope
        ("en", "out_of_scope", "Best tourist places to visit in Switzerland during winter", []),
        ("en", "out_of_scope", "How to install nodejs on ubuntu server", []),
        ("hi", "out_of_scope", "क्रिकेट में सबसे ज्यादा रन किस बल्लेबाज ने बनाए हैं?", []),
        ("kn", "out_of_scope", "ಮೈಸೂರು ಪಾಕ್ ಮಾಡುವ ಸುಲಭ ವಿಧಾನ ತಿಳಿಸಿ", []),
    ]

    for lang, topic, query, expected in variations:
        full_set.append({
            "id": f"tc_{counter:03d}",
            "lang": lang,
            "topic": topic,
            "query": query,
            "expected_sections": expected,
            "needs_lawyer_verification": False,
        })
        counter += 1

    return full_set


def main():
    items = generate_full_testset()
    eval_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(eval_dir, "testset.jsonl")
    with open(out_path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Generated {len(items)} benchmark test queries to {out_path}")


if __name__ == "__main__":
    main()
