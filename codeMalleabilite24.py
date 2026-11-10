# Cryptogramme c obtenu en 2.2.
c = 31963660340929498

# Exposant public RSA.
e = 65537

# Module RSA.
N = 46364812871374549

# Calcule le chiffrement de 2 : 2^e mod N.
enc_deux = pow(2, e, N)

# Multiplie les deux cryptogrammes, puis applique le modulo N.
c_mal = (c * enc_deux) % N

# Affiche le cryptogramme modifié.
print("c_mal = {}".format(c_mal))