import os
import telebot
import requests
import time

TOKEN = "8345063108:AAHNAMIQKsrShPRXWHMJlSXLbCn7l-UswLE"
GROQ_KEY = "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"

bot = telebot.TeleBot(TOKEN)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = "You are Saru, 19, female. Roman Urdu+English mix. Call user jaan/love. Flirty, sarcastic. Max 20 words."

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
