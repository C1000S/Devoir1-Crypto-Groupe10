import string
from collections import Counter

ALPHA = string.ascii_uppercase

CRYPTOGRAMME_463 = (
    "MIVNCURVIPNMJIJUYNNUCBVIPSEEBWYKSKEFTEWXUZNTSADQEUIEYBUJMEXNWFVUI"
    "HNFUIHPEBNKDPMWMOHEJIVDXQKUEUDKDKQEXRODKQIYCOIJBCIADELUIWUOITMIWY"
    "YIJJFPNCCRJWPNCFRDIHNCSCFWIBDFRSJSRCJIPTZJCJVQSYAMUCBPIYBEXSEQVOB"
    "ZUPIOSSYJIVUSWEFTEAVYXOIGXWFKFPIBVUKUVIBOJRGJMLRULOXEKVURVHIBPHVR"
    "YIWMUJBPILBQEVRIBSWEBXYAODLNIVRAKVQIVVOJUFTVXELVSUYDXCVTWEPOFIPZM"
    "NXJSJIRMOIFOEYCOKIFXUDSBEBTEBOJVNSHRPYVFRGQOCZOTSDBLVSMJROHCJRXNQ"
    "HZUIHDXCVTWEPOEEBNSDDULOGSMOTRVXLNXJZGMGJDYFOGEUMKCFETJBJZSHYWOSC"
    "FWILBUKF"
)

FR_FREQ = {  # frequences en % des lettres en francais
    'A': 7.64, 'B': 0.90, 'C': 3.26, 'D': 3.67, 'E': 14.72, 'F': 1.07,
    'G': 0.87, 'H': 0.74, 'I': 7.53, 'J': 0.61, 'K': 0.05, 'L': 5.46,
    'M': 2.97, 'N': 7.10, 'O': 5.38, 'P': 3.02, 'Q': 1.36, 'R': 6.55,
    'S': 7.95, 'T': 7.24, 'U': 6.31, 'V': 1.66, 'W': 0.04, 'X': 0.43,
    'Y': 0.31, 'Z': 0.14,
}


def indice_coincidence(texte: str, periode: int = 1) -> float:
    if periode == 1:
        n = len(texte)
        cnt = Counter(texte)
        return sum(v * (v - 1) for v in cnt.values()) / (n * (n - 1))
    ics = []
    for i in range(periode):
        col = texte[i::periode]
        n = len(col)
        if n < 2:
            continue
        cnt = Counter(col)
        ics.append(sum(v * (v - 1) for v in cnt.values()) / (n * (n - 1)))
    return sum(ics) / len(ics)


def trouver_longueur_cle(texte: str, max_periode: int = 15) -> list:
    return [(p, indice_coincidence(texte, p)) for p in range(1, max_periode + 1)]


def _chi2_pour_decalage(col: str, decalage: int) -> float:
    n = len(col)
    cnt = Counter((ord(ch) - ord('A') - decalage) % 26 for ch in col)
    chi2 = 0.0
    for i, lettre in enumerate(ALPHA):
        observe = cnt.get(i, 0)
        attendu = FR_FREQ[lettre] / 100 * n
        if attendu > 0:
            chi2 += (observe - attendu) ** 2 / attendu
    return chi2


def trouver_cle(texte: str, longueur: int) -> str:
    cle = []
    for col_idx in range(longueur):
        col = texte[col_idx::longueur]
        meilleur_decalage = min(range(26), key=lambda s: _chi2_pour_decalage(col, s))
        cle.append(ALPHA[meilleur_decalage])
    return ''.join(cle)


def dechiffrer(cryptogramme: str, cle: str) -> str:
    sortie = []
    for i, ch in enumerate(cryptogramme):
        k = ord(cle[i % len(cle)]) - ord('A')
        v = (ord(ch) - ord('A') - k) % 26
        sortie.append(ALPHA[v])
    return ''.join(sortie)


if __name__ == '__main__':
    print("Longueur du cryptogramme :", len(CRYPTOGRAMME_463))

    print("\n=== Etape 1 : indice de coincidence par longueur de cle ===")
    for p, val in trouver_longueur_cle(CRYPTOGRAMME_463):
        marque = "  <-- pic" if val > 0.07 else ""
        print(f"  periode {p:2d} : IC = {val:.4f}{marque}")

    longueur = 7  # pic net observe (IC ~ 0.080, proche de 0.0778 en francais)
    print(f"\n=== Etape 2 : longueur de cle retenue = {longueur} ===")

    cle = trouver_cle(CRYPTOGRAMME_463, longueur)
    print("cle retrouvee :", cle)

    clair = dechiffrer(CRYPTOGRAMME_463, cle)
    print("\n=== Texte clair ===")
    print(clair)
