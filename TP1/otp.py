def _xor_hex(data: bytes, key_hex: str) -> bytes:
    key = bytes.fromhex(key_hex)
    if len(data) != len(key):
        raise ValueError(
            f"le message doit faire exactement {len(key)} octets "
            f"({len(key) * 8} bits) pour correspondre a la cle, "
            f"recu {len(data)} octets"
        )
    return bytes(a ^ b for a, b in zip(data, key))


def chiffrer(message: str, key_hex: str) -> str:
    c = _xor_hex(message.encode('ascii'), key_hex)
    return c.hex()


def dechiffrer(cryptogramme_hex: str, key_hex: str) -> str:
    m = _xor_hex(bytes.fromhex(cryptogramme_hex), key_hex)
    return m.decode('ascii')


if __name__ == '__main__':
    executions = [
        "48f42f09be44cd985c7b8094f0be6f0c53b20f06",
        "13f6b41cb7c47c2ea63f8fe5fd14be142b6b8df7",
        "06ae29c5adf5b760e64d019df68e1b89e953ed68",
    ]

    message = "Bonjour la crypto !!"
    assert len(message) == 20

    for idx, key_hex in enumerate(executions, start=1):
        print(f"--- Execution {idx} ---")
        print("cle (hex)         :", key_hex)
        print("message en clair  :", message)
        c = chiffrer(message, key_hex)
        print("cryptogramme (hex):", c)
        m2 = dechiffrer(c, key_hex)
        print("re-dechiffrement  :", m2)
        assert m2 == message
        print()
