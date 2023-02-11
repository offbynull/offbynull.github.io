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
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="nan", style="dashed"]
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
"STATE_A" -> "STATE_B" [label="0.47892375838401857"]
"STATE_A" -> "STATE_E" [label="0.20185335948644684"]
"STATE_A" -> "STATE_F" [label="0.3192228821295345"]
"STATE_B" -> "STATE_C" [label="0.6256831875221601"]
"STATE_B" -> "STATE_D" [label="0.3743168124778398"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.7522189426920788"]
"STATE_F" -> "STATE_E" [label="0.24778105730792124"]
"STATE_SOURCE" -> "STATE_A" [label="0.34028035567873466"]
"STATE_SOURCE" -> "STATE_B" [label="0.2837541125491734"]
"STATE_SOURCE" -> "STATE_D" [label="0.37596553177209197"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.7771188806319642", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.06324430933746063", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.1596368100305752", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.03997168312712143", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.19250092390345175", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.7675273929694268", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.05654146044217752", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.4866935121144523", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.45676502744337016", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.01726570097647656", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.5212655892476552", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.4614687097758682", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.3646300101483889", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.2846832641602879", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.35068672569132303", style="dashed"]
}
```

Applying Baum-Welch learning for 3 cycles ...

 1. New transition probabilities:
    * SOURCE→A = 0.2242623804054355
    * SOURCE→B = 0.6781702392857792
    * SOURCE→D = 0.09756738030878531
    * D→A = 1.0
    * B→D = 0.39083385883046834
    * B→C = 0.6091661411695318
    * A→B = 0.6162872413798669
    * A→E = 0.1452993576901751
    * A→F = 0.2384134009299581
    * C→F = 1.0
    * E→A = 1.0
    * F→B = 0.8222293243094067
    * F→E = 0.17777067569059346

    New emission probabilities:
    * (C, z) = 0.8999510612735244
    * (B, z) = 0.9247147130625426
    * (B, y) = 0.06123544116014932
    * (E, z) = 0.45652831341481265
    * (F, y) = 0.1754786955983054
    * (D, z) = 0.635056127221957
    * (A, z) = 0.41922903292381014
    * (A, y) = 0.032530750118650566
    * (D, x) = 0.0078034454705278
    * (C, y) = 0.08811960519360716
    * (F, z) = 0.7095647946137075
    * (D, y) = 0.3571404273075151
    * (E, x) = 0.006755028261805201
    * (E, y) = 0.536716658323382
    * (B, x) = 0.01404984577730841
    * (F, x) = 0.11495650978798697
    * (A, x) = 0.5482402169575393
    * (C, x) = 0.01192933353286838

 1. New transition probabilities:
    * SOURCE→A = 0.040388727488285106
    * SOURCE→B = 0.9533557586841024
    * SOURCE→D = 0.006255513827612373
    * D→A = 1.0
    * B→D = 0.49300083292860636
    * B→C = 0.5069991670713937
    * A→B = 0.5019076115731023
    * A→E = 0.15334818538464615
    * A→F = 0.34474420304225156
    * E→A = 1.0
    * F→B = 0.7055532040525583
    * F→E = 0.2944467959474417
    * C→F = 1.0

    New emission probabilities:
    * (C, z) = 0.9555443286640688
    * (B, z) = 0.974426603852691
    * (B, y) = 0.019628405892365475
    * (E, z) = 0.1915074744792217
    * (F, y) = 0.21384530449924816
    * (D, z) = 0.6780323333002214
    * (A, z) = 0.36089779868059635
    * (A, y) = 0.01302108825203822
    * (D, x) = 0.0016381017067935936
    * (C, y) = 0.03864052674188712
    * (F, z) = 0.6736736077806853
    * (D, y) = 0.3203295649929851
    * (E, x) = 0.002324091392363636
    * (E, y) = 0.8061684341284147
    * (B, x) = 0.005944990254943404
    * (F, x) = 0.11248108772006664
    * (A, x) = 0.6260811130673654
    * (C, x) = 0.00581514459404412

 1. New transition probabilities:
    * SOURCE→A = 0.0012993536491830691
    * SOURCE→B = 0.998470021360772
    * SOURCE→D = 0.00023062499004485276
    * D→A = 1.0
    * B→D = 0.4928605609012597
    * B→C = 0.5071394390987403
    * A→B = 0.5940729821427889
    * A→E = 0.11695778802672414
    * A→F = 0.28896922983048723
    * E→A = 1.0
    * F→B = 0.552375450305526
    * F→E = 0.44762454969447396
    * C→F = 1.0

    New emission probabilities:
    * (C, z) = 0.9927573555811455
    * (B, z) = 0.9966371703088741
    * (B, y) = 0.0026741731861688635
    * (E, z) = 0.055406261485937885
    * (F, y) = 0.18882316192201687
    * (D, z) = 0.76138881725708
    * (A, z) = 0.36371176388369175
    * (A, y) = 0.005438210790523941
    * (D, x) = 4.010307600044527e-05
    * (C, y) = 0.007074326784402813
    * (F, z) = 0.7260518989222541
    * (D, y) = 0.23857107966691948
    * (E, x) = 0.0003125613682977566
    * (E, y) = 0.9442811771457642
    * (B, x) = 0.0006886565049570974
    * (F, x) = 0.08512493915572909
    * (A, x) = 0.6308500253257842
    * (C, x) = 0.00016831763445163256


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
"STATE_A" -> "STATE_B" [label="0.5939947837076764"]
"STATE_A" -> "STATE_E" [label="0.11702268122235741"]
"STATE_A" -> "STATE_F" [label="0.2889825350699662"]
"STATE_B" -> "STATE_C" [label="0.507138011496441"]
"STATE_B" -> "STATE_D" [label="0.49286198850355895"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5523649773100641"]
"STATE_F" -> "STATE_E" [label="0.447635022689936"]
"STATE_SOURCE" -> "STATE_A" [label="0.0013989339689923716"]
"STATE_SOURCE" -> "STATE_B" [label="0.9982705401987124"]
"STATE_SOURCE" -> "STATE_D" [label="0.00033052583229516424"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.6307607970866583", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.00553654982557627", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.3637026530877655", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.0007884199789634084", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.0027733411838137194", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.9964382388372229", style="dashed"]
"STATE_C" -> "SYMBOL_z" [label="0.9925595877048341", style="dashed"]
"STATE_C" -> "SYMBOL_y" [label="0.007172175131863255", style="dashed"]
"STATE_C" -> "SYMBOL_x" [label="0.0002682371633026418", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.00014006105768314035", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.2385994998169744", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.7612604391253424", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.0004124376370066547", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.944097947761436", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.055489614601557435", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.08519937934192652", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.18886650197142543", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.7259341186866481", style="dashed"]
}
```

</div>

`{bm-enable-all}`

