# Contribution de Rodier Marcel Tumamo Simo (CIP : tumr4770)

IFT814 – Cryptographie – Devoir 1 (Automne 2026) – Groupe 10  
Fiche de paramètres : `Equipe_03.txt`

## Contenu

```
Tumr4770/
├── README.md
├── code/
│   ├── solution_ift814.py   # toutes les parties (1.1 → 3.5 + bonus) dans un seul script
│   └── Equipe_03.txt        # fiche de paramètres (doit rester à côté du script)
├── resultats/
│   ├── resultats.json       # sortie complète du script (traces, attaques, vérifications)
│   
└── rapport/
    ├── IFT814_Devoir1_Groupe10_Rodier.pdf   # rapport complet (17 pages)
    
```

## Exécuter

```bash
cd code
python3 solution_ift814.py > ../resultats/resultats.json
```

Python 3 seulement, sans bibliothèque externe (`secrets`, `hashlib` pour les empreintes uniquement).
Le script vérifie lui-même les empreintes de la fiche et le rechiffrement de chaque résultat
(il s'arrête avec une erreur si une vérification échoue).

## Résultats principaux (message imposé `ceciestlemessageclairadechiffrer`)

| Partie | Résultat |
|---|---|
| 1.1 César double, exéc. 1/2/3 | `eyecgmvfgggmuuiyefcctufyebkzhlgl` / `vevixsmlxmxslazevltikawevhbfyrxr` / `wmwqyantyuyamiamwtuqlixmwpcnzzyz` |
| 1.2 Substitution, exéc. 1/2/3 | `afamfynqfzfyyrvfaqrmgrofapmhhgfg` / `oqogqtveqnqttiuqoeigbidqolgffbqb` / `xkxhkseokukssjgkxojhijqkxyhcciki` |
| 1.2 Cryptanalyse | « depuis des siècles les généraux… » – clé `ivbyachtjulwrkdozfgpesmxqn` |
| 2.1 OTP, exéc. 1/2/3 | `59f0ad43…83e0cb97` / `02f23656…fb394966` / `17aaab8f…390129f9` |
| 2.2 Réutilisation de clé | « protocole » en position 23 ; m1 = `modifiezimmediatementleprotocoledesecuritexxxxxx`, m2 = `leserveurcentralredemarreradimancheaminuitxxxxxx` |
| 3.2 Tags MAC m1…m4 | `3d00bd90`, `3d00bd90`, `c2ff426f`, `97aa173a` |
| 3.4 Forgerie | low32(k*) = `4c3af3f3`, tag forgé = `b48b1f21` |
| Bonus Vigenère | longueur 7, clé `beejkqr` |
