"""All user-facing text in English, Hindi and Kannada.

Keep every key present in all three languages; tests/test_i18n.py checks this.
Placeholders like {brand} and {domain} are filled in by explain.py.
"""

LANGS = {"en": "English", "hi": "हिंदी", "kn": "ಕನ್ನಡ"}

VERDICTS = {
    "scam": {
        "en": ("Likely scam", "This message is very likely a scam"),
        "hi": ("धोखा", "यह संदेश लगभग पक्का धोखा है"),
        "kn": ("ವಂಚನೆ", "ಈ ಸಂದೇಶ ಬಹುತೇಕ ವಂಚನೆ"),
    },
    "suspicious": {
        "en": ("Suspicious", "Be careful, this message looks suspicious"),
        "hi": ("संदिग्ध", "सावधान, यह संदेश संदिग्ध लगता है"),
        "kn": ("ಅನುಮಾನಾಸ್ಪದ", "ಎಚ್ಚರ, ಈ ಸಂದೇಶ ಅನುಮಾನಾಸ್ಪದವಾಗಿದೆ"),
    },
    "no_signs": {
        "en": ("No red flags", "No common scam signs found"),
        "hi": ("कोई संकेत नहीं", "धोखे के आम संकेत नहीं मिले"),
        "kn": ("ಲಕ್ಷಣಗಳಿಲ್ಲ", "ಸಾಮಾನ್ಯ ವಂಚನೆಯ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿಲ್ಲ"),
    },
}

FLAGS = {
    "otp_request": {
        "en": ("Asks for your OTP or PIN", "Banks and apps never ask you to share an OTP, PIN or CVV. Anyone who asks can empty your account."),
        "hi": ("आपका OTP या PIN मांगा गया है", "बैंक और ऐप कभी OTP, PIN या CVV शेयर करने को नहीं कहते। जो मांगता है, वह आपका खाता खाली कर सकता है।"),
        "kn": ("ನಿಮ್ಮ OTP ಅಥವಾ PIN ಕೇಳುತ್ತಿದೆ", "ಬ್ಯಾಂಕ್‌ಗಳು ಮತ್ತು ಆ್ಯಪ್‌ಗಳು OTP, PIN ಅಥವಾ CVV ಹಂಚಿಕೊಳ್ಳಲು ಎಂದಿಗೂ ಕೇಳುವುದಿಲ್ಲ. ಕೇಳುವವರು ನಿಮ್ಮ ಖಾತೆಯನ್ನು ಖಾಲಿ ಮಾಡಬಹುದು."),
    },
    "upi_pin_receive": {
        "en": ("Says you need your UPI PIN to receive money", "You never enter a UPI PIN or scan a QR code to receive money. Entering it sends money out of your account."),
        "hi": ("पैसे पाने के लिए UPI PIN डालने को कहता है", "पैसे पाने के लिए कभी UPI PIN डालना या QR स्कैन करना नहीं पड़ता। PIN डालने से पैसा आपके खाते से जाता है।"),
        "kn": ("ಹಣ ಪಡೆಯಲು UPI PIN ಹಾಕಲು ಹೇಳುತ್ತಿದೆ", "ಹಣ ಪಡೆಯಲು UPI PIN ಹಾಕುವ ಅಥವಾ QR ಸ್ಕ್ಯಾನ್ ಮಾಡುವ ಅಗತ್ಯವಿಲ್ಲ. PIN ಹಾಕಿದರೆ ಹಣ ನಿಮ್ಮ ಖಾತೆಯಿಂದ ಹೋಗುತ್ತದೆ."),
    },
    "remote_access": {
        "en": ("Asks you to install an app or share your screen", "Apps like AnyDesk, or an APK file from a message, let a stranger see and control your phone, including your banking apps."),
        "hi": ("ऐप इंस्टॉल करने या स्क्रीन शेयर करने को कहता है", "AnyDesk जैसे ऐप या संदेश से आई APK फ़ाइल से कोई अजनबी आपका फ़ोन और बैंकिंग ऐप देख और चला सकता है।"),
        "kn": ("ಆ್ಯಪ್ ಇನ್‌ಸ್ಟಾಲ್ ಮಾಡಲು ಅಥವಾ ಸ್ಕ್ರೀನ್ ಹಂಚಿಕೊಳ್ಳಲು ಹೇಳುತ್ತಿದೆ", "AnyDesk ನಂತಹ ಆ್ಯಪ್ ಅಥವಾ ಸಂದೇಶದಿಂದ ಬಂದ APK ಮೂಲಕ ಅಪರಿಚಿತರು ನಿಮ್ಮ ಫೋನ್ ಮತ್ತು ಬ್ಯಾಂಕಿಂಗ್ ಆ್ಯಪ್‌ಗಳನ್ನು ನಿಯಂತ್ರಿಸಬಹುದು."),
    },
    "digital_arrest": {
        "en": ("Threatens arrest or legal action", "Police, the CBI and other agencies don't arrest people over video calls or ask for money to close a case. A \"digital arrest\" is always a scam."),
        "hi": ("गिरफ्तारी या कानूनी कार्रवाई की धमकी", "पुलिस, CBI या कोई एजेंसी वीडियो कॉल पर गिरफ्तार नहीं करती और केस बंद करने के पैसे नहीं मांगती। \"डिजिटल अरेस्ट\" हमेशा धोखा है।"),
        "kn": ("ಬಂಧನ ಅಥವಾ ಕಾನೂನು ಕ್ರಮದ ಬೆದರಿಕೆ", "ಪೊಲೀಸ್, CBI ಅಥವಾ ಯಾವುದೇ ಸಂಸ್ಥೆ ವಿಡಿಯೋ ಕರೆಯಲ್ಲಿ ಬಂಧಿಸುವುದಿಲ್ಲ, ಪ್ರಕರಣ ಮುಚ್ಚಲು ಹಣ ಕೇಳುವುದಿಲ್ಲ. \"ಡಿಜಿಟಲ್ ಅರೆಸ್ಟ್\" ಯಾವಾಗಲೂ ವಂಚನೆ."),
    },
    "kyc_block": {
        "en": ("Says your account or KYC needs urgent action", "Fake \"KYC expired\" and \"account blocked\" alerts send you to a fake login page. A real bank asks you to visit a branch or use its official app."),
        "hi": ("खाता या KYC पर तुरंत कार्रवाई की बात", "नकली \"KYC खत्म\" या \"खाता ब्लॉक\" संदेश आपको नकली लॉगिन पेज पर ले जाते हैं। असली बैंक शाखा या अपने आधिकारिक ऐप पर बुलाता है।"),
        "kn": ("ಖಾತೆ ಅಥವಾ KYC ಬಗ್ಗೆ ತುರ್ತು ಕ್ರಮ ಕೇಳುತ್ತಿದೆ", "ನಕಲಿ \"KYC ಅವಧಿ ಮುಗಿದಿದೆ\" ಅಥವಾ \"ಖಾತೆ ಬ್ಲಾಕ್\" ಸಂದೇಶಗಳು ನಕಲಿ ಲಾಗಿನ್ ಪುಟಕ್ಕೆ ಕರೆದೊಯ್ಯುತ್ತವೆ. ನಿಜವಾದ ಬ್ಯಾಂಕ್ ಶಾಖೆಗೆ ಅಥವಾ ಅಧಿಕೃತ ಆ್ಯಪ್‌ಗೆ ಬರಲು ಹೇಳುತ್ತದೆ."),
    },
    "prize": {
        "en": ("Promises a prize, lottery or reward", "You can't win a lottery you never entered. These messages lead to a \"processing fee\" or a link that steals your details."),
        "hi": ("इनाम, लॉटरी या रिवॉर्ड का वादा", "जिस लॉटरी में आपने हिस्सा नहीं लिया, वह आप नहीं जीत सकते। ऐसे संदेश \"प्रोसेसिंग फीस\" या जानकारी चुराने वाले लिंक तक ले जाते हैं।"),
        "kn": ("ಬಹುಮಾನ, ಲಾಟರಿ ಅಥವಾ ರಿವಾರ್ಡ್ ಭರವಸೆ", "ನೀವು ಭಾಗವಹಿಸದ ಲಾಟರಿಯನ್ನು ಗೆಲ್ಲಲು ಸಾಧ್ಯವಿಲ್ಲ. ಇಂತಹ ಸಂದೇಶಗಳು \"ಪ್ರೊಸೆಸಿಂಗ್ ಶುಲ್ಕ\" ಅಥವಾ ಮಾಹಿತಿ ಕದಿಯುವ ಲಿಂಕ್‌ಗೆ ಕರೆದೊಯ್ಯುತ್ತವೆ."),
    },
    "job_task": {
        "en": ("Offers easy money for simple online tasks", "Task scams pay a little at first, then ask you to \"invest\" to unlock bigger payouts, and keep that money."),
        "hi": ("आसान ऑनलाइन काम के बदले पैसे", "टास्क स्कैम पहले थोड़े पैसे देते हैं, फिर बड़ी कमाई के नाम पर \"निवेश\" करवाकर पैसा रख लेते हैं।"),
        "kn": ("ಸುಲಭ ಆನ್‌ಲೈನ್ ಕೆಲಸಕ್ಕೆ ಹಣದ ಆಮಿಷ", "ಟಾಸ್ಕ್ ವಂಚನೆಗಳು ಮೊದಲು ಸ್ವಲ್ಪ ಹಣ ಕೊಡುತ್ತವೆ, ನಂತರ ದೊಡ್ಡ ಗಳಿಕೆಯ ಹೆಸರಲ್ಲಿ \"ಹೂಡಿಕೆ\" ಮಾಡಿಸಿ ಆ ಹಣ ಇಟ್ಟುಕೊಳ್ಳುತ್ತವೆ."),
    },
    "courier_issue": {
        "en": ("Claims a problem with a parcel", "Fake delivery messages ask you to \"update your address\" or pay a small fee through a link. Check the order in the courier's own app instead."),
        "hi": ("पार्सल में समस्या का दावा", "नकली डिलीवरी संदेश लिंक से \"पता अपडेट\" करने या छोटी फीस भरने को कहते हैं। ऑर्डर कूरियर के अपने ऐप में देखें।"),
        "kn": ("ಪಾರ್ಸೆಲ್‌ನಲ್ಲಿ ಸಮಸ್ಯೆ ಇದೆ ಎನ್ನುತ್ತಿದೆ", "ನಕಲಿ ಡೆಲಿವರಿ ಸಂದೇಶಗಳು ಲಿಂಕ್ ಮೂಲಕ \"ವಿಳಾಸ ಅಪ್ಡೇಟ್\" ಮಾಡಲು ಅಥವಾ ಸಣ್ಣ ಶುಲ್ಕ ಕಟ್ಟಲು ಹೇಳುತ್ತವೆ. ಆರ್ಡರ್ ಅನ್ನು ಕೊರಿಯರ್‌ನ ಸ್ವಂತ ಆ್ಯಪ್‌ನಲ್ಲಿ ಪರಿಶೀಲಿಸಿ."),
    },
    "bill_disconnect": {
        "en": ("Threatens to cut your electricity or service", "Power companies send notices through official channels. They don't text from a personal number asking you to call tonight."),
        "hi": ("बिजली या सेवा काटने की धमकी", "बिजली कंपनी आधिकारिक माध्यम से नोटिस भेजती है। वह किसी निजी नंबर से आज रात कॉल करने को नहीं कहती।"),
        "kn": ("ವಿದ್ಯುತ್ ಅಥವಾ ಸೇವೆ ಕಡಿತದ ಬೆದರಿಕೆ", "ವಿದ್ಯುತ್ ಕಂಪನಿಗಳು ಅಧಿಕೃತ ಮಾರ್ಗದಲ್ಲಿ ನೋಟಿಸ್ ಕಳುಹಿಸುತ್ತವೆ. ಖಾಸಗಿ ನಂಬರ್‌ನಿಂದ ಇಂದು ರಾತ್ರಿಯೇ ಕರೆ ಮಾಡಲು ಹೇಳುವುದಿಲ್ಲ."),
    },
    "investment": {
        "en": ("Promises guaranteed or very high returns", "Real investments can't guarantee returns. \"Tips groups\" and trading apps from strangers are a common way people lose their savings."),
        "hi": ("पक्का या बहुत ज़्यादा मुनाफ़ा देने का वादा", "असली निवेश में पक्का मुनाफ़ा नहीं होता। अजनबियों के \"टिप्स ग्रुप\" और ट्रेडिंग ऐप से लोग अपनी बचत गंवाते हैं।"),
        "kn": ("ಖಚಿತ ಅಥವಾ ಅತಿ ಹೆಚ್ಚು ಲಾಭದ ಭರವಸೆ", "ನಿಜವಾದ ಹೂಡಿಕೆಯಲ್ಲಿ ಲಾಭ ಖಚಿತವಿರುವುದಿಲ್ಲ. ಅಪರಿಚಿತರ \"ಟಿಪ್ಸ್ ಗ್ರೂಪ್\" ಮತ್ತು ಟ್ರೇಡಿಂಗ್ ಆ್ಯಪ್‌ಗಳಿಂದ ಜನರು ಉಳಿತಾಯ ಕಳೆದುಕೊಳ್ಳುತ್ತಾರೆ."),
    },
    "fee_request": {
        "en": ("Asks for a fee before you get something", "Charging a fee to release a prize, job, refund or parcel is how many scams take money."),
        "hi": ("कुछ पाने से पहले फीस मांगता है", "इनाम, नौकरी, रिफंड या पार्सल के लिए फीस भरवाना धोखे का आम तरीका है।"),
        "kn": ("ಏನನ್ನಾದರೂ ಪಡೆಯುವ ಮೊದಲು ಶುಲ್ಕ ಕೇಳುತ್ತಿದೆ", "ಬಹುಮಾನ, ಕೆಲಸ, ರೀಫಂಡ್ ಅಥವಾ ಪಾರ್ಸೆಲ್‌ಗಾಗಿ ಶುಲ್ಕ ಕಟ್ಟಿಸುವುದು ವಂಚನೆಯ ಸಾಮಾನ್ಯ ವಿಧಾನ."),
    },
    "off_platform": {
        "en": ("Moves you to Telegram or a private chat", "Scammers pull you off official channels so there's no record and no way to report them inside the app."),
        "hi": ("Telegram या निजी चैट पर बुलाता है", "धोखेबाज़ आपको आधिकारिक माध्यम से हटाकर निजी चैट पर ले जाते हैं ताकि कोई रिकॉर्ड न रहे।"),
        "kn": ("Telegram ಅಥವಾ ಖಾಸಗಿ ಚಾಟ್‌ಗೆ ಕರೆಯುತ್ತಿದೆ", "ವಂಚಕರು ದಾಖಲೆ ಉಳಿಯದಂತೆ ನಿಮ್ಮನ್ನು ಅಧಿಕೃತ ಮಾರ್ಗದಿಂದ ಖಾಸಗಿ ಚಾಟ್‌ಗೆ ಕರೆದೊಯ್ಯುತ್ತಾರೆ."),
    },
    "urgency": {
        "en": ("Rushes you to act now", "A deadline of hours or minutes is there to stop you checking with someone first."),
        "hi": ("तुरंत कुछ करने का दबाव", "घंटों या मिनटों की समय सीमा इसलिए दी जाती है ताकि आप पहले किसी से पूछ न सकें।"),
        "kn": ("ತಕ್ಷಣ ಏನಾದರೂ ಮಾಡುವಂತೆ ಒತ್ತಡ", "ಗಂಟೆ ಅಥವಾ ನಿಮಿಷಗಳ ಗಡುವು ನೀವು ಮೊದಲು ಯಾರನ್ನಾದರೂ ಕೇಳದಂತೆ ತಡೆಯಲು."),
    },
    "link_lookalike": {
        "en": ("Link imitates {brand}", "The link goes to {domain}, which is not an official {brand} website."),
        "hi": ("लिंक {brand} की नकल करता है", "यह लिंक {domain} पर जाता है, जो {brand} की आधिकारिक वेबसाइट नहीं है।"),
        "kn": ("ಲಿಂಕ್ {brand} ಅನ್ನು ನಕಲು ಮಾಡುತ್ತಿದೆ", "ಈ ಲಿಂಕ್ {domain} ಗೆ ಹೋಗುತ್ತದೆ, ಇದು {brand} ನ ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್ ಅಲ್ಲ."),
    },
    "link_brand_in_subdomain": {
        "en": ("Link hides another site behind {brand}'s name", "The link starts with {brand}, but the site that owns it is {domain}. The owner is the name just before the .com or .in ending."),
        "hi": ("लिंक {brand} के नाम के पीछे दूसरी साइट छिपाता है", "लिंक {brand} से शुरू होता है, पर असल में {domain} का है। असली मालिक वह नाम है जो .com या .in से ठीक पहले आता है।"),
        "kn": ("ಲಿಂಕ್ {brand} ಹೆಸರಿನ ಹಿಂದೆ ಬೇರೆ ಸೈಟ್ ಅಡಗಿಸಿದೆ", "ಲಿಂಕ್ {brand} ನಿಂದ ಶುರುವಾದರೂ ನಿಜವಾಗಿ {domain} ಗೆ ಸೇರಿದೆ. ನಿಜವಾದ ಮಾಲೀಕರು .com ಅಥವಾ .in ಗಿಂತ ಸ್ವಲ್ಪ ಮೊದಲು ಬರುವ ಹೆಸರು."),
    },
    "brand_unofficial_link": {
        "en": ("Mentions {brand} but links somewhere else", "The message names {brand}, but its link goes to {domain}."),
        "hi": ("{brand} का नाम, पर लिंक कहीं और", "संदेश में {brand} का नाम है, पर लिंक {domain} पर जाता है।"),
        "kn": ("{brand} ಹೆಸರು, ಆದರೆ ಲಿಂಕ್ ಬೇರೆಡೆಗೆ", "ಸಂದೇಶದಲ್ಲಿ {brand} ಹೆಸರಿದೆ, ಆದರೆ ಲಿಂಕ್ {domain} ಗೆ ಹೋಗುತ್ತದೆ."),
    },
    "link_shortener": {
        "en": ("Uses a shortened link", "{domain} hides where the link really goes."),
        "hi": ("छोटा किया हुआ लिंक", "{domain} यह छिपाता है कि लिंक असल में कहां जाता है।"),
        "kn": ("ಚಿಕ್ಕದಾಗಿಸಿದ ಲಿಂಕ್", "ಲಿಂಕ್ ನಿಜವಾಗಿ ಎಲ್ಲಿಗೆ ಹೋಗುತ್ತದೆ ಎಂಬುದನ್ನು {domain} ಮರೆಮಾಡುತ್ತದೆ."),
    },
    "link_risky_tld": {
        "en": ("Link has an unusual ending", "Web addresses ending in {domain} are cheap to register and common in scam links."),
        "hi": ("लिंक का पता असामान्य है", "{domain} पर खत्म होने वाले पते सस्ते मिलते हैं और धोखे के लिंक में आम हैं।"),
        "kn": ("ಲಿಂಕ್‌ನ ವಿಳಾಸ ಅಸಾಮಾನ್ಯವಾಗಿದೆ", "{domain} ನಲ್ಲಿ ಕೊನೆಗೊಳ್ಳುವ ವಿಳಾಸಗಳು ಅಗ್ಗವಾಗಿ ಸಿಗುತ್ತವೆ ಮತ್ತು ವಂಚನೆ ಲಿಂಕ್‌ಗಳಲ್ಲಿ ಸಾಮಾನ್ಯ."),
    },
    "link_ip": {
        "en": ("Link is a bare number address", "Real companies use a name, not a number like {domain}."),
        "hi": ("लिंक सिर्फ़ नंबर वाला पता है", "असली कंपनियां नाम वाला पता इस्तेमाल करती हैं, {domain} जैसा नंबर नहीं।"),
        "kn": ("ಲಿಂಕ್ ಕೇವಲ ಸಂಖ್ಯೆಯ ವಿಳಾಸ", "ನಿಜವಾದ ಕಂಪನಿಗಳು ಹೆಸರಿನ ವಿಳಾಸ ಬಳಸುತ್ತವೆ, {domain} ನಂತಹ ಸಂಖ್ಯೆ ಅಲ್ಲ."),
    },
    "link_punycode": {
        "en": ("Link uses look-alike letters", "{domain} borrows letters from other alphabets to look like a name you know."),
        "hi": ("लिंक में मिलते-जुलते अक्षर", "{domain} दूसरी लिपियों के अक्षरों से किसी जाने-पहचाने नाम जैसा दिखता है।"),
        "kn": ("ಲಿಂಕ್‌ನಲ್ಲಿ ಹೋಲುವ ಅಕ್ಷರಗಳು", "{domain} ಪರಿಚಿತ ಹೆಸರಿನಂತೆ ಕಾಣಲು ಬೇರೆ ಲಿಪಿಯ ಅಕ್ಷರಗಳನ್ನು ಬಳಸುತ್ತದೆ."),
    },
    "link_apk": {
        "en": ("Link downloads an app file", "An .apk file from a message can take over your phone. Install apps only from the Play Store."),
        "hi": ("लिंक से ऐप फ़ाइल डाउनलोड होती है", "संदेश से आई .apk फ़ाइल आपका फ़ोन कब्ज़े में ले सकती है। ऐप सिर्फ़ Play Store से इंस्टॉल करें।"),
        "kn": ("ಲಿಂಕ್ ಆ್ಯಪ್ ಫೈಲ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡುತ್ತದೆ", "ಸಂದೇಶದಿಂದ ಬಂದ .apk ನಿಮ್ಮ ಫೋನ್ ಅನ್ನು ವಶಪಡಿಸಿಕೊಳ್ಳಬಹುದು. ಆ್ಯಪ್‌ಗಳನ್ನು Play Store ನಿಂದ ಮಾತ್ರ ಇನ್‌ಸ್ಟಾಲ್ ಮಾಡಿ."),
    },
    "off_platform_link": {
        "en": ("Link opens a Telegram or WhatsApp chat", "{domain} takes you to a private chat with a stranger, outside any official channel."),
        "hi": ("लिंक Telegram या WhatsApp चैट खोलता है", "{domain} आपको किसी अजनबी से निजी चैट में ले जाता है, किसी आधिकारिक माध्यम के बाहर।"),
        "kn": ("ಲಿಂಕ್ Telegram ಅಥವಾ WhatsApp ಚಾಟ್ ತೆರೆಯುತ್ತದೆ", "{domain} ನಿಮ್ಮನ್ನು ಅಧಿಕೃತ ಮಾರ್ಗದ ಹೊರಗೆ ಅಪರಿಚಿತರ ಖಾಸಗಿ ಚಾಟ್‌ಗೆ ಕರೆದೊಯ್ಯುತ್ತದೆ."),
    },
    "model_wording": {
        "en": ("Wording matches known scam messages", "A classifier trained on labelled scam and normal messages rates this wording {pct}% likely to be a scam."),
        "hi": ("शब्द जाने-पहचाने धोखे वाले संदेशों जैसे हैं", "धोखे और सामान्य संदेशों पर प्रशिक्षित मॉडल इस भाषा को {pct}% धोखे जैसा मानता है।"),
        "kn": ("ಪದಗಳು ಪರಿಚಿತ ವಂಚನೆ ಸಂದೇಶಗಳಂತಿವೆ", "ವಂಚನೆ ಮತ್ತು ಸಾಮಾನ್ಯ ಸಂದೇಶಗಳ ಮೇಲೆ ತರಬೇತಿ ಪಡೆದ ಮಾದರಿ ಈ ಭಾಷೆಯನ್ನು {pct}% ವಂಚನೆಯಂತೆ ಪರಿಗಣಿಸುತ್ತದೆ."),
    },
}

ACTIONS = {
    "warn": {
        "en": [
            "Don't click the link, reply, or share any code.",
            "If you've already paid or shared details, call 1930 right away or report at cybercrime.gov.in.",
            "Report the sender on Sanchar Saathi (Chakshu) at sancharsaathi.gov.in, then block them.",
        ],
        "hi": [
            "लिंक पर क्लिक न करें, जवाब न दें और कोई कोड शेयर न करें।",
            "अगर पैसे दे चुके हैं या जानकारी शेयर कर चुके हैं, तो तुरंत 1930 पर कॉल करें या cybercrime.gov.in पर शिकायत करें।",
            "भेजने वाले की शिकायत sancharsaathi.gov.in पर संचार साथी (चक्षु) में करें, फिर उसे ब्लॉक करें।",
        ],
        "kn": [
            "ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ, ಉತ್ತರಿಸಬೇಡಿ, ಯಾವುದೇ ಕೋಡ್ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ.",
            "ಈಗಾಗಲೇ ಹಣ ಕೊಟ್ಟಿದ್ದರೆ ಅಥವಾ ಮಾಹಿತಿ ಹಂಚಿಕೊಂಡಿದ್ದರೆ, ತಕ್ಷಣ 1930 ಗೆ ಕರೆ ಮಾಡಿ ಅಥವಾ cybercrime.gov.in ನಲ್ಲಿ ದೂರು ನೀಡಿ.",
            "ಕಳುಹಿಸಿದವರ ಬಗ್ಗೆ sancharsaathi.gov.in ನಲ್ಲಿ ಸಂಚಾರ ಸಾಥಿ (ಚಕ್ಷು) ಮೂಲಕ ದೂರು ನೀಡಿ, ನಂತರ ಬ್ಲಾಕ್ ಮಾಡಿ.",
        ],
    },
    "clean": {
        "en": [
            "This checker knows common scam patterns, so a clean result doesn't prove a message is safe.",
            "If it asks for money, codes or personal details, check with the company using the number on its official website or your card.",
        ],
        "hi": [
            "यह जांच आम धोखों के तरीके पहचानती है, इसलिए साफ़ नतीजे का मतलब पक्की सुरक्षा नहीं।",
            "अगर यह पैसे, कोड या निजी जानकारी मांगे, तो कंपनी की आधिकारिक वेबसाइट या अपने कार्ड पर लिखे नंबर से पुष्टि करें।",
        ],
        "kn": [
            "ಈ ಪರಿಶೀಲನೆ ಸಾಮಾನ್ಯ ವಂಚನೆ ವಿಧಾನಗಳನ್ನು ಗುರುತಿಸುತ್ತದೆ, ಹಾಗಾಗಿ ಸ್ವಚ್ಛ ಫಲಿತಾಂಶವು ಸುರಕ್ಷತೆಯ ಖಾತರಿಯಲ್ಲ.",
            "ಹಣ, ಕೋಡ್ ಅಥವಾ ವೈಯಕ್ತಿಕ ಮಾಹಿತಿ ಕೇಳಿದರೆ, ಕಂಪನಿಯ ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್ ಅಥವಾ ನಿಮ್ಮ ಕಾರ್ಡ್‌ನಲ್ಲಿರುವ ನಂಬರ್‌ಗೆ ಕರೆ ಮಾಡಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
        ],
    },
}

UI = {
    "en": {
        "title": "Asli: check a message before you trust it",
        "heading": "Is this message asli?",
        "lede": "Paste a message you got on WhatsApp or SMS. Asli checks it for the tricks scammers use in India and tells you what it found.",
        "label": "Message",
        "placeholder": "Paste the message here",
        "or_image": "Or check a screenshot",
        "check": "Check message",
        "checking": "Checking…",
        "why": "What we found",
        "links": "Links in this message",
        "goes_to": "Goes to",
        "official": "Official site",
        "not_official": "Not an official site",
        "what_to_do": "What to do",
        "feedback_q": "Was this result right?",
        "yes": "Yes",
        "no": "No, it's wrong",
        "thanks": "Thanks. Your answer helps Asli learn.",
        "privacy": "Asli removes phone numbers, account numbers, OTPs and emails before saving a check. It never stores screenshots.",
        "examples": "Try an example",
        "ex_kyc": "Fake KYC alert",
        "ex_job": "Job offer",
        "ex_otp": "Real bank OTP",
        "empty": "Paste a message or choose a screenshot first.",
        "error": "Something went wrong on our side. Try again in a minute.",
        "too_many": "You've checked a lot of messages in a short time. Wait a minute and try again.",
        "no_text": "We couldn't read any text in that image. Paste the message instead.",
        "how_title": "How Asli decides",
        "how_1": "It reads the message for known tricks: asking for an OTP, fake KYC alerts, prize and job offers, arrest threats.",
        "how_2": "It checks where every link really goes, and flags look-alike bank and delivery sites.",
        "how_3": "A machine learning model trained on scam and normal messages scores the wording.",
        "helpline": "Lost money to a scam? Call 1930, the national cyber crime helpline.",
        "built_by": "Built by",
        "highlighted": "The highlighted words triggered the flags below.",
    },
    "hi": {
        "title": "असली: भरोसा करने से पहले संदेश जांचें",
        "heading": "क्या यह संदेश असली है?",
        "lede": "WhatsApp या SMS पर आया संदेश यहां पेस्ट करें। असली इसमें धोखेबाज़ों की आम चालें खोजता है और बताता है कि क्या मिला।",
        "label": "संदेश",
        "placeholder": "संदेश यहां पेस्ट करें",
        "or_image": "या स्क्रीनशॉट जांचें",
        "check": "संदेश जांचें",
        "checking": "जांच हो रही है…",
        "why": "हमें क्या मिला",
        "links": "इस संदेश के लिंक",
        "goes_to": "जाता है",
        "official": "आधिकारिक साइट",
        "not_official": "आधिकारिक साइट नहीं",
        "what_to_do": "क्या करें",
        "feedback_q": "क्या यह नतीजा सही था?",
        "yes": "हां",
        "no": "नहीं, गलत है",
        "thanks": "धन्यवाद। आपके जवाब से असली बेहतर बनता है।",
        "privacy": "जांच सेव करने से पहले असली फ़ोन नंबर, खाता नंबर, OTP और ईमेल हटा देता है। स्क्रीनशॉट कभी सेव नहीं होते।",
        "examples": "उदाहरण आज़माएं",
        "ex_kyc": "नकली KYC संदेश",
        "ex_job": "नौकरी का ऑफ़र",
        "ex_otp": "असली बैंक OTP",
        "empty": "पहले संदेश पेस्ट करें या स्क्रीनशॉट चुनें।",
        "error": "हमारी तरफ़ कुछ गड़बड़ हुई। एक मिनट बाद फिर कोशिश करें।",
        "too_many": "आपने कम समय में बहुत सारे संदेश जांचे हैं। एक मिनट रुककर फिर कोशिश करें।",
        "no_text": "उस तस्वीर में कोई टेक्स्ट नहीं पढ़ पाए। संदेश पेस्ट करें।",
        "how_title": "असली कैसे तय करता है",
        "how_1": "यह संदेश में जानी-पहचानी चालें खोजता है: OTP मांगना, नकली KYC संदेश, इनाम और नौकरी के ऑफ़र, गिरफ्तारी की धमकी।",
        "how_2": "यह देखता है कि हर लिंक असल में कहां जाता है, और नकली बैंक व डिलीवरी साइटें पकड़ता है।",
        "how_3": "धोखे और सामान्य संदेशों पर प्रशिक्षित मशीन लर्निंग मॉडल शब्दों को अंक देता है।",
        "helpline": "धोखे में पैसे गंवाए? राष्ट्रीय साइबर अपराध हेल्पलाइन 1930 पर कॉल करें।",
        "built_by": "बनाया",
        "highlighted": "रंगे हुए शब्दों से नीचे दिए संकेत मिले।",
    },
    "kn": {
        "title": "ಅಸಲಿ: ನಂಬುವ ಮೊದಲು ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
        "heading": "ಈ ಸಂದೇಶ ಅಸಲಿಯೇ?",
        "lede": "WhatsApp ಅಥವಾ SMS ನಲ್ಲಿ ಬಂದ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಅಂಟಿಸಿ. ಅಸಲಿ ವಂಚಕರ ಸಾಮಾನ್ಯ ತಂತ್ರಗಳನ್ನು ಹುಡುಕಿ, ಏನು ಸಿಕ್ಕಿತು ಎಂದು ತಿಳಿಸುತ್ತದೆ.",
        "label": "ಸಂದೇಶ",
        "placeholder": "ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಅಂಟಿಸಿ",
        "or_image": "ಅಥವಾ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಪರಿಶೀಲಿಸಿ",
        "check": "ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
        "checking": "ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ…",
        "why": "ನಮಗೆ ಸಿಕ್ಕಿದ್ದು",
        "links": "ಈ ಸಂದೇಶದಲ್ಲಿರುವ ಲಿಂಕ್‌ಗಳು",
        "goes_to": "ಹೋಗುವುದು",
        "official": "ಅಧಿಕೃತ ಸೈಟ್",
        "not_official": "ಅಧಿಕೃತ ಸೈಟ್ ಅಲ್ಲ",
        "what_to_do": "ಏನು ಮಾಡಬೇಕು",
        "feedback_q": "ಈ ಫಲಿತಾಂಶ ಸರಿಯಾಗಿತ್ತೇ?",
        "yes": "ಹೌದು",
        "no": "ಇಲ್ಲ, ತಪ್ಪಾಗಿದೆ",
        "thanks": "ಧನ್ಯವಾದ. ನಿಮ್ಮ ಉತ್ತರ ಅಸಲಿಯನ್ನು ಉತ್ತಮಗೊಳಿಸುತ್ತದೆ.",
        "privacy": "ಪರಿಶೀಲನೆ ಉಳಿಸುವ ಮೊದಲು ಅಸಲಿ ಫೋನ್ ನಂಬರ್, ಖಾತೆ ನಂಬರ್, OTP ಮತ್ತು ಇಮೇಲ್ ತೆಗೆದುಹಾಕುತ್ತದೆ. ಸ್ಕ್ರೀನ್‌ಶಾಟ್‌ಗಳನ್ನು ಎಂದಿಗೂ ಉಳಿಸುವುದಿಲ್ಲ.",
        "examples": "ಉದಾಹರಣೆ ಪ್ರಯತ್ನಿಸಿ",
        "ex_kyc": "ನಕಲಿ KYC ಸಂದೇಶ",
        "ex_job": "ಉದ್ಯೋಗದ ಆಫರ್",
        "ex_otp": "ನಿಜವಾದ ಬ್ಯಾಂಕ್ OTP",
        "empty": "ಮೊದಲು ಸಂದೇಶ ಅಂಟಿಸಿ ಅಥವಾ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಆಯ್ಕೆಮಾಡಿ.",
        "error": "ನಮ್ಮ ಕಡೆ ಏನೋ ತಪ್ಪಾಗಿದೆ. ಒಂದು ನಿಮಿಷದ ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "too_many": "ಕಡಿಮೆ ಸಮಯದಲ್ಲಿ ತುಂಬಾ ಸಂದೇಶಗಳನ್ನು ಪರಿಶೀಲಿಸಿದ್ದೀರಿ. ಒಂದು ನಿಮಿಷ ಕಾದು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "no_text": "ಆ ಚಿತ್ರದಲ್ಲಿ ಯಾವುದೇ ಪಠ್ಯ ಓದಲಾಗಲಿಲ್ಲ. ಸಂದೇಶವನ್ನು ಅಂಟಿಸಿ.",
        "how_title": "ಅಸಲಿ ಹೇಗೆ ನಿರ್ಧರಿಸುತ್ತದೆ",
        "how_1": "ಸಂದೇಶದಲ್ಲಿ ಪರಿಚಿತ ತಂತ್ರಗಳನ್ನು ಹುಡುಕುತ್ತದೆ: OTP ಕೇಳುವುದು, ನಕಲಿ KYC ಸಂದೇಶ, ಬಹುಮಾನ ಮತ್ತು ಉದ್ಯೋಗದ ಆಫರ್, ಬಂಧನದ ಬೆದರಿಕೆ.",
        "how_2": "ಪ್ರತಿ ಲಿಂಕ್ ನಿಜವಾಗಿ ಎಲ್ಲಿಗೆ ಹೋಗುತ್ತದೆ ಎಂದು ನೋಡಿ, ನಕಲಿ ಬ್ಯಾಂಕ್ ಮತ್ತು ಡೆಲಿವರಿ ಸೈಟ್‌ಗಳನ್ನು ಗುರುತಿಸುತ್ತದೆ.",
        "how_3": "ವಂಚನೆ ಮತ್ತು ಸಾಮಾನ್ಯ ಸಂದೇಶಗಳ ಮೇಲೆ ತರಬೇತಿ ಪಡೆದ ಮೆಷಿನ್ ಲರ್ನಿಂಗ್ ಮಾದರಿ ಪದಗಳಿಗೆ ಅಂಕ ನೀಡುತ್ತದೆ.",
        "helpline": "ವಂಚನೆಯಲ್ಲಿ ಹಣ ಕಳೆದುಕೊಂಡಿರಾ? ರಾಷ್ಟ್ರೀಯ ಸೈಬರ್ ಅಪರಾಧ ಸಹಾಯವಾಣಿ 1930 ಗೆ ಕರೆ ಮಾಡಿ.",
        "built_by": "ನಿರ್ಮಿಸಿದವರು",
        "highlighted": "ಬಣ್ಣ ಹಚ್ಚಿದ ಪದಗಳಿಂದ ಕೆಳಗಿನ ಸೂಚನೆಗಳು ಬಂದವು.",
    },
}

BRAND_NAMES = {
    "sbi": "SBI", "hdfc": "HDFC Bank", "icici": "ICICI Bank", "axis": "Axis Bank", "kotak": "Kotak",
    "pnb": "PNB", "canara": "Canara Bank", "paytm": "Paytm", "phonepe": "PhonePe", "gpay": "Google Pay",
    "amazon": "Amazon", "flipkart": "Flipkart", "indiapost": "India Post", "irctc": "IRCTC",
    "bluedart": "Blue Dart", "delhivery": "Delhivery", "fedex": "FedEx", "dhl": "DHL", "aadhaar": "Aadhaar",
    "uidai": "UIDAI", "incometax": "Income Tax", "epfo": "EPFO", "npci": "NPCI", "rbi": "RBI", "trai": "TRAI",
    "whatsapp": "WhatsApp",
}
