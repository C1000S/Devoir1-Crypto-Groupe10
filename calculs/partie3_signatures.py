#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFT814 - Devoir 2 - Equipe 05
Partie 3 : Signatures RSA "textbook" (meme cle (N, e, d) qu'en Partie 2)

  Sign(sk, m)   = m^d mod N
  Verify(pk, m, s) accepte si  s^e mod N == m

Couvre :
  3.1 Implementation de Sign / Verify + test (dont rejet si le message change)
  3.2 Oracle de signature simule + signatures imposees de la fiche
  3.3 Forgerie existentielle (sans oracle, sans d)
  3.4 Forgerie par message choisi (forgerie multiplicative) + preuve

Primitives implementees a la main, aleatoire via `secrets`.
"""

import secrets

# ---------------------------------------------------------------------------
# Cle de la Partie 2 (recalculee ici pour que le fichier soit autonome)
# ---------------------------------------------------------------------------
P = 209287069
Q = 221536921
E = 65537


def pow_mod(a, b, n):
    r, base, e = 1, a % n, b
    while e > 0:
        if e & 1:
            r = (r * base) % n
        base = (base * base) % n
        e >>= 1
    return r


def euclide_etendu(a, b):
    u_prec, u = 1, 0
    v_prec, v = 0, 1
    r_prec, r = a, b
    while r != 0:
        q = r_prec // r
        r_prec, r = r, r_prec - q * r
        u_prec, u = u, u_prec - q * u
        v_prec, v = v, v_prec - q * v
    return r_prec, u_prec, v_prec


def inverse_mod(a, n):
    g, u, _ = euclide_etendu(a % n, n)
    if g != 1:
        raise ValueError("non inversible")
    return u % n


N = P * Q
PHI = (P - 1) * (Q - 1)
D = inverse_mod(E, PHI)


# ---------------------------------------------------------------------------
# 3.1 Signature et verification
# ---------------------------------------------------------------------------
def sign(m, d=D, N=N):
    """Signature RSA textbook : s = m^d mod N (utilise la cle privee d)."""
    return pow_mod(m, d, N)


def verify(m, s, e=E, N=N):
    """Verification : accepte si s^e mod N == m (n'utilise que la cle publique)."""
    return pow_mod(s, e, N) == (m % N)


# ---------------------------------------------------------------------------
# 3.2 Oracle de signature simule
# ---------------------------------------------------------------------------
class OracleSignature:
    """
    Simule un signataire legitime. L'attaquant peut lui soumettre un message
    et recevoir la signature, mais n'apprend jamais d. On journalise les
    requetes pour pouvoir verifier qu'on n'a PAS interroge l'oracle sur la
    cible (contrainte de la question 3.4).
    """
    def __init__(self, d, N):
        self._d = d          # cle privee, "en coulisses", invisible pour l'attaquant
        self._N = N
        self.journal = []    # historique des messages soumis

    def demander_signature(self, m):
        self.journal.append(m)
        return pow_mod(m, self._d, self._N)


# ===========================================================================
# Demonstrations
# ===========================================================================
def demo_3_1():
    print("=" * 70)
    print("3.1  Implementation de Sign / Verify")
    print("=" * 70)
    for m in (123456789, 987654321987654):
        s = sign(m)
        print(f"  m = {m}")
        print(f"    s = Sign(m) = {s}")
        print(f"    Verify(m, s)        = {verify(m, s)}  (doit etre True)")
        # On modifie le message d'un seul bit (XOR 1 sur le bit de poids faible).
        m_altere = m ^ 1
        print(f"    Verify(m^1, s)      = {verify(m_altere, s)}  (doit etre False)")
    print()


def demo_3_2():
    print("=" * 70)
    print("3.2  Oracle de signature simule + signatures imposees")
    print("=" * 70)
    oracle = OracleSignature(D, N)
    m1 = 23151899524468793
    m2 = 15034505925449428
    s1 = oracle.demander_signature(m1)
    s2 = oracle.demander_signature(m2)
    print(f"  m1 = {m1}")
    print(f"  s1 = Sign(m1) = {s1}")
    print(f"      [Verification 3.2 attendue] 40495289341296419")
    print(f"      Verify(m1, s1) = {verify(m1, s1)}")
    print(f"  m2 = {m2}")
    print(f"  s2 = Sign(m2) = {s2}")
    print(f"      [Verification 3.2 attendue] 4958833821949512")
    print(f"      Verify(m2, s2) = {verify(m2, s2)}")
    print()
    return oracle, m1, m2, s1, s2


def demo_3_3():
    print("=" * 70)
    print("3.3  Forgerie existentielle (sans oracle, sans d)")
    print("=" * 70)
    # On choisit d'abord une signature s au hasard, PUIS on en deduit le message.
    s = 2 + secrets.randbelow(N - 3)
    m = pow_mod(s, E, N)          # m = s^e mod N  =>  Verify(m, s) vrai par construction
    print(f"  signature choisie au hasard s = {s}")
    print(f"  message deduit m = s^e mod N  = {m}")
    print(f"  Verify(m, s) = {verify(m, s)}  (toujours True)")
    print("  --> La paire (m, s) est valide, mais m n'est pas choisi par")
    print("      l'attaquant : c'est un entier quasi aleatoire. L'attaque est")
    print("      donc peu dangereuse si le protocole n'accepte que des messages")
    print("      STRUCTURES (format, hachage), ce que l'attaquant ne controle pas.")
    print()


def demo_3_4(oracle, m1, m2, s1, s2):
    print("=" * 70)
    print("3.4  Forgerie par message choisi (forgerie multiplicative)")
    print("=" * 70)
    # Cible : m_cible = m1 * m2 mod N. On NE demande PAS sa signature a l'oracle.
    m_cible = (m1 * m2) % N
    s_cible = (s1 * s2) % N       # s_cible = s1 * s2 mod N
    print(f"  m_cible = m1*m2 mod N = {m_cible}")
    print(f"      [Verification 3.4 attendue] 35566973915918092")
    print(f"  s_cible = s1*s2 mod N = {s_cible}")
    print(f"      [Verification 3.4 attendue] 7736092144531737")
    print(f"  Verify(m_cible, s_cible) = {verify(m_cible, s_cible)}  (doit etre True)")
    # Preuve qu'on n'a jamais soumis m_cible a l'oracle.
    print(f"  m_cible a-t-il ete soumis a l'oracle ? "
          f"{m_cible in oracle.journal}  (doit etre False)")
    print("\n  Preuve algebrique :")
    print("    s_cible^e = (s1*s2)^e = s1^e * s2^e  (mod N)")
    print("             = m1 * m2                   (car Verify(s1)=m1, Verify(s2)=m2)")
    print("             = m_cible                   (mod N)")
    print("    donc Verify(m_cible, s_cible) = 1, sans jamais signer m_cible.")
    print()


if __name__ == "__main__":
    print(f"N = {N}\ne = {E}\n")
    demo_3_1()
    oracle, m1, m2, s1, s2 = demo_3_2()
    demo_3_3()
    demo_3_4(oracle, m1, m2, s1, s2)
