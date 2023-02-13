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
"STATE_A" -> "STATE_B" [label="0.4550261644294683"]
"STATE_A" -> "STATE_E" [label="0.023453837423411523"]
"STATE_A" -> "STATE_F" [label="0.5215199981471201"]
"STATE_B" -> "STATE_C" [label="0.8257720481638238"]
"STATE_B" -> "STATE_D" [label="0.17422795183617626"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.9792515414032742"]
"STATE_F" -> "STATE_E" [label="0.020748458596725805"]
"STATE_SOURCE" -> "STATE_A" [label="0.585022218531348"]
"STATE_SOURCE" -> "STATE_B" [label="0.3081498191929455"]
"STATE_SOURCE" -> "STATE_D" [label="0.1068279622757066"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.4584892590848638", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.2909662645526036", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.25054447636253263", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.5734768613822266", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.20580556413441942", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.22071757448335405", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.298781329497983", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.14737645306116834", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.5538422174408487", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.43105689941252207", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.053076529445802434", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.5158665711416756", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.25604115160600105", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.0372473751115743", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.7067114732824247", style="dashed"]
}
```

Applying Baum-Welch learning for 3 cycles ...

 1. New transition probabilities:
    * SOURCE→A = 0.5474728938945381
    * SOURCE→B = 0.38517715817873155
    * SOURCE→D = 0.06734994792673031
    * B→D = 0.2219136341618965
    * B→C = 0.7780863658381033
    * A→B = 0.5821222457187905
    * A→F = 0.37824277864702216
    * A→E = 0.039634975634187206
    * D→A = 1.0
    * C→F = 1.0
    * F→E = 0.02483390753338713
    * F→B = 0.9751660924666129
    * E→A = 1.0

    New emission probabilities:
    * (D, z) = 0.6950203368806173
    * (F, z) = 0.686932782718254
    * (E, z) = 0.7349234882032316
    * (A, z) = 0.7783066402408754
    * (B, x) = 0.24537869599367965
    * (A, x) = 0.15225091752259698
    * (B, y) = 0.08951733612046482
    * (C, z) = 0.700239476693009
    * (C, y) = 0.10670373614645211
    * (B, z) = 0.6651039678858557
    * (A, y) = 0.0694424422365278
    * (E, x) = 0.048282747268344105
    * (F, x) = 0.052308656585263756
    * (E, y) = 0.21679376452842422
    * (D, y) = 0.19602268651774662
    * (F, y) = 0.2607585606964823
    * (D, x) = 0.1089569766016361
    * (C, x) = 0.19305678716053892

 1. New transition probabilities:
    * SOURCE→A = 0.7003268696321935
    * SOURCE→B = 0.2167597037468322
    * SOURCE→D = 0.08291342662097438
    * B→D = 0.2699210423882797
    * B→C = 0.7300789576117203
    * A→B = 0.5040279827895897
    * A→F = 0.45812300205184725
    * A→E = 0.03784901515856291
    * D→A = 1.0
    * F→E = 0.02863042740672929
    * F→B = 0.9713695725932708
    * C→F = 1.0
    * E→A = 1.0

    New emission probabilities:
    * (D, z) = 0.5958714799711974
    * (F, z) = 0.6852323255149328
    * (E, z) = 0.7637024962962761
    * (A, z) = 0.8129772747560421
    * (B, x) = 0.22145895564187137
    * (A, x) = 0.15388412657084352
    * (B, y) = 0.12160329392183847
    * (C, y) = 0.1161670201006784
    * (B, z) = 0.6569377504362902
    * (A, y) = 0.03313859867311453
    * (E, x) = 0.03458422674376545
    * (C, z) = 0.7044665715718174
    * (F, x) = 0.0764087897367362
    * (E, y) = 0.20171327695995853
    * (F, y) = 0.23835888474833095
    * (D, y) = 0.32327447675907256
    * (D, x) = 0.08085404326973014
    * (C, x) = 0.1793664083275043

 1. New transition probabilities:
    * SOURCE→A = 0.8155987503859211
    * SOURCE→B = 0.10815983281282404
    * SOURCE→D = 0.07624141680125483
    * B→D = 0.30469240363362454
    * B→C = 0.6953075963663753
    * A→B = 0.4165034389359505
    * A→F = 0.5511648187945203
    * A→E = 0.03233174226952906
    * D→A = 1.0
    * F→E = 0.024353870591602253
    * F→B = 0.9756461294083979
    * C→F = 1.0
    * E→A = 1.0

    New emission probabilities:
    * (D, z) = 0.48873660375683486
    * (F, z) = 0.7230066313655653
    * (E, z) = 0.7710553485653855
    * (A, z) = 0.8610376895304107
    * (B, x) = 0.25466994463757753
    * (A, x) = 0.12501044043959875
    * (B, y) = 0.1114059728578236
    * (C, y) = 0.11607816665327501
    * (B, z) = 0.6339240825045988
    * (A, y) = 0.013951870029990607
    * (E, x) = 0.037929284152478336
    * (C, z) = 0.6952469547072191
    * (F, x) = 0.053490718904667334
    * (E, y) = 0.19101536728213614
    * (F, y) = 0.22350264972976738
    * (D, y) = 0.43080459500888013
    * (D, x) = 0.08045880123428495
    * (C, x) = 0.18867487863950605


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
"STATE_A" -> "STATE_B" [label="0.4164784953873344"]
"STATE_A" -> "STATE_E" [label="0.03242201566482963"]
"STATE_A" -> "STATE_F" [label="0.5510994889478361"]
"STATE_B" -> "STATE_C" [label="0.6952685426578439"]
"STATE_B" -> "STATE_D" [label="0.3047314573421562"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.9755510192045568"]
"STATE_F" -> "STATE_E" [label="0.024448980795443158"]
"STATE_SOURCE" -> "STATE_A" [label="0.8154541141516757"]
"STATE_SOURCE" -> "STATE_B" [label="0.10822736460344301"]
"STATE_SOURCE" -> "STATE_D" [label="0.07631852124488138"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.8608794257026999", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.12507291856402952", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.014047655733270626", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.6338339323249015", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.2546935365766046", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.11147253109849407", style="dashed"]
"STATE_C" -> "SYMBOL_z" [label="0.695138413183264", style="dashed"]
"STATE_C" -> "SYMBOL_y" [label="0.11614332365617815", style="dashed"]
"STATE_C" -> "SYMBOL_x" [label="0.18871826316055784", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.48868999675780755", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.08053464084203235", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.43077536240016007", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.7709240713439823", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.038017878788841684", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.19105804986717598", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.7228897644362344", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.05357464651071413", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.22353558905305146", style="dashed"]
}
```

</div>

`{bm-enable-all}`

