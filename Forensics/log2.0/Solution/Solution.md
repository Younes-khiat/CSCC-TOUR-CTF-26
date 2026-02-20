````markdown
# log2.0 (Log Analysis)

### Step1 (Understanding the challenge):
> ##### We are given a compressed archive `log2.0.tar.gz` containing log files from a system that experienced an abnormal spike in network activity. The logs are filled with automated scans and anonymous connections. Our goal is to find the **real attacker's name and source IP** hidden among the noise.

### Step2 (Filtering the noise):
> ###### We extract the archive and start examining the log files:
> ```bash
> tar -xzf log2.0.tar.gz
> ```
> ###### The logs contain a lot of noise from automated scanners and bots. We need to filter out the legitimate traffic and automated scans to identify suspicious activity.
> ###### We look for patterns that stand out — unusual user agents, repeated failed attempts, or connections that don't match the automated scan patterns.

### Step3 (Identifying the attacker):
> ###### After careful analysis and filtering, we identify an attacker with the name **anonymos** operating from a specific IP address. This stands out from the automated traffic as the real malicious actor.
> ###### The attacker's IP is **185.199.109.153**.

**Flag:**
```
CSCC{anonymos_185.199.109.153}
```
````
