````markdown
# p6ac4et (DNS Exfiltration)

### Step1 (Understanding the challenge):
> ##### We are given a pcap file `packetX.pcap` containing a large amount of network traffic. The description hints that "paying attention to the names being sent reveals the hidden message" — this strongly suggests **DNS exfiltration**.

### Step2 (Analyzing the pcap):
> ###### We open the pcap in **Wireshark** and apply a DNS filter:
> ```
> dns
> ```
> ###### Among the DNS queries, we notice unusual domain names being queried. These are not normal domains — they contain encoded/suspicious subdomains that look like fragments of data being exfiltrated through DNS queries.

### Step3 (Extracting the flag):
> ###### We carefully examine the DNS query names (the subdomains being resolved). By collecting and arranging the relevant pieces from the DNS queries in order, we reconstruct the hidden message.
> ###### The flag is hidden across the DNS query names — extracting and concatenating the correct pieces reveals:

```
CSCC{f3l0uj4_chk0n_dns}
```
````
