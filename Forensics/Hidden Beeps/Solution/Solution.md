````markdown
# Hidden Beeps (Audio Forensics - DTMF Decoding)

### Step1 (Understanding the challenge):
> ##### We are given an audio recording `chalng.wav` that contains mysterious beeps. The description says to "decode the tones" — this is a strong hint towards **DTMF (Dual-Tone Multi-Frequency)** signaling, the same tones used in telephone keypads.

### Step2 (Analyzing the audio):
> ###### We open the audio file in a tool like **Audacity** or a spectrogram viewer to visualize the tones. Each beep corresponds to a DTMF tone, which maps to a specific digit or character on a phone keypad.
> ###### We can also use online DTMF decoders or tools like `multimon-ng` to automatically decode the tones:
> ```bash
> multimon-ng -t wav -a DTMF chalng.wav
> ```

### Step3 (Decoding the flag):
> ###### By decoding each DTMF tone in sequence, we recover the encoded message. The decoded tones translate to characters that form the flag.

**Flag:**
```
CSCC{dtmf_4ud10_tr4nsm1ss10n}
```
````
