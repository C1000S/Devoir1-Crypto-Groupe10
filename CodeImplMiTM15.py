p = 2**61 - 1  # Nombre premier public.
g = 37  # Générateur public.


def xor(message, secret):
    # Transforme le secret tronqué en quatre octets big-endian.
    cle = (secret % (2**32)).to_bytes(4, "big")

    # Répète les quatre octets pour chiffrer ou déchiffrer.
    return bytes(
        octet ^ cle[i % 4]
        for i, octet in enumerate(message)
    )


class Entite:
    # Cette classe représente Alice ou Bob.
    def __init__(self, nom, privee):
        self.nom = nom  # Mémorise le nom.
        self.privee = privee  # Mémorise la clé privée.
        self.publique = pow(g, privee, p)  # Calcule la clé publique.
        self.secret = None  # Le secret sera calculé après réception d’une clé.

    def recevoir_cle(self, publique):
        # Accepte la clé reçue sans vérifier son propriétaire.
        self.secret = pow(publique, self.privee, p)

    def chiffrer(self, texte):
        # Convertit le texte en ASCII, puis applique XOR.
        return xor(texte.encode("ascii"), self.secret)

    def dechiffrer(self, chiffre):
        # Applique XOR, puis transforme les octets en texte.
        return xor(chiffre, self.secret).decode("ascii")


class Mallory:
    def __init__(self):
        self.u = 123456789  # Exposant utilisé avec Alice.
        self.v = 987654321  # Exposant utilisé avec Bob.
        self.secret_alice = None  # Futur secret Alice–Mallory.
        self.secret_bob = None  # Futur secret Mallory–Bob.
        self.texte_lu = None  # Mémorise le message intercepté.

    def intercepter(self, expediteur, destinataire, type_message, contenu):
        # Intercepte les clés publiques pendant leur échange.
        if type_message == "cle":
            if expediteur.nom == "Alice":
                # Calcule le secret avec Alice à partir de sa clé publique.
                self.secret_alice = pow(contenu, self.u, p)

                # Envoie sa propre clé à Bob à la place de celle d’Alice.
                return pow(g, self.v, p)

            # Calcule le secret avec Bob à partir de sa clé publique.
            self.secret_bob = pow(contenu, self.v, p)

            # Envoie sa propre clé à Alice à la place de celle de Bob.
            return pow(g, self.u, p)

        # Intercepte un message envoyé par Alice.
        if expediteur.nom == "Alice":
            # Déchiffre avec le secret partagé avec Alice.
            self.texte_lu = xor(
                contenu, self.secret_alice
            ).decode("ascii")

            print("Mallory lit :", self.texte_lu)

            # Modifie le texte original.
            modifie = self.texte_lu.replace("aujourd hui", "DEMAIN")
            print("Mallory remplace par :", modifie)

            # Chiffre le texte modifié avec le secret partagé avec Bob.
            return xor(modifie.encode("ascii"), self.secret_bob)

        # Dans l’autre sens, lit le message de Bob.
        texte = xor(contenu, self.secret_bob)

        # Le chiffre à nouveau pour Alice.
        return xor(texte, self.secret_alice)


# Crée les trois entités.
alice = Entite("Alice", 974264167110881)
bob = Entite("Bob", 23179607248816)
mallory = Mallory()


def canal(expediteur, destinataire, type_message, contenu):
    # Tous les échanges passent obligatoirement par Mallory.
    transmis = mallory.intercepter(
        expediteur, destinataire, type_message, contenu
    )

    if type_message == "cle":
        # Le destinataire reçoit la clé remplacée par Mallory.
        destinataire.recevoir_cle(transmis)
        return None

    # Le destinataire déchiffre le message retransmis par Mallory.
    return destinataire.dechiffrer(transmis)


# Alice et Bob échangent leurs clés via le canal compromis.
canal(alice, bob, "cle", alice.publique)
canal(bob, alice, "cle", bob.publique)

# Vérifie les deux secrets établis par l’attaque.
assert alice.secret == mallory.secret_alice
assert bob.secret == mallory.secret_bob
assert alice.secret != bob.secret

# Alice chiffre le message qu’elle croit envoyer directement à Bob.
original = "nouvelle cle generee aujourd hui"
print("Alice croit envoyer à Bob :", original)

# Mallory intercepte, déchiffre, modifie et retransmet.
recu = canal(alice, bob, "message", alice.chiffrer(original))
print("Bob reçoit :", recu)

# Prouve que Mallory a retrouvé exactement le message original.
assert mallory.texte_lu == original

# Prouve que Bob reçoit le message modifié.
assert recu == "nouvelle cle generee DEMAIN"
assert recu != original

print("Mallory a lu et modifié le message : VRAI")