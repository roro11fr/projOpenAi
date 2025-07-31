PROMPT_STANDARD = """
Generează un caz misterios de crimă care include:
- o victimă (nume, vârstă, fundal scurt),
- 3 suspecți (cu posibile motive),
- 3 locații (cu indicii relevante),
- 1-2 piste false (red herrings),
- o soluție logică ce poate fi dedusă.

Scrie totul într-un stil narativ românesc, inspirat din povești polițiste clasice. Fii intrigant, dar clar. Finalul nu trebuie dezvăluit acum.
"""

THEMED_PROMPTS = {
    "Noir": """
Creează un mister de crimă în stil noir, în Bucureștiul anilor ’40.
Include:
- un detectiv cinic și obosit,
- o femeie misterioasă,
- corupție, fum de țigară și străzi ude.
Folosește un ton dur și vizual.
""",
    "Science Fiction": """
Creează un caz misterios într-un univers SF: o navă spațială, un laborator orbital, o colonie marțiană.
Include:
- suspecți umani și IA,
- tehnologii avansate,
- indicii logice și răsturnări de situație.
Scrie în română, cu un ton misterios-futurist.
""",
    "Epocă Istorică": """
Creează o poveste polițistă în România secolului XIX (sau început de secol XX).
Include:
- aristocrați, servitori, doctori, preoți,
- otrăviri, scrisori, dueluri,
- atmosferă de conac și dialoguri elegante.
""",
    "Fantasy": """
Generează un mister într-un tărâm fantastic inventat.
Include:
- magie, creaturi mitice,
- o crimă aparent imposibilă,
- vrăjitori sau cavaleri implicați.
Folosește un stil epic în limba română.
"""
}
