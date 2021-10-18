<div style="border:1px solid black;">

`{bm-disable-all}`

Fragments from sequencer:

 * ATAGGAC scanned in 1.
 * ATTGGAC scanned in 55.
 * TTGGACA scanned in 30.
 * TGGACAA scanned in 30.
 * GGACAAT scanned in 30.
 * GACAATC scanned in 30.
 * ACAATCT scanned in 30.
 * ACAGTCT scanned in 1.
 * CAATCTC scanned in 30.
 * AATCTCG scanned in 30.
 * ATCTCGG scanned in 30.
 * TCTCGGG scanned in 30.
 * CTCGGGC scanned in 55.
 * CTCGTGC scanned in 1.


Fragments after being broken to k=4:

 * ATAG broken out 1 times, so it probably appears in the genome 0.01 times.
 * TAGG broken out 1 times, so it probably appears in the genome 0.01 times.
 * AGGA broken out 1 times, so it probably appears in the genome 0.01 times.
 * GGAC broken out 146 times, so it probably appears in the genome 1.0 times.
 * ATTG broken out 55 times, so it probably appears in the genome 1.0 times.
 * TTGG broken out 85 times, so it probably appears in the genome 1.0 times.
 * TGGA broken out 115 times, so it probably appears in the genome 1.0 times.
 * GACA broken out 120 times, so it probably appears in the genome 1.0 times.
 * ACAA broken out 120 times, so it probably appears in the genome 1.0 times.
 * CAAT broken out 120 times, so it probably appears in the genome 1.0 times.
 * AATC broken out 120 times, so it probably appears in the genome 1.0 times.
 * ATCT broken out 120 times, so it probably appears in the genome 1.0 times.
 * ACAG broken out 1 times, so it probably appears in the genome 0.01 times.
 * CAGT broken out 1 times, so it probably appears in the genome 0.01 times.
 * AGTC broken out 1 times, so it probably appears in the genome 0.01 times.
 * GTCT broken out 1 times, so it probably appears in the genome 0.01 times.
 * TCTC broken out 120 times, so it probably appears in the genome 1.0 times.
 * CTCG broken out 146 times, so it probably appears in the genome 1.0 times.
 * TCGG broken out 115 times, so it probably appears in the genome 1.0 times.
 * CGGG broken out 85 times, so it probably appears in the genome 1.0 times.
 * GGGC broken out 55 times, so it probably appears in the genome 1.0 times.
 * TCGT broken out 1 times, so it probably appears in the genome 0.01 times.
 * CGTG broken out 1 times, so it probably appears in the genome 0.01 times.
 * GTGC broken out 1 times, so it probably appears in the genome 0.01 times.


De Bruijn graph:

```{dot}
digraph {
graph[center=true, margin=0.1, nodesep=0.1, ranksep=0.1]
node[shape=none, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
"ATA" -> "TAG" [color="#fc0000", label=" 0.010"];
"TAG" -> "AGG" [color="#fc0000", label=" 0.010"];
"AGG" -> "GGA" [color="#fc0000", label=" 0.010"];
"GGA" -> "GAC" [color="#000000", label=" 1.000"];
"GAC" -> "ACA" [color="#000000", label=" 1.000"];
"ATT" -> "TTG" [color="#000000", label=" 1.000"];
"TTG" -> "TGG" [color="#000000", label=" 1.000"];
"TGG" -> "GGA" [color="#000000", label=" 1.000"];
"ACA" -> "CAA" [color="#000000", label=" 1.000"];
"ACA" -> "CAG" [color="#fc0000", label=" 0.010"];
"CAA" -> "AAT" [color="#000000", label=" 1.000"];
"AAT" -> "ATC" [color="#000000", label=" 1.000"];
"ATC" -> "TCT" [color="#000000", label=" 1.000"];
"TCT" -> "CTC" [color="#000000", label=" 1.000"];
"CAG" -> "AGT" [color="#fc0000", label=" 0.010"];
"AGT" -> "GTC" [color="#fc0000", label=" 0.010"];
"GTC" -> "TCT" [color="#fc0000", label=" 0.010"];
"CTC" -> "TCG" [color="#000000", label=" 1.000"];
"TCG" -> "CGG" [color="#000000", label=" 1.000"];
"TCG" -> "CGT" [color="#fc0000", label=" 0.010"];
"CGG" -> "GGG" [color="#000000", label=" 1.000"];
"GGG" -> "GGC" [color="#000000", label=" 1.000"];
"CGT" -> "GTG" [color="#fc0000", label=" 0.010"];
"GTG" -> "TGC" [color="#fc0000", label=" 0.010"];
}

```


Problem paths:

 * Src: ACA, Dst: TCT, Branch: CAA->AAT->ATC
 * Src: ACA, Dst: TCT, Branch: CAG->AGT->GTC
 * Src: None, Dst: GGA, Branch: ATA->TAG->AGG
 * Src: None, Dst: GGA, Branch: ATT->TTG->TGG
 * Src: TCG, Dst: None, Branch: CGG->GGG->GGC
 * Src: TCG, Dst: None, Branch: CGT->GTG->TGC
</div>

`{bm-enable-all}`

