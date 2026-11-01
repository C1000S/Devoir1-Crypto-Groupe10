import string
ALPHA = string.ascii_lowercase

def _clean(texte: str) -> str:
    return ''.join(c for c in texte.lower() if c in ALPHA)

def chiffrer(message: str, k1: int, k2: int) -> str:
    m = _clean(message)
    sortie = []
    for i, c in enumerate(m):
        k = k1 if i % 2 == 0 else k2
        v = (ord(c) - ord('a') + k) % 26
        sortie.append(chr(v + ord('a')))
    return ''.join(sortie)

def dechiffrer(cryptogramme: str, k1: int, k2: int) -> str:
    c = _clean(cryptogramme)
    sortie = []
    for i, ch in enumerate(c):
        k = k1 if i % 2 == 0 else k2
        v = (ord(ch) - ord('a') - k) % 26
        sortie.append(chr(v + ord('a')))
    return ''.join(sortie)


if __name__ == '__main__':
    message = "rendreacesarcequiestacesar"

    executions = [
        (2, 20),
        (19, 0),
        (20, 8),
    ]

    for idx, (k1, k2) in enumerate(executions, start=1):
        c = chiffrer(message, k1, k2)
        m2 = dechiffrer(c, k1, k2)
        print(f"--- Execution {idx} : k1={k1}, k2={k2} ---")
        print("message en clair : ", _clean(message))
        print("cryptogramme      : ", c)
        print("re-dechiffrement  : ", m2)
        assert m2 == _clean(message), "erreur : le dechiffrement ne redonne pas le message"
        print()
