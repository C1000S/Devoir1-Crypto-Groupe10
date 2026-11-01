# IFT814 — Devoir 2 — Équipe 05

## Contenu du dépôt

```
TP2/
├── IFT814-Devoir2-A26v1.pdf     # énoncé
├── Equipe_05.txt                # fiche de paramètres (valeurs imposées)
├── calculs/                     # code Python (auto-implémenté, aucune lib de chiffrement)
│   ├── partie1_diffie_hellman.py   # 1.1 Gen/PubKey/Secret, 1.2 trace, 1.3 chiffrement XOR
│   ├── partie1_mitm.py             # 1.5 simulation homme du milieu
│   ├── partie2_rsa.py              # 2.1 keygen (Miller-Rabin, Euclide étendu) → 2.5
│   └── partie3_signatures.py       # 3.1 Sign/Verify → 3.4 forgerie multiplicative
```

## Reproduire toutes les traces

```bash
cd calculs
python3 partie1_diffie_hellman.py
python3 partie1_mitm.py
python3 partie2_rsa.py
python3 partie3_signatures.py
```



Déclaration d'usage des outils d'IA générative

> À adapter/valider par l'équipe avant la remise, selon l'usage réel.

Niveau 1 (balises de la Faculté des sciences) : un outil d'IA générative a été
utilisé pour **s'expliquer des notions** (logarithme discret, OAEP, PSS,
Miller-Rabin) et **structurer la rédaction**. Les algorithmes demandés
(exponentiation rapide, Euclide étendu, Miller-Rabin, DH, RSA, signatures) ont
été écrits et vérifiés par l'équipe ; toutes les traces ont été produites par
l'exécution de notre propre code et comparées aux valeurs `[Verification]` de la
fiche. Aucun code, trace ou réponse n'a été livré tel quel par l'outil sans
compréhension et vérification.

*(Si l'équipe n'a rien utilisé, remplacer par « aucun usage ».)*

## Conventions respectées

- `pow(a, b, n)` implémenté à la main par **carré-et-multiplication** (jamais de
  multiplication répétée ni de lib de chiffrement).
- Aléatoire via `secrets` (générateur cryptographiquement sûr).
- Aucune bibliothèque implémentant un chiffrement ou un MAC.
