# Enregistre le module RSA public.
N = 46364812871374549

# Enregistre l'exposant public utilisé pour vérifier les signatures.
e = 65537

# Regroupe N et e pour former la clé publique.
pk = (N, e)


# Définit la fonction de vérification de la signature s du message m.
def Verify(pk, m, s):

    # Récupère N et e dans la clé publique.
    N, e = pk

    # Vérifie que le message et la signature sont dans l'intervalle autorisé.
    if not (0 <= m < N and 0 <= s < N):

        # Rejette la signature si une valeur est invalide.
        return False

    # Accepte si s^e modulo N est égal au message m.
    return pow(s, e, N) == m


# Enregistre le premier message de la fiche.
m1 = 23151899524468793

# Enregistre le deuxième message de la fiche.
m2 = 15034505925449428

# Enregistre la signature de m1 obtenue en 3.2.
s1 = 40495289341296419

# Enregistre la signature de m2 obtenue en 3.2.
s2 = 4958833821949512

# Multiplie les messages et garde le reste de la division par N.
m_cible = (m1 * m2) % N

# Multiplie les signatures et garde le reste de la division par N.
s_cible = (s1 * s2) % N

# Affiche le message cible.
print("m_cible = {}".format(m_cible))

# Affiche la signature fabriquée.
print("s_cible = {}".format(s_cible))

# Affiche True si la signature est acceptée, sinon False.
print("Signature acceptee : {}".format(Verify(pk, m_cible, s_cible)))

# Convertit True en 1 ou False en 0 et affiche le résultat de Verify.
print("Verify(m_cible, s_cible) = {}".format(int(Verify(pk, m_cible, s_cible))))