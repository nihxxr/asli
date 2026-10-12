"""Generate the synthetic training set in data/train.csv.

Real scam corpora for Indian languages are scarce and full of personal data,
so this bootstraps the classifier from templates written after the common
scam formats reported by CERT-In, RBI and police advisories, plus everyday
messages that look similar (real OTP notices, delivery updates, offers).

The eval set in data/eval.csv is written by hand with different phrasing and
never generated here, so the eval measures generalisation beyond templates.
Replace or extend this with labelled user feedback once the app collects it.

Usage: python scripts/make_training_data.py [--n 2400] [--seed 7]
"""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "train.csv"

SLOTS = {
    "bank": ["SBI", "HDFC", "ICICI", "Axis Bank", "Kotak", "PNB", "Canara Bank", "Bank of Baroda", "YONO SBI"],
    "app": ["Paytm", "PhonePe", "Google Pay", "Amazon Pay"],
    "courier": ["India Post", "Blue Dart", "Delhivery", "FedEx", "DHL", "DTDC"],
    "shop": ["Amazon", "Flipkart", "Myntra", "Swiggy", "Zomato", "Meesho", "BigBasket"],
    "amt": ["499", "1,250", "2,999", "4,999", "9,800", "15,000", "25,000", "49,999", "1,00,000"],
    "small": ["25", "49", "50", "99", "120", "150"],
    "hrs": ["2", "6", "12", "24"],
    "name": ["Priya", "Rahul", "Anjali", "Neha", "Vikram", "Sneha", "Arjun", "Kavya", "Ravi", "Deepa"],
    "evil": ["sbi-kyc-update.xyz", "hdfc-netbanking.top", "icici-rewards.live", "kyc-verify-now.site",
             "bit.ly/3xKyc9", "rb.gy/upd8te", "indiapost-redelivery.info", "secure-yono.online",
             "pm-kisan-bonus.club", "bescom-bill.icu", "amaz0n-prize.shop", "flipkart-lucky.vip",
             "tinyurl.com/claim-reward", "203.0.113.45/login", "axis-points.buzz"],
    "good": ["https://www.amazon.in/your-orders", "https://www.flipkart.com/account/orders",
             "https://www.irctc.co.in", "https://www.hdfcbank.com", "https://onlinesbi.sbi",
             "https://www.indiapost.gov.in", "https://www.swiggy.com", "https://www.bluedart.com"],
    "otp": ["482913", "771204", "305566", "918273", "640021"],
    "phone": ["98765 43210", "+91 91234 56789", "8800123456", "7012345678"],
    "time": ["5 pm", "10:30 am", "7 baje", "tomorrow morning", "Sunday 11 am"],
    "place": ["Indiranagar", "Koramangala", "Jayanagar", "the office", "MG Road", "home"],
}

SCAM = [
    # KYC / account block
    "Dear customer, your {bank} account will be blocked today. Update your KYC immediately: {evil}",
    "{bank}: Your PAN card is not linked. Account will be suspended within {hrs} hours. Click {evil}",
    "Your {bank} net banking has been deactivated due to incomplete KYC. Verify now {evil}",
    "ALERT! {bank} YONO account freezed. Update PAN immediately to avoid closure {evil}",
    "Dear user your e-KYC is pending. Update before midnight or your {app} wallet will be blocked {evil}",
    "Aapka {bank} account aaj band ho jayega. Turant KYC update kare: {evil}",
    "Sir aapka khata block ho jayega, PAN card link karo abhi {evil}",
    "प्रिय ग्राहक, आपका {bank} खाता आज ब्लॉक हो जाएगा। तुरंत केवाईसी अपडेट करें {evil}",
    "आपका पैन कार्ड अपडेट नहीं है, खाता बंद कर दिया जाएगा। लिंक पर क्लिक करें {evil}",
    "ಆತ್ಮೀಯ ಗ್ರಾಹಕರೇ, ನಿಮ್ಮ {bank} ಖಾತೆ ಇಂದು ಬ್ಲಾಕ್ ಆಗುತ್ತದೆ. ತಕ್ಷಣ ಕೆವೈಸಿ ಅಪ್ಡೇಟ್ ಮಾಡಿ {evil}",
    "ನಿಮ್ಮ ಪ್ಯಾನ್ ಲಿಂಕ್ ಆಗಿಲ್ಲ, ಖಾತೆ ಸ್ಥಗಿತಗೊಳ್ಳುತ್ತದೆ. ಈಗಲೇ ನವೀಕರಿಸಿ {evil}",
    # OTP / PIN
    "Hello sir, I am calling from {bank} head office. Please share the OTP sent to your number to stop the unauthorised transaction",
    "Your card will be upgraded to platinum free. Kindly tell the OTP received to complete process",
    "Sir galti se OTP aapke number pe chala gaya, please bata do {otp} wala code",
    "Madam aapka refund process ho raha hai, OTP bhej do jaldi",
    "आपके नंबर पर आया ओटीपी बताइए, आपका कार्ड चालू हो जाएगा",
    "ನಿಮ್ಮ ಮೊಬೈಲ್‌ಗೆ ಬಂದ ಒಟಿಪಿ ಹೇಳಿ, ರೀಫಂಡ್ ತಕ್ಷಣ ಬರುತ್ತದೆ",
    "{name} here from {app} support. Send me the 6 digit code you just got so I can verify your account",
    # UPI collect
    "Congratulations! You have received cashback of Rs {amt} from {app}. Enter your UPI PIN to receive the money",
    "Refund of Rs {amt} initiated for your {shop} order. Approve the collect request and enter PIN to receive",
    "Rs {amt} credit pending. Scan the QR code and enter UPI PIN to get the amount in your account",
    "Paisa receive karne ke liye UPI PIN daalo, {amt} rupaye aapke account me aa jayenge",
    # Jobs / tasks
    "Part time job! Earn Rs {amt} daily by liking YouTube videos. Contact on Telegram t.me/hr_{name}",
    "Hi I'm {name} from an HR agency. Work from home, earn ₹3000 per day by rating hotels on Google Maps. Interested?",
    "Online job available. Daily income ₹2000-₹8000. Just like and subscribe. Message on WhatsApp wa.me/919876543210",
    "Prepaid task: invest Rs {small}0 and get Rs {amt} commission within 1 hour. Join our telegram group",
    "Ghar baithe kamaye ₹5000 roz. Sirf mobile chahiye. Abhi join kare",
    "घर बैठे रोज़ ₹5000 कमाएं। सिर्फ मोबाइल से काम। अभी संपर्क करें {phone}",
    "ಮನೆಯಿಂದಲೇ ದಿನಕ್ಕೆ ₹3000 ಸಂಪಾದಿಸಿ. ಟೆಲಿಗ್ರಾಮ್ ಗ್ರೂಪ್ ಸೇರಿ",
    "Hiring for {shop} online reviewers. Get Rs {small}0 for each review you post, payment daily. Reply YES to start",
    "We need people to rate products on {shop}. ₹{small}0 per rating, salary credited same day. WhatsApp {name} {phone}",
    # Courier / customs / digital arrest
    "{courier}: Your parcel is on hold due to incomplete address. Update within {hrs} hours: {evil}",
    "Your shipment could not be delivered. Pay redelivery fee Rs {small} here {evil}",
    "This is {courier} customer care. A parcel in your name has been seized by customs with illegal items. Press 1 to talk to officer",
    "Mumbai Police cyber crime cell: a case is registered against your Aadhaar number. Join video call on Skype or you will be arrested",
    "CBI officer here. You are under digital arrest. Do not disconnect the call and transfer Rs {amt} for verification",
    "TRAI notice: your mobile number will be disconnected in 2 hours due to illegal activity. Press 9 to speak to officer",
    "आपके नाम से पार्सल में ड्रग्स मिले हैं। डिजिटल अरेस्ट से बचने के लिए तुरंत कॉल करें",
    "ನಿಮ್ಮ ಹೆಸರಿನ ಪಾರ್ಸೆಲ್ ತಡೆಹಿಡಿಯಲಾಗಿದೆ, ವಿಳಾಸ ನವೀಕರಿಸಿ {evil}",
    # Electricity
    "Dear consumer your electricity power will be disconnected tonight at 9:30 pm because previous month bill was not updated. Call officer {phone}",
    "BESCOM: Your current connection will be cut today. Contact electricity officer immediately {phone}",
    "Bijli connection aaj raat kat jayega, bill update karne ke liye call kare {phone}",
    "प्रिय उपभोक्ता, आपकी बिजली आज रात काट दी जाएगी। तुरंत संपर्क करें {phone}",
    "ಆತ್ಮೀಯ ಗ್ರಾಹಕರೇ, ನಿಮ್ಮ ವಿದ್ಯುತ್ ಸಂಪರ್ಕ ಇಂದು ರಾತ್ರಿ ಕಡಿತಗೊಳ್ಳುತ್ತದೆ. ತಕ್ಷಣ ಕರೆ ಮಾಡಿ {phone}",
    # Prize / rewards
    "Congratulations! You have won Rs {amt} in the {shop} lucky draw. Claim your prize now {evil}",
    "Your {bank} credit card reward points worth Rs {amt} expire today. Redeem now {evil}",
    "KBC lottery winner! Your number won 25 lakh. Pay processing fee Rs {small}00 to claim",
    "Dear {shop} customer you are selected for a free iPhone. Claim your gift here {evil}",
    "Aapki lottery lagi hai ₹{amt} ki. Inaam lene ke liye registration fee bhejo",
    "बधाई हो! आपने ₹{amt} का इनाम जीता है। अभी दावा करें {evil}",
    "ಅಭಿನಂದನೆಗಳು! ನೀವು ₹{amt} ಬಹುಮಾನ ಗೆದ್ದಿದ್ದೀರಿ. ಈಗಲೇ ಪಡೆಯಿರಿ {evil}",
    # Investment
    "Join our VIP stock tips group, guaranteed returns of 30% monthly. Limited seats {evil}",
    "Double your money in 15 days with our crypto trading app. Assured profit. Message on Telegram",
    "IPO allotment group: insider tips, 5% daily profit. Join now",
    # Remote access / app install
    "Your {bank} refund is pending. Install AnyDesk and share the code with our executive to complete",
    "Download the {app} KYC support app from this link to verify your account {evil}/support.apk",
    # Family emergency / impersonation
    "Hi Mom this is my new number, my phone broke. Can you send Rs {amt} urgently, I'll explain later",
    "Uncle I am in hospital, please send {amt} on this UPI urgently, don't call I can't talk",
    "Sir this is your CEO. I'm in a meeting, buy Amazon gift cards worth {amt} urgently and send me the codes",
    # Loans
    "Instant loan approved Rs {amt} without documents. Pay processing fee Rs {small}9 to release amount",
    "Pre-approved personal loan of {amt}. Download app and grant contacts permission to get money in 5 minutes {evil}",
]

HAM = [
    # Real OTP and alerts
    "{otp} is your OTP for transaction of Rs {amt} at {shop}. Valid for 10 mins. Do not share it with anyone. -{bank}",
    "{otp} is the OTP to log in to your {app} account. Never share your OTP with anyone, including bank staff.",
    "Dear customer, Rs {amt} debited from A/c XX1234 on 12-10 via UPI. Not you? Call the number on the back of your card. -{bank}",
    "Rs {amt} credited to your account XX5678 by NEFT. Available balance updated. -{bank}",
    "Your {bank} credit card statement is ready. Total due Rs {amt}, due date 25th. Pay via the official app.",
    "OTP for your {shop} order delivery is {otp}. Share it only with the delivery agent at your door.",
    "आपके लेनदेन के लिए ओटीपी {otp} है। इसे किसी से साझा न करें। -{bank}",
    "ನಿಮ್ಮ ವಹಿವಾಟಿನ ಒಟಿಪಿ {otp}. ಇದನ್ನು ಯಾರೊಂದಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ. -{bank}",
    "{bank} never asks for your OTP, PIN or password over phone or SMS. Stay alert, stay safe.",
    # Deliveries and orders
    "Your {shop} order has been shipped and will arrive by Thursday. Track it at {good}",
    "{courier}: your shipment is out for delivery today. Our agent will call before arriving.",
    "Your {shop} order was delivered. Rate your experience in the app.",
    "Hi, delivery agent here, I'm downstairs with your {shop} parcel, please come down",
    "Aapka {shop} order kal tak deliver ho jayega. Order details app me dekhein.",
    "आपका ऑर्डर भेज दिया गया है और गुरुवार तक पहुंच जाएगा।",
    "ನಿಮ್ಮ {shop} ಆರ್ಡರ್ ಇಂದು ಡೆಲಿವರಿ ಆಗಲಿದೆ.",
    # Bills and services (legit wording)
    "Your electricity bill of Rs {amt} for September is generated. Pay by 20th via the official app or website.",
    "Jio: Your plan expires in 3 days. Recharge through MyJio app to continue services.",
    "Reminder: your Airtel postpaid bill of Rs {small}9 is due on 15th.",
    "Your appointment with Dr. {name} is confirmed for {time} at {place}. Reply C to cancel.",
    "IRCTC: PNR 4512345678 confirmed. Train 12627, coach S4 berth 32. Happy journey.",
    "Your Uber is arriving in 3 minutes. Look for a white Swift.",
    # Personal / work chat
    "Hey {name}, are we still meeting at {place} at {time}?",
    "Bhai kal movie chalein? {time} PVR",
    "Mummy I reached {place}, will call you after dinner",
    "Can you send me the slides before the meeting at {time}?",
    "Happy birthday {name}! Have an amazing year ahead",
    "Kal office aa rahe ho? Standup {time} pe hai",
    "Please send the electricity bill photo, I'll pay it from my account",
    "{name}, I've sent you Rs {amt} for the trip, check your {app}",
    "Did you get my {app} payment for dinner?",
    "माँ, मैं ठीक से पहुँच गया हूँ। रात को फ़ोन करूँगा।",
    "ಅಮ್ಮ, ನಾನು ಮನೆ ತಲುಪಿದೆ. ಊಟದ ನಂತರ ಕರೆ ಮಾಡುತ್ತೇನೆ.",
    "ನಾಳೆ {time} ಗೆ {place} ನಲ್ಲಿ ಸಿಗೋಣವೇ?",
    "कल शाम {time} पर मिलते हैं, {place} पर।",
    # Legit marketing
    "{shop} Big Billion Days: up to 70% off on electronics starting Friday. Shop in the app.",
    "Flat 20% off on your next {shop} order. Use code SAVE20. T&C apply.",
    "Your {bank} credit card has earned 250 reward points this month. View them in the official app.",
    "Hiring: {name} from our HR team will call you about the backend developer role you applied for on LinkedIn.",
    "Your job application at Infosys has been received. We'll email you next steps.",
    "SIP of Rs {small}00 in your mutual fund was processed successfully.",
    "Your Aadhaar was used for authentication at {time}. If this wasn't you, lock your biometrics on the UIDAI website.",
    "Income tax refund of Rs {amt} has been credited to your bank account. Details on incometax.gov.in",
    "Your {bank} Video KYC is due. Complete it in the official app when convenient.",
    "Share OTP {otp} with your driver to start the ride.",
    # Everyday Hinglish
    "Yaar {place} pe traffic bahut hai, thoda late ho jaunga",
    "Kya tum kal free ho? {time} chai peete hain",
    "Bhaiya order neeche guard ke paas chhod dena",
    "Didi ne bola {time} tak ghar aa jana",
    "Arre {name}, notes bhej de kal ke lecture ke",
    "Paise mil gaye, thanks bro",
    "Gym chalega kal subah? {time}",
    "Mummy ne khana bheja hai, shaam ko le jaana",
    "Main {place} pahunch gaya, tu kahan hai?",
    "Rent maine {app} se bhej diya hai, check kar lena",
    "Kal holiday hai kya office me?",
    "Bhai match dekhne aa raha hai? {time} start hai",
    "Order deliver ho gaya, packing achhi thi",
    # Everyday Hindi
    "मैं {time} तक घर पहुंच जाऊंगा।",
    "आज खाने में क्या बना है?",
    "दादी की दवाई ले आना, पर्ची फ्रिज पर है।",
    "बैठक कल {time} बजे होगी, सभी समय पर आएं।",
    "आपके खाते में ₹{amt} जमा हुए हैं। -{bank}",
    "आपका बिल ₹{small}0 है, अंतिम तिथि 20 तारीख है। आधिकारिक ऐप से भुगतान करें।",
    "जन्मदिन की बहुत बहुत शुभकामनाएं {name}!",
    "आपकी डॉक्टर से मुलाकात कल {time} पर तय है।",
    "आपका {shop} ऑर्डर डिलीवर हो गया है।",
    "कल स्कूल में अभिभावक बैठक है, ज़रूर आइए।",
    "ट्रेन दो घंटे लेट है, स्टेशन देर से आना।",
    "आपके कार्ड से ₹{amt} का भुगतान हुआ है। -{bank}",
    # Everyday Kannada
    "ನಾನು {time} ಗೆ ಮನೆಗೆ ಬರುತ್ತೇನೆ",
    "ಇಂದು ಊಟಕ್ಕೆ ಏನು ಮಾಡಿದ್ದೀಯ?",
    "ನಾಳೆ ಕಚೇರಿಯಲ್ಲಿ ಸಭೆ ಇದೆ, ಬೇಗ ಬನ್ನಿ",
    "ಹುಟ್ಟುಹಬ್ಬದ ಶುಭಾಶಯಗಳು {name}!",
    "ನಿಮ್ಮ ಖಾತೆಗೆ ₹{amt} ಜಮೆಯಾಗಿದೆ. -{bank}",
    "ನಿಮ್ಮ ಕಾರ್ಡ್‌ನಿಂದ ₹{amt} ಪಾವತಿಯಾಗಿದೆ. -{bank}",
    "ನಿಮ್ಮ ವಿದ್ಯುತ್ ಬಿಲ್ ₹{small}0, ಕೊನೆಯ ದಿನಾಂಕ 20. ಅಧಿಕೃತ ಆ್ಯಪ್ ಮೂಲಕ ಪಾವತಿಸಿ",
    "ಡಾಕ್ಟರ್ ಭೇಟಿ ನಾಳೆ {time} ಕ್ಕೆ ನಿಗದಿಯಾಗಿದೆ",
    "ನಿಮ್ಮ {shop} ಆರ್ಡರ್ ತಲುಪಿದೆ",
    "ಬಸ್ ತಡವಾಗಿದೆ, ಅರ್ಧ ಗಂಟೆ ಆಗುತ್ತದೆ",
    "ಮಗುವಿನ ಶಾಲೆಯ ಶುಲ್ಕ ಕಟ್ಟಿದ್ದೇನೆ, ರಸೀದಿ ಇಟ್ಟುಕೊ",
    "{place} ಹತ್ತಿರ ಹೊಸ ಹೋಟೆಲ್ ಶುರುವಾಗಿದೆ, ಹೋಗೋಣ",
]


def fill(template: str, rng: random.Random) -> str:
    out = template
    for key, values in SLOTS.items():
        token = "{" + key + "}"
        while token in out:
            out = out.replace(token, rng.choice(values), 1)
    return out


def jitter(text: str, rng: random.Random) -> str:
    """Small surface changes real messages have: case, punctuation, prefixes."""
    r = rng.random()
    if r < 0.15:
        text = text.upper()
    elif r < 0.3:
        text = text.lower()
    if rng.random() < 0.2:
        text = text.replace(".", "..").replace(",", " ,")
    if rng.random() < 0.15:
        text = rng.choice(["Dear Sir/Madam, ", "Hello, ", "Hi, ", "Namaste, "]) + text
    return text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2400)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    rows, seen = [], set()
    half = args.n // 2
    for label, pool in ((1, SCAM), (0, HAM)):
        tries = 0
        count = 0
        while count < half and tries < half * 20:
            tries += 1
            msg = jitter(fill(rng.choice(pool), rng), rng)
            if msg in seen:
                continue
            seen.add(msg)
            rows.append((msg, label))
            count += 1
    rng.shuffle(rows)
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["text", "label"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT} ({sum(r[1] for r in rows)} scam)")


if __name__ == "__main__":
    main()
