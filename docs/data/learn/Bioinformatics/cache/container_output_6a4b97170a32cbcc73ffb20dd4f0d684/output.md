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
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="nan", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="nan", style="dashed"]
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
"STATE_A" -> "STATE_B" [label="0.442928960042021"]
"STATE_A" -> "STATE_E" [label="0.054190866820284914"]
"STATE_A" -> "STATE_F" [label="0.5028801731376941"]
"STATE_B" -> "STATE_C" [label="0.9474969037501693"]
"STATE_B" -> "STATE_D" [label="0.05250309624983077"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.3055450621119093"]
"STATE_F" -> "STATE_E" [label="0.6944549378880907"]
"STATE_SOURCE" -> "STATE_A" [label="0.32780355897096763"]
"STATE_SOURCE" -> "STATE_B" [label="0.5611876621742033"]
"STATE_SOURCE" -> "STATE_D" [label="0.11100877885482895"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.014832475330121398", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.3328534521302139", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.6523140725396648", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.3856561675893814", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.41620679642493114", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.1981370359856874", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.8007566361700912", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.04092420679138892", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.15831915703851993", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.30218275273948375", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.27285040778512987", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.42496683947538644", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.31276805123935636", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.40656104576977836", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.2806709029908653", style="dashed"]
}
```

Applying Baum-Welch learning for 3 cycles ...

 1. New transition probabilities:
    * SOURCE→B = 0.9226123403947917
    * SOURCE→A = 0.040952567926599175
    * SOURCE→D = 0.0364350916786091
    * D→A = 1.0
    * A→B = 0.5764722621482435
    * A→F = 0.40819275961663554
    * A→E = 0.015334978235120904
    * B→C = 0.8037334233202656
    * B→D = 0.19626657667973427
    * C→F = 1.0
    * F→B = 0.5727518610523413
    * F→E = 0.4272481389476588
    * E→A = 1.0

    New emission probabilities:
    * (A, x) = 0.28317336640721774
    * (A, y) = 0.5691380817212273
    * (E, z) = 0.7316341828939239
    * (A, z) = 0.14768855187155508
    * (C, z) = 0.7593081151609289
    * (B, z) = 0.7596646682126519
    * (F, y) = 0.04345571223225823
    * (B, x) = 0.18892134289141
    * (D, z) = 0.9960938666443724
    * (F, z) = 0.8709114292802557
    * (B, y) = 0.05141398889593808
    * (D, y) = 0.0035554787420818846
    * (E, y) = 0.15530363809333034
    * (C, y) = 0.06693513112760656
    * (E, x) = 0.11306217901274557
    * (C, x) = 0.17375675371146465
    * (D, x) = 0.0003506546135458451
    * (F, x) = 0.08563285848748586

 1. New transition probabilities:
    * SOURCE→B = 0.9286041399786551
    * SOURCE→A = 0.030364812501393522
    * SOURCE→D = 0.04103104751995143
    * D→A = 1.0
    * A→B = 0.5611620276386833
    * A→F = 0.42857859438184825
    * A→E = 0.01025937797946805
    * B→C = 0.544334102657392
    * B→D = 0.4556658973426077
    * F→B = 0.630092084420863
    * F→E = 0.369907915579137
    * E→A = 1.0
    * C→F = 1.0

    New emission probabilities:
    * (A, x) = 0.37341778098229217
    * (A, y) = 0.48776395725815647
    * (E, z) = 0.651279516828542
    * (A, z) = 0.1388182617595513
    * (C, z) = 0.9314205674141743
    * (B, z) = 0.7629553864330778
    * (F, y) = 0.06327150018787758
    * (B, x) = 0.16052765026146873
    * (D, z) = 0.9987672880684514
    * (F, z) = 0.7847857915533103
    * (B, y) = 0.07651696330545359
    * (D, y) = 0.0012111277393856892
    * (E, y) = 0.318759950645521
    * (C, y) = 0.0345246627751449
    * (E, x) = 0.029960532525937018
    * (C, x) = 0.03405476981068082
    * (D, x) = 2.158419216299836e-05
    * (F, x) = 0.1519427082588122

 1. New transition probabilities:
    * SOURCE→B = 0.9942877159408319
    * SOURCE→A = 0.0014257830481250741
    * SOURCE→D = 0.0042865010110430335
    * D→A = 1.0
    * A→B = 0.46145323930382337
    * A→F = 0.5347379873691611
    * A→E = 0.003808773327015512
    * B→C = 0.4447294493877592
    * B→D = 0.5552705506122408
    * F→B = 0.6591543582193055
    * F→E = 0.34084564178069465
    * E→A = 1.0
    * C→F = 1.0

    New emission probabilities:
    * (A, x) = 0.4518777759547301
    * (A, y) = 0.42588388793289805
    * (E, z) = 0.43353272357052164
    * (A, z) = 0.12223833611237192
    * (C, z) = 0.974211044074626
    * (B, z) = 0.8174450337599177
    * (F, y) = 0.03944446185287677
    * (B, x) = 0.10467390489185226
    * (D, z) = 0.9988328559679983
    * (F, z) = 0.8033179907903832
    * (B, y) = 0.07788106134823011
    * (D, y) = 0.001153813066882197
    * (E, y) = 0.5607249765762802
    * (C, y) = 0.019982437639297697
    * (E, x) = 0.005742299853198215
    * (C, x) = 0.0058065182860762374
    * (D, x) = 1.3330965119510797e-05
    * (F, x) = 0.15723754735674025


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
"STATE_A" -> "STATE_B" [label="0.4614148148593656"]
"STATE_A" -> "STATE_E" [label="0.003907601046701501"]
"STATE_A" -> "STATE_F" [label="0.534677584093933"]
"STATE_B" -> "STATE_C" [label="0.4447405012875017"]
"STATE_B" -> "STATE_D" [label="0.5552594987124984"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.6591225337125629"]
"STATE_F" -> "STATE_E" [label="0.34087746628743715"]
"STATE_SOURCE" -> "STATE_A" [label="0.0015253254504899272"]
"STATE_SOURCE" -> "STATE_B" [label="0.9940894890941037"]
"STATE_SOURCE" -> "STATE_D" [label="0.004385185455406412"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.12230164561868632", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.4518422232877438", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.42585613109357", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.8172998438067757", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.1047424821472081", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.0779576740460163", style="dashed"]
"STATE_C" -> "SYMBOL_z" [label="0.9740188384230991", style="dashed"]
"STATE_C" -> "SYMBOL_y" [label="0.020076414714883233", style="dashed"]
"STATE_C" -> "SYMBOL_x" [label="0.005904746862017632", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.9986332659882019", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.0001132969760267028", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.0012534370357714657", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.43350267276869103", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.005840547688891549", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.5606567795424174", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.8031770376790793", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.1572903602486656", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.03953260207225509", style="dashed"]
}
```

</div>

`{bm-enable-all}`

