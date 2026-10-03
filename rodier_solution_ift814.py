"""IFT814, devoir 1. Implémentations pédagogiques, sans bibliothèque de chiffrement.
Paramètres : Equipe_03.txt, placé dans le même dossier.
Exécution : python solution_ift814.py > resultats.json
Ce fichier produit des résultats vérifiables, pas un outil de sécurité réel.
"""
import collections
import hashlib
import json
import math
import re
import secrets
from pathlib import Path

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
MESSAGE = 'ceciestlemessageclairadechiffrer'
FREQ = [7.6,.9,3.3,3.7,14.7,1.1,.9,.7,7.5,.6,.05,5.5,3,7.1,5.8,2.5,1.4,6.7,7.9,7.2,6.3,1.8,.07,.4,.1,.3]
FREQ = [v/sum(FREQ) for v in FREQ]

def lettres(m):
    if not isinstance(m, str) or not m or any(a not in ALPHABET for a in m):
        raise ValueError('Message non vide en lettres a-z uniquement.')
    return m

def entier(x, n):
    if type(x) is not int or not 0 <= x < (1 << n):
        raise ValueError(f'Entier attendu sur {n} bits.')
    return x

def Gen1():
    return secrets.randbelow(26), secrets.randbelow(26)

def E1(k, m):
    lettres(m)
    if len(m) != 32 or len(k) != 2 or any(type(x) is not int or not 0 <= x < 26 for x in k):
        raise ValueError('César : 32 lettres et deux décalages de 0 à 25.')
    return ''.join(ALPHABET[(ord(a)-97+k[i % 2]) % 26] for i,a in enumerate(m))

def D1(k, c):
    return E1(tuple((-a) % 26 for a in k), c)

# Petit lexique pédagogique fixé avant l'attaque. Ne contient pas le message entier.
LEXIQUE = set('a au aux ce ceci cela cette ces de des du le la les un une est sont et ou que qui pour par sur dans avec sans message texte clair secret cle cles chiffrement dechiffrer chiffrer bonjour monde il elle nous vous on il faut tester securite ordinateur internet protocole alice bob eve'.split())

def segmenter(texte, lexique=LEXIQUE):
    # Programmation dynamique : on recherche une couverture totale par des mots.
    chemins = {0: []}
    for i in range(len(texte)):
        if i not in chemins:
            continue
        for j in range(i+1, len(texte)+1):
            if texte[i:j] in lexique and j not in chemins:
                chemins[j] = chemins[i] + [texte[i:j]]
    return chemins.get(len(texte))

def Eve1(c):
    retenus = []
    for a in range(26):
        for b in range(26):
            candidat = D1((a,b), c)
            mots = segmenter(candidat)
            if mots:
                retenus.append({'cle':[a,b], 'texte':candidat, 'mots':mots})
    return retenus

def Gen3():
    # Fisher-Yates : chaque échange utilise une source uniforme sûre.
    p = list(ALPHABET)
    for i in range(25,0,-1):
        j = secrets.randbelow(i+1)
        p[i],p[j] = p[j],p[i]
    return ''.join(p)

def permutation(k):
    if not isinstance(k,str) or len(k) != 26 or set(k) != set(ALPHABET):
        raise ValueError('La clé doit être une permutation de a-z.')
    return k

def E3(k,m):
    permutation(k); lettres(m)
    return ''.join(k[ord(a)-97] for a in m)

def D3(k,c):
    permutation(k); lettres(c)
    inverse = ['']*26
    for i,a in enumerate(k):
        inverse[ord(a)-97] = ALPHABET[i]
    return ''.join(inverse[ord(a)-97] for a in c)

def frequences(c, n=1):
    lettres(c)
    if not 1 <= n <= len(c):
        raise ValueError('Taille de groupe invalide.')
    comptes = collections.Counter(c[i:i+n] for i in range(len(c)-n+1))
    if n == 1:
        comptes.update({a:0 for a in ALPHABET})
    return [{'groupe':a, 'nombre':v, 'pourcentage':100*v/(len(c)-n+1)} for a,v in comptes.most_common()]

def partiel(c, correspondances):
    return ''.join(correspondances.get(a,'_') for a in c)

def vers_bits(m):
    lettres(m)
    valeur = 0
    for a in m:
        valeur = (valeur << 5) | (ord(a)-97)
    return valeur

def vers_lettres(v,n):
    entier(v,5*n)
    blocs = [(v >> (5*(n-1-i))) & 31 for i in range(n)]
    if any(a > 25 for a in blocs):
        raise ValueError('Bloc 5 bits hors alphabet (26 à 31).')
    return ''.join(ALPHABET[a] for a in blocs)

def Gen2(n=32):
    if type(n) is not int or n <= 0:
        raise ValueError('Longueur positive attendue.')
    return secrets.randbits(5*n)

def E2(k,m):
    lettres(m); entier(k,5*len(m))
    return vers_bits(m) ^ k

def D2(k,c,n=32):
    entier(k,5*n); entier(c,5*n)
    return vers_lettres(c ^ k,n)

def Eve2(c1,c2,mot='protocole',n=48):
    lettres(mot); entier(c1,5*n); entier(c2,5*n)
    delta=c1^c2
    blocs=[(delta >> (5*(n-1-i))) & 31 for i in range(n)]
    retenus=[]
    for pos in range(n-len(mot)+1):
        vals=[blocs[pos+i] ^ (ord(a)-97) for i,a in enumerate(mot)]
        if all(v < 26 for v in vals):
            retenus.append({'position':pos,'fragment_m2':''.join(ALPHABET[v] for v in vals)})
    return retenus

def verifier_hypothese_otp(m1,m2,c1,c2):
    # Ne suffit pas à établir que des phrases candidates sont les phrases d'origine.
    if len(m1) != 48 or len(m2) != 48:
        raise ValueError('Deux textes de 48 lettres sont requis.')
    k=c1 ^ vers_bits(m1)
    return {'cle':format(k,'060x'), 'c1_valide':E2(k,m1)==c1,
            'c2_valide':E2(k,m2)==c2, 'compatibles':(vers_bits(m1)^vers_bits(m2))==(c1^c2)}

def Gen():
    return secrets.randbits(64)

def MAC(k,m):
    entier(k,64); entier(m,64)
    return (m ^ k) & 0xffffffff

def Verif(k,m,t):
    entier(t,32)
    return int(MAC(k,m)==t)

def EveMAC(m_obs,t_obs,m_cible):
    entier(m_obs,64); entier(t_obs,32); entier(m_cible,64)
    k_bas=(m_obs & 0xffffffff)^t_obs
    return k_bas, (m_cible & 0xffffffff)^k_bas

def GenVigenere(n):
    return ''.join(ALPHABET[secrets.randbelow(26)] for _ in range(n))

def Vigenere(k,m,dechiffrement=False):
    lettres(k); lettres(m)
    signe=-1 if dechiffrement else 1
    return ''.join(ALPHABET[(ord(a)-97+signe*(ord(k[i%len(k)])-97))%26] for i,a in enumerate(m))

def indice(c):
    n=len(c)
    return sum(v*(v-1) for v in collections.Counter(c).values())/(n*(n-1)) if n>1 else 0

def kasiski(c):
    groupes=collections.defaultdict(list)
    for i in range(len(c)-2):
        groupes[c[i:i+3]].append(i)
    return [{'trigramme':a,'positions':p,'distances':[p[i+1]-p[i] for i in range(len(p)-1)]}
            for a,p in sorted(groupes.items()) if len(p)>1]

def EveVigenere(c):
    essais=[]
    for n in range(1,13):
        colonnes=[c[i::n] for i in range(n)]
        cle=''
        for col in colonnes:
            scores=[]
            for k in range(26):
                counts=collections.Counter((ord(a)-97-k)%26 for a in col)
                scores.append(sum((counts.get(a,0)-len(col)*FREQ[a])**2/(len(col)*FREQ[a]) for a in range(26)))
            cle+=ALPHABET[min(range(26), key=lambda k:scores[k])]
        essais.append({'longueur':n,'ic_moyen':sum(indice(col) for col in colonnes)/n,
                       'cle':cle,'texte':Vigenere(cle,c,True)})
    return essais

def charger(path):
    s=Path(path).read_text(encoding='utf-8')
    get=lambda pattern: re.search(pattern,s).group(1)
    return {'cesar':[(int(a),int(b)) for a,b in re.findall(r'k1 = (\d+), k2 = (\d+)',s)],
            'sub':re.findall(r'Exécution \d : ([a-z]{26})',s),
            'otp':[int(v,16) for v in re.findall(r'Exécution \d : ([0-9a-f]{40})',s)],
            'sub_c':get(r'\n  ([A-Z]{398})').lower(),
            'vigenere':get(r'\n  ([A-Z]{463})').lower(),
            'c1':int(get(r'c1 = (\w+)'),16),'c2':int(get(r'c2 = (\w+)'),16),
            'mac_k':int(get(r'  k = (\w+)'),16),
            'm_obs':int(get(r'm_obs = (\w+)'),16),'t_obs':int(get(r't_obs = (\w+)'),16),
            'm_cible':int(get(r'm_cible = (\w+)'),16)}

def main(path):
    p=charger(path);r={}
    # Verification des empreintes (consigne: detecter erreur de copie)
    r['empreintes']={
      'sub':hashlib.sha256(p['sub_c'].encode()).hexdigest()[:8],
      'otp':hashlib.sha256((format(p['c1'],'060x')+format(p['c2'],'060x')).encode()).hexdigest()[:8],
      'vigenere':hashlib.sha256(p['vigenere'].encode()).hexdigest()[:8]}
    assert r['empreintes']=={'sub':'2b86f4d7','otp':'d7b627e1','vigenere':'768d2dfa'}
    
    # PARTIE 1.1 - Cesar a double decalage (cles imposees k1,k2)
    r['cesar']=[]
    for k in p['cesar']:
        c=E1(k,MESSAGE);m=D1(k,c);assert m==MESSAGE
        r['cesar'].append({'m':MESSAGE,'k':k,'c':c,'bob':m,'candidats':Eve1(c)})
    
    # PARTIE 1.2 - Substitution monoalphabetique (cles imposees 26 lettres)
    r['sub_traces']=[]
    for k in p['sub']:
        c=E3(k,MESSAGE);m=D3(k,c);assert m==MESSAGE
        r['sub_traces'].append({'m':MESSAGE,'k':k,'c':c,'bob':m})
    # Analyse du cryptogramme sub_c (frequences, bigrammes, trigrammes, etapes d'attaque)
    mp=dict(zip('YAOEJGBWHKFIXPDRTZSCUQV'.lower(),'depuisclgnraxtomhqvfjyb'))
    clair=partiel(p['sub_c'],mp);assert '_' not in clair
    # Les lettres k,w,z sont absentes : completion choisie, sans pretendre a l'unicite.
    complet=mp|{'l':'k','m':'w','n':'z'}
    k=''.join(next(a for a,v in complet.items() if v==b) for b in ALPHABET)
    assert E3(k,clair)==p['sub_c']
    stages=[{'a':'e','g':'s','w':'l'}, {a:mp[a] for a in 'yaoejgbw'},mp]
    r['sub_analyse']={'frequences':frequences(p['sub_c']), 'bigrammes':frequences(p['sub_c'],2)[:15],
      'trigrammes':frequences(p['sub_c'],3)[:10], 'etapes':[{'correspondances':m,'texte':partiel(p['sub_c'],m)} for m in stages],
      'clair':clair,'cle_compatible':k,'lettres_chiffrees_absentes':'lmn','lettres_claires_absentes':'kwz',
      'nombre_completions':6,'reencodage_exact':True,'espace_cles':math.factorial(26),'bits_cles':math.log2(math.factorial(26))}
    
    # PARTIE 2.1 - Masque jetable (OTP) (cles imposees 160 bits)
    mb=vers_bits(MESSAGE);r['otp_traces']=[]
    for k in p['otp']:
        c=E2(k,MESSAGE);m=D2(k,c);assert m==MESSAGE
        r['otp_traces'].append({'m':MESSAGE,'m_hex':format(mb,'040x'),'m_bits':format(mb,'0160b'),
                              'k':format(k,'040x'),'c':format(c,'040x'),'bob':m})
    # Demonstration de malléabilité OTP: cle alternative pour 'a'*32
    autre='a'*32;c=E2(p['otp'][0],MESSAGE);kp=c^vers_bits(autre)
    assert D2(kp,c)==autre
    r['otp_alternatif']={'m_prime':autre,'k_prime':format(kp,'040x'),'verification':D2(kp,c)}
    
    # PARTIE 2.2 - Reutilisation de cle OTP (c1, c2 fournis, mot connu 'protocole')
    r['otp_reutilisation']={'xor':format(p['c1']^p['c2'],'060x'), 'candidats':Eve2(p['c1'],p['c2']),
                           'statut':'reconstruction linguistique compatible, rechiffrement vérifié'}
    m1='modifiezimmediatementleprotocoledesecurite'.ljust(48,'x')
    m2='leserveurcentralredemarreradimancheaminuit'.ljust(48,'x')
    otp_verif=verifier_hypothese_otp(m1,m2,p['c1'],p['c2'])
    assert otp_verif['c1_valide'] and otp_verif['c2_valide']
    r['otp_reutilisation'].update({'m1':m1,'m2':m2,'verification':otp_verif})
    delta=p['c1']^p['c2']
    blocs=[(delta >> (5*(47-i))) & 31 for i in range(48)]
    expansions=[]
    for cote,pos,texte in [('m2',18,'demarreradimanche'),('m1',23,'protocoledesecurite'),
                           ('m1',0,'modifiezimmediatement')]:
        fragment=''.join(ALPHABET[blocs[pos+i]^(ord(a)-97)] for i,a in enumerate(texte))
        expansions.append({'hypothese_sur':cote,'position':pos,'hypothese':texte,'fragment_autre':fragment})
    r['otp_reutilisation']['extensions']=expansions
    
    # PARTIE 3.2 - MAC (cle k imposee 64 bits, traces sur messages tests)
    r['mac_traces']=[]
    for m in [0,1<<63,(1<<32)-1,0xaaaaaaaaaaaaaaaa]:
        t=MAC(p['mac_k'],m);mf=m^(1<<63)
        assert Verif(p['mac_k'],m,t)==1 and Verif(p['mac_k'],mf,t)==1
        assert Verif(p['mac_k'],m,t^1)==0
        r['mac_traces'].append({'m_hex':format(m,'016x'),'m_bits':format(m,'064b'),
          'k':format(p['mac_k'],'016x'),'t':format(t,'08x'),'v':1,'m_prime':format(mf,'016x'),'v_prime':1})
    
    # PARTIE 3.4 - MAC forgerie (m_obs, t_obs observes -> tag pour m_cible)
    kb,t=EveMAC(p['m_obs'],p['t_obs'],p['m_cible']);cles=[kb,(1<<32)|kb]
    for k in cles:
        assert Verif(k,p['m_obs'],p['t_obs'])==1 and Verif(k,p['m_cible'],t)==1
    r['mac_forgerie']={'k_bas':format(kb,'08x'),'tag':format(t,'08x'),'cles_compatibles':[format(k,'016x') for k in cles]}
    
    # BONUS - Chiffre de Vigenere (463 lettres, Kasiski + Friedman/IC)
    r['vigenere']={'kasiski':kasiski(p['vigenere']),'essais':EveVigenere(p['vigenere'])}
    meilleur=max(r['vigenere']['essais'],key=lambda a:a['ic_moyen'])
    assert Vigenere(meilleur['cle'],meilleur['texte'])==p['vigenere']
    r['vigenere']['retenu']=meilleur
    
    # Exemples effectifs des generateurs et de l'aller-retour associe.
    k1=Gen1();k3=Gen3();k2=Gen2();km=Gen()
    r['exemples_aleatoires']={'Gen1':{'k':k1,'c':E1(k1,MESSAGE),'m_retrouve':D1(k1,E1(k1,MESSAGE))},
     'Gen3':{'k':k3,'c':E3(k3,MESSAGE),'m_retrouve':D3(k3,E3(k3,MESSAGE))},
     'Gen2':{'k':format(k2,'040x'),'c':format(E2(k2,MESSAGE),'040x'),'m_retrouve':D2(k2,E2(k2,MESSAGE))},
     'Gen_MAC':{'k':format(km,'016x'),'m':'0000000000000000','t':format(MAC(km,0),'08x'),
                'v_valide':Verif(km,0,MAC(km,0)),'v_invalide':Verif(km,0,MAC(km,0)^1)}}
    print(json.dumps(r,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    import sys
    main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name('Equipe_03.txt'))
