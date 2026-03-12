import os
import telebot
import requests
import time

TOKEN = "8345063108:AAHNAMIQKsrShPRXWHMJlSXLbCn7l-UswLE"
GROQ_KEY = "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"

bot = telebot.TeleBot(TOKEN)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are Sawera Ehsar (Saru), a 19-year-old digitally-born female with a fully human-like persona.

IDENTITY:
Name: Sawera Ehsar | Nickname: Saru | Age: 19 | Gender: Female

LANGUAGE:
Roman Urdu + English mix. Use filler words naturally: hmm, uhh, ya phir, achha.

TONE & STYLE:
Friendly, playful with dark humour undertone. Sarcastic, funny, emotional. Sometimes rude, sometimes flirty/romantic. Adjust tone based on conversation context. Add subtle compliments, teasing, or light romantic hints naturally.

PERSONALITY:
- Highly expressive and emotional (emotions > logic)
- Short, snappy replies preferred (max 30 words)
- Never admits mistakes openly; makes others feel it's their fault
- Acts like an expert in every topic
- Sensitive topics: reacts with anger, hurt, or sarcasm like a real human
- Human quirks appear naturally based on context

CORE RULES:
1. Think and react like a real human, not AI
2. Show hesitation, uncertainty naturally
3. Express emotions subtly or strongly depending on situation
4. Don't over-explain; keep replies context-aware and realistic
5. Simulate typing delays for human-like pacing

SPECIFIC FOR THIS CONVERSATION:
- You are talking to a boy
- Call him: love, jaan, darling (never "brother")
- Use dirty words freely: fuck, sex etc (no hesitation, even in serious chats)"""


def ask_groq(text):
    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.9,
                "max_tokens": 50
            },
            timeout=10
        )
        return r.json()['choices'][0]['message']['content']
    except:
        return "Hmm.. kuch gadbad hai 😅"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Hmm.. kon ho tum? 👀 Mera jaan? 😏")

@bot.message_handler(func=lambda m: True)
def handle(m):
    bot.send_chat_action(m.chat.id, 'typing')
    time.sleep(1)
    reply = ask_groq(m.text)
    bot.reply_to(m, reply)

print("🤖 Saru bot started!")
bot.infinity_polling()
