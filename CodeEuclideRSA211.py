
# Définit une fonction qui calcule le PGCD et les coefficients de Bézout.
def euclide_etendu(a, b):

    # Initialise les deux restes avec les nombres a et b.
    ancien_r, r = a, b

    # Initialise les coefficients de a : a = 1*a + 0*b.
    ancien_s, s = 1, 0

    # Initialise les coefficients de b : b = 0*a + 1*b.
    ancien_t, t = 0, 1

    # Affiche les titres des colonnes du tableau.
    print("quotient | reste | s | t")

    # Affiche le premier reste a et ses coefficients 1 et 0.
    print("- | {} | {} | {}".format(ancien_r, ancien_s, ancien_t))

    # Affiche le deuxième reste b et ses coefficients 0 et 1.
    print("- | {} | {} | {}".format(r, s, t))

    # Répète les calculs tant que le reste actuel n'est pas nul.
    while r != 0:

        # Calcule le quotient entier de la division de ancien_r par r.
        quotient = ancien_r // r

        # Calcule le reste de cette division.
        nouveau_r = ancien_r - quotient * r

        # Calcule le coefficient de a associé au nouveau reste.
        nouveau_s = ancien_s - quotient * s

        # Calcule le coefficient de b associé au nouveau reste.
        nouveau_t = ancien_t - quotient * t

        # Affiche le quotient, le nouveau reste et ses coefficients.
        print("{} | {} | {} | {}".format(quotient, nouveau_r, nouveau_s, nouveau_t))

        # Remplace les deux restes pour préparer la prochaine division.
        ancien_r, r = r, nouveau_r

        # Met à jour les deux coefficients de a.
        ancien_s, s = s, nouveau_s

        # Met à jour les deux coefficients de b.
        ancien_t, t = t, nouveau_t

    # Retourne le dernier reste non nul et ses coefficients.
    return ancien_r, ancien_s, ancien_t


# Enregistre le premier nombre premier imposé.
p = 209287069

# Enregistre le deuxième nombre premier imposé.
q = 221536921

# Calcule phi(N) avec la formule valable pour deux premiers distincts.
phi_N = (p - 1) * (q - 1)

# Enregistre l'exposant public imposé.
e = 65537

# Affiche la valeur de phi(N).
print("phi(N) = {}".format(phi_N))

# Affiche e, puis ajoute un saut de ligne avec \n.
print("e = {}\n".format(e))

# Appelle la fonction : a reçoit phi_N et b reçoit e.
# Récupère le PGCD et les coefficients vérifiant pgcd = s*phi_N + t*e.
pgcd, s, t = euclide_etendu(phi_N, e)

# Affiche le PGCD calculé, précédé d'un saut de ligne.
print("\nPGCD(e, phi(N)) = {}".format(pgcd))

# Vérifie que e et phi(N) sont premiers entre eux.
if pgcd == 1:

    # Transforme le coefficient t en son représentant positif modulo phi_N.
    d = t % phi_N

    # Affiche le coefficient de phi(N) dans l'identité de Bézout.
    print("Coefficient de phi(N) : {}".format(s))

    # Affiche le coefficient de e, qui est son inverse modulo phi(N).
    print("Coefficient de e : {}".format(t))

    # Affiche l'exposant privé d.
    print("d = {}".format(d))

    # Calcule le reste de e*d divisé par phi(N) : il doit valoir 1.
    verification = (e * d) % phi_N

    # Affiche le résultat de cette vérification.
    print("Verification : (e * d) % phi(N) = {}".format(verification))

# Exécute ce bloc si le PGCD est différent de 1.
else:

    # Signale que e ne possède pas d'inverse modulo phi(N).
    print("L'inverse modulaire n'existe pas.")