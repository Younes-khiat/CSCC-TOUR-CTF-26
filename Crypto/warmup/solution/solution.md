````markdown
# Warmup (Multi-Encoding)

### Step1 (Understanding the challenge):
> ##### We are given a file `challenge.txt` containing three encoded parts. Each part uses a different encoding method. We need to decode all three parts and concatenate them to reconstruct the flag.
> ```
> [part 1] pfpp{Pelc10_
> [part 2] VFZSV1psWnFUbmxsVVQwOQ==
> [part 3] \x5a\x6c\x56\x75\x58\x30\x59\x77\x63\x6c\x39\x49\x4e\x47\x4e\x72\x4d\x33\x49\x6b\x4a\x48\x30\x3d
> ```

### Step2 (Decoding Part 1 — ROT13):
> ###### The first part `pfpp{Pelc10_` looks like a ROT13-encoded string. Applying ROT13 decryption:
> ```
> pfpp{Pelc10_  →  cscc{Cryp10_
> ```
> ###### We get the beginning of our flag: **cscc{Cryp10_**

### Step3 (Decoding Part 2 — Triple Base64):
> ###### The second part `VFZSV1psWnFUbmxsVVQwOQ==` is Base64 encoded. But it requires **three rounds** of Base64 decoding:
> ```
> VFZSV1psWnFUbmxsVVQwOQ==  →  TVRWZlZqTnllUT09  (1st base64)
> TVRWZlZqTnllUT09          →  MTVfVjNyeQ==       (2nd base64)
> MTVfVjNyeQ==              →  15_V3ry            (3rd base64)
> ```
> ###### We get the second part: **15_V3ry**

### Step4 (Decoding Part 3 — Hex to ASCII then Base64):
> ###### The third part contains hex-escaped bytes. First we convert the hex bytes to ASCII:
> ```
> \x5a\x6c\x56\x75\x58\x30\x59\x77\x63\x6c\x39\x49\x4e\x47\x4e\x72\x4d\x33\x49\x6b\x4a\x48\x30\x3d
> →  ZlVuX0Ywcl9INGNrM3IkJH0=
> ```
> ###### The result is a Base64 string. Decoding it:
> ```
> ZlVuX0Ywcl9INGNrM3IkJH0=  →  fUn_F0r_H4ck3r$$}
> ```
> ###### We get the third part: **fUn_F0r_H4ck3r$$}**

### Step5 (Assembling the flag):
> ###### We concatenate all three decoded parts:
> ```
> cscc{Cryp10_ + 15_V3ry + fUn_F0r_H4ck3r$$}
> ```

**Flag:**
```
cscc{Cryp10_15_V3ry_fUn_F0r_H4ck3r$$}
```
````
