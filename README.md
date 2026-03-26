# VerifyIt — WhatsApp Fact-Check Bot

> ⚠️ **This is a testing prototype** built as a bonus extension of a college assignment.
> It is not a production-ready product. Use it for demo and testing purposes only.

---

## What is VerifyIt?

VerifyIt is a WhatsApp-based fact-checking bot that analyses forwarded messages and tells you if they are **real or fake** — within seconds, without leaving WhatsApp.

Built as part of a **Design Thinking & Entrepreneurial Mindset** assignment (TYBSc Data Science, Sem 6).

---

## How It Works

```
User forwards suspicious WhatsApp message
            ↓
Green-API receives and sends to Python bot
            ↓
Groq AI (Llama 3.3 70B) analyses the message
            ↓
Bot replies with verdict + reason + advice
```

---

## Verdict Types

| Verdict | Meaning |
|---------|---------|
| ✅ VERIFIED | Message is true |
| ❌ FAKE | Message is false |
| ⚠️ PARTIALLY TRUE | Mixed truth |
| 🔍 UNVERIFIED | Cannot confirm |

---

## Tech Stack

| Component | Tool | Cost |
|-----------|------|------|
| WhatsApp Integration | Green-API (Free Developer Tier) | Free |
| AI Engine | Groq API — Llama 3.3 70B | Free |
| Backend | Python 3 | Free |
| **Total** | | **Rs. 0** |

---

## Commands

| Send | Response |
|------|----------|
| `hi` | Welcome message |
| `help` | Usage instructions |
| `about` | About VerifyIt |
| `example` | Sample fact check |
| Any message | AI fact-check verdict |

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/verifyit-bot.git
cd verifyit-bot
```

### 2. Install dependencies
```bash
pip install requests groq flask
```

### 3. Get your free API keys
- **Groq API Key** → https://console.groq.com
- **Green-API credentials** → https://green-api.com (free developer plan)

### 4. Configure bot.py
```python
GROQ_API_KEY       = "your_groq_key_here"
ID_INSTANCE        = "your_instance_id"
API_TOKEN_INSTANCE = "your_api_token"
BASE_URL           = "https://XXXX.api.greenapi.com/waInstanceXXXXXX"
```
> Note: Check your Green-API dashboard for the correct `apiUrl` — it may differ from the default.

### 5. Run
```bash
python bot.py
```

---

## Testing Results

Tested on 7 real WhatsApp messages:

- **Accuracy: 6/7 (85.7%)**
- **Wrong verdicts: 0**
- **Average response time: 2–4 seconds**

---

## ⚠️ Limitations (Prototype)

- Runs **locally only** — bot stops when terminal closes
- **Text messages only** — no image or video fact-checking
- **English only** — Hindi/Marathi not yet supported
- **Not suitable for production** — no rate limiting, no database, no scaling
- Accuracy depends on Groq AI knowledge — very recent events may not be verified correctly

---

## Project Context

This bot was built as a **bonus prototype** for a college assignment on Design Thinking. The assignment involved:

1. Identifying a real problem — misinformation on WhatsApp
2. Interviewing real users
3. Designing a solution (VerifyIt)
4. Building a working prototype — this bot

**Course:** Design Thinking & Entrepreneurial Mindset
**Program:** TYBSc Data Science, Sem 6

---

## License

This project is for **educational and demo purposes only.**
Not affiliated with WhatsApp, Meta, Google, or Groq.
