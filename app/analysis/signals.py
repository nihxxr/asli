"""Red-flag rules in English, Hinglish, Hindi and Kannada.

Each signal has a weight between 0 and 1: roughly how likely a message is a
scam if this signal alone fires. The verdict combines weights with a
noisy-OR, so two medium signals add up to more than either one.

Rules catch the patterns people can explain ("it asked for your OTP"), and
the classifier in model.py catches wording the rules miss.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

I = re.IGNORECASE

# Words that turn "share your OTP" into "do not share your OTP"
NEGATION = re.compile(
    r"(?i)(\bdo\s*n[o']t\b|\bdont\b|\bnever\b|\bnot\b|\bmat\b|\bna\s*kare|\bkabhi\b|"
    r"न\s*करें|ना\s*करें|मत|कभी|नहीं|(?:^|\s)न(?:\s|$)|ಬೇಡಿ|ಎಂದಿಗೂ|ಮಾಡಬೇಡಿ)"
)

# Legitimate OTP hand-offs: rides, deliveries, at the door
OTP_HANDOFF = re.compile(
    r"(?i)(driver|captain|rider|delivery\s+(agent|executive|partner|boy|person)|at\s+(your|the)\s+door|doorstep|"
    r"to\s+start\s+(the|your)\s+(trip|ride)|ड्राइवर|डिलीवरी\s*एजेंट|ಚಾಲಕ|ಡೆಲಿವರಿ\s*ಏಜೆಂಟ್)"
)

SEND = r"(share|send|tell|forward|give|provide|enter|type|reply\s+with|batao|bata\s*do|bhejo|bhej\s*do|de\s*do|daalo|dalo|share\s*karo|share\s*kar)"
SECRET = r"(otp|o\.t\.p|one[\s-]?time\s+password|upi\s+pin|atm\s+pin|\bpin\b(?!\s*code)|cvv|mpin|password|verification\s+code)"


@dataclass
class Signal:
    id: str
    weight: float
    patterns: list
    negatable: bool = False
    allow: re.Pattern | None = None  # context that makes a match legitimate


@dataclass
class Hit:
    id: str
    weight: float
    spans: list = field(default_factory=list)  # [(start, end)]
    detail: str = ""


SIGNALS = [
    Signal("otp_request", 0.85, [
        re.compile(SEND + r"[^.\n]{0,40}?" + SECRET, I),
        re.compile(SECRET + r"[^.\n]{0,30}?" + SEND, I),
        re.compile(r"(ओटीपी|पिन)[^।\n]{0,25}?(बताएं|बताइए|बताओ|भेजें|भेजिए|भेजो|शेयर\s*करें)"),
        re.compile(r"(ಒಟಿಪಿ|ಪಿನ್)[^.\n]{0,25}?(ಹಂಚಿಕೊಳ್ಳಿ|ಕಳುಹಿಸಿ|ಹೇಳಿ|ತಿಳಿಸಿ)"),
    ], negatable=True, allow=OTP_HANDOFF),
    Signal("upi_pin_receive", 0.9, [
        re.compile(r"(enter|put|daalo|dalo)[^.\n]{0,25}(upi\s*)?pin[^.\n]{0,40}(receive|get|claim|credit|refund|cashback|paise|money)", I),
        re.compile(r"(receive|claim|get)[^.\n]{0,40}(refund|cashback|money|amount)[^.\n]{0,40}(enter|scan|approve)[^.\n]{0,20}(pin|qr|request)", I),
        re.compile(r"(scan|approve|accept)[^.\n]{0,30}(qr|collect\s+request|payment\s+request)[^.\n]{0,40}(receive|refund|cashback|get)", I),
    ]),
    Signal("remote_access", 0.8, [
        re.compile(r"\b(anydesk|teamviewer|quick\s*support|rustdesk|airdroid|screen\s*shar(e|ing))\b", I),
        re.compile(r"\b(download|install)\b[^.\n]{0,30}\b(app|apk|application)\b[^.\n]{0,40}\b(kyc|refund|verify|support|update)\b", I),
    ]),
    Signal("digital_arrest", 0.85, [
        re.compile(r"\bdigital\s+arrest\b", I),
        re.compile(r"\b(cbi|ncb|ed|narcotics|cyber\s*(crime|cell)|customs|police|mumbai\s+police|crime\s+branch)\b[^.\n]{0,80}\b(arrest|warrant|case\s+(is\s+)?(registered|filed)|fir|video\s+call|skype)\b", I),
        re.compile(r"\btrai\b[^.\n]{0,60}\b(disconnect|block|suspend|illegal)\b", I),
        re.compile(r"(डिजिटल\s*अरेस्ट|गिरफ्तार|गिरफ़्तार)"),
        re.compile(r"(ಬಂಧನ|ಬಂಧಿಸ)"),
    ]),
    Signal("kyc_block", 0.55, [
        re.compile(r"\b(e-?kyc|kyc|pan(\s*card)?|aadhaa?r)\b[^.\n]{0,40}\b(update|expir|pending|suspend|block|incomplete|link|verify|deactivat)", I),
        re.compile(r"\b(account|a/c|card|wallet|sim|yono|net\s*banking)\b[^.\n]{0,40}\b(will\s+be|has\s+been|is|ho\s+jayega|hoga|been)\s+(temporarily\s+)?(blocked|suspended|deactivated|closed|freezed|frozen|band|disabled|on\s+hold)", I),
        re.compile(r"\b(khata|account)\s+(band|block)\s+(ho\s+jayega|hoga|kar\s+diya)", I),
        re.compile(r"(केवाईसी|पैन\s*कार्ड)[^।\n]{0,30}(अपडेट|समाप्त|ब्लॉक)"),
        re.compile(r"(खाता|अकाउंट)[^।\n]{0,20}(बंद|ब्लॉक|निलंबित)"),
        re.compile(r"(ಕೆವೈಸಿ|ಪ್ಯಾನ್)[^.\n]{0,30}(ಅಪ್ಡೇಟ್|ನವೀಕರಿಸಿ)"),
        re.compile(r"(ಖಾತೆ)[^.\n]{0,25}(ಬ್ಲಾಕ್|ಸ್ಥಗಿತ|ನಿರ್ಬಂಧ)"),
    ]),
    Signal("prize", 0.5, [
        re.compile(r"\b(you\s+(have\s+)?won|winner|lottery|lucky\s+draw|jackpot|kbc|scratch\s+card|claim\s+your\s+(prize|reward|gift)|selected\s+for\s+(a\s+)?(reward|gift|prize))\b", I),
        re.compile(r"\b(reward\s+points?|cashback)\b[^.\n]{0,40}\b(expir|redeem\s+(now|today)|claim)", I),
        re.compile(r"\b(lottery\s+lagi|inaam|inam)\b", I),
        re.compile(r"(लॉटरी|इनाम|बधाई\s*हो[^।\n]{0,30}जीत)"),
        re.compile(r"(ಲಾಟರಿ|ಬಹುಮಾನ)"),
    ]),
    Signal("job_task", 0.55, [
        re.compile(r"\b(work\s+from\s+home|part[\s-]?time\s+job|online\s+job|daily\s+(income|earning|payout)|earn\s+(rs\.?|₹|inr)?\s?\d[\d,]*\s*(\+\s*)?(daily|per\s+day|a\s+day|/day))\b", I),
        re.compile(r"\b(like|subscribe|rate|review)\b[^.\n]{0,25}\b(youtube|videos?|hotels?|products?|google\s+maps)\b[^.\n]{0,40}\b(earn|paid|pay|commission|salary|₹|rs)\b", I),
        re.compile(r"\b(prepaid|merchant)\s+task(s)?\b", I),
        re.compile(r"(rs\.?|₹|inr)\s?\d[\d,]*\s*(for|per)\s+(every\s+)?(\d+\s+)?(product\s+)?(reviews?|likes?|tasks?|videos?|ratings?)\b", I),
        re.compile(r"\b(salary|payment|payout)\s+daily\b|\bdaily\s+(salary|payment|payout)\b", I),
        re.compile(r"\bghar\s+baith(e|kar)\b|\bkamaa?(o|ye|yein)\b", I),
        re.compile(r"(घर\s*बैठे|रोज़?\s*कमाएं|कमाइए)"),
        re.compile(r"(ಮನೆಯಿಂದಲೇ|ಮನೆಯಲ್ಲೇ\s*ಕುಳಿತು|ಸಂಪಾದಿಸಿ)"),
    ]),
    Signal("courier_issue", 0.4, [
        re.compile(r"\b(parcel|package|shipment|courier|consignment)\b[^.\n]{0,60}\b(on\s+hold|held|seized|returned|undeliver|could\s+not\s+be\s+delivered|address\s+(is\s+)?(incomplete|incorrect|invalid)|redeliver|illegal|drugs|customs)\b", I),
        re.compile(r"(पार्सल|कूरियर)[^।\n]{0,40}(रोका|जब्त|पता\s*(अधूरा|गलत))"),
        re.compile(r"(ಪಾರ್ಸೆಲ್|ಕೊರಿಯರ್)[^.\n]{0,40}(ತಡೆ|ವಿಳಾಸ)"),
    ]),
    Signal("bill_disconnect", 0.55, [
        re.compile(r"\b(electricity|power|light|current|gas|bijli)\b[^.\n]{0,60}\b(disconnect|cut|kat|band)", I),
        re.compile(r"(बिजली)[^।\n]{0,40}(कट|काट|बंद)"),
        re.compile(r"(ವಿದ್ಯುತ್|ಕರೆಂಟ್)[^.\n]{0,40}(ಕಡಿತ|ಸ್ಥಗಿತ)"),
    ]),
    Signal("investment", 0.55, [
        re.compile(r"\b(guaranteed|assured|fixed)\s+(returns?|profit|income)\b", I),
        re.compile(r"\bdouble\s+(your|the)\s+money\b|\bpaisa\s+double\b", I),
        re.compile(r"\b\d{1,3}\s?%\s*(daily|per\s+day|weekly|a\s+week|monthly)\s*(returns?|profit)?\b", I),
        re.compile(r"\b(stock|trading|ipo|crypto|forex)\b[^.\n]{0,40}\b(tips?|group|vip|signals?|insider)\b", I),
    ]),
    Signal("fee_request", 0.3, [
        re.compile(r"\b(registration|processing|verification|customs|clearance|release|security|activation|redelivery)\s+(fee|charge|charges|deposit|amount)\b", I),
        re.compile(r"\bpay\b[^.\n]{0,15}(rs\.?|₹|inr)\s?\d+[^.\n]{0,40}\b(to\s+(receive|get|release|activate|unlock|avoid))", I),
    ]),
    Signal("off_platform", 0.3, [
        re.compile(r"\b(contact|message|ping|join|dm)\b[^.\n]{0,20}\b(on|via|at)\b[^.\n]{0,10}\b(telegram|whatsapp)\b", I),
        re.compile(r"\btelegram\b", I),
    ]),
    Signal("urgency", 0.25, [
        re.compile(r"\b(urgent(ly)?|immediately|within\s+\d+\s*(hours?|hrs?|minutes?|mins?)|today\s+itself|before\s+midnight|last\s+(chance|warning|reminder|date\s+today)|act\s+now|expires?\s+today|turant|abhi\s+(karo|kare)|aaj\s+hi)\b", I),
        re.compile(r"(तुरंत|आज\s*ही|अंतिम\s*चेतावनी)"),
        re.compile(r"(ತಕ್ಷಣ|ಇಂದೇ|ಈಗಲೇ|ಕೊನೆಯ\s*ಎಚ್ಚರಿಕೆ)"),
    ]),
]

BRAND_MENTION = re.compile(
    r"\b(sbi|state\s+bank|hdfc|icici|axis|kotak|pnb|canara|bank\s+of\s+baroda|paytm|phonepe|gpay|google\s+pay|"
    r"amazon|flipkart|india\s*post|irctc|blue\s*dart|delhivery|fedex|dhl|aadhaa?r|uidai|income\s*tax|epfo|"
    r"npci|rbi|reserve\s+bank|trai|bescom|electricity\s+board|customs)\b",
    I,
)


def _negated(text: str, start: int) -> bool:
    window = text[max(0, start - 18):start]
    return bool(NEGATION.search(window))


def find_signals(text: str) -> list[Hit]:
    hits = []
    for sig in SIGNALS:
        spans = []
        for rx in sig.patterns:
            for m in rx.finditer(text):
                if sig.negatable and (_negated(text, m.start()) or NEGATION.search(m.group(0))):
                    continue
                if sig.allow and sig.allow.search(text[max(0, m.start() - 40):m.end() + 50]):
                    continue
                spans.append((m.start(), m.end()))
        if spans:
            hits.append(Hit(sig.id, sig.weight, _merge(spans)))
    return hits


def brand_mentions(text: str) -> list[str]:
    return sorted({m.group(0).lower() for m in BRAND_MENTION.finditer(text)})


def _merge(spans):
    spans = sorted(spans)
    out = [list(spans[0])]
    for s, e in spans[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]
