#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFT814 - Devoir 2 - Equipe 05
Partie 2 : RSA "textbook" (sans padding)

Couvre :
  2.1 Generation de la paire de cles (test de primalite Miller-Rabin,
      calcul de d = e^-1 mod phi(N) par l'algorithme d'Euclide etendu)
  2.2 Chiffrement et dechiffrement
  2.3 Cas limites : Enc(0), Enc(1), Enc(N-1), determinisme
  2.4 Malleabilite (homomorphisme multiplicatif)
  2.5 Attaque par dictionnaire sur un petit espace de messages

Toutes les primitives (exponentiation, primalite, inverse modulaire) sont
implementees a la main. Le seul aleatoire (temoins de Miller-Rabin) utilise
le module `secrets`.
"""

import secrets

# ---------------------------------------------------------------------------
# Parametres imposes par la fiche (Equipe 05)
# ---------------------------------------------------------------------------
P = 209287069
Q = 221536921
E = 65537


# ---------------------------------------------------------------------------
# Exponentiation modulaire rapide
# ---------------------------------------------------------------------------
def pow_mod(a, b, n):
    r, base, e = 1, a % n, b
    while e > 0:
        if e & 1:
            r = (r * base) % n
        base = (base * base) % n
        e >>= 1
    return r


# ---------------------------------------------------------------------------
# Algorithme d'Euclide etendu : renvoie (g, u, v) tel que a*u + b*v = g = pgcd(a,b)
# ---------------------------------------------------------------------------
def euclide_etendu(a, b):
    # Version iterative, en gardant la trace des coefficients de Bezout.
    u_prec, u = 1, 0
    v_prec, v = 0, 1
    r_prec, r = a, b
    while r != 0:
        quotient = r_prec // r
        r_prec, r = r, r_prec - quotient * r
        u_prec, u = u, u_prec - quotient * u
        v_prec, v = v, v_prec - quotient * v
    # a*u_prec + b*v_prec = r_prec = pgcd(a, b)
    return r_prec, u_prec, v_prec


def inverse_mod(a, n):
    """Inverse de a modulo n (necessite pgcd(a, n) = 1)."""
    g, u, _ = euclide_etendu(a % n, n)
    if g != 1:
        raise ValueError(f"{a} n'est pas inversible modulo {n} (pgcd = {g})")
    return u % n


# ---------------------------------------------------------------------------
# 2.1 Test de primalite de Miller-Rabin (probabiliste)
# ---------------------------------------------------------------------------
def miller_rabin(n, nb_temoins=20):
    """
    Test probabiliste. Principe : si n est premier impair, alors pour tout a
    dans [2, n-2] on a a^(n-1) = 1 mod n (petit theoreme de Fermat), et en
    ecrivant n-1 = 2^s * d (d impair), la suite a^d, a^(2d), ... atteint 1
    uniquement via la valeur -1 (les seules racines carrees de 1 modulo un
    premier sont +/-1). Si une seule de ces conditions echoue pour un temoin a,
    n est COMPOSE avec certitude. Si elle tient pour k temoins aleatoires, n
    est premier avec une probabilite d'erreur <= 4^-k.
    """
    if n < 2:
        return False
    # Petits premiers : elimination rapide des cas evidents.
    for petit in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == petit:
            return True
        if n % petit == 0:
            return False
    # Ecriture n - 1 = 2^s * d avec d impair.
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # Boucle sur les temoins aleatoires.
    for _ in range(nb_temoins):
        a = 2 + secrets.randbelow(n - 3)      # temoin dans [2, n-2]
        x = pow_mod(a, d, n)
        if x == 1 or x == n - 1:
            continue                           # a ne revele rien, on passe
        compose = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                compose = False                # on a trouve -1 : OK pour ce a
                break
        if compose:
            return False                       # a est un temoin de compositude
    return True


# ---------------------------------------------------------------------------
# 2.1 Generation / verification de la cle
# ---------------------------------------------------------------------------
def generer_cle(p=P, q=Q, e=E):
    """Renvoie (N, phi, e, d) a partir de p, q premiers."""
    assert miller_rabin(p), "p n'est pas premier"
    assert miller_rabin(q), "q n'est pas premier"
    N = p * q
    phi = (p - 1) * (q - 1)
    g, _, _ = euclide_etendu(e, phi)
    assert g == 1, "e et phi(N) ne sont pas premiers entre eux"
    d = inverse_mod(e, phi)
    return N, phi, e, d


# ---------------------------------------------------------------------------
# 2.2 Chiffrement / dechiffrement RSA textbook
# ---------------------------------------------------------------------------
def rsa_enc(m, e, N):
    return pow_mod(m, e, N)


def rsa_dec(c, d, N):
    return pow_mod(c, d, N)


# ===========================================================================
# Demonstrations
# ===========================================================================
def demo_2_1():
    print("=" * 70)
    print("2.1  Generation de la paire de cles")
    print("=" * 70)
    print(f"  p = {P}  premier (Miller-Rabin) ? {miller_rabin(P)}")
    print(f"  q = {Q}  premier (Miller-Rabin) ? {miller_rabin(Q)}")
    N, phi, e, d = generer_cle()
    print(f"  N = p*q = {N}")
    print(f"  phi(N) = (p-1)(q-1) = {phi}")
    print(f"  e = {e}  ;  pgcd(e, phi) = {euclide_etendu(e, phi)[0]}")
    print(f"  d = e^-1 mod phi(N) = {d}")
    print(f"      [Verification 2.1 attendue] 42716440715327873")
    # Controle : e*d = 1 mod phi
    print(f"  controle e*d mod phi = {(e * d) % phi} (doit valoir 1)")
    print()
    return N, phi, e, d


def demo_2_2(N, e, d):
    print("=" * 70)
    print("2.2  Chiffrement et dechiffrement")
    print("=" * 70)
    m = 1394500914838255
    c = rsa_enc(m, e, N)
    print(f"  m = {m}")
    print(f"  c = m^e mod N = {c}")
    print(f"      [Verification 2.2 attendue] 31963660340929498")
    print(f"  controle Dec(Enc(m)) = {rsa_dec(c, d, N)} (doit valoir m : "
          f"{rsa_dec(c, d, N) == m})")
    c_prime = 3632978084399643
    m_prime = rsa_dec(c_prime, d, N)
    print(f"  c' (impose) = {c_prime}")
    print(f"  m' = Dec(c') = c'^d mod N = {m_prime}")
    print(f"      [Verification 2.2 attendue] 45361714772588724")
    print()
    return m, c


def demo_2_3(N, e, d):
    print("=" * 70)
    print("2.3  Cas limites et determinisme")
    print("=" * 70)
    for m in (0, 1, N - 1):
        c = rsa_enc(m, e, N)
        etiquette = {0: "Enc(0)", 1: "Enc(1)", N - 1: "Enc(N-1)"}[m]
        print(f"  {etiquette:9s} = {c}")
    print("  --> Enc(0)=0, Enc(1)=1, Enc(N-1)=N-1 : ces clairs sont points")
    print("      fixes de l'exponentiation. Un attaquant RECONNAIT le clair")
    print("      directement, sans aucune cryptanalyse.")
    print("  --> RSA textbook est DETERMINISTE : m identique => c identique.")
    print("      Deux cryptogrammes egaux trahissent deux clairs egaux.")
    print()


def demo_2_4(N, e, d, m, c):
    print("=" * 70)
    print("2.4  Malleabilite (homomorphisme multiplicatif)")
    print("=" * 70)
    # c_mal = c * 2^e mod N = Enc(m) * Enc(2) = Enc(2m mod N), sans connaitre m.
    c_mal = (c * pow_mod(2, e, N)) % N
    print(f"  c_mal = c * 2^e mod N = {c_mal}")
    print(f"      [Verification 2.4 attendue] 35103694930280065")
    dec_cmal = rsa_dec(c_mal, d, N)
    print(f"  Dec(c_mal) = {dec_cmal}")
    print(f"      [Verification 2.4 attendue] 2789001829676510")
    print(f"  2m mod N   = {(2 * m) % N}  (egal a Dec(c_mal) : "
          f"{dec_cmal == (2 * m) % N})")
    print("  --> En multipliant le chiffre par 2^e, on obtient le chiffre de 2m")
    print("      SANS connaitre m ni d : RSA textbook est malleable.")
    print()


def demo_2_5(N, e, c):
    print("=" * 70)
    print("2.5  Attaque par dictionnaire (petit espace de messages)")
    print("=" * 70)
    # Scenario : l'attaquant sait que m est un "montant" plausible dans un petit
    # ensemble. On construit >= 1000 candidats incluant la vraie valeur m.
    m_vrai = 1394500914838255
    # On fabrique 1000 candidats "plausibles" autour de la vraie valeur.
    candidats = [m_vrai + delta for delta in range(-499, 501)]  # 1000 valeurs
    print(f"  Taille du dictionnaire : {len(candidats)} candidats")
    print(f"  (il inclut la vraie valeur m = {m_vrai})")
    essais = 0
    trouve = None
    for cand in candidats:
        essais += 1
        if rsa_enc(cand, e, N) == c:      # on chiffre et on compare au c intercepte
            trouve = cand
            break
    print(f"  Cryptogramme intercepte c = {c}")
    print(f"  --> m retrouve = {trouve}  en {essais} essais")
    print(f"      (correct : {trouve == m_vrai})")
    print("  Comme RSA textbook est deterministe et sans aleatoire, chiffrer")
    print("  chaque candidat et comparer a c suffit a identifier le bon clair.")
    print()


if __name__ == "__main__":
    N, phi, e, d = demo_2_1()
    m, c = demo_2_2(N, e, d)
    demo_2_3(N, e, d)
    demo_2_4(N, e, d, m, c)
    demo_2_5(N, e, c)
