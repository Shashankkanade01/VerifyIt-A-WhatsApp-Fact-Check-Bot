# VerifyIt - WhatsApp Fact-Check Bot

> **This is a testing prototype** built as a bonus extension of a college assignment.
> It is not a production-ready product. Use it for demo and testing purposes only.

---

## What is VerifyIt?

VerifyIt is a WhatsApp-based fact-checking bot that analyses forwarded messages and tells you if they are **real or fake** - within seconds, without leaving WhatsApp.

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
| AI Engine | Groq API — llama-3.3-70b-versatile  | Free |
| Backend | Python | Free |
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

## Testing Results

Tested on 7 real WhatsApp messages:

- **Accuracy: 6/7 (85.7%)**
- **Wrong verdicts: 0**
- **Average response time: 2–4 seconds**

---

## Limitations (Prototype)

- Runs **locally only** — bot stops when terminal closes
- **Text messages only** — no image or video fact-checking
- **English only** — Hindi/Marathi not yet supported
- **Not suitable for production** — no rate limiting, no database, no scaling
- Accuracy depends on AI Models knowledge — very recent events may not be verified correctly

---

## Project Context

This bot was built as a **bonus prototype** for a college assignment on Design Thinking. The assignment involved:

1. Identifying a real problem — misinformation on WhatsApp
2. Interviewing real users
3. Designing a solution (VerifyIt)
4. Building a working prototype — this bot

---
