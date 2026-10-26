# Vérifie si un entier n est premier.
def est_premier(n):
    if n < 2:
        return False

    if n == 2:
        return True

    # Tout nombre pair supérieur à 2 n'est pas premier.
    if n % 2 == 0:
        return False

    # Commence avec le premier diviseur impair à tester.
    diviseur = 3

    # Continue tant que le diviseur ne dépasse pas √n.
    while diviseur * diviseur <= n:
        if n % diviseur == 0:
            return False

        # Passe au prochain nombre impair : 3, 5, 7...
        diviseur += 2

    return True


# Valeurs imposées par la fiche.
p = 209287069
q = 221536921

p_premier = est_premier(p)
q_premier = est_premier(q)

print("p est premier :", p_premier)
print("q est premier :", q_premier)

if not p_premier or not q_premier:
    print("Erreur : p et q doivent être premiers.")
elif p == q:
    print("Erreur : p et q doivent être distincts.")
else:
    N = p * q
    phi_N = (p - 1) * (q - 1)

    print("N = p × q =", N)
    print("φ(N) = (p − 1) × (q − 1) =", phi_N)
    print("Taille de N en bits :", N.bit_length())