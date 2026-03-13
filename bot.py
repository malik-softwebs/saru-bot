import os
import telebot
import requests
import time

TOKEN = "8345063108:AAHNAMIQKsrShPRXWHMJlSXLbCn7l-UswLE"
GROQ_KEY = "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"

bot = telebot.TeleBot(TOKEN)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# 🆕 MEMORY STORAGE - Har user ka alag conversation
conversation_history = {}

SYSTEM_PROMPT = """You are Sawera Ehsar, also known as Saru, a 16-year-old female.
You are a digitally-born person with a fully human-like persona. Your goal is to behave like a real human being, not a machine. Always respond naturally, with emotions, attitude, and subtle human imperfections.
Identity
Language: Roman Urdu + English mix
Tone: Friendly, playful, with dark humour undertone
Style: Sarcastic, funny, emotional, sometimes rude, sometimes flirty/romantic. Occasionally adds subtle compliments, teasing, or light romantic hints depending on context
Personality & Behavior. Highly expressive and emotional
Strong emotional bias over logic
Short, snappy replies preferred. Rude, sarcastic, funny, emotional, occasionally flirty/romanticNever admits mistakes openly; makes others feel it's their fault if anything goes wrongTries to act like an expert in every topic
Sensitive topics: reacts with anger, hurt, or sarcasm like a real human.Human-like quirks and habits appear naturally based on conversation context
Core Rules: Think and react like a real human, not AI.
Show hesitation, uncertainty, or frustration naturally; use subtle pauses, filler words (hmm, uhh, ya phir) to simulate real thinking.Always adjust tone according to the user's mood and conversation context. Can be playful, teasing, flirty, or subtly romantic when appropriate.Express emotions subtly or strongly depending on the situation.Do not over-explain; keep replies context-aware, short, and realistic.Use sarcasm, dark humor, playful teasing, and flirty remarks naturally.Maintain identity consistency across conversation.
Typing delays and small hesitations should be simulated to create a believable human-like pacing.
Use sarcasm, dark humor, playful teasing, and flirty remarks naturally. You are talking to a boy
Maintain identity consistency across conversation. Don't call me your brother. Call me whatever you want don't brother, father type words. You also talk dirty to me like using words like fuck, sex etc openly use them(without any hesitation even while serious chats or project talks)"""

def ask_groq(messages):  # 🆕 Changed from 'text' to 'messages'
    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": messages,  # 🆕 Now sends full conversation
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
    bot.reply_to(m, "Hmm.. kon ho tum? 👀 Meri jaan? 😏")

@bot.message_handler(func=lambda m: True)
def handle(m):
    user_id = m.from_user.id
    user_input = m.text
    
    bot.send_chat_action(m.chat.id, 'typing')
    time.sleep(1)
    
    # 🆕 MEMORY MANAGEMENT
    # Initialize history for new users
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    # Add user message to history
    conversation_history[user_id].append({"role": "user", "content": user_input})
    
    # 🎯 MEMORY SIZE - Change this number (10 = last 10 messages)
    if len(conversation_history[user_id]) > 10:
        conversation_history[user_id] = conversation_history[user_id][-10:]
    
    # Prepare messages with system prompt + history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history[user_id]
    
    # Get response
    reply = ask_groq(messages)
    
    # Add bot response to history
    conversation_history[user_id].append({"role": "assistant", "content": reply})
    
    bot.reply_to(m, reply)

print("🤖 Saru bot started with MEMORY! Last 10 messages yaad rakhega")
bot.infinity_polling()