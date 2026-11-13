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
"STATE_A" -> "STATE_B" [label="0.16667438902447784"]
"STATE_A" -> "STATE_E" [label="0.5726332216474378"]
"STATE_A" -> "STATE_F" [label="0.26069238932808436"]
"STATE_B" -> "STATE_C" [label="0.3394180914339415"]
"STATE_B" -> "STATE_D" [label="0.6605819085660584"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.12052721016099735"]
"STATE_F" -> "STATE_E" [label="0.8794727898390027"]
"STATE_SOURCE" -> "STATE_A" [label="0.28672847375913574"]
"STATE_SOURCE" -> "STATE_B" [label="0.414509894349515"]
"STATE_SOURCE" -> "STATE_D" [label="0.2987616318913492"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.4586506644862434", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.35718117754379985", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.18416815796995684", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.46656393453820794", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.2830279406918338", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.25040812476995833", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.46064828052362056", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.3514965993977714", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.18785512007860797", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.41561713340811657", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.21001152465786244", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.374371341934021", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.46764808205480574", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.13160775070687603", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.40074416723831835", style="dashed"]
}
```

Applying Baum-Welch learning for 3 cycles ...

 1. New transition probabilities:
    * SOURCE→A = 0.22573543223696912
    * SOURCE→B = 0.3248911602582637
    * SOURCE→D = 0.4493734075047672
    * A→E = 0.5888030236303627
    * A→B = 0.20498743333477004
    * A→F = 0.20620954303486733
    * D→A = 1.0
    * B→D = 0.7627093904377751
    * B→C = 0.23729060956222495
    * C→F = 1.0
    * E→A = 1.0
    * F→E = 0.8633062403764713
    * F→B = 0.1366937596235287

    New emission probabilities:
    * (A, z) = 0.7507173589085092
    * (F, z) = 0.5143951957856459
    * (B, z) = 0.7666161465887507
    * (D, z) = 0.8744209436285257
    * (C, y) = 0.1115908601555518
    * (B, x) = 0.11437165302328213
    * (C, z) = 0.7618144980227753
    * (C, x) = 0.12659464182167304
    * (E, y) = 0.2426433796944585
    * (A, y) = 0.08166969954390231
    * (B, y) = 0.11901220038796725
    * (E, z) = 0.570782601476895
    * (F, x) = 0.1486720132484136
    * (E, x) = 0.1865740188286464
    * (F, y) = 0.33693279096594053
    * (D, x) = 0.06721070115951555
    * (D, y) = 0.05836835521195862
    * (A, x) = 0.16761294154758843

 1. New transition probabilities:
    * SOURCE→A = 0.15730853798131184
    * SOURCE→B = 0.3212192039800242
    * SOURCE→D = 0.521472258038664
    * A→E = 0.5806040725408432
    * A→B = 0.20529276483386696
    * A→F = 0.21410316262528986
    * D→A = 1.0
    * B→D = 0.7674912119142155
    * B→C = 0.23250878808578462
    * E→A = 1.0
    * C→F = 1.0
    * F→E = 0.8647251198613123
    * F→B = 0.1352748801386879

    New emission probabilities:
    * (A, z) = 0.7514088901944634
    * (F, z) = 0.4847430715405044
    * (B, z) = 0.8340501914890244
    * (D, z) = 0.9355321516069679
    * (C, y) = 0.08167630306479583
    * (B, x) = 0.06852244430609845
    * (C, z) = 0.8488737438565583
    * (C, x) = 0.06944995307864579
    * (E, y) = 0.2700007600864314
    * (A, y) = 0.06836307082954061
    * (B, y) = 0.09742736420487727
    * (E, z) = 0.5095424204611411
    * (F, x) = 0.13320659076040556
    * (E, x) = 0.2204568194524275
    * (F, y) = 0.38205033769909025
    * (D, x) = 0.02557504184918951
    * (D, y) = 0.03889280654384259
    * (A, x) = 0.1802280389759958

 1. New transition probabilities:
    * SOURCE→A = 0.08584239928615975
    * SOURCE→B = 0.3422427577360065
    * SOURCE→D = 0.5719148429778339
    * A→E = 0.5722240283829966
    * A→B = 0.21358749626630968
    * A→F = 0.21418847535069363
    * D→A = 1.0
    * B→D = 0.7649939439685262
    * B→C = 0.23500605603147356
    * E→A = 1.0
    * C→F = 1.0
    * F→E = 0.8706170847833382
    * F→B = 0.12938291521666168

    New emission probabilities:
    * (A, z) = 0.7655253521888177
    * (F, z) = 0.4377870669547677
    * (B, z) = 0.8949649442655515
    * (D, z) = 0.9696731944776145
    * (C, y) = 0.046149267933188874
    * (B, x) = 0.03641437703562503
    * (C, z) = 0.9297909756842322
    * (C, x) = 0.024059756382579085
    * (E, y) = 0.2974576275844383
    * (A, y) = 0.049335507677585114
    * (B, y) = 0.06862067869882346
    * (E, z) = 0.4485580521559886
    * (F, x) = 0.1108709478553918
    * (E, x) = 0.2539843202595732
    * (F, y) = 0.45134198518984014
    * (D, x) = 0.006344325685052984
    * (D, y) = 0.02398247983733247
    * (A, x) = 0.1851391401335972


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
"STATE_A" -> "STATE_B" [label="0.21362340924353668"]
"STATE_A" -> "STATE_E" [label="0.5721523826681962"]
"STATE_A" -> "STATE_F" [label="0.2142242080882672"]
"STATE_B" -> "STATE_C" [label="0.23505904422262908"]
"STATE_B" -> "STATE_D" [label="0.7649409557773709"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.12945702381189927"]
"STATE_F" -> "STATE_E" [label="0.8705429761881006"]
"STATE_SOURCE" -> "STATE_A" [label="0.08591662429887008"]
"STATE_SOURCE" -> "STATE_B" [label="0.3422400857102933"]
"STATE_SOURCE" -> "STATE_D" [label="0.5718432899908366"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.18518358505807977", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.7653957334687771", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.04942068147314318", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.036503426007822685", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.8947965053139574", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.06870006867822", style="dashed"]
"STATE_C" -> "SYMBOL_y" [label="0.04623539731399467", style="dashed"]
"STATE_C" -> "SYMBOL_z" [label="0.929612092056615", style="dashed"]
"STATE_C" -> "SYMBOL_x" [label="0.02415251062939026", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.006442392967162837", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.9694823497726829", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.024075257260154432", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.2540081178242259", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.44852349510745637", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.2974683870683178", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.1109376665554252", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.437755740232698", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.45130659321187666", style="dashed"]
}
```

</div>

`{bm-enable-all}`

