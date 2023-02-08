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
"STATE_A" -> "STATE_B" [label="0.37084398063040624"]
"STATE_A" -> "STATE_E" [label="0.3011968196498261"]
"STATE_A" -> "STATE_F" [label="0.32795919971976767"]
"STATE_B" -> "STATE_C" [label="0.895456674940541"]
"STATE_B" -> "STATE_D" [label="0.10454332505945899"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.504295332095392"]
"STATE_F" -> "STATE_E" [label="0.495704667904608"]
"STATE_SOURCE" -> "STATE_A" [label="0.24224723827794753"]
"STATE_SOURCE" -> "STATE_B" [label="0.3206816756132005"]
"STATE_SOURCE" -> "STATE_D" [label="0.437071086108852"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.13739329216338653", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.19227040536014312", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.6703363024764704", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.7357233444642208", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.10860795051910055", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.1556687050166785", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.5268944293728581", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.26739983027869557", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.20570574034844627", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.4363466693501706", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.36985649274720345", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.19379683790262603", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.08032937467820499", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.2640083718416932", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.6556622534801019", style="dashed"]
}
```

Applying Baum-Welch learning for 3 cycles ...

 1. New transition probabilities:
    * SOURCE→B = 0.2706219152688455
    * SOURCE→A = 0.19282770342409403
    * SOURCE→D = 0.5365503813070606
    * D→A = 1.0
    * B→C = 0.898428066091151
    * B→D = 0.10157193390884911
    * A→F = 0.3759099878442794
    * A→B = 0.31251611732188606
    * A→E = 0.3115738948338346
    * C→F = 1.0
    * E→A = 1.0
    * F→B = 0.38593115153573
    * F→E = 0.61406884846427

    New emission probabilities:
    * (A, z) = 0.7453330698341533
    * (E, z) = 0.7735826816052319
    * (F, z) = 0.7142908861221592
    * (C, z) = 0.4811666884165533
    * (D, z) = 0.9783578542278979
    * (D, y) = 0.004683395459885838
    * (B, z) = 0.4116284285913943
    * (B, y) = 0.08167925953626202
    * (C, y) = 0.09600938877189728
    * (C, x) = 0.4228239228115496
    * (F, x) = 0.02920432582428936
    * (E, x) = 0.17531937777747847
    * (A, x) = 0.021015153534177915
    * (F, y) = 0.2565047880535513
    * (E, y) = 0.05109794061728953
    * (A, y) = 0.2336517766316689
    * (D, x) = 0.016958750312216334
    * (B, x) = 0.5066923118723435

 1. New transition probabilities:
    * SOURCE→B = 0.011222516148321102
    * SOURCE→A = 0.19856356942454653
    * SOURCE→D = 0.7902139144271324
    * D→A = 1.0
    * B→C = 0.876890581210029
    * B→D = 0.12310941878997068
    * A→F = 0.28089237537914186
    * A→B = 0.36964621003247117
    * A→E = 0.34946141458838703
    * E→A = 1.0
    * F→B = 0.25700406826152977
    * F→E = 0.7429959317384701
    * C→F = 1.0

    New emission probabilities:
    * (A, z) = 0.6893749170766224
    * (E, z) = 0.7992307715151333
    * (F, z) = 0.7168175461364193
    * (C, z) = 0.7613911685116559
    * (D, z) = 0.9984013183987887
    * (D, y) = 0.00056995034089254
    * (B, z) = 0.32067018675110065
    * (B, y) = 0.09223550410522911
    * (C, y) = 0.06134928406224788
    * (C, x) = 0.1772595474260965
    * (F, x) = 0.03428318478756893
    * (E, x) = 0.18769975665384855
    * (A, x) = 0.003637274214656609
    * (F, y) = 0.2488992690760115
    * (E, y) = 0.013069471831018128
    * (A, y) = 0.30698780870872105
    * (D, x) = 0.0010287312603189228
    * (B, x) = 0.5870943091436701

 1. New transition probabilities:
    * SOURCE→B = 0.00024049132708213648
    * SOURCE→A = 0.05223720496436499
    * SOURCE→D = 0.9475223037085528
    * D→A = 1.0
    * B→C = 0.9032426697358633
    * B→D = 0.0967573302641368
    * A→F = 0.1880013165192982
    * A→B = 0.5036666777838507
    * A→E = 0.30833200569685143
    * E→A = 1.0
    * F→B = 0.10260503802092744
    * F→E = 0.8973949619790725
    * C→F = 1.0

    New emission probabilities:
    * (A, z) = 0.5624469092897886
    * (E, z) = 0.8484930620416489
    * (F, z) = 0.8298287959427371
    * (C, z) = 0.949285125013261
    * (D, z) = 0.999942499511677
    * (D, y) = 2.1631114010485995e-05
    * (B, z) = 0.2636706517633922
    * (B, y) = 0.024299520064180014
    * (C, y) = 0.018278007426290935
    * (C, x) = 0.032436867560448064
    * (F, x) = 0.022364547840577398
    * (E, x) = 0.15066691930991963
    * (A, x) = 0.00013833281151946446
    * (F, y) = 0.14780665621668534
    * (E, y) = 0.0008400186484313717
    * (A, y) = 0.437414757898692
    * (D, x) = 3.5869374312568515e-05
    * (B, x) = 0.7120298281724277


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
"STATE_A" -> "STATE_B" [label="0.5036155931059187"]
"STATE_A" -> "STATE_E" [label="0.30833950384569764"]
"STATE_A" -> "STATE_F" [label="0.18804490304838362"]
"STATE_B" -> "STATE_C" [label="0.9031620373283974"]
"STATE_B" -> "STATE_D" [label="0.09683796267160247"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.1026845011207033"]
"STATE_F" -> "STATE_E" [label="0.8973154988792967"]
"STATE_SOURCE" -> "STATE_A" [label="0.05232150851181146"]
"STATE_SOURCE" -> "STATE_B" [label="0.0003403892103190408"]
"STATE_SOURCE" -> "STATE_D" [label="0.9473381022778695"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.00023826133311952863", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.5623781958310393", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.43738354283584124", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.7119162532964387", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.26369154430010217", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.024392202403458976", style="dashed"]
"STATE_C" -> "SYMBOL_z" [label="0.9491003948947926", style="dashed"]
"STATE_C" -> "SYMBOL_y" [label="0.01837249567758766", style="dashed"]
"STATE_C" -> "SYMBOL_x" [label="0.032527109427619785", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.00013582862572485106", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.9997425767386554", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.00012159463561980007", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.15072170279907993", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.848338560473507", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.0009397367274131481", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.022457810497428173", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.8296798919751447", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.14786229752742713", style="dashed"]
}
```

</div>

`{bm-enable-all}`

