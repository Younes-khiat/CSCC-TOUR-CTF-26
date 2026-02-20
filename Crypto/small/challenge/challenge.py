from Crypto.Util.number import getPrime, bytes_to_long , long_to_bytes 

flag = b"cscc{RSA_1s_w3ak_w1tH_sm4ll_Pr1m3$}"

pt = bytes_to_long(flag)

p = getPrime(512)
q = getPrime(512)

n = p * q

e = 3

ct = pow(pt,e,n)

print(f"N = {n}")
print(f"e = {e}")
print(f"CT = {ct}")