#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFT814 - Cryptographie - Devoir 2
Equipe 05 - Script de test

Ce script contient tous les paramètres du Devoir 2 et permet de tester
chaque partie (Diffie-Hellman, RSA textbook, Signatures RSA).
"""

import sys
from math import gcd
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse

# ========================================
# PARAMÈTRES - ÉQUIPE 05
# ========================================

# PARTIE 1 - Diffie-Hellman modulo p = 2^61 - 1
DH_PARAMS = {
    'p': 2305843009213693951,  # 2^61 - 1
    'g': 37,  # racine primitive modulo p
    'x_Alice': 974264167110881,  # clé privée imposée d'Alice
    'y_Bob': 23179607248816,  # clé privée imposée de Bob
    'message': "nouvelle cle generee aujourd hui",
    # Vérifications
    'h_A': 1728559941401253307,
    'h_B': 1512476708919266528,
    'K_trunc': 3512349958,  # K_AB mod 2^32
    'ciphertext_hex': "bf354070b4365963f1395963f13d5068b4285063f13b406cbe2f4762f132406f"
}

# PARTIE 2 - RSA textbook
RSA_PARAMS = {
    'p': 209287069,
    'q': 221536921,
    'e': 65537,
    'm': 1394500914838255,
    "c_prime": 3632978084399643,  # c' à déchiffrer
    # Vérifications
    'd': 42716440715327873,
    'c': 31963660340929498,
    "m_prime": 45361714772588724,
    'c_mal': 35103694930280065,
    'dec_c_mal': 2789001829676510  # doit valoir 2m mod N
}

# PARTIE 3 - Signatures RSA textbook (même clé qu'en partie 2)
SIG_PARAMS = {
    'm1': 23151899524468793,
    'm2': 15034505925449428,
    # Vérifications
    's1': 40495289341296419,
    's2': 4958833821949512,
    'm_cible': 35566973915918092,
    's_cible': 7736092144531737
}


# ========================================
# PARTIE 1 - DIFFIE-HELLMAN
# ========================================

def dh_partie1():
    """Test de la partie 1 - Diffie-Hellman"""
    print("=" * 60)
    print("PARTIE 1 - Diffie-Hellman modulo p = 2^61 - 1")
    print("=" * 60)
    
    p = DH_PARAMS['p']
    g = DH_PARAMS['g']
    x = DH_PARAMS['x_Alice']
    y = DH_PARAMS['y_Bob']
    
    print(f"p = {p} (2^61 - 1)")
    print(f"g = {g}")
    print(f"x_Alice = {x}")
    print(f"y_Bob   = {y}")
    print()
    
    # 1.2 Calcul des clés publiques
    print("1.2) Calcul des clés publiques")
    h_A = pow(g, x, p)
    h_B = pow(g, y, p)
    print(f"h_A = g^x mod p = {h_A}")
    print(f"Vérification: {h_A == DH_PARAMS['h_A']}")
    print(f"h_B = g^y mod p = {h_B}")
    print(f"Vérification: {h_B == DH_PARAMS['h_B']}")
    print()
    
    # Calcul de la clé secrète partagée
    print("Calcul de la clé secrète partagée K_AB")
    K_AB = pow(h_B, x, p)  # côté Alice
    K_AB_bob = pow(h_A, y, p)  # côté Bob
    print(f"K_AB (Alice) = h_B^x mod p = {K_AB}")
    print(f"K_AB (Bob)   = h_A^y mod p = {K_AB_bob}")
    print(f"K_AB identique: {K_AB == K_AB_bob}")
    print()
    
    # 1.2 Troncature modulo 2^32
    print("1.2) Troncature de la clé")
    K_trunc = K_AB % (2**32)
    print(f"K_AB mod 2^32 = {K_trunc}")
    print(f"Vérification: {K_trunc == DH_PARAMS['K_trunc']}")
    print()
    
    # 1.3 Chiffrement XOR
    print("1.3) Chiffrement XOR du message")
    message = DH_PARAMS['message']
    print(f"Message: \"{message}\"")
    print(f"Longueur: {len(message)} octets")
    
    # Convertir message en bytes
    msg_bytes = message.encode('utf-8')
    # Convertir K_trunc en bytes (4 octets little/big endian selon besoin)
    # Utiliser little endian ou big endian - à adapter selon le devoir
    K_bytes = K_trunc.to_bytes(4, byteorder='little')
    print(f"K (4 octets, little endian): {K_bytes.hex()}")
    
    # Chiffrement XOR (répétition de la clé)
    ciphertext_bytes = bytearray()
    for i, b in enumerate(msg_bytes):
        ciphertext_bytes.append(b ^ K_bytes[i % 4])
    
    ciphertext_hex = ciphertext_bytes.hex()
    print(f"Ciphertext (hex): {ciphertext_hex}")
    print(f"Vérification: {ciphertext_hex == DH_PARAMS['ciphertext_hex']}")
    print()
    
    # Déchiffrement
    plaintext_bytes = bytearray()
    for i, b in enumerate(ciphertext_bytes):
        plaintext_bytes.append(b ^ K_bytes[i % 4])
    print(f"Déchiffrement: \"{plaintext_bytes.decode('utf-8')}\"")
    print()


# ========================================
# PARTIE 2 - RSA TEXTBOOK
# ========================================

def rsa_partie2():
    """Test de la partie 2 - RSA textbook"""
    print("=" * 60)
    print("PARTIE 2 - RSA textbook")
    print("=" * 60)
    
    p = RSA_PARAMS['p']
    q = RSA_PARAMS['q']
    e = RSA_PARAMS['e']
    m = RSA_PARAMS['m']
    c_prime = RSA_PARAMS['c_prime']
    
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"e = {e}")
    print(f"m = {m}")
    print(f"c' = {c_prime}")
    print()
    
    # Calcul de N
    N = p * q
    print(f"N = p*q = {N}")
    print()
    
    # 2.1 Calcul de d
    print("2.1) Calcul de l'exposant de dechiffrement d")
    phi_N = (p-1) * (q-1)
    print(f"phi(N) = (p-1)(q-1) = {phi_N}")
    d = pow(e, -1, phi_N)
    print(f"d = e^(-1) mod phi(N) = {d}")
    print(f"Verification: {d == RSA_PARAMS['d']}")
    # Verification alternative
    print(f"e*d mod phi(N) = {(e*d) % phi_N}")
    print()
    
    # 2.2 Chiffrement et déchiffrement
    print("2.2) Chiffrement et déchiffrement")
    c = pow(m, e, N)
    print(f"c = m^e mod N = {c}")
    print(f"Vérification: {c == RSA_PARAMS['c']}")
    
    m_prime = pow(c_prime, d, N)
    print(f"m' = (c')^d mod N = {m_prime}")
    print(f"Vérification: {m_prime == RSA_PARAMS['m_prime']}")
    print()
    
    # 2.4 Propriété multiplicative (homomorphisme)
    print("2.4) Propriété multiplicative de RSA")
    print("Calculons c_mal = c * 2^e mod N et voyons si Dec(c_mal) = 2m mod N")
    c_mal = (c * pow(2, e, N)) % N
    print(f"c_mal = c * 2^e mod N = {c_mal}")
    print(f"Vérification: {c_mal == RSA_PARAMS['c_mal']}")
    
    dec_c_mal = pow(c_mal, d, N)
    print(f"Dec(c_mal) = (c_mal)^d mod N = {dec_c_mal}")
    print(f"Vérification: {dec_c_mal == RSA_PARAMS['dec_c_mal']}")
    
    expected = (2 * m) % N
    print(f"2*m mod N = {expected}")
    print(f"Dec(c_mal) == 2*m mod N: {dec_c_mal == expected}")
    print()
    
    return N, d


# ========================================
# PARTIE 3 - SIGNATURES RSA TEXTBOOK
# ========================================

def rsa_signatures_partie3(N, d, e):
    """Test de la partie 3 - Signatures RSA textbook"""
    print("=" * 60)
    print("PARTIE 3 - Signatures RSA textbook")
    print("=" * 60)
    
    m1 = SIG_PARAMS['m1']
    m2 = SIG_PARAMS['m2']
    
    print(f"m1 = {m1}")
    print(f"m2 = {m2}")
    print(f"N = {N}, d = {d}, e = {e}")
    print()
    
    # 3.2 Génération des signatures
    print("3.2) Génération des signatures")
    s1 = pow(m1, d, N)
    s2 = pow(m2, d, N)
    print(f"s1 = (m1)^d mod N = {s1}")
    print(f"Vérification: {s1 == SIG_PARAMS['s1']}")
    
    s2_calc = pow(m2, d, N)
    print(f"s2 = (m2)^d mod N = {s2_calc}")
    print(f"Vérification: {s2_calc == SIG_PARAMS['s2']}")
    print()
    
    # Vérification des signatures
    print("Vérification: m1 == (s1)^e mod N ?")
    m1_verif = pow(s1, e, N)
    print(f"(s1)^e mod N = {m1_verif}")
    print(f"Vérifie: {m1_verif == m1}")
    print()
    
    # 3.4 Attaque par multiplication
    print("3.4) Attaque par multiplication sur signatures RSA textbook")
    print("Si l'oracle signe m1 et m2, on peut forger une signature pour m1*m2 mod N")
    
    m_cible = (m1 * m2) % N
    s_cible = (s1 * s2_calc) % N
    print(f"m_cible = m1*m2 mod N = {m_cible}")
    print(f"Vérification: {m_cible == SIG_PARAMS['m_cible']}")
    print(f"s_cible = s1*s2 mod N = {s_cible}")
    print(f"Vérification: {s_cible == SIG_PARAMS['s_cible']}")
    print()
    
    # Vérification de la signature forgée
    print("Vérification de la signature forgée:")
    m_cible_verif = pow(s_cible, e, N)
    print(f"(s_cible)^e mod N = {m_cible_verif}")
    print(f"m_cible = {m_cible}")
    print(f"Vérifie = {(s_cible^e) % N == m_cible}")  # Python style
    print(f"Vérifie (correct): {pow(s_cible, e, N) == m_cible}")
    print()


def main():
    """Fonction principale"""
    print("\n" + "=" * 60)
    print("IFT814 - DEVOIR 2 - ÉQUIPE 05")
    print("Tests des parties 1, 2 et 3")
    print("=" * 60 + "\n")
    
    try:
        # Partie 1
        dh_partie1()
        print("\n")
        
        # Partie 2
        N, d = rsa_partie2()
        print("\n")
        
        # Partie 3
        e = RSA_PARAMS['e']
        rsa_signatures_partie3(N, d, e)
        
        print("=" * 60)
        print("Tous les tests terminés avec succès!")
        print("=" * 60)
        
    except Exception as ex:
        print(f"Erreur: {ex}", file=sys.stderr)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
