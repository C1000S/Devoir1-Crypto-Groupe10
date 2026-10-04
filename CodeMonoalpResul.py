# ============================================================
# PI_SUB : CHIFFREMENT PAR SUBSTITUTION MONO-ALPHABETIQUE
# ============================================================

# Alphabet utilisé
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


# ============================================================
# CRYPTOGRAMME DE DEPART
# ============================================================

C_original = (
    "YAOEJGYAGGJABWAGWAGHAKAFIEXAPWAGYJOWDRIPAGBTAFBTAKPIPFIKGRAPPFAW"
    "AEFGDFYFAGGIKGZEAWAKKARJOEJGGAWAGWJFAEKOFDPDBDWAYABTIKHAYABWAGO"
    "AFRAPIYAEXOAFGDKKAGYABDKSAKJFYEKGABFAPBDRREKAKOIFWIKPYASIKPPDEP"
    "WARDKYAEKDFYJKIPAEFZEIKPJZEAGECCJGIRRAKPOEJGGIKPODEFFIJPBIGGAFOW"
    "EGJAEFGGQGPARAGYABTJCCFARAKPEPJWJGAGIEUDEFYTEJGEFJKPAFKAPWAGAWAS"
    "AGDKPRIFBTAUEGZEIEGDRRAPYAWIBDWWJKAODEFDVGAFSAFWABDEBTAFYEGDWAJ"
    "WGEFPDEPAWIFAHJDK"
).lower()


# ============================================================
# TEXTE CLAIR RETROUVE
# ============================================================

M = (
    "depuisdessiecleslesgenerauxetlesdiplomatescherchentatransmettre"
    "leursordressansquelennemipuisseleslireunprotocoledechangedecles"
    "permetadeuxpersonnesdeconvenirdunsecretcommunenparlantdevanttout"
    "lemondeunordinateurquantiquesuffisammentpuissantpourraitcasser"
    "plusieurssystemesdechiffrementutilisesaujourdhuisurinternetles"
    "elevesontmarchejusquausommetdelacollinepourobserverlecoucherdu"
    "soleilsurtoutelaregion"
)


# ============================================================
# CLE COMPLETE
# ============================================================

# La position de chaque lettre de la clé correspond à :
#
# alphabet : abcdefghijklmnopqrstuvwxyz
# clé      : ivbyachtjulwrkdozfgpesmxqn
#
# Exemple :
# a -> i
# b -> v
# c -> b
# d -> y
# e -> a
# etc.

k = "ivbyachtjulwrkdozfgpesmxqn"


# ============================================================
# E3 : CHIFFREMENT
# ============================================================

def E3(M, k):

    # Chaîne vide qui contiendra le cryptogramme
    C = ""

    # Parcourt chaque lettre du message clair
    for lettre in M:

        # Cherche la position de la lettre
        # dans l'alphabet.
        position = ALPHABET.index(lettre)

        # Prend la lettre située à la même
        # position dans la clé.
        lettre_chiffree = k[position]

        # Ajoute cette lettre au cryptogramme
        C += lettre_chiffree

    # Retourne le cryptogramme
    return C


# ============================================================
# D3 : DECHIFFREMENT
# ============================================================

def D3(C, k):

    # Création d'une permutation inverse
    inverse = [''] * 26

    # Construction de la clé inverse
    for i in range(26):

        # Exemple :
        # si a -> i
        # alors i -> a dans la clé inverse

        position = ALPHABET.index(k[i])

        inverse[position] = ALPHABET[i]

    # Transformation de la liste en chaîne
    inverse = ''.join(inverse)

    # Message clair vide
    M = ""

    # Parcourt chaque lettre du cryptogramme
    for lettre in C:

        # Position de la lettre chiffrée
        position = ALPHABET.index(lettre)

        # Recherche de la lettre claire
        M += inverse[position]

    # Retourne le message clair
    return M


# ============================================================
# AFFICHAGE DE LA CLE
# ============================================================

print("=" * 60)
print("CLE DE SUBSTITUTION")
print("=" * 60)

print("Alphabet :", ALPHABET)
print("Clé k    :", k)

print("\nCorrespondances :")

for i in range(26):
    print(ALPHABET[i], "->", k[i])


# ============================================================
# VERIFICATION DES LONGUEURS
# ============================================================

print("\n" + "=" * 60)
print("VERIFICATION DES LONGUEURS")
print("=" * 60)

print("Longueur du texte clair :", len(M))

print(
    "Longueur du cryptogramme :",
    len(C_original)
)


# ============================================================
# CHIFFREMENT DU TEXTE CLAIR
# ============================================================

C_calcule = E3(M, k)


print("\n" + "=" * 60)
print("CHIFFREMENT AVEC E3")
print("=" * 60)

print("\nTexte clair :")
print(M)

print("\nCryptogramme calculé :")
print(C_calcule)


# ============================================================
# COMPARAISON AVEC LE CRYPTOGRAMME ORIGINAL
# ============================================================

print("\n" + "=" * 60)
print("VERIFICATION DU CRYPTOGRAMME")
print("=" * 60)

print("\nCryptogramme original :")
print(C_original)

print("\nCryptogramme calculé :")
print(C_calcule)


# Comparaison caractère par caractère
verification = (C_calcule == C_original)


print("\nE3(k, texte clair) == cryptogramme original ?")

print(verification)


# ============================================================
# DECHIFFREMENT AVEC D3
# ============================================================

M_dechiffre = D3(C_original, k)


print("\n" + "=" * 60)
print("DECHIFFREMENT AVEC D3")
print("=" * 60)

print("\nTexte déchiffré :")

print(M_dechiffre)


# ============================================================
# VERIFICATION DU DECHIFFREMENT
# ============================================================

print("\nD3(k, cryptogramme) == texte clair ?")

print(M_dechiffre == M)


# ============================================================
# RESULTAT FINAL
# ============================================================

print("\n" + "=" * 60)
print("RESULTAT FINAL")
print("=" * 60)

if C_calcule == C_original and M_dechiffre == M:

    print("SUCCES")
    print("Le chiffrement et le déchiffrement sont corrects.")

else:

    print("ERREUR")
    print("Les résultats ne correspondent pas.")