#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFT814 - Devoir 2 - Equipe 05
Partie 1 : Diffie-Hellman modulo p = 2^61 - 1 (nombre premier de Mersenne)

Couvre :
  1.1 Implementation du protocole (Gen, PubKey, Secret) + exemple complet
  1.2 Trace avec les cles imposees de la fiche
  1.3 Chiffrement par flot XOR avec la cle derivee (K tronque a 32 bits)

Aucune bibliotheque de chiffrement n'est utilisee : l'exponentiation modulaire
est implementee a la main par "carre-et-multiplication". Le seul tirage
aleatoire (1.1) utilise le module `secrets` (generateur cryptographiquement sur).
"""

import secrets

# ---------------------------------------------------------------------------
# Parametres publics (identiques pour toute la classe, voir la fiche)
# ---------------------------------------------------------------------------
P = 2**61 - 1              # = 2305843009213693951, premier de Mersenne
G = 37                     # racine primitive modulo P (ordre multiplicatif = P-1)


# ---------------------------------------------------------------------------
# Exponentiation modulaire rapide : a^b mod n (carre-et-multiplication)
# Complexite : O(log b) multiplications, au lieu de O(b) pour la methode naive.
# ---------------------------------------------------------------------------
def pow_mod(a, b, n):
    """Retourne a^b mod n sans jamais manipuler a^b en entier."""
    resultat = 1
    base = a % n
    exposant = b
    while exposant > 0:
        if exposant & 1:            # bit de poids faible a 1 -> on multiplie
            resultat = (resultat * base) % n
        base = (base * base) % n     # on met la base au carre a chaque etape
        exposant >>= 1               # on passe au bit suivant
    return resultat


# ---------------------------------------------------------------------------
# 1.1 Le protocole Diffie-Hellman
# ---------------------------------------------------------------------------
def gen(p=P):
    """Choisit un exposant prive aleatoire dans {2, ..., p-2} (generateur sur)."""
    # secrets.randbelow(n) renvoie un entier uniforme dans [0, n-1].
    # On veut [2, p-2] : on tire dans [0, p-4] puis on decale de 2.
    return 2 + secrets.randbelow(p - 3)


def pub_key(x, g=G, p=P):
    """Demi-cle publique : h = g^x mod p."""
    return pow_mod(g, x, p)


def secret(cle_privee, cle_publique_recue, p=P):
    """Secret partage : (cle_publique_recue)^(cle_privee) mod p."""
    return pow_mod(cle_publique_recue, cle_privee, p)


# ---------------------------------------------------------------------------
# 1.3 Chiffrement par flot XOR avec la cle derivee
# ---------------------------------------------------------------------------
def cle_flot_depuis_secret(K, nb_octets=4):
    """Tronque le secret K a 32 bits et le represente sur 4 octets big-endian."""
    K32 = K % (2**32)                       # troncature a 32 bits
    return K32.to_bytes(nb_octets, 'big')   # representation "big-endian"/boutisme


def chiffrer_xor(message_bytes, cle_bytes):
    """c[i] = m[i] XOR cle[i mod len(cle)], octet par octet."""
    k = len(cle_bytes)
    return bytes(message_bytes[i] ^ cle_bytes[i % k] for i in range(len(message_bytes)))


# Le XOR est involutif : dechiffrer = rechiffrer avec la meme cle.
def dechiffrer_xor(cipher_bytes, cle_bytes):
    return chiffrer_xor(cipher_bytes, cle_bytes)


# ===========================================================================
# Demonstrations
# ===========================================================================
def demo_1_1():
    print("=" * 70)
    print("1.1  Exemple d'execution complet (cles aleatoires choisies par le code)")
    print("=" * 70)
    # Alice et Bob tirent chacun une cle privee aleatoire.
    a = gen()
    b = gen()
    hA = pub_key(a)          # Alice publie h_A = g^a
    hB = pub_key(b)          # Bob   publie h_B = g^b
    # Chacun calcule le secret a partir de la demi-cle recue.
    K_alice = secret(a, hB)  # (h_B)^a
    K_bob   = secret(b, hA)  # (h_A)^b
    print(f"  cle privee Alice a = {a}")
    print(f"  cle privee Bob   b = {b}")
    print(f"  h_A = g^a mod p = {hA}")
    print(f"  h_B = g^b mod p = {hB}")
    print(f"  secret cote Alice = {K_alice}")
    print(f"  secret cote Bob   = {K_bob}")
    print(f"  --> les deux secrets coincident ? {K_alice == K_bob}")
    print()


def demo_1_2():
    print("=" * 70)
    print("1.2  Trace avec les cles imposees de la fiche (Equipe 05)")
    print("=" * 70)
    x = 974264167110881       # cle privee imposee d'Alice
    y = 23179607248816        # cle privee imposee de Bob
    hA = pub_key(x)
    hB = pub_key(y)
    K = secret(x, hB)         # = h_B^x
    K_bis = secret(y, hA)     # = h_A^y (doit etre egal)
    print(f"  x = {x}")
    print(f"  y = {y}")
    print(f"  h_A = g^x mod p = {hA}")
    print(f"      [Verification 1.2 attendue] 1728559941401253307")
    print(f"  h_B = g^y mod p = {hB}")
    print(f"      [Verification 1.2 attendue] 1512476708919266528")
    print(f"  K = h_B^x = h_A^y mod p = {K}  (coherence : {K == K_bis})")
    print(f"  K mod 2^32 = {K % (2**32)}")
    print(f"      [Verification 1.2 attendue] 3512349958")
    print()
    return K


def demo_1_3(K):
    print("=" * 70)
    print("1.3  Chiffrement par flot XOR du message de la fiche")
    print("=" * 70)
    message = "nouvelle cle generee aujourd hui"
    m_bytes = message.encode('ascii')
    cle = cle_flot_depuis_secret(K)       # K tronque a 32 bits -> 4 octets big-endian
    c_bytes = chiffrer_xor(m_bytes, cle)
    print(f"  message clair        : {message!r}")
    print(f"  cle (K mod 2^32) hex : {cle.hex()}")
    print(f"  chiffre (hex)        : {c_bytes.hex()}")
    print(f"      [Verification 1.3 attendue]"
          f" bf354070b4365963f1395963f13d5068b4285063f13b406cbe2f4762f132406f")
    # Verification du dechiffrement (doit redonner le clair)
    clair = dechiffrer_xor(c_bytes, cle).decode('ascii')
    print(f"  dechiffre            : {clair!r}  (identique : {clair == message})")
    print()


if __name__ == "__main__":
    print(f"p = 2^61 - 1 = {P}")
    print(f"g = {G}\n")
    demo_1_1()
    K = demo_1_2()
    demo_1_3(K)
