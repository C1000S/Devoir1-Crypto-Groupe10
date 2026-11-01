
m_obs = 0x34de51e80a5b0373
t_obs = 0x4661f080
m_cible = 0xf330a664f8b1ecd2

MASK64 = (1 << 64) - 1
MASK32 = (1 << 32) - 1


def tronc_poids_faible(x64: int) -> int:
    return x64 & MASK32


def tronc_poids_fort(x64: int) -> int:
    return (x64 >> 32) & MASK32


def forger(hypothese_troncature):
    delta = (m_obs ^ m_cible) & MASK64
    t_forge = t_obs ^ hypothese_troncature(delta)
    return t_forge


if __name__ == '__main__':
    print("m_obs   =", hex(m_obs))
    print("t_obs   =", hex(t_obs))
    print("m_cible =", hex(m_cible))
    print()
    print("tag forge (poids faible) :", hex(forger(tronc_poids_faible)))
    print("tag forge (poids fort)   :", hex(forger(tronc_poids_fort)))
    print()
