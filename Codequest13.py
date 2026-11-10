K = 397785387543180550  # Secret partagé complet d’Alice et Bob.

K_tronque = K % (2**32)  # Conserve les 32 derniers bits du secret.
k = K_tronque.to_bytes(4, "big")  # Convertit la clé en 4 octets : d1 5a 35 06.

message = "nouvelle cle generee aujourd hui"  # Message correspondant au résultat fourni.
m = message.encode("ascii")  # Convertit chaque caractère en un octet ASCII.

c = bytearray()  # Crée un tableau vide pour les octets chiffrés.

for i in range(len(m)):  # Parcourt toutes les positions du message.
    octet_cle = k[i % 4]  # Sélectionne un des quatre octets de la clé.
    octet_chiffre = m[i] ^ octet_cle  # Applique le XOR entre le message et la clé.
    c.append(octet_chiffre)  # Ajoute l’octet obtenu au résultat.

print("Clé en hexadécimal :", k.hex())  # Affiche d15a3506.
print("Message chiffré :", c.hex())  # Affiche le chiffrement en hexadécimal.

