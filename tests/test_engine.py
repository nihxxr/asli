import pytest

from app import i18n
from app.analysis.engine import analyse, check
from app.analysis.redact import redact
from app.analysis.urls import analyse_url, find_links


def flags(text):
    return {h.id for h in analyse(text).hits}


@pytest.mark.parametrize("text,expected", [
    ("Dear customer your SBI account will be blocked today. Update KYC: http://sbi-kyc-update.xyz", "scam"),
    ("Please share the OTP you received to stop the transaction", "scam"),
    ("Enter your UPI PIN to receive the cashback of Rs 500", "scam"),
    ("You are under digital arrest. Join the Skype video call now", "scam"),
    ("प्रिय ग्राहक, आपका खाता आज ब्लॉक हो जाएगा। तुरंत केवाईसी अपडेट करें", "suspicious"),
    ("Bhai kal movie chalein? 7 baje PVR", "no_signs"),
    ("482913 is your OTP for Rs 500 at Amazon. Do not share it with anyone. -HDFC Bank", "no_signs"),
])
def test_verdicts(text, expected):
    v = analyse(text).verdict
    if expected == "suspicious":
        assert v in ("suspicious", "scam")
    else:
        assert v == expected


def test_negated_otp_is_not_a_request():
    assert "otp_request" not in flags("Never share your OTP with anyone. Bank staff will not ask for it.")
    assert "otp_request" not in flags("अपना ओटीपी किसी को न बताएं")
    assert "otp_request" not in flags("ಯಾರಿಗೂ ನಿಮ್ಮ ಒಟಿಪಿ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ")


def test_ride_otp_handoff_is_allowed():
    assert "otp_request" not in flags("Share OTP 4821 with the driver to start the trip")


def test_pin_code_is_not_pin():
    assert "otp_request" not in flags("Please share your pin code for delivery")


def test_kannada_and_hindi_requests():
    assert "otp_request" in flags("ನಿಮ್ಮ ಮೊಬೈಲ್‌ಗೆ ಬಂದ ಒಟಿಪಿ ಹೇಳಿ")
    assert "otp_request" in flags("आपके नंबर पर आया ओटीपी बताइए")


def test_lookalike_and_official_links():
    assert ("link_lookalike" in dict(analyse_url("http://hdfc-netbanking.top/x", 0, 1).flags))
    assert dict(analyse_url("https://onlinesbi.sbi.secure-login.co/verify", 0, 1).flags).get("link_brand_in_subdomain")
    official = analyse_url("https://www.hdfcbank.com/personal", 0, 1)
    assert official.official and not official.flags
    assert analyse_url("https://bescom.karnataka.gov.in", 0, 1).official
    assert "link_ip" in dict(analyse_url("http://203.0.113.9/login", 0, 1).flags)
    assert "link_shortener" in dict(analyse_url("https://bit.ly/abc", 0, 1).flags)


def test_taxis_is_not_axis():
    assert not analyse_url("https://bangaloretaxis.com", 0, 1).flags


def test_link_offsets_point_at_url():
    text = "Click http://sbi-kyc.xyz/a now"
    link = find_links(text)[0]
    assert text[link.start:link.end] == "http://sbi-kyc.xyz/a"


def test_brand_with_unofficial_link():
    assert "brand_unofficial_link" in flags("Your Amazon refund is ready, log in at refund-help.com")


def test_explain_in_every_language():
    for lang in i18n.LANGS:
        r = check("Share your OTP now http://sbi-kyc.xyz", lang)
        assert r["language"] == lang
        assert r["flags"] and all(f["title"] and "{" not in f["title"] + f["detail"] for f in r["flags"])
        assert r["actions"]


def test_spans_are_inside_text():
    r = check("URGENT: share the OTP to unblock your SBI account http://sbi-help.xyz")
    for f in r["flags"]:
        for s, e in f["spans"]:
            assert 0 <= s < e <= len(r["text"])


def test_redaction():
    out = redact("Call 98765 43210 or +91 9123456789, OTP 482913, a/c 123456789012, mail a.b@gmail.com, "
                 "upi rahul@okhdfc, link https://x.xyz/login?token=secret amount Rs 4,999")
    for leaked in ("98765", "9123456789", "482913", "123456789012", "a.b@gmail.com", "rahul@okhdfc", "token=secret"):
        assert leaked not in out
    assert "https://x.xyz/login" in out and "4,999" in out


def test_i18n_keys_match():
    base = set(i18n.UI["en"])
    for lang in i18n.LANGS:
        assert set(i18n.UI[lang]) == base
        for table in (i18n.FLAGS, i18n.VERDICTS):
            for key, by_lang in table.items():
                assert lang in by_lang, (key, lang)
        assert len(i18n.ACTIONS["warn"][lang]) == len(i18n.ACTIONS["warn"]["en"])
