solution 
import requests
from Crypto.Util.number import inverse, long_to_bytes
import sympy

def factorize_n(N):
    factors = list(sympy.factorint(N).keys())
    if len(factors) == 2:
        return factors[0], factors[1]
    else:
        print("error")
        return None, None

N = "li yjik "
e = 3
ct = "li yjik"

p, q = factorize_n(N)

if p and q:
    print(f"p: {p}")
    print(f"q: {q}")

    phi_n = (p - 1) * (q - 1)
    print(f"phi(n): {phi_n}")
    
    d = inverse(e, phi_n)
    print(f"private key d: {d}")
    
    M = pow(ct, d, N)
    flag = long_to_bytes(M).decode('utf-8', errors='ignore')
    print("decrypted flag:",flag)
else:
    print("problem")