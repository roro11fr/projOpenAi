from openai import OpenAI

client = OpenAI()
def ask_question(history, question, model="gpt-3.5-turbo"):
    messages = [{"role": "system", "content": "Ești un narator român de povești polițiste. Răspunde într-un stil narativ, misterios și coerent."}]
    messages += history
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    reply = response.choices[0].message.content
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": reply})
    return reply, history


def try_solution(history, solution, model="gpt-3.5-turbo"):
    messages = [{"role": "system", "content": "Ești judecătorul cazului și trebuie să evaluezi dacă detectivul a identificat corect criminalul. Răspunde în limba română, într-un stil narativ."}]
    messages += history[-10:]  # Ultimele 10 mesaje pentru context
    messages.append({
        "role": "user",
        "content": f"Detectivul crede că a rezolvat cazul:\n{solution}\nEvaluează dacă are dreptate și explică răspunsul."
    })

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    reply = response.choices[0].message.content
    history.append({"role": "user", "content": f"rezolvare: {solution}"})
    history.append({"role": "assistant", "content": reply})
    return reply, history


def get_hint(history, model="gpt-3.5-turbo"):
    messages = [{"role": "system", "content": "Ești un narator AI care oferă un indiciu subtil despre misterul actual. Nu da răspunsul final. Fii misterios, dar util."}]
    messages += history
    messages.append({"role": "user", "content": "Poți să-mi dai un indiciu legat de investigație?"})

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    reply = response.choices[0].message.content
    history.append({"role": "user", "content": "hint:"})
    history.append({"role": "assistant", "content": reply})
    return reply, history
