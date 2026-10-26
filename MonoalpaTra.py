import secrets

# ============================================================
# Alphabet
# ============================================================
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


# ============================================================
# GEN3 : génération aléatoire d'une permutation
# ============================================================
def Gen3():

    # On transforme l'alphabet en liste
    k = list(ALPHABET)

    # Mélange de Fisher-Yates
    for i in range(25, 0, -1):

        # Choisit une position aléatoire
        j = secrets.randbelow(i + 1)

        # Échange les deux lettres
        k[i], k[j] = k[j], k[i]

    # Transforme la liste en chaîne de caractères
    return ''.join(k)


# ============================================================
# E3 : chiffrement
# ============================================================
def E3(M, k):

    C = ""

    # Parcourt chaque lettre du message
    for lettre in M:

        # Vérifie que la lettre appartient à l'alphabet
        if lettre in ALPHABET:

            # Cherche la position de la lettre
            position = ALPHABET.index(lettre)

            # Remplace par la lettre correspondante dans k
            C += k[position]

        else:
            # Conserve les espaces ou caractères spéciaux
            C += lettre

    return C


# ============================================================
# D3 : déchiffrement
# ============================================================
def D3(C, k):

    # --------------------------------------------------------
    # ÉTAPE 1 : calcul de la permutation inverse k^-1
    # --------------------------------------------------------

    # On crée une liste de 26 cases vides
    inverse = [''] * 26

    # Parcourt les 26 positions
    for i in range(26):

        # ALPHABET[i] = lettre originale
        # k[i]        = lettre chiffrée
        #
        # Exemple :
        # si c -> a
        # alors k^-1(a) = c

        position = ALPHABET.index(k[i])

        inverse[position] = ALPHABET[i]

    # Transforme la liste en chaîne
    inverse = ''.join(inverse)

    # Affiche la permutation inverse
    print("Permutation k  :", k)
    print("Permutation k⁻¹:", inverse)

    # --------------------------------------------------------
    # ÉTAPE 2 : déchiffrement
    # --------------------------------------------------------

    M = ""

    # Parcourt le cryptogramme
    for lettre in C:

        if lettre in ALPHABET:

            # Cherche la position de la lettre dans l'alphabet
            position = ALPHABET.index(lettre)

            # Utilise la permutation inverse
            M += inverse[position]

        else:
            M += lettre

    return M


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

# Message clair
m = "ceciestlemessageclairadechiffrer"


# ============================================================
# EXÉCUTION 1
# ============================================================

k1 = "rsaofhvpmwtqzbkcigynxldeju"

print("\n================ EXÉCUTION 1 ================")

print("Message clair :", m)

C1 = E3(m, k1)

print("Cryptogramme  :", C1)

M1 = D3(C1, k1)

print("Message déchiffré :", M1)


# ============================================================
# EXÉCUTION 2
# ============================================================

k2 = "ixodqfulgkaenhscjbtvmpzyrw"

print("\n================ EXÉCUTION 2 ================")

print("Message clair :", m)

C2 = E3(m, k2)

print("Cryptogramme  :", C2)

M2 = D3(C2, k2)

print("Message déchiffré :", M2)


# ============================================================
# EXÉCUTION 3
# ============================================================

k3 = "jwxqkcgyhftoudpvrisenmabzl"

print("\n================ EXÉCUTION 3 ================")

print("Message clair :", m)

C3 = E3(m, k3)

print("Cryptogramme  :", C3)

M3 = D3(C3, k3)

print("Message déchiffré :", M3)