# CSCC-TOUR-CTF-26

> **Official repository for the CSCC Club's intern activity — *CSCC TOUR CTF 2026*.** This CTF was organized by the members of **Club CSCC** as a hands-on cybersecurity competition covering Web Exploitation, Reverse Engineering, Cryptography, Forensics, and OSINT.

---

## 📁 Repository Structure

```
├── Web/              # Web exploitation challenges
├── Reverse/          # Reverse engineering challenges
├── Crypto/           # Cryptography challenges
├── Forensics/        # Digital forensics challenges
└── Osint/            # Open-source intelligence challenges
```

Each challenge follows the same directory layout:
```
Challenge-Name/
├── Challenge/        # Challenge files (source, Dockerfile, docker-compose, assets)
│   ├── challenge.yml / *.yaml
│   ├── docker-compose.yml   (if hosting is required)
│   ├── Dockerfile
│   └── ...
└── Solution/         # Writeup and solve scripts
    ├── Solution.md
    └── ...
```

---

## 🌐 Web

| # | Challenge | Difficulty | Author | Description | Hosted |
|---|-----------|-----------|--------|-------------|--------|
| 1 | **Inspector1** | Easy | Houddini | Web pentesters have sharp eyes, focus and look carefully! | ✅ Port `5001` |
| 2 | **Inspector2** | Hard | Houddini | You'll probably need Sharingan for this one | ✅ Port `5000` |
| 3 | **LFLF** | Easy | Sx1im | The flag is hidden somewhere in the system files. Can you find it? | ✅ Port `5002` |
| 4 | **Manager** | Medium | Sx1im | Just a simple file manager, what can go wrong? | ✅ Port `5003` |
| 5 | **Remote** | Medium | Sx1im | You think you won when you got LFI last time? Good luck now. | ✅ Port `5004` |
| 6 | **SSTore** | Medium | Sx1im | Welcome to our store, enjoy your shopping! | ✅ Port `5005` |

### 🐳 Hosting Web Challenges

All web challenges require **Docker** to run. Clone the repo and use `docker compose` to build and start each challenge:

```bash
git clone https://github.com/<org>/CSCC-TOUR-CTF.git
cd CSCC-TOUR-CTF
```

#### Inspector1 — Port `5001`
```bash
cd Web/inspector1/challenge
docker compose up -d --build
# Access at http://localhost:5001
```

#### Inspector2 — Port `5000`
```bash
cd Web/inspector2/challenge
docker compose up -d --build
# Access at http://localhost:5000
```

#### LFLF — Port `5002`
```bash
cd Web/LFLF/Challenge
docker compose up -d --build
# Access at http://localhost:5002
```

#### Manager — Port `5003`
```bash
cd Web/manager/Challenge
docker compose up -d --build
# Access at http://localhost:5003
```

#### Remote — Port `5004`
```bash
cd Web/Remote/Challenge
docker compose up -d --build
# Access at http://localhost:5004
```

#### SSTore — Port `5005`
```bash
cd Web/SSTore/Challenge
docker compose up -d --build
# Access at http://localhost:5005
```

> **To stop a challenge:**
> ```bash
> docker compose down
> ```

---

## 🔓 Reverse Engineering

| # | Challenge | Difficulty | Author | Description | Hosted |
|---|-----------|-----------|--------|-------------|--------|
| 1 | **XOR Me Maybe** | Easy | Malek | A simple binary that uses a repeating key to modify your input | ❌ |
| 2 | **The Magical Password** | Medium | c0ff33 | Welcome to the Magical Password Challenge! | ✅ Port `4445` |
| 3 | **Layers of Obscurity** | Medium | Malek | Multiple transformations: byte reversal, XOR with repeating key, and swapping adjacent byte pairs | ❌ |
| 4 | **Vibe Coder's AES** | Hard | Malek | The vibe coder made a critical bug in his code… | ❌ |

### 🐳 Hosting Reverse Challenges

Only **The Magical Password** requires hosting — it runs as a network service via `ncat`:

```bash
git clone https://github.com/<org>/CSCC-TOUR-CTF.git
cd CSCC-TOUR-CTF
```

#### The Magical Password — Port `4445`
```bash
cd Reverse/The_Magical_Password/challenge
docker compose up -d --build
# Connect at: nc localhost 4445
```

> **To stop:**
> ```bash
> docker compose down
> ```

---

## 🔐 Cryptography

| # | Challenge | Difficulty | Author | Description |
|---|-----------|-----------|--------|-------------|
| 1 | **Warmup** | Easy | — | Three-part encoding: ROT13, Triple Base64, and Hex → Base64 |
| 2 | **Rolling** | Easy | Sx1im | Keeep Rooolllling — circular bit-shift cipher |
| 3 | **Science** | Easy | Sx1im | Nostalgic — DNA / amino acid cipher |
| 4 | **Small** | Medium | C0ff33 | RSA with small primes — classic RSA attack |

---

## 🔍 Forensics

| # | Challenge | Difficulty | Author | Description |
|---|-----------|-----------|--------|-------------|
| 1 | **Hidden Beeps** | Easy | — | Decode DTMF tones from an audio recording |
| 2 | **imageX** | Easy | — | Image steganography |
| 3 | **log2.0** | Easy | — | Log analysis — find the attacker's name & IP |
| 4 | **log2.1** | Medium | — | Log analysis — identify the real attack technique & timestamp |
| 5 | **p6ac4et** | Medium | — | DNS exfiltration from a pcap capture |
| 6 | **Silent Pixels** | Medium | — | Pixel-level image steganography (StegSolve) |
| 7 | **Who Are You** | Medium | — | Network forensics — pcap analysis |

---

## 🕵️ OSINT

| # | Challenge | Difficulty | Author | Description |
|---|-----------|-----------|--------|-------------|
| 1 | **Find The Place** | Easy | — | Geolocation from a photograph |
| 2 | **Kempoo_ka** | Medium | Houddini | Find the person who brought Kempo to Algeria |
| 3 | **middleware:middleware...** | Medium | Houddini | A high-severity CVE in Next.js disclosed by an Algerian researcher |
| 4 | **The Forgotten Page** | Medium | — | Identify a book from a single page |

---

## 🛠️ Quick Start — Host All Challenges at Once

```bash
# Clone the repository
git clone https://github.com/<org>/CSCC-TOUR-CTF.git
cd CSCC-TOUR-CTF

# Start all web challenges
for dir in Web/inspector1/challenge Web/inspector2/challenge Web/LFLF/Challenge Web/manager/Challenge Web/Remote/Challenge Web/SSTore/Challenge; do
  (cd "$dir" && docker compose up -d --build)
done

# Start the reverse challenge
(cd Reverse/The_Magical_Password/challenge && docker compose up -d --build)
```

### Port Summary

| Challenge | Category | Port | Access |
|-----------|----------|------|--------|
| Inspector1 | Web | `5001` | `http://localhost:5001` |
| Inspector2 | Web | `5000` | `http://localhost:5000` |
| LFLF | Web | `5002` | `http://localhost:5002` |
| Manager | Web | `5003` | `http://localhost:5003` |
| Remote | Web | `5004` | `http://localhost:5004` |
| SSTore | Web | `5005` | `http://localhost:5005` |
| The Magical Password | Reverse | `4445` | `nc localhost 4445` |

---

## 👥 Contributors

- **Houddini** — Web, OSINT
- **Sx1im** — Web, Crypto
- **Malek** — Reverse Engineering
- **C0ff33** — Reverse Engineering, Crypto
