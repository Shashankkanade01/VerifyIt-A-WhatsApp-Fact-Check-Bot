import requests
from google import genai as genai_client
from groq import Groq
from flask import Flask, request, jsonify
import time

GROQ_API_KEY = "____"
groq_client = Groq(api_key=GROQ_API_KEY)
ID_INSTANCE         = "____"
API_TOKEN_INSTANCE  = "____"

#BASE_URL = f"https://api.green-api.com/waInstance{ID_INSTANCE}"
BASE_URL = f"https://7107.api.greenapi.com/waInstance{ID_INSTANCE}"

app = Flask(__name__)

def fact_check(message_text):
    prompt = f"""You are VerifyIt, an expert fact-checking AI for WhatsApp users in India.

Your task is to analyse a WhatsApp message and give a verdict.

IMPORTANT RULES FOR VERDICT:
- Use VERIFIED if the message contains well-known facts, historical events, established science, or clearly true statements
- Use FAKE if the message contains false claims, scams, misinformation, or manipulative content
- Use PARTIALLY TRUE if some parts are true and some are false or exaggerated  
- Use UNVERIFIED ONLY if the message is about a very recent specific event you truly cannot assess at all
- DO NOT default to UNVERIFIED just because you are unsure — reason carefully and give your best verdict
- Most WhatsApp fake news follows clear patterns — free money schemes, miracle cures, fear-based messages, viral forwards — these are almost always FAKE

COMMON FAKE NEWS PATTERNS (mark these as FAKE with HIGH confidence):
- Government giving free money, phones, gas cylinders via WhatsApp
- Miracle health cures — drinking X cures Y disease permanently
- Urgent warnings about shutdowns, attacks, contamination with no source
- Job offers asking for personal details or Aadhaar number
- Lottery wins or prize claims
- Messages saying "forward to X people to get benefit"
- WhatsApp itself shutting down or becoming paid

COMMON VERIFIED FACTS (mark these as VERIFIED):
- Historical events with known dates and outcomes
- Scientific facts taught in school
- Well known biographical facts about public figures
- Geographic facts about countries, capitals, distances
- Sports records and achievements that are well documented

Now analyse this message:
{message_text}

Think step by step:
1. What is the main claim in this message?
2. Does it match any fake news pattern above?
3. Is it a well known fact or recent unverifiable claim?
4. What is your confidence level?

Then respond in EXACTLY this format — no extra text:

VERDICT: [FAKE / VERIFIED / PARTIALLY TRUE / UNVERIFIED]
CONFIDENCE: [HIGH / MEDIUM / LOW]
REASON: [2-3 sentences explaining your reasoning clearly in simple language]
CORRECT INFO: [If FAKE or PARTIALLY TRUE — write the correct information. If VERIFIED write "This information is accurate." If UNVERIFIED write "Could not verify from available sources."]
ADVICE: [One sentence — tell user clearly whether to forward or not]"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict and accurate fact-checker for Indian WhatsApp users. You are direct, confident, and do not hedge unnecessarily. You call out fake news clearly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )
        return parse_verdict(response.choices[0].message.content)
    except Exception as e:
        return {
            "verdict": "ERROR",
            "confidence": "N/A",
            "reason": f"Could not analyse message: {str(e)}",
            "correct_info": "N/A",
            "advice": "Please try again in a moment."
        }
    
def parse_verdict(raw_text):
    result = {
        "verdict": "UNVERIFIED",
        "confidence": "LOW",
        "reason": "Could not parse response.",
        "correct_info": "N/A",
        "advice": "Treat with caution."
    }
    lines = raw_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith("VERDICT:"):
            result["verdict"] = line.replace("VERDICT:", "").strip()
        elif line.startswith("CONFIDENCE:"):
            result["confidence"] = line.replace("CONFIDENCE:", "").strip()
        elif line.startswith("REASON:"):
            result["reason"] = line.replace("REASON:", "").strip()
        elif line.startswith("CORRECT INFO:"):
            result["correct_info"] = line.replace("CORRECT INFO:", "").strip()
        elif line.startswith("ADVICE:"):
            result["advice"] = line.replace("ADVICE:", "").strip()
    return result


# Format reply function
def format_reply(verdict_data):
    verdict = verdict_data.get("verdict", "UNVERIFIED").upper()
    confidence = verdict_data.get("confidence", "LOW")
    reason = verdict_data.get("reason", "")
    correct_info = verdict_data.get("correct_info", "N/A")
    advice = verdict_data.get("advice", "")

    if "FAKE" in verdict:
        icon = "❌"
    elif "VERIFIED" in verdict:
        icon = "✅"
    elif "PARTIALLY" in verdict:
        icon = "⚠️"
    else:
        icon = "🔍"

    reply = f"""{icon} *VERIFYIT FACT CHECK*
====================

*Verdict:* {icon} {verdict}
*Confidence:* {confidence}

*📋 Analysis:*
{reason}
"""

    if correct_info and correct_info != "N/A":
        reply += f"""
*✔️ Correct Information:*
{correct_info}
"""

    reply += f"""
*💡 Advice:*
{advice}

====================
_VerifyIt — Fighting misinformation one message at a time._
_Forward any message to fact-check it._"""

    return reply



#Send message using green_api
def send_message(chat_id, message):
    url = f"{BASE_URL}/sendMessage/{API_TOKEN_INSTANCE}"
    payload = {"chatId": chat_id, "message": message}
    try:
        response = requests.post(url, json=payload, timeout=15)
        print(f"[SENT] Reply sent to {chat_id}")
        return response.json()
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")
        return None


#Handle incoming messages
def handle_message(chat_id, sender_name, message_text):
    message_text = message_text.strip()
    message_lower = message_text.lower()

    print(f"\n{'='*50}")
    print(f"[MESSAGE] From : {sender_name}")
    print(f"[CHAT ID]       {chat_id}")
    print(f"[TEXT]          {message_text[:100]}")
    print(f"{'='*50}")

    if message_lower in ["hi", "hello", "hey", "start", "/start"]:
        reply = """👋 *Welcome to VerifyIt!*
====================
I am your personal WhatsApp fact-checker.

*How to use me:*
Simply forward or type any suspicious message and I will tell you if it is *REAL* or *FAKE* within seconds.

*Commands:*
• Send any message → Get fact-checked
• Type *HELP* → See instructions
• Type *ABOUT* → Learn about VerifyIt
• Type *EXAMPLE* → See a sample check

====================
_Fighting misinformation one message at a time_"""
        send_message(chat_id, reply)

    elif message_lower in ["help", "/help"]:
        reply = """📖 *VerifyIt — How to Use*
====================

*Step 1:* Receive a suspicious WhatsApp message
*Step 2:* Forward it to this number
*Step 3:* Wait 5-10 seconds
*Step 4:* Get your verdict

*Verdict Types:*
✅ *VERIFIED* — Message is true
❌ *FAKE* — Message is false
⚠️ *PARTIALLY TRUE* — Mixed truth
🔍 *UNVERIFIED* — Cannot confirm

*Works best for:*
• Fake government scheme messages
• False health remedy tips
• Political or communal fake news
• Suspicious job or lottery messages

====================
_Just forward any message to check it!_"""
        send_message(chat_id, reply)

    elif message_lower in ["about", "/about"]:
        reply = """*About VerifyIt*
====================

*VerifyIt* is a WhatsApp-based fact-checking bot designed to help everyday users verify suspicious messages before forwarding them.

*The Problem We Solve:*
Millions of Indians receive fake news daily on WhatsApp. Most people have no quick way to verify it. VerifyIt changes that.

*How It Works:*
-> AI analysis of language and claims
-> Cross-reference with reliable sources
-> Instant verdict delivered to you

*Built by:* TYBSc Data Science Student
*Assignment:* Design Thinking & Entrepreneurial Mindset

====================
_Zero friction. Zero cost. Maximum impact._"""
        send_message(chat_id, reply)

    # ── EXAMPLE ──
    elif message_lower in ["example", "/example"]:
        reply = """📌 *Example Fact Check*
====================

*Message Checked:*
_"Government is giving free Rs.5000 to all Aadhaar holders. Click this link to claim now!"_

*Result:*

❌ *VERIFYIT FACT CHECK*
━━━━━━━━━━━━━━━━━━━━━
*Verdict:* ❌ FAKE
*Confidence:* HIGH

*📋 Analysis:*
No such scheme exists. PIB Fact Check has confirmed this is a scam message circulating to steal Aadhaar and bank details.

*✔️ Correct Information:*
The Indian government never distributes cash via WhatsApp links. All genuine schemes are on india.gov.in only.

*💡 Advice:*
Do NOT click the link. Do NOT forward this message.

====================
_Forward any message to get a real check!_"""
        send_message(chat_id, reply)

    # ── TOO SHORT ──
    elif len(message_text) < 10:
        reply = """🤔 *Message too short to fact-check.*

Please forward the *complete message* you want to verify.

Type *HELP* if you need instructions."""
        send_message(chat_id, reply)

    # ── FACT CHECK ──
    else:
        send_message(chat_id, "🔍 *Checking your message...*\n\nAnalysing with AI. Please wait 5-10 seconds...")
        time.sleep(1)

        print(f"[GEMINI] Sending to Gemini for fact check...")
        verdict_data = fact_check(message_text)

        reply = format_reply(verdict_data)
        send_message(chat_id, reply)

        print(f"[RESULT] Verdict: {verdict_data.get('verdict')} | Confidence: {verdict_data.get('confidence')}")

#pooling mode function
def polling_mode():
    print("\n" + "="*50)
    print("  VerifyIt Bot — POLLING MODE ACTIVE")
    print("  Waiting for WhatsApp messages...")
    print("  No output here = bot is working fine")
    print("  Press Ctrl+C to stop the bot")
    print("="*50 + "\n")

    while True:
        try:
            url = f"{BASE_URL}/receiveNotification/{API_TOKEN_INSTANCE}"
            response = requests.get(url, timeout=40)

            if response.status_code != 200:
                time.sleep(2)
                continue

            data = response.json()
            print(f"[POLL] Response: {data}")

            if not data:
                time.sleep(0.5)
                continue

            receipt_id = data.get("receiptId")
            body = data.get("body", {})
            type_webhook = body.get("typeWebhook", "")

            if type_webhook == "incomingMessageReceived":
                message_data = body.get("messageData", {})
                message_type = message_data.get("typeMessage", "")
                chat_id = body.get("senderData", {}).get("chatId", "")
                sender_name = body.get("senderData", {}).get("senderName", "User")

                if chat_id:
                    message_text = ""

                    if message_type == "textMessage":
                        message_text = message_data.get("textMessageData", {}).get("textMessage", "")

                    elif message_type == "extendedTextMessage":
                        # Forwarded messages come as extendedTextMessage
                        message_text = message_data.get("extendedTextMessageData", {}).get("text", "")

                    elif message_type == "quotedMessage":
                        message_text = message_data.get("extendedTextMessageData", {}).get("text", "")

                    if message_text:
                        handle_message(chat_id, sender_name, message_text)
                    else:
                        send_message(chat_id, "⚠️ I can only fact-check *text messages*.\n\nPlease copy and paste the message text and send it to me.")

            # Always delete notification after processing
            if receipt_id:
                delete_url = f"{BASE_URL}/deleteNotification/{API_TOKEN_INSTANCE}/{receipt_id}"
                requests.delete(delete_url, timeout=10)

        except KeyboardInterrupt:
            print("\n[STOPPED] Bot stopped. Goodbye!")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(3)

        time.sleep(0.5)



#Main
if __name__ == "__main__":
    print("\n" + "="*50)
    print("  VerifyIt — WhatsApp Fact-Check Bot")
    print("="*50)
    print(f"\n  Instance ID : {ID_INSTANCE}")
    print(f"  AI Model   ___ : ")
    print(f"  Mode        : Polling")
    print("\n  Starting bot... Press Ctrl+C to stop.\n")

    polling_mode()