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
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="nan", style="dashed"]
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
"STATE_A" -> "STATE_B" [label="0.39327444694150604"]
"STATE_A" -> "STATE_E" [label="0.30428013980469654"]
"STATE_A" -> "STATE_F" [label="0.30244541325379753"]
"STATE_B" -> "STATE_C" [label="0.19144899665878315"]
"STATE_B" -> "STATE_D" [label="0.8085510033412169"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5494925838411161"]
"STATE_F" -> "STATE_E" [label="0.4505074161588839"]
"STATE_SOURCE" -> "STATE_A" [label="0.4384910114258597"]
"STATE_SOURCE" -> "STATE_B" [label="0.02855695061765201"]
"STATE_SOURCE" -> "STATE_D" [label="0.5329520379564883"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.23881583345236174", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.5886542344591134", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.17252993208852507", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.35484865824556094", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.2627393433471308", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.38241199840730833", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.6490777420667946", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.03789003793231291", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.3130322200008925", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.12648406193383224", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.8213060225084832", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.052209915557684554", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.7987093745190996", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.02776042461356043", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.17353020086734003", style="dashed"]
}
```

Applying Baum-Welch learning for 3 cycles ...

 1. New transition probabilities:
    * SOURCE→D = 0.057316662147615244
    * SOURCE→A = 0.9410031449341135
    * SOURCE→B = 0.0016801929182712085
    * A→F = 0.18590112958022711
    * A→E = 0.5559300264479639
    * A→B = 0.25816884397180884
    * B→D = 0.7771863303584333
    * B→C = 0.22281366964156693
    * D→A = 1.0
    * C→F = 1.0
    * F→E = 0.5881988669040558
    * F→B = 0.41180113309594435
    * E→A = 1.0

    New emission probabilities:
    * (D, x) = 0.602585276311825
    * (F, z) = 0.071567418640522
    * (A, z) = 0.822397302406259
    * (E, z) = 0.9557482806399094
    * (C, z) = 0.6074106059429042
    * (B, z) = 0.544748295402998
    * (D, y) = 0.2660799663541854
    * (D, z) = 0.13133475733398975
    * (A, y) = 0.06999407785886932
    * (A, x) = 0.10760861973487178
    * (F, x) = 0.12372222946088743
    * (C, y) = 0.10677239725358928
    * (E, x) = 0.018268876432292868
    * (B, x) = 0.2991104593882216
    * (F, y) = 0.8047103518985905
    * (C, x) = 0.28581699680350636
    * (E, y) = 0.02598284292779777
    * (B, y) = 0.1561412452087805

 1. New transition probabilities:
    * SOURCE→D = 0.002120242738120323
    * SOURCE→A = 0.9977450539753295
    * SOURCE→B = 0.0001347032865501758
    * A→F = 0.2112309344951291
    * A→E = 0.464355032642709
    * A→B = 0.3244140328621619
    * B→D = 0.8112826977976546
    * B→C = 0.18871730220234503
    * D→A = 1.0
    * F→E = 0.6306697673066404
    * F→B = 0.36933023269335963
    * C→F = 1.0
    * E→A = 1.0

    New emission probabilities:
    * (D, x) = 0.8757266054608124
    * (F, z) = 0.043426399101658734
    * (A, z) = 0.9043132607310673
    * (E, z) = 0.9685527831575375
    * (C, z) = 0.7845140225015985
    * (B, z) = 0.5542110308546896
    * (D, y) = 0.05814361399686442
    * (D, z) = 0.06612978054232274
    * (A, y) = 0.04003830379241178
    * (A, x) = 0.05564843547652064
    * (F, x) = 0.010620873637741135
    * (C, y) = 0.014800732350948462
    * (E, x) = 0.014571186703614365
    * (B, x) = 0.2272111552033302
    * (F, y) = 0.9459527272606001
    * (C, x) = 0.20068524514745298
    * (E, y) = 0.016876030138848176
    * (B, y) = 0.21857781394198011

 1. New transition probabilities:
    * SOURCE→D = 8.63040249247278e-06
    * SOURCE→A = 0.999990895866932
    * SOURCE→B = 4.7373057555314456e-07
    * A→F = 0.20719091823390837
    * A→E = 0.3684323260447649
    * A→B = 0.42437675572132666
    * B→D = 0.8295258972794963
    * B→C = 0.1704741027205037
    * D→A = 1.0
    * F→E = 0.7776769783995062
    * F→B = 0.22232302160049386
    * C→F = 1.0
    * E→A = 1.0

    New emission probabilities:
    * (D, x) = 0.9793971356197538
    * (F, z) = 0.011558628089682069
    * (A, z) = 0.9910961805720288
    * (E, z) = 0.9851092912208763
    * (C, z) = 0.8894151933653446
    * (B, z) = 0.566393745251961
    * (D, y) = 0.0009867357296941843
    * (D, z) = 0.019616128650552195
    * (A, y) = 0.003865811134278446
    * (A, x) = 0.005038008293692823
    * (F, x) = 8.677544041974953e-05
    * (C, y) = 3.4621688581242006e-05
    * (E, x) = 0.011675945315994274
    * (B, x) = 0.12439624617379086
    * (F, y) = 0.9883545964698982
    * (C, x) = 0.11055018494607437
    * (E, y) = 0.0032147634631295545
    * (B, y) = 0.30921000857424824


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
"STATE_A" -> "STATE_B" [label="0.42434945088606085"]
"STATE_A" -> "STATE_E" [label="0.36842179950491344"]
"STATE_A" -> "STATE_F" [label="0.20722874960902565"]
"STATE_B" -> "STATE_C" [label="0.17053999472155937"]
"STATE_B" -> "STATE_D" [label="0.8294600052784407"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.2223785458913156"]
"STATE_F" -> "STATE_E" [label="0.7776214541086844"]
"STATE_SOURCE" -> "STATE_A" [label="0.9997909585793581"]
"STATE_SOURCE" -> "STATE_B" [label="0.00010044359749630424"]
"STATE_SOURCE" -> "STATE_D" [label="0.0001085978231455291"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.00396462174775412", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.9908989108987591", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.005136467353486777", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.30921724340122786", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.5663238480975317", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.12445890850124049", style="dashed"]
"STATE_C" -> "SYMBOL_z" [label="0.8892484188396925", style="dashed"]
"STATE_C" -> "SYMBOL_y" [label="0.0001345813141869859", style="dashed"]
"STATE_C" -> "SYMBOL_x" [label="0.11061699984612051", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.0010864098067521586", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.019710215585876427", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.9792033746073714", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.003313769332329855", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.9849138170757534", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.011772413591916697", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.9881581490251907", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.011655131550217003", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.00018671942459237183", style="dashed"]
}
```

</div>

`{bm-enable-all}`

