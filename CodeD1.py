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

#============================================================
# EXÉCUTION
# ============================================================
C = "fjfnhxwqhrhxvfjjfqdnufgjfmlkiwhw"
k = (3, 5)

M = D1(C, k)

print("Message chiffré :", C)
print("Clé k1 :", k[0])
print("Clé k2 :", k[1])
print("Message déchiffré :", M)