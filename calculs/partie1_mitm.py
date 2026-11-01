#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFT814 - Devoir 2 - Equipe 05
Partie 1.5 : Attaque de l'homme du milieu (Man-In-The-Middle) sur Diffie-Hellman
             NON authentifie.

Trois entites logicielles (Alice, Bob, Mallory). Mallory controle le canal :
il intercepte les deux demi-cles publiques et negocie SEPAREMENT un secret
avec Alice (K_A) et un autre avec Bob (K_B). Il peut donc dechiffrer, lire,
modifier, puis re-chiffrer tout message qui transite, sans qu'Alice ni Bob
ne s'en apercoive.

On reutilise le chiffrement par flot XOR de la question 1.3.
"""

import secrets

P = 2**61 - 1
G = 37


def pow_mod(a, b, n):
    """a^b mod n par carre-et-multiplication."""
    r, base, e = 1, a % n, b
    while e > 0:
        if e & 1:
            r = (r * base) % n
        base = (base * base) % n
        e >>= 1
    return r


def gen():
    return 2 + secrets.randbelow(P - 3)


def cle_flot(K):
    """K tronque a 32 bits -> 4 octets big-endian (comme en 1.3)."""
    return (K % (2**32)).to_bytes(4, 'big')


def xor(data, cle):
    return bytes(data[i] ^ cle[i % len(cle)] for i in range(len(data)))


# ---------------------------------------------------------------------------
# Les trois entites
# ---------------------------------------------------------------------------
class Partie:
    """Alice ou Bob : possede une cle privee et derive un secret."""
    def __init__(self, nom):
        self.nom = nom
        self.prive = gen()
        self.publique = pow_mod(G, self.prive, P)   # g^prive mod p
        self.K = None

    def etablir_secret(self, demi_cle_recue):
        self.K = pow_mod(demi_cle_recue, self.prive, P)
        return self.K


class Mallory:
    """L'attaquant au milieu : deux cles privees, une par victime."""
    def __init__(self):
        # Une cle privee pour parler a Alice, une autre pour parler a Bob.
        self.prive_vers_alice = gen()
        self.prive_vers_bob = gen()
        self.pub_vers_alice = pow_mod(G, self.prive_vers_alice, P)
        self.pub_vers_bob = pow_mod(G, self.prive_vers_bob, P)
        self.K_avec_alice = None   # secret partage Mallory <-> Alice
        self.K_avec_bob = None     # secret partage Mallory <-> Bob


def simulation_mitm():
    print("=" * 70)
    print("1.5  Simulation d'une attaque de l'homme du milieu")
    print("=" * 70)

    alice = Partie("Alice")
    bob = Partie("Bob")
    mallory = Mallory()

    # --- Echange des demi-cles, TOUT passe par Mallory ---------------------
    # Alice croit envoyer h_A a Bob ; Mallory l'intercepte et renvoie SA
    # propre demi-cle a Bob. Symetriquement pour Bob.
    print("\n[Echange des demi-cles -- le canal est controle par Mallory]")
    print(f"  Alice envoie h_A = {alice.publique}")
    print(f"  Bob   envoie h_B = {bob.publique}")
    print(f"  Mallory remplace : Alice recoit {mallory.pub_vers_alice} (de Mallory)")
    print(f"  Mallory remplace : Bob   recoit {mallory.pub_vers_bob} (de Mallory)")

    # Alice derive son secret avec ce qu'elle a recu (= demi-cle de Mallory).
    K_A = alice.etablir_secret(mallory.pub_vers_alice)
    # Mallory derive le MEME secret de son cote (avec la vraie demi-cle d'Alice).
    mallory.K_avec_alice = pow_mod(alice.publique, mallory.prive_vers_alice, P)

    # Idem cote Bob.
    K_B = bob.etablir_secret(mallory.pub_vers_bob)
    mallory.K_avec_bob = pow_mod(bob.publique, mallory.prive_vers_bob, P)

    print("\n[Secrets etablis]")
    print(f"  Alice  croit partager  K_A = {K_A}")
    print(f"  Mallory partage avec Alice = {mallory.K_avec_alice}"
          f"  (identique : {K_A == mallory.K_avec_alice})")
    print(f"  Bob    croit partager  K_B = {K_B}")
    print(f"  Mallory partage avec Bob   = {mallory.K_avec_bob}"
          f"  (identique : {K_B == mallory.K_avec_bob})")
    print(f"\n  --> Il existe DEUX secrets distincts (K_A != K_B : {K_A != K_B}).")
    print(f"      Alice et Bob croient pourtant partager une seule cle commune.")

    # --- Un message transite : Alice -> (Mallory) -> Bob ------------------
    print("\n[Alice envoie un message qu'elle croit destine directement a Bob]")
    message = "transfere 100 dollars a Bob"
    print(f"  message clair d'Alice : {message!r}")

    # Alice chiffre avec K_A (qu'elle croit partage avec Bob).
    c_alice = xor(message.encode('ascii'), cle_flot(K_A))
    print(f"  chiffre d'Alice (hex) : {c_alice.hex()}")

    # Mallory intercepte : il dechiffre avec K_A (qu'il connait).
    lu_par_mallory = xor(c_alice, cle_flot(mallory.K_avec_alice)).decode('ascii')
    print(f"\n[Mallory intercepte et DECHIFFRE avec K_A]")
    print(f"  Mallory lit : {lu_par_mallory!r}")
    assert lu_par_mallory == message, "Mallory devrait lire le clair exact"

    # Mallory MODIFIE le message, puis le re-chiffre avec K_B pour Bob.
    message_modifie = "transfere 900 dollars a Mallory"
    c_pour_bob = xor(message_modifie.encode('ascii'), cle_flot(mallory.K_avec_bob))
    print(f"  Mallory reecrit : {message_modifie!r}")
    print(f"  re-chiffre pour Bob (hex) : {c_pour_bob.hex()}")

    # Bob dechiffre avec K_B : il obtient le message falsifie, sans rien detecter.
    recu_par_bob = xor(c_pour_bob, cle_flot(K_B)).decode('ascii')
    print(f"\n[Bob dechiffre avec K_B]")
    print(f"  Bob lit : {recu_par_bob!r}")
    print(f"  Bob a-t-il recu le message original d'Alice ? "
          f"{recu_par_bob == message}")
    print(f"  Bob detecte-t-il une alteration ? Non : le dechiffrement est")
    print(f"  parfaitement valide de son point de vue.")
    print("\n[Conclusion] Mallory a lu ET modifie le message en restant invisible.")


if __name__ == "__main__":
    simulation_mitm()
