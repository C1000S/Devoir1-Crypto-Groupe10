# Cryptogramme indépendant fourni dans la fiche.
c_prime = 3632978084399643

# Exposant privé de déchiffrement.
d = 42716440715327873

# Module RSA.
N = 46364812871374549

# Exposant public, utilisé pour vérifier le résultat.
e = 65537

# Calcule le message déchiffré : m' = c'^d mod N.
m_prime = pow(c_prime, d, N)

# Affiche le message déchiffré.
print("Message dechiffre m' = {}".format(m_prime))

# Rechiffre le message pour retrouver le cryptogramme initial.
c_verification = pow(m_prime, e, N)

# Vérifie que le cryptogramme retrouvé est identique à c'.
print("Verification correcte : {}".format(c_verification == c_prime))