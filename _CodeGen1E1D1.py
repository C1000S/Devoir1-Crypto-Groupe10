
# Importation du module random afin de générer plusieurs nombres aléatoires
import random

# Definition de l'alphabet que notre chiffrement va utiliser
# La position de 'a' est 0, 'b' est 1, ..., 'z' est 25
lettres = "abcdefghijklmnopqrstuvwxyz"


# ============================================================
# Gen1 : génération de la clé								
# ============================================================

# On définit la fonction Gen1 qui va générer une clé
def Gen1():

    # On choisit au hasard un nombre entre 0 et 25
    # Ce nombre sera notre première clé k1
    k1 = random.randrange(26)

    # On choisit au hasard un deuxième nombre entre 0 et 25
    # Ce nombre sera notre deuxième clé k2
    k2 = random.randrange(26)

    # On retourne la clé sous forme d'un couple (k1, k2)
    return (k1, k2)


# ============================================================
# E1 : chiffrement
# ============================================================

# On définit la fonction E1
# M représente le message clair
# k représente la clé (k1, k2)
lettres = "abcdefghijklmnopqrstuvwxyz"
def E1(M, k):

    # On récupère la première valeur de la clé
    # k[0] correspond à k1
    k1 = k[0]

    # On récupère la deuxième valeur de la clé
    # k[1] correspond à k2
    k2 = k[1]

    # On crée une chaîne vide qui contiendra
    # progressivement le message chiffré
    C = ""

    # enumerate() permet de parcourir le message
    # i représente la position de la lettre
    # lettre représente la lettre elle-même
    for i, lettre in enumerate(M):

        # On vérifie si la position est paire
        # i % 2 == 0 signifie que le reste de la division
        # de i par 2 est égal à 0
        if i % 2 == 0:

            # Pour une position paire, on utilise k1
            decalage = k1

        # Si la position n'est pas paire,
        # elle est donc impaire
        else:

            # Pour une position impaire, on utilise k2
            decalage = k2

        # On cherche la position de la lettre dans l'alphabet
        # Exemple : 'a' = 0, 'b' = 1, 'c' = 2, etc.
        x = lettres.index(lettre)

        # On ajoute le décalage à la position de la lettre
        # % 26 permet de rester dans l'alphabet
        y = (x + decalage) % 26

        # On transforme le nombre obtenu en lettre
        # Exemple : 0 donne 'a', 1 donne 'b', etc.
        lettre_chiffree = lettres[y]

        # On ajoute la lettre chiffrée au résultat final
        C = C + lettre_chiffree

    # On retourne le message chiffré
    return C



# ============================================================
# D1 : déchiffrement
# ============================================================

# On définit la fonction D1
# C représente le message chiffré
# k représente la clé (k1, k2)
lettres = "abcdefghijklmnopqrstuvwxyz"
def D1(C, k):

    # On récupère la première clé
    k1 = k[0]

    # On récupère la deuxième clé
    k2 = k[1]

    # On crée une chaîne vide
    # Elle contiendra le message déchiffré
    M = ""

    # On parcourt toutes les lettres du message chiffré
    # i représente la position
    # lettre représente la lettre chiffrée
    for i, lettre in enumerate(C):

        # Si la position est paire
        if i % 2 == 0:

            # On utilise k1 pour effectuer le déchiffrement
            decalage = k1

        # Sinon, la position est impaire
        else:

            # On utilise k2 pour effectuer le déchiffrement
            decalage = k2

        # On trouve la position de la lettre chiffrée
        # dans l'alphabet
        y = lettres.index(lettre)

        # Pour déchiffrer, on soustrait le décalage
        # % 26 permet de gérer le retour au début de l'alphabet
        x = (y - decalage) % 26

        # On transforme la position obtenue en lettre
        lettre_claire = lettres[x]

        # On ajoute la lettre déchiffrée au message final
        M = M + lettre_claire

    # On retourne le message clair
    return M

# ============================================================
# EXEMPLE TRACES D'EXECUTION COMPLETE (ALICE, EVE, BOB)
# ============================================================


# ============================================================
# ALICE
# ============================================================

print("\n================ ALICE ================\n")

# Alice définit le message clair
M = "ceciestlemessageclairadechiffrer"

print("Alice :")
print("Message clair :", M)

# Les deux clés sont imposées pour les traces
k1 = int(input("Entrez la valeur de k1 imposée pour le groupe 10 (0 à 25) : "))
k2 = int(input("Entrez la valeur de k2 imposée pour le groupe 10 (0 à 25) : "))

# Création de la clé
k = (k1, k2)

print("Clé secrète :")
print("k1 =", k1)
print("k2 =", k2)
print("k  =", k)

# Alice chiffre le message
C = E1(M, k)

print("Message chiffré :", C)


# ============================================================
# EVE
# ============================================================

print("\n================ EVE =================\n")

# Eve intercepte le message chiffré
C_Eve = C

print("Eve intercepte le message chiffré :")
print("C =", C_Eve)

# Eve ne connaît pas la clé
print("Eve ne connaît pas la clé :")
print("k = ???")


# ============================================================
# BOB
# ============================================================

print("\n================ BOB =================\n")

# Bob reçoit le message chiffré
print("Bob reçoit le message chiffré :")
print("C =", C)

# Bob possède la clé secrète
print("Bob possède la clé :")
print("k =", k)

# Bob déchiffre le message
M2 = D1(C, k)

print("Message déchiffré :", M2)


# ============================================================
# VERIFICATION
# ============================================================

print("\n================ RESULTAT =============\n")

print("Alice envoie :", C)
print("Eve intercepte :", C)
print("Bob déchiffre :", M2)

if M == M2:
    print("\nc'est PARFAIT Le message de Bob est identique au message d'Alice.")
else:
    print("\npas BON DESOLE Erreur de déchiffrement.")
