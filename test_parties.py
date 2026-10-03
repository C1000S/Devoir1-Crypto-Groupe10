#!/usr/bin/env python3
"""Test script to run each PARTIE of Equipe_03.txt individually.

Usage:
    python3 test_parties.py [partie]
    
    partie can be: 1.1, 1.2, 2.1, 2.2, 3.2, 3.4, vigenere, all
    Default: all
"""

import sys
from rodier_solution_ift814 import *

def test_partie_1_1(p):
    """PARTIE 1.1 - César à double décalage
    
    Intent: Test encryption/decryption with the 3 imposed keys and verify
    Eve1 attack finds the correct key by dictionary segmentation.
    
    Expected: For each key (k1,k2), E1/D1 roundtrip recovers MESSAGE.
    Eve1 returns exactly 1 candidate with the correct key and segmented words.
    """
    print("=" * 60)
    print("PARTIE 1.1 - César à double décalage")
    print("=" * 60)
    for i, k in enumerate(p['cesar'], 1):
        c = E1(k, MESSAGE)
        m = D1(k, c)
        assert m == MESSAGE, f"Roundtrip failed for key {k}"
        candidats = Eve1(c)
        print(f"Exécution {i}: key={k}")
        print(f"  Chiffré: {c}")
        print(f"  Déchiffré: {m}")
        print(f"  Candidats Eve1: {len(candidats)}")
        for cand in candidats:
            print(f"    key={cand['cle']} texte='{cand['texte']}' mots={cand['mots']}")
        # Verify the correct key is found
        assert any(cand['cle'] == list(k) for cand in candidats), "Correct key not found by Eve1"
    print("[OK] All 3 executions verified\n")

def test_partie_1_2(p):
    """PARTIE 1.2 - Substitution monoalphabétique
    
    Intent: Test encryption/decryption with the 3 imposed substitution keys.
    
    Expected: For each 26-letter key, E3/D3 roundtrip recovers MESSAGE.
    """
    print("=" * 60)
    print("PARTIE 1.2 - Substitution monoalphabétique")
    print("=" * 60)
    for i, k in enumerate(p['sub'], 1):
        c = E3(k, MESSAGE)
        m = D3(k, c)
        assert m == MESSAGE, f"Roundtrip failed for key {k}"
        print(f"Exécution {i}: key={k}")
        print(f"  Chiffré: {c}")
        print(f"  Déchiffré: {m}")
    print("[OK] All 3 executions verified\n")

def test_partie_2_1(p):
    """PARTIE 2.1 - Masque jetable (OTP)
    
    Intent: Test OTP encryption/decryption with the 3 imposed 160-bit keys.
    Verify the alternative key derivation (malleability demonstration).
    
    Expected: For each key, E2/D2 roundtrip recovers MESSAGE.
    Alternative key k' = c ^ bits('a'*32) decrypts c to 'a'*32.
    """
    print("=" * 60)
    print("PARTIE 2.1 - Masque jetable (OTP)")
    print("=" * 60)
    for i, k in enumerate(p['otp'], 1):
        c = E2(k, MESSAGE)
        m = D2(k, c)
        assert m == MESSAGE, f"Roundtrip failed for key {k}"
        print(f"Exécution {i}: key={format(k, '040x')}")
        print(f"  Chiffré (hex): {format(c, '040x')}")
        print(f"  Déchiffré: {m}")
    
    # Test malleability: derive key that maps ciphertext to 'a'*32
    autre = 'a' * 32
    c = E2(p['otp'][0], MESSAGE)
    kp = c ^ vers_bits(autre)
    m2 = D2(kp, c)
    assert m2 == autre, "Malleability test failed"
    print(f"\nMalleability demo:")
    print(f"  Original message: {MESSAGE}")
    print(f"  Ciphertext: {format(c, '040x')}")
    print(f"  Alternative key: {format(kp, '040x')}")
    print(f"  Decrypts to: {m2}")
    print("[OK] OTP verified + malleability demonstrated\n")

def test_partie_2_2(p):
    """PARTIE 2.2 - Réutilisation de clé OTP
    
    Intent: Analyze two ciphertexts encrypted with the same OTP key.
    Use known-plaintext attack (Eve knows 'protocole' is in m1).
    
    Expected: XOR of ciphertexts equals XOR of plaintexts.
    Eve2 finds candidate positions for 'protocole' in m1.
    Full reconstruction yields two plausible French messages.
    """
    print("=" * 60)
    print("PARTIE 2.2 - Réutilisation de clé OTP")
    print("=" * 60)
    c1, c2 = p['c1'], p['c2']
    xor = c1 ^ c2
    print(f"c1: {format(c1, '060x')}")
    print(f"c2: {format(c2, '060x')}")
    print(f"c1 ^ c2: {format(xor, '060x')}")
    
    candidats = Eve2(c1, c2, mot='protocole', n=48)
    print(f"\nEve2 candidates for 'protocole' in m1:")
    for cand in candidats:
        print(f"  Position {cand['position']}: m2 fragment = '{cand['fragment_m2']}'")
    
    # Verify the reconstructed messages
    m1 = 'modifiezimmediatementleprotocoledesecurite'.ljust(48, 'x')
    m2 = 'leserveurcentralredemarreradimancheaminuit'.ljust(48, 'x')
    verif = verifier_hypothese_otp(m1, m2, c1, c2)
    assert verif['c1_valide'] and verif['c2_valide'], "Reconstructed messages don't match ciphertexts"
    print(f"\nReconstructed messages verified:")
    print(f"  m1: {m1}")
    print(f"  m2: {m2}")
    print(f"  Key: {verif['cle']}")
    print("[OK] OTP reuse attack verified\n")

def test_partie_3_2(p):
    """PARTIE 3.2 - MAC (Message Authentication Code)
    
    Intent: Test the weak MAC construction MAC(k,m) = (m ^ k) & 0xffffffff.
    Demonstrate collision: m and m ^ (1<<63) produce same tag.
    
    Expected: For test messages, MAC/Verif work correctly.
    Flipping bit 63 of message doesn't change the tag (collision).
    """
    print("=" * 60)
    print("PARTIE 3.2 - MAC")
    print("=" * 60)
    k = p['mac_k']
    test_messages = [0, 1<<63, (1<<32)-1, 0xaaaaaaaaaaaaaaaa]
    for m in test_messages:
        t = MAC(k, m)
        mf = m ^ (1 << 63)
        v1 = Verif(k, m, t)
        v2 = Verif(k, mf, t)
        v3 = Verif(k, m, t ^ 1)
        assert v1 == 1 and v2 == 1 and v3 == 0, f"MAC verification failed for m={format(m,'016x')}"
        print(f"m={format(m, '016x')} t={format(t, '08x')} v={v1} m'={format(mf, '016x')} v'={v2}")
    print("[OK] MAC verified + collision demonstrated (bit 63 ignored)\n")

def test_partie_3_4(p):
    """PARTIE 3.4 - MAC Forgery
    
    Intent: Forge a valid tag for m_cible given one observed (m_obs, t_obs) pair.
    The MAC only uses lower 32 bits of key, so we can recover k_low and forge.
    
    Expected: EveMAC recovers k_low = (m_obs & 0xffffffff) ^ t_obs.
    Two compatible full keys: k_low and (1<<32) | k_low.
    Both verify for m_obs and produce same tag for m_cible.
    """
    print("=" * 60)
    print("PARTIE 3.4 - MAC Forgery")
    print("=" * 60)
    kb, t = EveMAC(p['m_obs'], p['t_obs'], p['m_cible'])
    print(f"Observed: m_obs={format(p['m_obs'], '016x')} t_obs={format(p['t_obs'], '08x')}")
    print(f"Target:   m_cible={format(p['m_cible'], '016x')}")
    print(f"Recovered k_low: {format(kb, '08x')}")
    print(f"Forged tag for m_cible: {format(t, '08x')}")
    
    cles = [kb, (1 << 32) | kb]
    for k in cles:
        v1 = Verif(k, p['m_obs'], p['t_obs'])
        v2 = Verif(k, p['m_cible'], t)
        print(f"  Key {format(k, '016x')}: Verif(m_obs)={v1} Verif(m_cible)={v2}")
        assert v1 == 1 and v2 == 1
    print("[OK] MAC forgery successful\n")

def test_vigenere(p):
    """BONUS - Chiffre de Vigenère
    
    Intent: Break Vigenère cipher using Kasiski examination and
    Friedman test (index of coincidence) for key length detection,
    then frequency analysis per column.
    
    Expected: Kasiski finds repeated trigrams with distances suggesting key length 7.
    Friedman test confirms key length 7 (highest IC).
    Key 'beejkqr' decrypts to French text about electrical grid, crypto concepts.
    """
    print("=" * 60)
    print("BONUS - Chiffre de Vigenère")
    print("=" * 60)
    
    # Kasiski
    kas = kasiski(p['vigenere'])
    print("Kasiski examination (repeated trigrams):")
    for k in kas:
        print(f"  {k['trigramme']}: positions {k['positions']} distances {k['distances']}")
    
    # Friedman / IC test
    essais = EveVigenere(p['vigenere'])
    print("\nFriedman test (average IC per key length):")
    for e in essais:
        marker = " <- BEST" if e['longueur'] == 7 else ""
        print(f"  Length {e['longueur']}: IC={e['ic_moyen']:.6f} key='{e['cle']}'{marker}")
    
    meilleur = max(essais, key=lambda a: a['ic_moyen'])
    assert meilleur['longueur'] == 7, "Expected key length 7"
    assert meilleur['cle'] == 'beejkqr', f"Expected key 'beejkqr', got '{meilleur['cle']}'"
    print(f"\nBest key: {meilleur['cle']} (length {meilleur['longueur']})")
    print(f"Decrypted text preview: {meilleur['texte'][:100]}...")
    print("[OK] Vigenère broken successfully\n")

def main():
    if len(sys.argv) > 1:
        partie = sys.argv[1]
    else:
        partie = 'all'
    
    p = charger('Equipe_03.txt')
    
    # Verify empreintes first
    empreintes = {
        'sub': hashlib.sha256(p['sub_c'].encode()).hexdigest()[:8],
        'otp': hashlib.sha256((format(p['c1'], '060x') + format(p['c2'], '060x')).encode()).hexdigest()[:8],
        'vigenere': hashlib.sha256(p['vigenere'].encode()).hexdigest()[:8]
    }
    expected = {'sub': '2b86f4d7', 'otp': 'd7b627e1', 'vigenere': '768d2dfa'}
    assert empreintes == expected, f"Empreintes mismatch: {empreintes} != {expected}"
    print(f"[OK] Empreintes verified: {empreintes}\n")
    
    tests = {
        '1.1': test_partie_1_1,
        '1.2': test_partie_1_2,
        '2.1': test_partie_2_1,
        '2.2': test_partie_2_2,
        '3.2': test_partie_3_2,
        '3.4': test_partie_3_4,
        'vigenere': test_vigenere,
    }
    
    if partie == 'all':
        for name, test_fn in tests.items():
            test_fn(p)
        print("=" * 60)
        print("ALL TESTS PASSED")
        print("=" * 60)
    elif partie in tests:
        tests[partie](p)
    else:
        print(f"Unknown partie: {partie}")
        print(f"Available: {', '.join(tests.keys())}, all")
        sys.exit(1)

if __name__ == '__main__':
    main()