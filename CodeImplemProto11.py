import secrets  # Importe l’outil qui permet de choisir des nombres aléatoires sûrs.

p = 2**61 - 1  # Calcule le nombre premier public p.
g = 37  # Définit le générateur public g.


def Gen():  # Définit la fonction qui crée une clé privée.
    return secrets.randbelow(p - 3) + 2  # Renvoie un nombre aléatoire entre 2 et p - 2 inclus.


def PubKey(x):  # Définit la fonction qui reçoit une clé privée x.
    return pow(g, x, p)  # Renvoie g à la puissance x, modulo p : la clé publique.


def Secret(cle_privee, cle_publique_recue):  # Reçoit notre clé privée et la clé publique de l’autre.
    return pow(cle_publique_recue, cle_privee, p)  # Calcule et renvoie le secret partagé.


# CRÉATION DES CLÉS PRIVÉES

a = Gen()  # Choisit au hasard la clé privée d’Alice.
b = Gen()  # Choisit au hasard la clé privée de Bob.

print("Clé privée d'Alice :", a)  # Affiche la clé privée d’Alice pour cet exemple.
print("Clé privée de Bob :", b)  # Affiche la clé privée de Bob pour cet exemple.


# CALCUL DES CLÉS PUBLIQUES

A = PubKey(a)  # Calcule la clé publique d’Alice à partir de sa clé privée.
B = PubKey(b)  # Calcule la clé publique de Bob à partir de sa clé privée.

print("Clé publique d'Alice :", A)  # Affiche la clé publique qu’Alice transmet à Bob.
print("Clé publique de Bob :", B)  # Affiche la clé publique que Bob transmet à Alice.


# CALCUL DU SECRET PARTAGÉ

secret_alice = Secret(a, B)  # Alice utilise sa clé privée a et la clé publique B de Bob.
secret_bob = Secret(b, A)  # Bob utilise sa clé privée b et la clé publique A d’Alice.

print("Secret calculé par Alice :", secret_alice)  # Affiche le secret obtenu par Alice.
print("Secret calculé par Bob :", secret_bob)  # Affiche le secret obtenu par Bob.


# VÉRIFICATION DE L’ÉGALITÉ DES SECRETS

resultat = "VRAI" if secret_alice == secret_bob else "FAUX"  # Choisit VRAI si les secrets sont égaux, sinon FAUX.
print("Secret partagé identique :", resultat)  # Affiche le résultat de la comparaison.

assert secret_alice == secret_bob  # Déclenche une erreur si les deux secrets sont différents.