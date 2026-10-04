# Importation du module random afin de générer plusieurs nombres aléatoires
import random

# Definition de l'alphabet que notre chiffrement va utiliser
# La position de 'a' est 0, 'b' est 1, ..., 'z' est 25
lettres = "abcdefghijklmnopqrstuvwxyz"


# ============================================================
# Gen1 : génération de la clé
# ============================================================

# On définit la fonction Gen1 qui va générer une clé
def Gen1():

    # On choisit au hasard un nombre entre 0 et 25
    # Ce nombre sera notre première clé k1
    k1 = random.randrange(26)

    # On choisit au hasard un deuxième nombre entre 0 et 25
    # Ce nombre sera notre deuxième clé k2
    k2 = random.randrange(26)

    # On retourne la clé sous forme d'un couple (k1, k2)
    return (k1, k2)

#Execution de Gen1
k = Gen1()
print("Cle generé :",k)
