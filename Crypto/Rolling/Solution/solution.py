
import string
def rotate_left(byte, n):
   n = n % 8
   return ((byte << n) & 0xff) | (byte >> (8 - n))


with open("cipher.txt", "r") as f:
    bits = f.read().strip().split()

decoded = ""

for i in range(8):
    decoded = ""
    for byte in bits:
        b = int(byte, 2)
        decoded += chr(rotate_left(b, i))
    if all(c in string.printable for c in decoded):
        print(f"[Shift {i}]")
        print(decoded)

