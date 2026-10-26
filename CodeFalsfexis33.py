# Enregistre le module RSA N.
# Cette valeur est publique : l'attaquant peut la connaître.
N = 46364812871374549

# Enregistre l'exposant public e.
# Il sert à vérifier les signatures.
e = 65537

# Regroupe N et e dans un tuple, c'est-à-dire un groupe de valeurs.
# pk signifie « public key », donc « clé publique ».
pk = (N, e)


# Définit une fonction appelée Verify.
# Elle reçoit la clé publique pk, le message m et la signature s.
def Verify(pk, m, s):

    # Extrait les deux valeurs de la clé publique.
    # La première est placée dans N et la deuxième dans e.
    N, e = pk

    # Vérifie que m et s sont compris entre 0 inclus et N exclu.
    # and exige que les deux conditions soient respectées.
    # not inverse le résultat : ce bloc s'exécute si une valeur est invalide.
    if not (0 <= m < N and 0 <= s < N):

        # Retourne False pour rejeter la paire.
        # return quitte immédiatement la fonction.
        return False

    # Calcule s^e modulo N avec pow(s, e, N).
    # Compare ensuite ce résultat au message m avec ==.
    # Retourne True si les valeurs sont égales, sinon False.
    return pow(s, e, N) == m


# L'attaquant choisit le nombre 2 comme signature.
# Il ne demande pas cette signature à l'oracle : il la choisit lui-même.
s = 2

# Calcule le message correspondant : m = s^e modulo N.
# Ce calcul utilise uniquement les informations publiques.
# Le message est donc obtenu APRÈS le choix de la signature.
m = pow(s, e, N)

# Affiche le message calculé.
# .format(m) remplace {} par la valeur de m.
print("Message m = {}".format(m))

# Affiche la signature choisie.
# .format(s) remplace {} par la valeur de s.
print("Signature s = {}".format(s))

# Appelle Verify pour vérifier la paire (m, s).
# Remplace {} par le résultat True ou False, puis l'affiche.
print("Signature acceptee : {}".format(Verify(pk, m, s)))