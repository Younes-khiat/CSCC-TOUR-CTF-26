````markdown
# Who Are You (Network Forensics)

### Step1 (Understanding the challenge):
> ##### We are given a pcap file `Who_Are_You.pcap`. The challenge name "Who Are You" suggests we need to identify someone or something from the network capture.

### Step2 (Analyzing the pcap):
> ###### We open the pcap in **Wireshark** and examine the captured packets. We look for identifying information such as:
> - HTTP headers (User-Agent, Host, etc.)
> - DNS queries revealing hostnames
> - Protocol-specific identifiers
> - Any cleartext credentials or identity markers

### Step3 (Identifying the target):
> ###### By carefully analyzing the network traffic, we uncover the identity hidden within the packets. The key information is found by examining the relevant protocol fields and reconstructing the communication flow.

> ###### Refer to the detailed writeup PDF for the full step-by-step walkthrough.
````
