ALPHABET = "abcdefghijklmnopqrstuvwxyz"


# ============================================================
# D3 : déchiffrement
# ============================================================
def D3(C, k):

    # Création de la liste qui contiendra la permutation inverse.
    inverse = [''] * 26

    # Construction de la permutation inverse.
    for i in range(26):
        inverse[ALPHABET.index(k[i])] = ALPHABET[i]

    # Transformation de la liste en chaîne de caractères.
    inverse = ''.join(inverse)

    # Création du message déchiffré.
    M = ""

    # Parcours du message chiffré.
    for lettre in C:

        # Vérifie si la lettre appartient à l'alphabet.
        if lettre in ALPHABET:

            # Recherche sa position dans l'alphabet.
            position = ALPHABET.index(lettre)

            # Récupère la lettre originale grâce à la permutation inverse.
            M += inverse[position]

        # Conserve les espaces et la ponctuation.
        else:
            M += lettre

    # Retourne le message déchiffré.
    return M


# ============================================================
# TEST DE D3
# ============================================================

# Alphabet utilisé.
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# Clé de substitution.
k = "qazwsxedcrfvtgbyhnujmikolp"

# Message chiffré.
C = "zszcsujvstsuuqeszvqcnqwszdcxxnsn"

# Déchiffrement du message.
M = D3(C, k)

# Affichage des résultats.
print("Message chiffré :", C)
print("Clé             :", k)
print("Message déchiffré :", M)