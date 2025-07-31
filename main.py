from memory import load_session, save_session
from detective_engine import ask_question
from prompts import MYSTERY_CREATOR_PROMPT, THEMED_PROMPTS
from openai import OpenAI

client = OpenAI()
SESSION_FILE = "sessions/case1.json"

tematica = input("Alege tematica (noir / sf / epoca / fantasy): ").strip().lower()
prompt = THEMED_PROMPTS.get(tematica, MYSTERY_CREATOR_PROMPT)

history = load_session(SESSION_FILE)
if not history:
    print("🔎 Generăm un nou caz misterios...\n")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a crime story narrator."},
            {"role": "user", "content": prompt}
        ]
    )
    intro = response.choices[0].message.content
    print(intro)
    history.append({"role": "assistant", "content": intro})
    save_session(SESSION_FILE, history)

print("\n💬 Poți începe să investighezi! Scrie „exit” pentru a ieși.\n")

while True:
    question = input("Tu 🕵️: ")
    if question.strip().lower() in ["exit", "quit"]:
        print("📝 Sesiunea a fost salvată.")
        save_session(SESSION_FILE, history)
        break

    reply, history = ask_question(history, question)
    print(f"\n🧠 AI Detectiv: {reply}\n")
    save_session(SESSION_FILE, history)
    print("🔄 Sesiunea a fost actualizată.")