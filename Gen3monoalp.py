# Importe le module "secrets".
# Ce module permet de générer des nombres aléatoires
# de manière sécurisée, ce qui est adapté à la cryptographie.
import secrets


# Définit l'alphabet utilisé par notre chiffrement.
# Ici, on travaille uniquement avec les 26 lettres minuscules
# de a à z.
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


# ============================================================
# Gen3 : génération aléatoire d'une clé de substitution
# ============================================================

# Définition de la fonction Gen3().
# Cette fonction va générer une clé de substitution aléatoire.
def Gen3():

    # Transforme la chaîne ALPHABET en une liste de caractères.
    #
    # Exemple :
    # ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    #
    # devient :
    # ['a', 'b', 'c', 'd', ..., 'z']
    #
    # Une liste est utilisée parce qu'on va mélanger
    # les lettres à l'intérieur.
    k = list(ALPHABET)


    # ========================================================
    # Mélange de Fisher-Yates
    # ========================================================

    # La boucle parcourt la liste de la dernière position
    # jusqu'à la deuxième position.
    #
    # len(k) vaut 26, donc :
    # range(25, 0, -1)
    #
    # signifie que i prendra successivement les valeurs :
    # 25, 24, 23, ..., 2, 1
    for i in range(len(k) - 1, 0, -1):

        # Génère un nombre aléatoire j compris entre 0 et i inclus.
        #
        # randbelow(i + 1) donne :
        # 0 <= j < i + 1
        #
        # donc :
        # 0 <= j <= i
        #
        # Le module "secrets" utilise une source d'aléatoire
        # adaptée aux applications cryptographiques.
        j = secrets.randbelow(i + 1)


        # Échange les deux lettres situées aux positions i et j.
        #
        # Exemple :
        # si k[i] = 'z' et k[j] = 'c',
        # après l'échange :
        # k[i] = 'c' et k[j] = 'z'
        #
        # Cette opération permet de mélanger progressivement
        # toutes les lettres de l'alphabet.
        k[i], k[j] = k[j], k[i]


    # Transforme la liste mélangée en une chaîne de caractères.
    #
    # Exemple :
    # ['q', 'w', 'e', ..., 'a']
    #
    # devient :
    # "qwe...a"
    #
    # La chaîne obtenue représente la clé de substitution k.
    return ''.join(k)
    # Appel de la fonction Gen3 et affichage de la clé
print(Gen3())