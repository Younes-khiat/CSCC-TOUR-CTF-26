# Science 

## Step1 : base64 decode

```
selim@debian:~/ghidra/ghidra_11.4_PUBLIC$ echo -n 'Q3lzU2VyQ3lzQ3lze1BoZTFBc240TGV1TGV1VHlyX1VTZXIxQXNuR2x5X0FzcDRDeXNfU2VyQ3lz
MTNBc25DeXMzX0x5c0FzbjBUcnBMZXUzQXNwR2x5R2x1fQo=' | base64 -d
CysSerCysCys{Phe1Asn4LeuLeuTyr_USer1AsnGly_Asp4Cys_SerCys13AsnCys3_LysAsn0TrpLeu3AspGlyGlu}
``` 

## Step2 : DNA cipher using dcode.fr

**CysSerCysCys{Phe1Asn4LeuLeuTyr_USer1AsnGly_Asp4Cys_SerCys13AsnCys3_LysAsn0TrpLeu3AspGlyGlu}**
we get :
**CSCCF[NB]LLYUS[NB]G[DB]CSC[NB]CK[NB]WL[DB]G[EZ]**

### finally we replcae the [NB] and [DG] with the numbers and signs from the first decoded string and we get the flag

**CSCC{F1n4lly_us1ng_B4c_sc13nc3_kn0wl3dge}**
