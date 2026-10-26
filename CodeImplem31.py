# Enregistre le module RSA, commun aux clés publique et privée.
# Il a été calculé avec N = p * q.
N = 46364812871374549

# Enregistre l'exposant public.
# Il permet de vérifier les signatures.
e = 65537

# Enregistre l'exposant privé.
# Il permet de créer les signatures.
d = 42716440715327873

# Regroupe N et d dans un tuple appelé sk.
# sk signifie « secret key », c'est-à-dire clé privée.
sk = (N, d)

# Regroupe N et e dans un tuple appelé pk.
# pk signifie « public key », c'est-à-dire clé publique.
pk = (N, e)


# Crée une fonction appelée Sign.
# Elle reçoit la clé privée sk et le message numérique m.
def Sign(sk, m):

    # Extrait les deux éléments du tuple sk.
    # La première valeur est placée dans N et la deuxième dans d.
    N, d = sk

    # Vérifie si le message ne respecte pas 0 <= m < N.
    # not inverse la condition : le bloc s'exécute si m est invalide.
    if not (0 <= m < N):

        # Arrête l'exécution en signalant une valeur de message incorrecte.
        raise ValueError("Le message doit respecter 0 <= m < N.")

    # Calcule la signature s = m^d mod N.
    # pow effectue directement l'exponentiation modulaire.
    # return transmet la signature au code qui a appelé la fonction.
    return pow(m, d, N)


# Crée une fonction appelée Verify.
# Elle reçoit la clé publique pk, le message m et la signature s.
def Verify(pk, m, s):

    # Extrait N et e de la clé publique.
    N, e = pk

    # Vérifie que le message ET la signature sont dans l'intervalle autorisé.
    # and exige que les deux conditions soient vraies.
    # not déclenche le rejet si au moins une condition est fausse.
    if not (0 <= m < N and 0 <= s < N):

        # Retourne False (« faux ») : la signature est rejetée.
        # return quitte immédiatement la fonction.
        return False

    # Calcule s^e mod N et compare le résultat au message m.
    # == signifie « est égal à ? ».
    # Retourne True si les valeurs sont égales, sinon False.
    return pow(s, e, N) == m


# Crée une liste contenant les deux messages à tester.
messages = [100, 12589]

# Parcourt la liste.
# Au premier passage, m vaut 42 ; au deuxième, m vaut 12345.
for m in messages:

    # Appelle Sign avec la clé privée et le message actuel.
    # Enregistre la signature retournée dans la variable signature.
    signature = Sign(sk, m)

    # Vérifie la signature avec la clé publique et le message original.
    # Enregistre True ou False dans accepte.
    accepte = Verify(pk, m, signature)

    # Effectue un XOR entre le message et le nombre 1.
    # Cela inverse uniquement le bit le plus à droite du message.
    # Enregistre le résultat dans message_modifie.
    message_modifie = m ^ 1

    # Vérifie la signature originale sur le message modifié.
    # Aucune nouvelle signature n'est créée.
    # Enregistre le résultat de cette vérification.
    accepte_apres_modification = Verify(pk, message_modifie, signature)

    # Affiche le message original.
    # \n ajoute un saut de ligne avant le texte.
    # .format(m) remplace {} par la valeur de m.
    print("\nMessage original : {}".format(m))

    # Affiche la signature calculée.
    # {} est remplacé par la valeur de signature.
    print("Signature : {}".format(signature))

    # Affiche True si la signature du message original est acceptée.
    print("Signature acceptee : {}".format(accepte))

    # Affiche la valeur du message après modification d'un bit.
    print("Message modifie : {}".format(message_modifie))

    # Affiche le résultat de la vérification sur le message modifié.
    # L'instruction est répartie sur trois lignes pour faciliter la lecture.
    print("Signature acceptee apres modification : {}".format(
        accepte_apres_modification
    ))