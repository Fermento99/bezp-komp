#Paweł Kajanek

import sys


SPECIAL = "00100000"

def xor(str1, str2):
    if len(str1) != len(str2):
        raise IndexError("str1 and str2 are not the same length")
    out = ''
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            out += '0'
        else:
            out += '1'
    return out

def decrypt_char(c, k):
    p = xor(k, c)
    p = int('0b'+p, 2)
    print(chr(p), end='')

def check_key(k, c):
    p = xor(k, c)
    p = int('0b'+p, 2)
    if p in range(44,58) or p in range(65, 91) or p in range(97, 123) or p == 32:
        return True
    return False

def get_cryptograms(file):
    f = open(file, "r")
    raw = f.read()
    f.close()

    tab = [c.split(" ") for c in raw.splitlines()]
    return tab

def determin_key(crypto, pos):
    keys = []
    for c1 in range(len(crypto)):
        if len(crypto[c1]) <= pos:
            continue
        for c2 in range(c1, len(crypto)):
            if len(crypto[c2]) <= pos:
                continue
            x = xor(crypto[c1][pos], crypto[c2][pos])
            if x.startswith('010'):
                keys.append(xor(crypto[c1][pos], SPECIAL))
                keys.append(xor(crypto[c2][pos], SPECIAL))
    
    out = []
    for k in keys:
        f = True
        for c in crypto:
            if len(c) <= pos:
                continue
            if not check_key(c[pos],k):
                f = False
        
        if f and k not in out:
            out.append(k)
    return out

def decrypt(c, k):
    count = [len(keys) for keys in k]
    index = [0 for key in k]
    for i in range(len(c)):
        if len(k[i]) > 1:
            print('{', end='')
            for a in k[i]:
                decrypt_char(c[i], a)
            print('}', end='')
        elif len(k[i]) == 1:
            decrypt_char(c[i], k[i][0])
        else:
            print('?', end='')
    

if __name__ == "__main__":
    cryptograms = get_cryptograms(sys.argv[1])
    l = max([len(c) for c in cryptograms])
    keys = []
    for i in range(l):
        keys.append(determin_key(cryptograms, i))
    
    for crpt in cryptograms:
        decrypt(crpt, keys)
        print()
    