import streamlit as st
import os
from datetime import datetime
from memory import load_session, save_session
from detective_engine import ask_question, try_solution, get_hint
from openai import OpenAI
from prompts import THEMED_PROMPTS, PROMPT_STANDARD
import requests
import sseclient
# Initialize OpenAI client
client = OpenAI()

st.set_page_config(page_title="AI Detectiv", page_icon="🕵️")

st.title("🕵️ AI Detectiv")
st.markdown("Rezolvă un caz misterios generat de AI. Alege tematica și începe investigația!")

# Inițializare directoare
sessions_dir = "sessions"
os.makedirs(sessions_dir, exist_ok=True)

# Init state
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False
if "question" not in st.session_state:
    st.session_state["question"] = ""
if "history" not in st.session_state:
    st.session_state["history"] = None


def stream_gpt_response(history, model="gpt-3.5-turbo"):
    import time
    url = "http://127.0.0.1:8000/chat/stream"
    headers = {"Content-Type": "application/json"}
    payload = {"history": history[-10:], "model": model}
    response = requests.post(url, headers=headers, json=payload, stream=True)

    full_reply = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            print("🟡 TOKEN:", line)
            full_reply += line
            yield line
    print("✅ FINAL:", full_reply)



# Selectare caz
existing_cases = [f for f in os.listdir(sessions_dir) if f.endswith(".json")]
selected_case = st.selectbox("Alege un caz existent sau creează unul nou", ["(caz nou)"] + existing_cases)

if selected_case == "(caz nou)":
    tematica = st.selectbox("Alege tematica", list(THEMED_PROMPTS.keys()) + ["Random"])
    if st.button("🔮 Generează caz nou"):
        prompt = THEMED_PROMPTS.get(tematica) or PROMPT_STANDARD
        with st.spinner("🧠 Generăm misterul..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ești un narator român de povești polițiste."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            SESSION_FILE = f"{sessions_dir}/case_{timestamp}.json"
            history = [{"role": "assistant", "content": content}]
            save_session(SESSION_FILE, history)
            st.session_state["session_file"] = SESSION_FILE
            st.session_state["history"] = history
else:
    SESSION_FILE = f"{sessions_dir}/{selected_case}"
    history = load_session(SESSION_FILE)
    st.session_state["session_file"] = SESSION_FILE
    st.session_state["history"] = history

# Afișează conversația completă
SESSION_FILE = st.session_state.get("session_file")
# ✅ Afișăm conversația și input-ul doar dacă există un caz activ
if SESSION_FILE and st.session_state["history"] is not None and len(st.session_state["history"]) > 0:
    st.subheader("📖 Conversația completă:")
    for msg in st.session_state["history"]:
        if msg["role"] == "user":
            st.markdown(f"**🕵️ Tu:** {msg['content']}")
        elif msg["role"] == "assistant":
            content = msg["content"]
            if any(k in content.lower() for k in ["indiciu", "vinovat", "motiv", "adevăr", "dovezi"]):
                st.markdown(f"💡 **AI:** {content}")
            else:
                st.markdown(f"🧠 AI:** {content}")

    # ✅ Input + buton trimite doar dacă există caz
    st.text_input("Adresează o întrebare sau scrie 'rezolvare: ...'", key="question")
    if st.button("📤 Trimite"):
        st.session_state["submitted"] = True


# Procesare întrebări (o singură dată per click)
if st.session_state.get("submitted") and st.session_state["history"] is not None:
    question = st.session_state["question"]
    history = st.session_state["history"]

    if question.strip().lower().startswith("rezolvare:"):
        sol = question.replace("rezolvare:", "").strip()
        reply, history = try_solution(history, sol)
        save_session(st.session_state["session_file"], history)
        st.session_state["history"] = history
        st.session_state["submitted"] = False
        st.markdown(f"**🧠 AI:** {reply}")

    elif question.strip().lower().startswith("hint"):
        reply, history = get_hint(history)
        save_session(st.session_state["session_file"], history)
        st.session_state["history"] = history
        st.session_state["submitted"] = False
        st.markdown(f"**💡 Hint AI:** {reply}")

    else:
        # trimite întrebarea normală la endpoint /chat/stream
        history.append({"role": "user", "content": question})
        st.markdown("**🧠 AI (în timp real):** ", unsafe_allow_html=True)
        full_reply = ""
        stream_placeholder = st.empty()
        for token in stream_gpt_response(history):
            full_reply += token
            stream_placeholder.markdown(f"**🧠 AI:** {full_reply}")
        history.append({"role": "assistant", "content": full_reply})
        save_session(st.session_state["session_file"], history)
        st.session_state["history"] = history
        st.session_state["submitted"] = False

