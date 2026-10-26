# Enregistre l'exposant public utilisé pour chiffrer les candidats.
e = 65537

# Enregistre le module RSA public N.
N = 46364812871374549

# Enregistre le cryptogramme intercepté que l'on cherche à reproduire.
c = 31963660340929498

# Prépare 1000 candidats, de 1394500914838000 à 1394500914838999.
# La dernière borne de range est exclue.
candidats = range(1394500914838000, 1394500914839000)

# Compte les candidats avec len et affiche leur nombre.
# .format remplace {} par la valeur calculée.
print("Nombre de candidats : {}".format(len(candidats)))

# Initialise le compteur à zéro, car aucun candidat n'a encore été testé.
essais = 0

# Indique qu'aucun message n'a encore été trouvé.
# None signifie ici « aucune valeur pour le moment ».
message_trouve = None

# Prend chaque candidat, un à un, dans l'ordre croissant.
for candidat in candidats:

    # Ajoute 1 au compteur à chaque candidat testé.
    essais += 1

    # Calcule le chiffrement du candidat : candidat^e modulo N.
    c_candidat = pow(candidat, e, N)

    # Vérifie si ce chiffrement est égal au cryptogramme intercepté.
    # == compare deux valeurs, tandis que = affecte une valeur.
    if c_candidat == c:

        # Enregistre le candidat qui a produit le bon cryptogramme.
        message_trouve = candidat

        # Quitte la boucle puisqu'on a trouvé le message recherché.
        break

# Vérifie qu'un message a été trouvé et enregistré.
if message_trouve is not None:

    # Affiche la valeur du message retrouvé.
    print("Message retrouve : {}".format(message_trouve))

    # Affiche combien de candidats ont été testés avant de le trouver.
    print("Nombre d'essais : {}".format(essais))

# Exécute ce bloc si aucun candidat n'a donné le cryptogramme attendu.
else:

    # Indique que le message recherché n'était pas parmi les candidats.
    print("Aucun candidat ne correspond.")