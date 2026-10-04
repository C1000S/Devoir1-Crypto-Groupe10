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
#============================================================
# EXÉCUTION
# ============================================================

M = "ceciestlemessageclairadechiffrer"

k = (3, 5)

C = E1(M, k)

print("Message clair :", M)
print("Clé k1 :", k[0])
print("Clé k2 :", k[1])
print("Message chiffré :", C)