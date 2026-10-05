
# ============================================================
# EVE : ATTAQUE PAR FORCE BRUTE
# ============================================================

# Alphabet utilisé pour le chiffrement
lettres = "abcdefghijklmnopqrstuvwxyz"


# ============================================================
# FONCTION DE DECHIFFREMENT D1
# ============================================================

def D1(C, cle):

    # Récupération des deux clés
    k1, k2 = cle

    # Message déchiffré
    M = ""

    # Parcours du cryptogramme
    for i, c in enumerate(C):

        # Conversion de la lettre en nombre 0 à 25
        x = lettres.index(c)

        # Indices pairs : utilisation de k1
        if i % 2 == 0:
            x = (x - k1) % 26

        # Indices impairs : utilisation de k2
        else:
            x = (x - k2) % 26

        # Conversion du nombre en lettre
        M += lettres[x]

    return M


# ============================================================
# Petit dictionnaire de mots français
# permettant de donner un score aux messages obtenus
# ============================================================

dictionnaire = [
    "ce",
    "ceci",
    "est",
    "le",
    "la",
    "les",
    "de",
    "des",
    "du",
    "un",
    "une",
    "message",
    "clair",
    "chiffrer",
    "chiffre",
    "et",
    "en",
    "pour",
    "avec",
    "que",
    "qui",
    "dans",
    "sur"
]


# ============================================================
# Fonction de score
# ============================================================

def score_message(message):

    score = 0

    # On cherche les mots du dictionnaire
    for mot in dictionnaire:

        if mot in message:
            score += len(mot) ** 2

    return score


# ============================================================
# Eve teste les 676 clés possibles
# ============================================================

def attaque_eve(C):

    candidats = []

    # k1 peut prendre les valeurs 0 à 25
    for k1 in range(26):

        # k2 peut prendre les valeurs 0 à 25
        for k2 in range(26):

            # Eve essaie de déchiffrer
            M_test = D1(C, (k1, k2))

            # Elle calcule le score du message
            score = score_message(M_test)

            # Elle conserve le résultat
            candidats.append((score, k1, k2, M_test))

    # On classe les candidats du meilleur score
    # au plus faible
    candidats.sort(reverse=True)

    return candidats


# ============================================================
# LES 3 CRYPTOGRAMMES
# ============================================================

cryptogrammes = [
    ("Cryptogramme 1", "eyecgmvfgggmuuiyefcctufyebkzhlgl"),
    ("Cryptogramme 2", "vevixsmlxmxslazevltikawevhbfyrxr"),
    ("Cryptogramme 3", "wmwqyantyuyamiamwtuqlixmwpcnzzyz")
]


# ============================================================
# ATTAQUE D'EVE
# ============================================================

for nom, C in cryptogrammes:

    print("\n============================================")
    print(nom)
    print("============================================")

    print("Cryptogramme :", C)

    # Lancement de l'attaque
    candidats = attaque_eve(C)

    # Nombre total de clés testées
    print("\nNombre total de clés testées :", len(candidats))

    print("\nMeilleurs candidats :")

    # Affichage des 5 meilleurs candidats
    for score, k1, k2, message in candidats[:5]:

        print(
            "Score =", score,
            "| k1 =", k1,
            "| k2 =", k2,
            "| message =", message
        )

    # Meilleur candidat
    meilleur = candidats[0]

    print("\n>>> Clé retrouvée par Eve :")
    print("k1 =", meilleur[1])
    print("k2 =", meilleur[2])

    print("\n>>> Score du meilleur candidat :")
    print(meilleur[0])

    print("\n>>> Message retenu par Eve :")
    print(meilleur[3])

