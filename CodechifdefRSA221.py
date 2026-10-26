# Message numérique imposé par la fiche.
m = 1394500914838255

# Exposant public RSA.
e = 65537

# Module RSA : N = p * q.
N = 46364812871374549

# Calcule le message chiffré : c = m^e mod N.
c = pow(m, e, N)

# Affiche le message chiffré.
print("Message chiffre c = {}".format(c))