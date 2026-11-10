# Enregistre l'exposant public e, utilisé pour chiffrer les messages.
e = 65537

# Enregistre le module N, obtenu en multipliant p par q.
N = 46364812871374549

# Calcule 0 élevé à la puissance e, modulo N : le résultat est 0.
c_zero = pow(0, e, N)

# Calcule 1 élevé à la puissance e, modulo N : le résultat est 1.
c_un = pow(1, e, N)

# Calcule (N - 1) élevé à la puissance e, modulo N.
# Comme e est impair, le résultat est N - 1.
c_N_moins_un = pow(N - 1, e, N)

# Remplace {} par la valeur de c_zero et affiche le résultat.
print("Enc(0) = {}".format(c_zero))

# Remplace {} par la valeur de c_un et affiche le résultat.
print("Enc(1) = {}".format(c_un))

# Remplace {} par la valeur de c_N_moins_un et affiche le résultat.
print("Enc(N - 1) = {}".format(c_N_moins_un))