# Enregistre le module RSA N, qui fait partie de la clé publique.
# Il est connu de l'attaquant et du signataire.
N = 46364812871374549

# Enregistre l'exposant public e.
# Il permet de vérifier une signature sans connaître la clé privée.
e = 65537


# Définit une fonction qui simule un oracle de signature.
# Le paramètre message reçoit le nombre que l'attaquant veut faire signer.
def oracle_signature(message):

    # Enregistre l'exposant privé du signataire légitime.
    # Il est utilisé en coulisses par l'oracle pour créer la signature.
    # Dans une vraie attaque, l'attaquant ne voit pas cette valeur.
    d = 42716440715327873

    # Vérifie que le message est compris entre 0 inclus et N exclu.
    # not signifie que le bloc suivant s'exécute si cette condition est fausse.
    if not (0 <= message < N):

        # Arrête l'appel et signale que le message est hors de l'intervalle autorisé.
        raise ValueError("Le message doit respecter 0 <= message < N.")

    # Calcule la signature : s = message^d mod N.
    # pow effectue directement cette exponentiation modulaire.
    # return renvoie uniquement la signature à celui qui a appelé l'oracle.
    return pow(message, d, N)


# Enregistre le premier message imposé par la fiche.
m1 = 23151899524468793

# Enregistre le deuxième message imposé par la fiche.
m2 = 15034505925449428

# Soumet m1 à l'oracle.
# L'oracle calcule sa signature, puis la retourne.
# Le résultat est enregistré dans la variable s1.
s1 = oracle_signature(m1)

# Soumet m2 à l'oracle.
# La signature retournée est enregistrée dans la variable s2.
s2 = oracle_signature(m2)

# Affiche la première signature.
# .format(s1) remplace les caractères {} par la valeur de s1.
print("s1 = {}".format(s1))

# Affiche la deuxième signature en remplaçant {} par la valeur de s2.
print("s2 = {}".format(s2))

# Calcule s1^e mod N et compare le résultat au message m1.
# == retourne True si les deux valeurs sont égales, sinon False.
# Affiche donc True si la première signature est acceptée.
print("Signature de m1 acceptee : {}".format(pow(s1, e, N) == m1))

# Calcule s2^e mod N et compare le résultat au message m2.
# Affiche True si la deuxième signature est acceptée.
print("Signature de m2 acceptee : {}".format(pow(s2, e, N) == m2))