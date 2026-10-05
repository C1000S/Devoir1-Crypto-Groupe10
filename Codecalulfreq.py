
# On importe Counter depuis le module collections.
# Counter permet de compter automatiquement le nombre d'apparitions
# de chaque élément dans une chaîne de caractères.
from collections import Counter


# ============================================================
# CRYPTOGRAMME
# ============================================================

# On place le cryptogramme dans une variable appelée C.
# Les triples guillemets permettent d'écrire une longue chaîne
# de caractères sur une seule variable.
C = """YAOEJGYAGGJABWAGWAGHAKAFIEXAPWAGYJOWDRIPAGBTAFBTAKPIPFIKGRAPPFAWAEFGDFYFAGGIKGZEAWAKKARJOEJGGAWAGWJFAEKOFDPDBDWAYABTIKHAYABWAGOAFRAPIYAEXOAFGDKKAGYABDKSAKJFYEKGABFAPBDRREKAKOIFWIKPYASIKPPDEPWARDKYAEKDFYJKIPAEFZEIKPJZEAGECCJGIRRAKPOEJGGIKPODEFFIJPBIGGAFOWEGJAEFGGQGPARAGYABTJCCFARAKPEPJWJGAGIEUDEFYTEJGEFJKPAFKAPWAGAWASAGDKPRIFBTAUEGZEIEGDRRAPYAWIBDWWJKAODEFDVGAFSAFWABDEBTAFYEGDWAJWGEFPDEPAWIFAHJDK"""


# ============================================================
# 1. LONGUEUR
# ============================================================

# len(C) calcule le nombre total de caractères contenus dans C.
# print() affiche le résultat à l'écran.
print("Longueur :", len(C))


# ============================================================
# 2. FREQUENCE DES LETTRES
# ============================================================

# Counter(C) compte combien de fois chaque lettre apparaît
# dans le cryptogramme.
# Exemple : si A apparaît 50 fois, Counter enregistrera A : 50.
freq_lettres = Counter(C)

# On affiche un titre pour identifier cette partie du programme.
# \n permet de faire un retour à la ligne avant le titre.
print("\n=== FREQUENCE DES LETTRES ===")

# most_common() trie les lettres de la plus fréquente
# à la moins fréquente.
#
# La boucle récupère deux informations :
# - lettre : la lettre étudiée
# - nombre : le nombre de fois où elle apparaît
for lettre, nombre in freq_lettres.most_common():

    # On calcule le pourcentage d'apparition de la lettre.
    #
    # nombre = nombre d'apparitions de la lettre
    # len(C) = nombre total de lettres
    #
    # Exemple :
    # 50 / 398 * 100 = 12,56 %
    pourcentage = nombre / len(C) * 100

    # On affiche :
    # - la lettre
    # - son nombre d'occurrences
    # - son pourcentage
    #
    # round(pourcentage, 2) arrondit le résultat
    # à deux chiffres après la virgule.
    print(
        lettre,
        ":", nombre,
        "occurrences -",
        round(pourcentage, 2),
        "%"
    )


# ============================================================
# 3. FREQUENCE DES BIGRAMMES
# ============================================================

# On crée une liste vide appelée bigrammes.
# Cette liste servira à stocker toutes les paires
# de lettres consécutives du cryptogramme.
bigrammes = []

# On parcourt le cryptogramme caractère par caractère.
#
# len(C) - 1 est utilisé parce qu'un bigramme contient
# toujours deux lettres.
#
# Exemple :
# C = ABCDE
#
# i = 0 -> AB
# i = 1 -> BC
# i = 2 -> CD
# i = 3 -> DE
for i in range(len(C) - 1):

    # C[i:i+2] récupère deux caractères consécutifs
    # à partir de la position i.
    #
    # Exemple :
    # si i = 0, C[0:2] donne les deux premières lettres.
    bigramme = C[i:i+2]

    # On ajoute le bigramme obtenu dans la liste.
    bigrammes.append(bigramme)


# On compte combien de fois chaque bigramme apparaît.
# Counter va produire quelque chose comme :
# GA : 25
# AG : 20
# KA : 18
# etc.
freq_bigrammes = Counter(bigrammes)

# On affiche le titre de cette partie.
print("\n=== BIGRAMMES ===")

# most_common(20) sélectionne les 20 bigrammes
# les plus fréquents.
#
# Pour chaque bigramme, on récupère :
# - bigramme : les deux lettres
# - nombre : le nombre d'apparitions
for bigramme, nombre in freq_bigrammes.most_common(20):

    # On affiche le bigramme et son nombre d'apparitions.
    print(bigramme, ":", nombre)


# ============================================================
# 4. DECHIFFREMENT PARTIEL
# ============================================================

# On crée une première partie de la clé de substitution.
#
# Cela signifie que l'on suppose :
#
# A dans le cryptogramme -> E dans le texte clair
# G dans le cryptogramme -> A dans le texte clair
# E dans le cryptogramme -> S dans le texte clair
# F dans le cryptogramme -> I dans le texte clair
# K dans le cryptogramme -> T dans le texte clair
#
# Ces correspondances sont des hypothèses obtenues
# notamment grâce à l'analyse fréquentielle.
cle_partielle = {
    'A': 'E',
    'G': 'A',
    'E': 'S',
    'F': 'I',
    'K': 'T'
}


# On crée une chaîne vide.
# Elle servira à construire progressivement
# le texte déchiffré.
texte_partiel = ""


# On parcourt chaque lettre du cryptogramme C.
#
# Exemple :
# si C commence par YAOE...
# la boucle traite successivement :
# Y
# A
# O
# E
# ...
for lettre in C:

    # On vérifie si la lettre actuelle possède
    # une correspondance dans notre clé partielle.
    if lettre in cle_partielle:

        # Si la lettre existe dans la clé,
        # on ajoute la lettre claire correspondante
        # à texte_partiel.
        #
        # Exemple :
        # lettre = A
        # cle_partielle['A'] = E
        #
        # On ajoute donc E au texte.
        texte_partiel += cle_partielle[lettre]

    # Si la lettre n'est pas encore connue
    # dans notre clé partielle...
    else:

        # ...on ajoute "_" à la place.
        #
        # Le "_" signifie :
        # "Nous ne connaissons pas encore cette lettre."
        texte_partiel += "_"


# On affiche un titre pour le résultat.
print("\n=== TEXTE PARTIEL ===")

# On affiche le texte obtenu après remplacement
# des lettres dont nous connaissons déjà la correspondance.
print(texte_partiel)
