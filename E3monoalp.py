# ============================================================
# E3 : chiffrement par substitution
# ============================================================

# Définit l'alphabet utilisé pour le chiffrement.
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


# Définition de la fonction E3.
# M représente le message en clair.
# k représente la clé de substitution.
def E3(M, k):

    # Crée une chaîne vide qui servira à construire
    # progressivement le message chiffré.
    C = ""

    # Parcourt chaque caractère du message M.
    for lettre in M:

        # Vérifie si le caractère appartient à l'alphabet.
        if lettre in ALPHABET:

            # Recherche la position de la lettre dans l'alphabet.
            #
            # Exemple :
            # a → position 0
            # b → position 1
            # c → position 2
            position = ALPHABET.index(lettre)

            # Remplace la lettre par la lettre située
            # à la même position dans la clé k.
            C += k[position]

        # Si le caractère n'est pas dans l'alphabet,
        # on le conserve tel quel.
        #
        # Cela permet de conserver les espaces,
        # chiffres et signes de ponctuation.
        else:
            C += lettre

    # Retourne le message chiffré.
    return C


# ============================================================
# TEST DE LA FONCTION E3
# ============================================================

# Définit le message en clair.
M = "ceciestlemessageclairadechiffrer"

# Définit une clé de substitution.
k = "qazwsxedcrfvtgbyhnujmikolp"

# Chiffre le message avec E3.
C = E3(M, k)

# Affiche le message original.
print("Message clair  :", M)

# Affiche la clé utilisée.
print("Clé             :", k)

# Affiche le message chiffré.
print("Message chiffré :", C)