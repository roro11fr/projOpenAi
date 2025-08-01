# 🕵️ AI Detectiv

Un proiect interactiv scris în Python ce permite utilizatorului să rezolve mistere generate de un model AI. Fiecare caz este unic, generat cu ajutorul OpenAI, iar interacțiunea se face în limba română, printr-o interfață grafică Streamlit sau din terminal. Răspunsurile AI-ului sunt livrate în **timp real** printr-un backend FastAPI care utilizează **streaming completions** (`stream=True`).

---

## 🔍 Descriere

AI Detectiv este o aplicație interactivă unde utilizatorii pot investiga cazuri de crimă generate automat de un model de limbaj (GPT-3.5-turbo). Utilizatorul joacă rolul detectivului: pune întrebări, cere indicii și propune soluții. AI-ul răspunde în timp real printr-un API specializat, într-un stil narativ adaptat tematicii selectate.

---

## 🧠 Funcționalități principale

- Generare de cazuri misterioase complet narative și coerente
- Selectare tematică (Noir, SF, Fantasy, Epocă istorică)
- Interacțiune conversațională în limba română
- Evaluarea propunerilor de soluție de către AI (rol de judecător)
- Oferirea de hint-uri intermediare subtile, fără spoilere
- Salvarea sesiunii conversaționale local (`.json`)
- **Streaming complet în timp real** prin `FastAPI` + `StreamingResponse`
- Interfață grafică prietenoasă în `Streamlit`

---

## ⚙️ Arhitectură tehnică

```
                          ┌────────────────────────┐
                          │ Streamlit Frontend     │
                          │ (detective_app.py)     │◄─────┐
                          └────────────────────────┘      │
                                     │                    │ HTTP POST (stream)
                                     ▼                    │
                          ┌────────────────────────┐      │
                          │ FastAPI Backend        │◄─────┘
                          │ (streaming_api.py)     │
                          └────────────────────────┘
                                     │
                                     ▼
                        🔁 OpenAI GPT-3.5 Turbo (stream=True)
```

### 🔧 Backend FastAPI

Fișierul `streaming_api.py` definește un endpoint `/chat/stream` care:

- Primește istoria conversației (ultimele 10 mesaje)
- Creează un `completion` cu `stream=True` pentru a transmite răspunsul token cu token
- Returnează răspunsul prin `StreamingResponse` către clientul Streamlit

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True
)
```

---

## 🗂 Structura proiectului

```
projOpenAi/
│
├── main.py                # Interfață CLI (terminal) pentru investigații
├── detective_app.py       # Interfața Streamlit cu streaming AI
├── streaming_api.py       # FastAPI backend pentru completări în timp real
├── detective_engine.py    # Funcții: întrebare, soluție, hint
├── prompts.py             # Prompturi tematice pentru generarea misterelor
├── memory.py              # Load/save sesiuni în fișiere JSON
├── sessions/              # Sesiuni conversaționale salvate
└── README.md              # Documentația proiectului
```

---

## ▶️ Cum rulezi proiectul

### 1. Clonare
```bash
git clone https://github.com/roro11fr/projOpenAi.git
cd projOpenAi
```

### 2. Instalare dependențe
```bash
pip install -r requirements.txt
```
sau:
```bash
pip install openai streamlit fastapi uvicorn sseclient
```

### 3. Setare OpenAI API Key
```bash
export OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

---

### 4. Pornește backend-ul de streaming (FastAPI)
```bash
uvicorn streaming_api:app --reload
```

### 5. Pornește aplicația interactivă
```bash
streamlit run detective_app.py
```

sau:
## 🔮 Tematici disponibile

| Tematică         | Elemente specifice                                                 |
|------------------|---------------------------------------------------------------------|
| Noir             | Detectiv obosit, Bucureștiul anilor '40, corupție, străzi ude      |
| SF               | Colonie marțiană, IA suspicioase, tehnologii avansate              |
| Epocă Istorică   | Aristocrați, otrăviri, dueluri, conac românesc                     |
| Fantasy          | Vrăjitori, magie, creaturi mitice, crimă imposibilă                |

---

## 🧪 Exemple de funcționalități GPT

- `ask_question()` → trimite întrebarea și primește răspuns narativ
- `try_solution()` → trimite soluția detectivului și primește verdictul AI
- `get_hint()` → oferă indicii subtile fără a dezvălui finalul

---

## Autori

Proiect realizat în cadrul **DavaX Academy** de către [roro11fr](https://github.com/roro11fr),  
cu sprijinul OpenAI GPT și framework-uri moderne Python (FastAPI, Streamlit, Uvicorn).
