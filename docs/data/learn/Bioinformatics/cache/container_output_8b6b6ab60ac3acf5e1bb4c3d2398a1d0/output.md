<div style="border:1px solid black;">

`{bm-disable-all}`

Deriving HMM probabilities using the following settings...

```
transitions:
  SOURCE: [A, B, D]
  A: [B, E ,F]
  B: [C, D]
  C: [F]
  D: [A]
  E: [A]
  F: [E, B]
emissions:
  SOURCE: []
  A: [x, y, z]
  B: [x, y, z]
  C: []  # C is non-emitting
  D: [x, y, z]
  E: [x, y, z]
  F: [x, y, z]
source_state: SOURCE
sink_state: SINK  # Must not exist in HMM (used only for Viterbi graph)
emission_seq: [z, z, x, z, z, z, y, z, z, z, z, y, x]
cycles: 3
pseudocount: 0.0001

```

The following HMM was produced (no probabilities) ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_D" [label="D"]
"STATE_E" [label="E"]
"STATE_F" [label="F"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_B" [label="nan"]
"STATE_A" -> "STATE_E" [label="nan"]
"STATE_A" -> "STATE_F" [label="nan"]
"STATE_B" -> "STATE_C" [label="nan"]
"STATE_B" -> "STATE_D" [label="nan"]
"STATE_C" -> "STATE_F" [label="nan"]
"STATE_D" -> "STATE_A" [label="nan"]
"STATE_E" -> "STATE_A" [label="nan"]
"STATE_F" -> "STATE_B" [label="nan"]
"STATE_F" -> "STATE_E" [label="nan"]
"STATE_SOURCE" -> "STATE_A" [label="nan"]
"STATE_SOURCE" -> "STATE_B" [label="nan"]
"STATE_SOURCE" -> "STATE_D" [label="nan"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="nan", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="nan", style="dashed"]
}
```

The following HMM was produced after applying randomized probabilities ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_D" [label="D"]
"STATE_E" [label="E"]
"STATE_F" [label="F"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_B" [label="0.3506088059554482"]
"STATE_A" -> "STATE_E" [label="0.23144703836391511"]
"STATE_A" -> "STATE_F" [label="0.4179441556806367"]
"STATE_B" -> "STATE_C" [label="0.39076723626890214"]
"STATE_B" -> "STATE_D" [label="0.6092327637310979"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5930532936559136"]
"STATE_F" -> "STATE_E" [label="0.4069467063440864"]
"STATE_SOURCE" -> "STATE_A" [label="0.3486551016741398"]
"STATE_SOURCE" -> "STATE_B" [label="0.30098545597929416"]
"STATE_SOURCE" -> "STATE_D" [label="0.3503594423465661"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.4106339718254369", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.31970116445400976", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.2696648637205533", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.19102894341762833", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.36695631229933046", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.44201474428304127", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.7139475365317169", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.22776784562604088", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.05828461784224219", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.35411593932964786", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.5304032231032663", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.11548083756708596", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.15436004876344153", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.5130064765853755", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.3326334746511829", style="dashed"]
}
```

Applying Baum-Welch learning for 3 cycles ...

 1. New transition probabilities:
    * SOURCE→A = 0.5183038378917265
    * SOURCE→B = 0.3414358535486437
    * SOURCE→D = 0.14026030855962976
    * D→A = 1.0
    * B→C = 0.4893876592057337
    * B→D = 0.5106123407942663
    * C→F = 1.0
    * A→F = 0.431405261804243
    * A→B = 0.31674245890341796
    * A→E = 0.25185227929233905
    * F→B = 0.5444192993393085
    * F→E = 0.45558070066069106
    * E→A = 1.0

    New emission probabilities:
    * (E, z) = 0.7482285684380175
    * (A, z) = 0.7124498937056265
    * (B, x) = 0.1183058698476471
    * (C, z) = 0.7016080100091178
    * (D, z) = 0.5771881303695249
    * (D, y) = 0.04107342283369915
    * (F, z) = 0.7794234251021908
    * (B, y) = 0.27708434966848794
    * (E, y) = 0.06666489366741461
    * (B, z) = 0.6046097804838647
    * (A, y) = 0.15281554874070344
    * (C, x) = 0.11164417675237281
    * (C, y) = 0.18674781323850953
    * (F, x) = 0.06515913340180375
    * (F, y) = 0.15541744149600561
    * (D, x) = 0.381738446796776
    * (E, x) = 0.18510653789456794
    * (A, x) = 0.13473455755367023

 1. New transition probabilities:
    * SOURCE→A = 0.6965180604297475
    * SOURCE→B = 0.20291644623247718
    * SOURCE→D = 0.10056549333777536
    * D→A = 1.0
    * B→C = 0.4566501874543301
    * B→D = 0.54334981254567
    * A→F = 0.42362640141567964
    * A→B = 0.33324166475549244
    * A→E = 0.24313193382882783
    * C→F = 1.0
    * F→B = 0.5391302580928752
    * F→E = 0.46086974190712476
    * E→A = 1.0

    New emission probabilities:
    * (E, z) = 0.7336110380788181
    * (A, z) = 0.763426377100875
    * (B, x) = 0.11490895519726718
    * (C, z) = 0.6705481441971572
    * (D, z) = 0.5403489364796934
    * (D, y) = 0.03646295235912837
    * (F, z) = 0.777996756825875
    * (B, y) = 0.30492614075427565
    * (E, y) = 0.06736937645732276
    * (B, z) = 0.580164904048457
    * (A, y) = 0.13553083198759416
    * (C, x) = 0.15157809810055314
    * (C, y) = 0.17787375770228978
    * (F, x) = 0.07749006111134185
    * (F, y) = 0.14451318206278296
    * (D, x) = 0.4231881111611783
    * (E, x) = 0.19901958546385934
    * (A, x) = 0.10104279091153069

 1. New transition probabilities:
    * SOURCE→A = 0.8521765656249575
    * SOURCE→B = 0.08420073277182107
    * SOURCE→D = 0.06362270160322148
    * D→A = 1.0
    * B→C = 0.4241817066140237
    * B→D = 0.5758182933859762
    * A→F = 0.4138215081969912
    * A→B = 0.36279768913535454
    * A→E = 0.22338080266765398
    * C→F = 1.0
    * F→B = 0.5190128892235419
    * F→E = 0.48098711077645784
    * E→A = 1.0

    New emission probabilities:
    * (E, z) = 0.7410905522065484
    * (A, z) = 0.816470530163523
    * (B, x) = 0.10117359435382782
    * (C, z) = 0.5897231266733372
    * (D, z) = 0.44789920623973667
    * (D, y) = 0.03331255182015798
    * (F, z) = 0.8089669197879186
    * (B, y) = 0.3427872720126575
    * (E, y) = 0.0578181588262359
    * (B, z) = 0.5560391336335145
    * (A, y) = 0.12263528809853937
    * (C, x) = 0.21946825233891357
    * (C, y) = 0.19080862098774956
    * (F, x) = 0.05834172721298762
    * (F, y) = 0.1326913529990938
    * (D, x) = 0.5187882419401053
    * (E, x) = 0.2010912889672157
    * (A, x) = 0.060894181737937716


The following HMM was produced after Baum-Welch learning was applied for 3 cycles ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_D" [label="D"]
"STATE_E" [label="E"]
"STATE_F" [label="F"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_B" [label="0.36278885247961074"]
"STATE_A" -> "STATE_E" [label="0.2234137785340938"]
"STATE_A" -> "STATE_F" [label="0.41379736898629543"]
"STATE_B" -> "STATE_C" [label="0.4241968672405756"]
"STATE_B" -> "STATE_D" [label="0.5758031327594243"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5190090874060609"]
"STATE_F" -> "STATE_E" [label="0.48099091259393917"]
"STATE_SOURCE" -> "STATE_A" [label="0.8520209593371564"]
"STATE_SOURCE" -> "STATE_B" [label="0.08427545013678003"]
"STATE_SOURCE" -> "STATE_D" [label="0.06370359052606367"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.060975888971246346", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.8163256324737809", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.12269847855497289", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.10124322138741162", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.5559723419309354", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.3427844366816531", style="dashed"]
"STATE_C" -> "SYMBOL_z" [label="0.5896462328034959", style="dashed"]
"STATE_C" -> "SYMBOL_x" [label="0.219502401618428", style="dashed"]
"STATE_C" -> "SYMBOL_y" [label="0.19085136557807608", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.5187326221534593", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.447864846785701", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.03340253106083973", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.20113094968231102", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.74096826172803", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.05790078858965901", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.05842419995300172", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.8088242725061667", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.13275152754083153", style="dashed"]
}
```

</div>

`{bm-enable-all}`

