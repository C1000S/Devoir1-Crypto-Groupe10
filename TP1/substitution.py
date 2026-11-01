import string
import math
import random
from collections import Counter

ALPHA = string.ascii_lowercase

def chiffrer(message: str, cle: str) -> str:
    cle = cle.lower()
    table = {ALPHA[i]: cle[i] for i in range(26)}
    return ''.join(table.get(c, c) for c in message.lower())

def dechiffrer(cryptogramme: str, cle: str) -> str:
    cle = cle.lower()
    table = {cle[i]: ALPHA[i] for i in range(26)}
    return ''.join(table.get(c, c) for c in cryptogramme.lower())

# ---------------------------------------------------------------------------
# Cryptanalyse (cryptogramme seul) du texte de 398 lettres
# ---------------------------------------------------------------------------

CRYPTOGRAMME_398 = (
    "YAOEJGYAGGJABWAGWAGHAKAFIEXAPWAGYJOWDRIPAGBTAFBTAKPIPFIKGRAPPFAWA"
    "EFGDFYFAGGIKGZEAWAKKARJOEJGGAWAGWJFAEKOFDPDBDWAYABTIKHAYABWAGOAFRA"
    "PIYAEXOAFGDKKAGYABDKSAKJFYEKGABFAPBDRREKAKOIFWIKPYASIKPPDEPWARDKY"
    "AEKDFYJKIPAEFZEIKPJZEAGECCJGIRRAKPOEJGGIKPODEFFIJPBIGGAFOWEGJAEFG"
    "GQGPARAGYABTJCCFARAKPEPJWJGAGIEUDEFYTEJGEFJKPAFKAPWAGAWASAGDKPRIF"
    "BTAUEGZEIEGDRRAPYAWIBDWWJKAODEFDVGAFSAFWABDEBTAFYEGDWAJWGEFPDEPAW"
    "IFAHJDK"
)
def solution_398():
    return ''.join(SOLUTION_CLE_CIPHER_VERS_CLAIR[c] for c in CRYPTOGRAMME_398)


def casser_par_frequence(cryptogramme: str, french_freq_order='EAISNTRULODCPMVQGFBHXJYZKW'):
    """Etape 1 (a la main / rapide) : mapping  par frequence des lettres."""
    cnt = Counter(cryptogramme.upper())
    cipher_by_freq = [l for l, _ in cnt.most_common()]
    for l in string.ascii_uppercase:
        if l not in cipher_by_freq:
            cipher_by_freq.append(l)
    key_map = dict(zip(cipher_by_freq, french_freq_order))
    return ''.join(key_map[c] for c in cryptogramme.upper())


SOLUTION_CLE_CIPHER_VERS_CLAIR = {
    'A': 'E', 'G': 'S', 'E': 'U', 'F': 'R', 'K': 'N', 'P': 'T', 'W': 'L',
    'D': 'O', 'J': 'I', 'I': 'A', 'Y': 'D', 'B': 'C', 'R': 'M', 'O': 'P',
    'T': 'H', 'Z': 'Q', 'S': 'V', 'C': 'F', 'H': 'G', 'X': 'X', 'U': 'J',
    'Q': 'Y', 'V': 'B', 'L': 'W', 'M': 'K', 'N': 'Z',
}


if __name__ == '__main__':
    # --- 1) executions avec cles imposees (traces) ---
    executions = [
        "rsaofhvpmwtqzbkcigynxldeju",
        "ixodqfulgkaenhscjbtvmpzyrw",
        "jwxqkcgyhftoudpvrisenmabzl",
    ]
    message = "venividivici"
    for idx, cle in enumerate(executions, start=1):
        c = chiffrer(message, cle)
        m2 = dechiffrer(c, cle)
        print(f"--- Execution {idx} ---")
        print("cle               :", cle)
        print("message en clair  :", message)
        print("cryptogramme      :", c)
        print("re-dechiffrement  :", m2)
        assert m2 == message
        print()

    # --- 2) cryptanalyse du cryptogramme de 398 lettres ---
    print("=== Cryptanalyse (cryptogramme seul), 398 lettres ===")
    clair = solution_398()
    print("texte clair retrouve :")
    print(clair)
