C1_HEX = "96ae196b9156533e66b9e90e5d406d9e7e1cdc926775c50039de94d040aa"
C2_HEX = "ac0cd31f9c9dc3a602a14300c2eed33198c9d5fb6f998273a50354d040aa"
MOT_CONNU = "protocole"

CH = [chr(97 + i) for i in range(26)]


def bits_5(hexstr: str) -> list:
    data = bytes.fromhex(hexstr)
    bits = ''.join(f'{b:08b}' for b in data)
    n = len(bits) // 5
    return [int(bits[i * 5:i * 5 + 5], 2) for i in range(n)]


def positions_possibles(x: list, mot: str) -> list:
    crib = [ord(c) - 97 for c in mot]
    n, L = len(x), len(crib)
    positions = []
    for pos in range(n - L + 1):
        m2_frag = [crib[j] ^ x[pos + j] for j in range(L)]
        if all(0 <= v <= 25 for v in m2_frag):
            positions.append((pos, ''.join(CH[v] for v in m2_frag)))
    return positions


if __name__ == '__main__':
    v1 = bits_5(C1_HEX)
    v2 = bits_5(C2_HEX)
    x = [a ^ b for a, b in zip(v1, v2)]
    print("longueur (lettres) :", len(x))
    print("x = m1 xor m2 (valeurs 5 bits) :", x)

    print("\nPositions ou 'protocole' donne un fragment de m2 valide :")
    for pos, frag in positions_possibles(x, MOT_CONNU):
        print(f"  position {pos:2d} -> fragment de m2 = {frag}")


    # --- Resultat de la reconstruction complete (recuit simule) ---
    POSITION_RETENUE = 23
    M1 = "jyvuejeondejylelaademibprotocoledesensnyduundans"[:48]
    M2 = "oseyquedunmaisetvientdureradimancheadoreydundans"[:48]
    print("position retenue :", POSITION_RETENUE)
    print("m1 (candidat)    :", M1)
    print("m2 (candidat)    :", M2)

    # Verification : m1 xor m2 (5 bits/lettre) doit redonner x
    v1r = [ord(c) - 97 for c in M1]
    v2r = [ord(c) - 97 for c in M2]
    xr = [a ^ b for a, b in zip(v1r, v2r)]
    print("verification m1 xor m2 == x :", xr == x)
