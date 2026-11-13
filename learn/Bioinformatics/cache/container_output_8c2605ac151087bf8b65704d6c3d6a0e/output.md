<div style="border:1px solid black;">

`{bm-disable-all}`

Executing neighbour joining phylogeny **soft** clustering using the following settings...

```
{
  filename: GDS6010.soft_no_replicates_single_control.xz,
  gene_column: ID_REF,  # col name for gene ID
  sample_columns: [
    GSM1626001,  # col name for control @ 24 hrs (treat this as a measure of "before infection")
    GSM1626004,  # col name for infection @ 6 hrs
    GSM1626007,  # col name for infection @ 12 hrs
    GSM1626010   # col name for infection @ 24 hrs
  ],
  std_dev_limit: 1.6,  # reject anything with std dev less than this
  metric: euclidean,  # OPTIONS: euclidean, manhattan, cosine, pearson
  dist_capture: 0.5,
  edge_scale: 3.0
}

```

The following neighbour joining phylogeny tree was produced ...

```{dot}
graph G {
 layout=neato
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
A23P10091 [style=filled, fillcolor="#f6501e"]
A23P101636 [style=filled, fillcolor="#fd12eb"]
A23P117873 [style=filled, fillcolor="#fae91d"]
A23P118894
A23P119448 [style=filled, fillcolor="#fae91d"]
A23P122210 [style=filled, fillcolor="#f6501e"]
A23P125278 [style=filled, fillcolor="#a1fc11"]
A23P127013 [style=filled, fillcolor="#f6501e"]
A23P133263 [style=filled, fillcolor="#fc2d2d"]
A23P133949 [style=filled, fillcolor="#f88420"]
A23P13465 [style=filled, fillcolor="#2736f3"]
A23P137825
A23P139786
A23P140475 [style=filled, fillcolor="#fe0c7c"]
A23P144096 [style=filled, fillcolor="#f6501e"]
A23P144549
A23P14863
A23P156873
A23P161218
A23P162300
A23P170050 [style=filled, fillcolor="#f90fb1"]
A23P17663 [style=filled, fillcolor="#1994fd"]
A23P202361 [style=filled, fillcolor="#f6501e"]
A23P204087
A23P20814 [style=filled, fillcolor="#1994fd"]
A23P214821
A23P21990 [style=filled, fillcolor="#2afd3a"]
A23P22027
A23P24004
A23P258633 [style=filled, fillcolor="#2ecefe"]
A23P26314 [style=filled, fillcolor="#f6501e"]
A23P306211 [style=filled, fillcolor="#f6501e"]
A23P321860
A23P326700 [style=filled, fillcolor="#4a2bf8"]
A23P328145 [style=filled, fillcolor="#2736f3"]
A23P348992 [style=filled, fillcolor="#f6501e"]
A23P353316 [style=filled, fillcolor="#f6501e"]
A23P35412
A23P36985
A23P384551 [style=filled, fillcolor="#dbf933"]
A23P385067 [style=filled, fillcolor="#f88420"]
A23P390032 [style=filled, fillcolor="#f6501e"]
A23P391443 [style=filled, fillcolor="#f6501e"]
A23P396934 [style=filled, fillcolor="#f90fb1"]
A23P397671 [style=filled, fillcolor="#f88420"]
A23P400945
A23P401361 [style=filled, fillcolor="#f6501e"]
A23P416434 [style=filled, fillcolor="#13fb5a"]
A23P424727 [style=filled, fillcolor="#7c2dfb"]
A23P426681
A23P4283 [style=filled, fillcolor="#9b06f8"]
A23P4286
A23P45871 [style=filled, fillcolor="#1994fd"]
A23P46070 [style=filled, fillcolor="#fae91d"]
A23P47904 [style=filled, fillcolor="#4a2bf8"]
A23P48513
A23P500844 [style=filled, fillcolor="#31fb9e"]
A23P501634 [style=filled, fillcolor="#f6501e"]
A23P52266
A23P6263
A23P64828 [style=filled, fillcolor="#9b06f8"]
A23P69606 [style=filled, fillcolor="#dbf933"]
A23P69768 [style=filled, fillcolor="#7c2dfb"]
A23P73096
A23P82567 [style=filled, fillcolor="#4a2bf8"]
A23P95417 [style=filled, fillcolor="#f90fb1"]
A23P98622 [style=filled, fillcolor="#a1fc11"]
A24P101601 [style=filled, fillcolor="#f6501e"]
A24P109111 [style=filled, fillcolor="#22f4c4"]
A24P112730 [style=filled, fillcolor="#77f627"]
A24P115990
A24P117294
A24P118391
A24P119813 [style=filled, fillcolor="#f7b92f"]
A24P128524
A24P136161 [style=filled, fillcolor="#f6501e"]
A24P140621
A24P144337 [style=filled, fillcolor="#f6501e"]
A24P148907
A24P152855 [style=filled, fillcolor="#f6501e"]
A24P162211 [style=filled, fillcolor="#31fb9e"]
A24P162393 [style=filled, fillcolor="#fae91d"]
A24P170384 [style=filled, fillcolor="#f6501e"]
A24P196428
A24P201936 [style=filled, fillcolor="#f6501e"]
A24P212127
A24P215804 [style=filled, fillcolor="#f6501e"]
A24P220984 [style=filled, fillcolor="#13fb5a"]
A24P237661 [style=filled, fillcolor="#f6501e"]
A24P246591 [style=filled, fillcolor="#fc2d2d"]
A24P247536 [style=filled, fillcolor="#f6501e"]
A24P25040 [style=filled, fillcolor="#f6501e"]
A24P25437 [style=filled, fillcolor="#dbf933"]
A24P265407
A24P269527
A24P281730 [style=filled, fillcolor="#f6501e"]
A24P28722
A24P289067 [style=filled, fillcolor="#dbf933"]
A24P290188 [style=filled, fillcolor="#f6501e"]
A24P298099 [style=filled, fillcolor="#f6501e"]
A24P298604 [style=filled, fillcolor="#f6501e"]
A24P303091
A24P304071
A24P315474 [style=filled, fillcolor="#f6501e"]
A24P316965 [style=filled, fillcolor="#f92e5d"]
A24P343929 [style=filled, fillcolor="#f92e5d"]
A24P344251 [style=filled, fillcolor="#f7b92f"]
A24P345866
A24P350017 [style=filled, fillcolor="#f6501e"]
A24P350160 [style=filled, fillcolor="#f6501e"]
A24P350771 [style=filled, fillcolor="#2ecefe"]
A24P358337 [style=filled, fillcolor="#f6501e"]
A24P38722 [style=filled, fillcolor="#f7b92f"]
A24P391574 [style=filled, fillcolor="#f6501e"]
A24P392505 [style=filled, fillcolor="#f6501e"]
A24P400180 [style=filled, fillcolor="#2afd3a"]
A24P400751 [style=filled, fillcolor="#f6501e"]
A24P42557
A24P476247 [style=filled, fillcolor="#f88420"]
A24P482104
A24P54863 [style=filled, fillcolor="#22f4c4"]
A24P558750 [style=filled, fillcolor="#22f4c4"]
A24P58187 [style=filled, fillcolor="#f6501e"]
A24P59554 [style=filled, fillcolor="#22f4c4"]
A24P644742
A24P66780 [style=filled, fillcolor="#4a2bf8"]
A24P66932 [style=filled, fillcolor="#f6501e"]
A24P67364 [style=filled, fillcolor="#31fb9e"]
A24P677219
A24P68088 [style=filled, fillcolor="#f90fb1"]
A24P702912
A24P711050 [style=filled, fillcolor="#1afafa"]
A24P738168 [style=filled, fillcolor="#f88420"]
A24P75543 [style=filled, fillcolor="#f6501e"]
A24P761130 [style=filled, fillcolor="#f6501e"]
A24P80915
A24P812018 [style=filled, fillcolor="#1afafa"]
A24P837537 [style=filled, fillcolor="#13fb5a"]
A24P84719
A24P871687 [style=filled, fillcolor="#a1fc11"]
A24P884376 [style=filled, fillcolor="#f6501e"]
A24P887239 [style=filled, fillcolor="#f90fb1"]
A24P889237 [style=filled, fillcolor="#fd12eb"]
A24P911648 [style=filled, fillcolor="#f6501e"]
A24P913156
A24P914102 [style=filled, fillcolor="#0f58fc"]
A24P915675 [style=filled, fillcolor="#f6501e"]
A24P917866 [style=filled, fillcolor="#1afafa"]
A24P920826
A24P922139 [style=filled, fillcolor="#f88420"]
A24P922979 [style=filled, fillcolor="#dbf933"]
A24P923534 [style=filled, fillcolor="#dbf933"]
A24P924251 [style=filled, fillcolor="#f6501e"]
A24P925673 [style=filled, fillcolor="#4efe2e"]
A24P927304 [style=filled, fillcolor="#fd12eb"]
A24P927770 [style=filled, fillcolor="#f88420"]
A24P928156 [style=filled, fillcolor="#4a2bf8"]
A24P929835
A24P931030 [style=filled, fillcolor="#fae91d"]
A24P934145 [style=filled, fillcolor="#fd12eb"]
A24P937039 [style=filled, fillcolor="#f88420"]
A24P941946 [style=filled, fillcolor="#f6501e"]
A24P943866 [style=filled, fillcolor="#fe0c7c"]
A32P107002
A32P112263
A32P112279
A32P112401 [style=filled, fillcolor="#f6501e"]
A32P11262
A32P118481 [style=filled, fillcolor="#f6501e"]
A32P12355 [style=filled, fillcolor="#f88420"]
A32P139302 [style=filled, fillcolor="#f6501e"]
A32P15128 [style=filled, fillcolor="#f92e5d"]
A32P181937
A32P186038 [style=filled, fillcolor="#1afafa"]
A32P197744
A32P200787
A32P203917 [style=filled, fillcolor="#f88420"]
A32P20582 [style=filled, fillcolor="#f6501e"]
A32P206344 [style=filled, fillcolor="#dbf933"]
A32P206561 [style=filled, fillcolor="#d934f7"]
A32P207096 [style=filled, fillcolor="#4efe2e"]
A32P211048 [style=filled, fillcolor="#0f58fc"]
A32P220152 [style=filled, fillcolor="#f6501e"]
A32P224666 [style=filled, fillcolor="#f6501e"]
A32P226605
A32P230196 [style=filled, fillcolor="#f6501e"]
A32P233735 [style=filled, fillcolor="#f6501e"]
A32P234202 [style=filled, fillcolor="#f6501e"]
A32P234294 [style=filled, fillcolor="#f6501e"]
A32P25243 [style=filled, fillcolor="#f7b92f"]
A32P26401 [style=filled, fillcolor="#22f4c4"]
A32P302205
A32P332551 [style=filled, fillcolor="#4a2bf8"]
A32P34970 [style=filled, fillcolor="#f6501e"]
A32P387648 [style=filled, fillcolor="#77f627"]
A32P396186 [style=filled, fillcolor="#d934f7"]
A32P461976
A32P4792 [style=filled, fillcolor="#f6501e"]
A32P73452 [style=filled, fillcolor="#f6501e"]
A32P75141
A32P75357
A32P82119 [style=filled, fillcolor="#22f4c4"]
A32P94199 [style=filled, fillcolor="#f6501e"]
N1
N10
N100
N101 [style=filled, fillcolor="#22f4c4"]
N102 [style=filled, fillcolor="#22f4c4"]
N103
N104
N105
N106
N107
N108
N109
N11
N110 [style=filled, fillcolor="#1afafa"]
N111 [style=filled, fillcolor="#1afafa"]
N112 [style=filled, fillcolor="#1afafa"]
N113 [style=filled, fillcolor="#1afafa"]
N114
N115
N116 [style=filled, fillcolor="#2ecefe"]
N117
N118 [style=filled, fillcolor="#2ecefe"]
N119
N12
N120
N121
N122 [style=filled, fillcolor="#13fb5a"]
N123
N124
N125 [style=filled, fillcolor="#13fb5a"]
N126 [style=filled, fillcolor="#f6501e"]
N127
N128 [style=filled, fillcolor="#13fb5a"]
N129 [style=filled, fillcolor="#f6501e"]
N13
N130
N131 [style=filled, fillcolor="#31fb9e"]
N132 [style=filled, fillcolor="#f6501e"]
N133
N134 [style=filled, fillcolor="#f6501e"]
N135 [style=filled, fillcolor="#31fb9e"]
N136
N137
N138 [style=filled, fillcolor="#f6501e"]
N139 [style=filled, fillcolor="#f6501e"]
N14
N140 [style=filled, fillcolor="#31fb9e"]
N141 [style=filled, fillcolor="#f6501e"]
N142 [style=filled, fillcolor="#f6501e"]
N143 [style=filled, fillcolor="#0f58fc"]
N144 [style=filled, fillcolor="#0f58fc"]
N145 [style=filled, fillcolor="#f6501e"]
N146 [style=filled, fillcolor="#f6501e"]
N147 [style=filled, fillcolor="#f6501e"]
N148 [style=filled, fillcolor="#f6501e"]
N149 [style=filled, fillcolor="#f6501e"]
N15
N150 [style=filled, fillcolor="#f6501e"]
N151 [style=filled, fillcolor="#f6501e"]
N152 [style=filled, fillcolor="#f6501e"]
N153 [style=filled, fillcolor="#f6501e"]
N154 [style=filled, fillcolor="#f6501e"]
N155 [style=filled, fillcolor="#f6501e"]
N156 [style=filled, fillcolor="#d934f7"]
N157 [style=filled, fillcolor="#f6501e"]
N158 [style=filled, fillcolor="#d934f7"]
N159 [style=filled, fillcolor="#f6501e"]
N16
N160 [style=filled, fillcolor="#f6501e"]
N161 [style=filled, fillcolor="#f6501e"]
N162 [style=filled, fillcolor="#f6501e"]
N163 [style=filled, fillcolor="#f6501e"]
N164 [style=filled, fillcolor="#f6501e"]
N165 [style=filled, fillcolor="#f6501e"]
N166 [style=filled, fillcolor="#f6501e"]
N167 [style=filled, fillcolor="#f6501e"]
N168 [style=filled, fillcolor="#f6501e"]
N169 [style=filled, fillcolor="#f6501e"]
N17
N170 [style=filled, fillcolor="#f6501e"]
N171 [style=filled, fillcolor="#f6501e"]
N172 [style=filled, fillcolor="#f6501e"]
N173 [style=filled, fillcolor="#f6501e"]
N174 [style=filled, fillcolor="#f6501e"]
N175 [style=filled, fillcolor="#f6501e"]
N176 [style=filled, fillcolor="#f6501e"]
N177 [style=filled, fillcolor="#f6501e"]
N178 [style=filled, fillcolor="#f6501e"]
N179 [style=filled, fillcolor="#f6501e"]
N18 [style=filled, fillcolor="#9b06f8"]
N180 [style=filled, fillcolor="#f6501e"]
N181 [style=filled, fillcolor="#f6501e"]
N182 [style=filled, fillcolor="#f6501e"]
N183 [style=filled, fillcolor="#f6501e"]
N184 [style=filled, fillcolor="#f6501e"]
N185 [style=filled, fillcolor="#f6501e"]
N186 [style=filled, fillcolor="#f6501e"]
N187 [style=filled, fillcolor="#f6501e"]
N188 [style=filled, fillcolor="#f6501e"]
N189 [style=filled, fillcolor="#f6501e"]
N19 [style=filled, fillcolor="#9b06f8"]
N190 [style=filled, fillcolor="#f6501e"]
N191 [style=filled, fillcolor="#f6501e"]
N192 [style=filled, fillcolor="#f6501e"]
N193 [style=filled, fillcolor="#f6501e"]
N194 [style=filled, fillcolor="#f6501e"]
N195 [style=filled, fillcolor="#f6501e"]
N196 [style=filled, fillcolor="#f6501e"]
N197 [style=filled, fillcolor="#f6501e"]
N198 [style=filled, fillcolor="#f6501e"]
N199 [style=filled, fillcolor="#f6501e"]
N2 [style=filled, fillcolor="#1994fd"]
N20 [style=filled, fillcolor="#9b06f8"]
N200 [style=filled, fillcolor="#f6501e"]
N201 [style=filled, fillcolor="#f6501e"]
N21
N22
N23
N24
N25 [style=filled, fillcolor="#f92e5d"]
N26 [style=filled, fillcolor="#f92e5d"]
N27
N28
N29
N3 [style=filled, fillcolor="#1994fd"]
N30
N31
N32 [style=filled, fillcolor="#fc2d2d"]
N33 [style=filled, fillcolor="#f88420"]
N34 [style=filled, fillcolor="#f88420"]
N35 [style=filled, fillcolor="#f88420"]
N36
N37
N38 [style=filled, fillcolor="#fc2d2d"]
N39 [style=filled, fillcolor="#f88420"]
N4 [style=filled, fillcolor="#1994fd"]
N40 [style=filled, fillcolor="#2afd3a"]
N41 [style=filled, fillcolor="#f88420"]
N42 [style=filled, fillcolor="#f88420"]
N43 [style=filled, fillcolor="#f88420"]
N44 [style=filled, fillcolor="#a1fc11"]
N45 [style=filled, fillcolor="#fd12eb"]
N46 [style=filled, fillcolor="#f88420"]
N47 [style=filled, fillcolor="#a1fc11"]
N48 [style=filled, fillcolor="#fd12eb"]
N49 [style=filled, fillcolor="#f88420"]
N5
N50 [style=filled, fillcolor="#fd12eb"]
N51 [style=filled, fillcolor="#4efe2e"]
N52 [style=filled, fillcolor="#a1fc11"]
N53 [style=filled, fillcolor="#2736f3"]
N54 [style=filled, fillcolor="#4efe2e"]
N55 [style=filled, fillcolor="#f90fb1"]
N56 [style=filled, fillcolor="#4a2bf8"]
N57
N58
N59 [style=filled, fillcolor="#f90fb1"]
N6
N60 [style=filled, fillcolor="#f90fb1"]
N61 [style=filled, fillcolor="#2736f3"]
N62 [style=filled, fillcolor="#f90fb1"]
N63 [style=filled, fillcolor="#4a2bf8"]
N64 [style=filled, fillcolor="#4a2bf8"]
N65 [style=filled, fillcolor="#4a2bf8"]
N66 [style=filled, fillcolor="#f7b92f"]
N67
N68 [style=filled, fillcolor="#f7b92f"]
N69 [style=filled, fillcolor="#4a2bf8"]
N7
N70 [style=filled, fillcolor="#f7b92f"]
N71 [style=filled, fillcolor="#fae91d"]
N72 [style=filled, fillcolor="#f7b92f"]
N73 [style=filled, fillcolor="#f7b92f"]
N74 [style=filled, fillcolor="#fae91d"]
N75 [style=filled, fillcolor="#fae91d"]
N76 [style=filled, fillcolor="#fae91d"]
N77
N78 [style=filled, fillcolor="#fae91d"]
N79
N8
N80
N81 [style=filled, fillcolor="#77f627"]
N82 [style=filled, fillcolor="#dbf933"]
N83 [style=filled, fillcolor="#dbf933"]
N84 [style=filled, fillcolor="#dbf933"]
N85 [style=filled, fillcolor="#dbf933"]
N86 [style=filled, fillcolor="#dbf933"]
N87 [style=filled, fillcolor="#dbf933"]
N88
N89 [style=filled, fillcolor="#fe0c7c"]
N9
N90
N91
N92 [style=filled, fillcolor="#22f4c4"]
N93 [style=filled, fillcolor="#22f4c4"]
N94
N95 [style=filled, fillcolor="#22f4c4"]
N96 [style=filled, fillcolor="#22f4c4"]
N97
N98 [style=filled, fillcolor="#7c2dfb"]
N99 [style=filled, fillcolor="#22f4c4"]
N197 -- N201 [label="0.06", len=0.1796630824]
N197 -- N180 [label="0.12", len=0.3493579105]
N152 -- A23P137825 [label="0.56", len=1.6747631852]
N152 -- N151 [label="0.06", len=0.1819289460]
N151 -- N149 [label="0.06", len=0.1924179311]
N151 -- A32P234202 [label="0.17", len=0.5013230085]
N150 -- N148 [label="0.08", len=0.2400196495]
N150 -- A32P73452 [label="0.09", len=0.2604220116]
N149 -- N140 [label="0.30", len=0.8901591685]
N149 -- A24P358337 [label="0.36", len=1.0885704366]
N148 -- A24P315474 [label="0.13", len=0.3852562440]
N148 -- N142 [label="0.16", len=0.4785232370]
N197 -- A24P392505 [label="0.18", len=0.5310691063]
N147 -- A24P136161 [label="0.21", len=0.6440278618]
N147 -- N146 [label="0.12", len=0.3483374780]
N146 -- A32P224666 [label="0.25", len=0.7599073839]
N146 -- A24P298099 [label="0.22", len=0.6508337657]
N145 -- A24P290188 [label="0.18", len=0.5528552049]
N145 -- N139 [label="0.08", len=0.2254382297]
N144 -- A32P11262 [label="0.87", len=2.6019269372]
N144 -- N143 [label="0.02", len=0.0555139758]
N143 -- A32P211048 [label="0.08", len=0.2359277055]
N143 -- A24P914102 [label="0.08", len=0.2536209986]
N196 -- N188 [label="0.17", len=0.4985005409]
N142 -- A24P152855 [label="0.28", len=0.8385259680]
N142 -- N141 [label="0.08", len=0.2394921027]
N141 -- A24P884376 [label="0.12", len=0.3595526116]
N141 -- N138 [label="0.08", len=0.2549041490]
N140 -- A24P162211 [label="0.21", len=0.6447592442]
N140 -- N135 [label="0.17", len=0.4956482005]
N139 -- N134 [label="0.26", len=0.7663634529]
N139 -- A32P112401 [label="0.22", len=0.6536207567]
N138 -- A32P20582 [label="0.34", len=1.0157348390]
N138 -- A24P298604 [label="0.41", len=1.2216704874]
N196 -- N193 [label="0.07", len=0.1950352351]
N137 -- A23P426681 [label="1.69", len=5.0832717061]
N137 -- N127 [label="0.59", len=1.7741976495]
N136 -- A32P107002 [label="0.78", len=2.3392089173]
N136 -- N119 [label="0.94", len=2.8311404446]
N135 -- N133 [label="0.15", len=0.4418451736]
N135 -- N131 [label="0.22", len=0.6633446976]
N134 -- N132 [label="0.05", len=0.1599900649]
N134 -- N128 [label="0.32", len=0.9472979370]
N133 -- A24P128524 [label="0.52", len=1.5450293728]
N133 -- N130 [label="0.23", len=0.6805547436]
N195 -- N194 [label="0.00", len=0.0143638716]
N132 -- A24P101601 [label="0.33", len=1.0033948703]
N132 -- N129 [label="0.23", len=0.6813115609]
N131 -- A24P67364 [label="0.16", len=0.4700620948]
N131 -- A23P500844 [label="0.21", len=0.6250955931]
N130 -- A24P84719 [label="0.70", len=2.1112169418]
N130 -- N124 [label="0.16", len=0.4860244146]
N129 -- N126 [label="0.19", len=0.5636300217]
N129 -- A32P118481 [label="0.26", len=0.7942464380]
N128 -- A24P837537 [label="0.45", len=1.3378152176]
N128 -- N125 [label="0.18", len=0.5335055704]
N195 -- N192 [label="0.06", len=0.1656455625]
N127 -- N115 [label="0.79", len=2.3817261998]
N127 -- N123 [label="0.35", len=1.0645416792]
N126 -- A24P148907 [label="0.72", len=2.1679229753]
N126 -- N121 [label="0.40", len=1.1862689767]
N125 -- A23P416434 [label="0.13", len=0.3913243460]
N125 -- N122 [label="0.27", len=0.7957835488]
N124 -- A24P644742 [label="0.18", len=0.5414988162]
N124 -- N113 [label="0.57", len=1.7066974969]
N123 -- N107 [label="0.90", len=2.7130714685]
N123 -- N120 [label="0.16", len=0.4742448344]
N194 -- A24P350160 [label="0.13", len=0.3770721884]
N122 -- N118 [label="0.34", len=1.0185065517]
N122 -- A24P220984 [label="0.17", len=0.5097281540]
N121 -- A24P80915 [label="0.55", len=1.6542897806]
N121 -- A24P677219 [label="1.01", len=3.0342107850]
N120 -- A23P144549 [label="1.09", len=3.2747595526]
N120 -- N117 [label="0.24", len=0.7058344013]
N119 -- N109 [label="0.57", len=1.7106787978]
N119 -- N90 [label="1.43", len=4.2847423733]
N118 -- N116 [label="0.11", len=0.3306830947]
N118 -- A24P350771 [label="0.25", len=0.7639987451]
N194 -- N191 [label="0.09", len=0.2627943465]
N117 -- N114 [label="0.26", len=0.7928191693]
N117 -- A24P482104 [label="0.30", len=0.8878528193]
N116 -- N106 [label="0.57", len=1.7010254754]
N116 -- A23P258633 [label="0.31", len=0.9384180781]
N115 -- N105 [label="0.58", len=1.7349997048]
N115 -- A24P115990 [label="1.62", len=4.8521307718]
N114 -- A24P345866 [label="0.35", len=1.0466262558]
N114 -- N108 [label="0.20", len=0.6060774850]
N113 -- N112 [label="0.10", len=0.2952598896]
N113 -- N111 [label="0.11", len=0.3388375470]
N193 -- A23P26314 [label="0.15", len=0.4624579296]
N112 -- N110 [label="0.07", len=0.2227331591]
N112 -- A24P917866 [label="0.21", len=0.6162640873]
N111 -- A24P812018 [label="0.22", len=0.6555032634]
N111 -- A24P711050 [label="0.29", len=0.8693552014]
N110 -- N38 [label="0.45", len=1.3457814882]
N110 -- A32P186038 [label="0.34", len=1.0197665417]
N109 -- N100 [label="0.50", len=1.4902301655]
N109 -- N94 [label="0.48", len=1.4311965701]
N108 -- A32P197744 [label="0.68", len=2.0267419458]
N108 -- N104 [label="0.27", len=0.8072731202]
N193 -- A32P94199 [label="0.17", len=0.5156862281]
N107 -- N14 [label="4.68", len=14.0490438797]
N107 -- A23P156873 [label="0.80", len=2.4066146341]
N106 -- N98 [label="0.50", len=1.5086825152]
N106 -- A32P112263 [label="0.28", len=0.8500901534]
N105 -- N103 [label="0.14", len=0.4124796781]
N105 -- N67 [label="1.12", len=3.3738886943]
N104 -- A23P162300 [label="0.74", len=2.2056214086]
N104 -- N102 [label="0.22", len=0.6652506682]
N103 -- N97 [label="0.32", len=0.9704211833]
N103 -- A32P75357 [label="1.36", len=4.0847154902]
N201 -- N200 [label="0.02", len=0.0450282171]
N192 -- A23P401361 [label="0.16", len=0.4688378269]
N102 -- N101 [label="0.09", len=0.2587415709]
N102 -- A32P26401 [label="0.41", len=1.2255870078]
N101 -- N99 [label="0.11", len=0.3438879188]
N101 -- A24P54863 [label="0.41", len=1.2449615665]
N100 -- N69 [label="0.98", len=2.9394259367]
N100 -- A24P920826 [label="0.38", len=1.1497955683]
N99 -- N96 [label="0.08", len=0.2400685966]
N99 -- N95 [label="0.08", len=0.2388080001]
N98 -- A23P69768 [label="0.09", len=0.2583226828]
N98 -- A23P424727 [label="0.10", len=0.3003713260]
N192 -- A23P122210 [label="0.09", len=0.2730372847]
N97 -- N91 [label="0.25", len=0.7499667363]
N97 -- N79 [label="0.70", len=2.1061966412]
N96 -- N89 [label="0.41", len=1.2207186896]
N96 -- A24P109111 [label="0.20", len=0.6072437443]
N95 -- A32P82119 [label="0.14", len=0.4232680869]
N95 -- N93 [label="0.10", len=0.2978202833]
N94 -- N81 [label="0.52", len=1.5659705188]
N94 -- A24P265407 [label="0.66", len=1.9891335189]
N93 -- N87 [label="0.41", len=1.2410458911]
N93 -- N92 [label="0.02", len=0.0661258575]
N191 -- N190 [label="0.05", len=0.1402968654]
N92 -- A24P59554 [label="0.24", len=0.7303038908]
N92 -- A24P558750 [label="0.26", len=0.7730777167]
N91 -- A24P929835 [label="1.45", len=4.3509629814]
N91 -- N77 [label="0.78", len=2.3357223264]
N90 -- N80 [label="0.35", len=1.0648636588]
N90 -- N88 [label="0.16", len=0.4659418041]
N89 -- A23P140475 [label="0.26", len=0.7815166126]
N89 -- A24P943866 [label="0.31", len=0.9389225745]
N88 -- A23P321860 [label="2.32", len=6.9567304908]
N88 -- N78 [label="0.44", len=1.3301431863]
N191 -- A32P4792 [label="0.35", len=1.0585683054]
N87 -- N84 [label="0.16", len=0.4660686319]
N87 -- N86 [label="0.12", len=0.3620328678]
N86 -- A24P923534 [label="0.04", len=0.1138273939]
N86 -- N85 [label="0.03", len=0.0812267226]
N85 -- N83 [label="0.08", len=0.2261843071]
N85 -- A24P289067 [label="0.11", len=0.3197072987]
N84 -- A24P25437 [label="0.10", len=0.3073463681]
N84 -- A32P206344 [label="0.05", len=0.1498577431]
N83 -- A23P69606 [label="0.05", len=0.1617253356]
N83 -- N82 [label="0.03", len=0.0995837756]
N190 -- N189 [label="0.04", len=0.1253637336]
N82 -- A24P922979 [label="0.05", len=0.1639451548]
N82 -- A23P384551 [label="0.01", len=0.0390112221]
N81 -- A32P387648 [label="0.29", len=0.8609863076]
N81 -- A24P112730 [label="0.19", len=0.5748605759]
N80 -- A24P913156 [label="0.45", len=1.3531654218]
N80 -- A23P118894 [label="0.70", len=2.0947473131]
N79 -- A32P181937 [label="0.81", len=2.4310927463]
N79 -- A24P42557 [label="0.62", len=1.8555082233]
N78 -- N73 [label="0.25", len=0.7523768019]
N78 -- N76 [label="0.11", len=0.3402658171]
N190 -- N185 [label="0.09", len=0.2636815302]
N77 -- A23P36985 [label="1.20", len=3.5969746723]
N77 -- N61 [label="0.42", len=1.2498714274]
N76 -- N75 [label="0.11", len=0.3423505697]
N76 -- N74 [label="0.13", len=0.3883435658]
N75 -- A24P931030 [label="0.08", len=0.2320705142]
N75 -- A23P46070 [label="0.05", len=0.1510509022]
N74 -- A23P117873 [label="0.05", len=0.1514915431]
N74 -- N71 [label="0.06", len=0.1871976763]
N73 -- N70 [label="0.09", len=0.2666583514]
N73 -- N72 [label="0.04", len=0.1148609469]
N189 -- A24P400751 [label="0.11", len=0.3185955104]
N72 -- A24P119813 [label="0.31", len=0.9266858820]
N72 -- N62 [label="0.37", len=1.1150055092]
N71 -- A23P119448 [label="0.07", len=0.2139500526]
N71 -- A24P162393 [label="0.19", len=0.5645401884]
N70 -- A32P25243 [label="0.21", len=0.6332400724]
N70 -- N68 [label="0.15", len=0.4432031272]
N69 -- A23P82567 [label="0.31", len=0.9196094980]
N69 -- N65 [label="0.17", len=0.5184784581]
N68 -- A24P38722 [label="0.18", len=0.5417347068]
N68 -- N66 [label="0.05", len=0.1475360549]
N189 -- N182 [label="0.17", len=0.4967805479]
N67 -- N37 [label="0.62", len=1.8739253371]
N67 -- N36 [label="1.08", len=3.2483860634]
N66 -- A24P344251 [label="0.19", len=0.5773081055]
N66 -- A24P196428 [label="0.62", len=1.8651782255]
N65 -- A23P47904 [label="0.28", len=0.8272577585]
N65 -- N64 [label="0.03", len=0.0830311160]
N64 -- A32P332551 [label="0.30", len=0.8946085919]
N64 -- N63 [label="0.02", len=0.0697784105]
N63 -- N56 [label="0.13", len=0.4042568572]
N63 -- A24P66780 [label="0.06", len=0.1820099296]
N188 -- N187 [label="0.03", len=0.0820431651]
N62 -- N60 [label="0.04", len=0.1348554474]
N62 -- N55 [label="0.18", len=0.5408204078]
N61 -- N58 [label="0.09", len=0.2597718468]
N61 -- N53 [label="0.26", len=0.7701353198]
N60 -- A23P396934 [label="0.10", len=0.2872364313]
N60 -- N59 [label="0.06", len=0.1699798037]
N59 -- A24P68088 [label="0.18", len=0.5341099690]
N59 -- A23P170050 [label="0.12", len=0.3457161044]
N58 -- N57 [label="0.05", len=0.1368759061]
N58 -- N54 [label="0.15", len=0.4542326366]
N188 -- N186 [label="0.04", len=0.1174566202]
N57 -- N52 [label="0.25", len=0.7498592263]
N57 -- N50 [label="0.34", len=1.0244707024]
N56 -- A24P928156 [label="0.04", len=0.1092425231]
N56 -- A23P326700 [label="0.03", len=0.0851462984]
N55 -- A24P887239 [label="0.12", len=0.3644698502]
N55 -- A23P95417 [label="0.08", len=0.2429192604]
N54 -- N51 [label="0.21", len=0.6360255764]
N54 -- N49 [label="0.26", len=0.7785179710]
N53 -- A23P13465 [label="0.21", len=0.6166911433]
N53 -- A23P328145 [label="0.25", len=0.7394597596]
N201 -- A32P230196 [label="0.17", len=0.5130724769]
N187 -- N176 [label="0.18", len=0.5461914128]
N52 -- A23P125278 [label="0.38", len=1.1527010813]
N52 -- N47 [label="0.22", len=0.6534678920]
N51 -- A32P207096 [label="0.26", len=0.7788015296]
N51 -- A24P925673 [label="0.41", len=1.2154135354]
N50 -- N48 [label="0.04", len=0.1075661443]
N50 -- A24P889237 [label="0.23", len=0.6826009152]
N49 -- N46 [label="0.11", len=0.3188338031]
N49 -- A24P937039 [label="0.31", len=0.9324552283]
N48 -- A23P101636 [label="0.23", len=0.7027343043]
N48 -- N45 [label="0.15", len=0.4636012334]
N187 -- A23P202361 [label="0.13", len=0.3783516047]
N47 -- N44 [label="0.14", len=0.4109249444]
N47 -- A23P98622 [label="0.23", len=0.7027121512]
N46 -- N43 [label="0.14", len=0.4073400665]
N46 -- N42 [label="0.21", len=0.6403492534]
N45 -- A24P927304 [label="0.50", len=1.4927835920]
N45 -- A24P934145 [label="0.11", len=0.3274718255]
N44 -- N40 [label="0.20", len=0.6052466016]
N44 -- A24P871687 [label="0.37", len=1.1051400947]
N43 -- A24P476247 [label="0.33", len=1.0022238727]
N43 -- A24P927770 [label="0.25", len=0.7434374937]
N186 -- N184 [label="0.06", len=0.1853456163]
N42 -- N41 [label="0.04", len=0.1241514105]
N42 -- A23P385067 [label="0.14", len=0.4232024632]
N41 -- N39 [label="0.14", len=0.4271179708]
N41 -- A23P133949 [label="0.10", len=0.3080227385]
N40 -- A23P21990 [label="0.47", len=1.4107004031]
N40 -- A24P400180 [label="0.34", len=1.0241059967]
N39 -- N34 [label="0.23", len=0.6944925769]
N39 -- N35 [label="0.17", len=0.5053036452]
N38 -- N32 [label="0.17", len=0.4957975235]
N38 -- A24P246591 [label="0.33", len=0.9904014694]
N186 -- A24P144337 [label="0.09", len=0.2567278994]
N37 -- N29 [label="1.42", len=4.2470080157]
N37 -- A32P226605 [label="1.00", len=3.0054253505]
N36 -- A24P303091 [label="0.89", len=2.6653623436]
N36 -- A24P702912 [label="1.24", len=3.7331763723]
N35 -- A32P203917 [label="0.04", len=0.1109567345]
N35 -- A24P738168 [label="0.08", len=0.2281041494]
N34 -- A24P922139 [label="0.06", len=0.1747042099]
N34 -- N33 [label="0.10", len=0.3142885393]
N33 -- A32P12355 [label="0.08", len=0.2446761942]
N33 -- A23P397671 [label="0.22", len=0.6714866267]
N185 -- A24P911648 [label="0.18", len=0.5342287332]
N32 -- N31 [label="0.16", len=0.4940640867]
N32 -- A23P133263 [label="0.48", len=1.4325994928]
N31 -- A23P73096 [label="0.97", len=2.9230879167]
N31 -- N30 [label="0.84", len=2.5247515433]
N30 -- A24P118391 [label="0.67", len=1.9969119538]
N30 -- N27 [label="0.52", len=1.5668899717]
N29 -- N28 [label="0.08", len=0.2316576570]
N29 -- N26 [label="0.40", len=1.2080328221]
N28 -- N24 [label="0.65", len=1.9371004586]
N28 -- A24P304071 [label="1.15", len=3.4527681372]
N185 -- N183 [label="0.07", len=0.2168104726]
N27 -- N23 [label="0.65", len=1.9403006440]
N27 -- A32P75141 [label="2.34", len=7.0060385345]
N26 -- A24P316965 [label="0.21", len=0.6285392687]
N26 -- N25 [label="0.10", len=0.2875514459]
N25 -- A32P15128 [label="0.31", len=0.9264200849]
N25 -- A24P343929 [label="0.06", len=0.1910454448]
N24 -- A23P161218 [label="0.96", len=2.8727293193]
N24 -- N21 [label="0.50", len=1.4854220959]
N23 -- A32P200787 [label="0.34", len=1.0156288876]
N23 -- N22 [label="0.22", len=0.6635006039]
N184 -- A24P58187 [label="0.11", len=0.3345969748]
N22 -- N16 [label="0.91", len=2.7446899793]
N22 -- A24P269527 [label="0.75", len=2.2622141455]
N21 -- N20 [label="0.49", len=1.4742949287]
N21 -- A23P204087 [label="0.17", len=0.5045821736]
N20 -- A23P64828 [label="0.32", len=0.9728740049]
N20 -- N19 [label="0.09", len=0.2754044242]
N19 -- A23P4283 [label="0.29", len=0.8620084973]
N19 -- N18 [label="0.18", len=0.5395772617]
N18 -- A24P117294 [label="0.68", len=2.0281501167]
N18 -- N17 [label="0.08", len=0.2462214992]
N184 -- A24P237661 [label="0.07", len=0.2195411882]
N17 -- A23P4286 [label="0.60", len=1.7918028353]
N17 -- N13 [label="0.98", len=2.9440789736]
N16 -- N15 [label="0.59", len=1.7693807527]
N16 -- A24P212127 [label="0.48", len=1.4342967541]
N15 -- N12 [label="0.90", len=2.6943637174]
N15 -- N11 [label="1.55", len=4.6649860688]
N14 -- A32P302205 [label="0.42", len=1.2454253706]
N14 -- A32P461976 [label="0.85", len=2.5630837497]
N13 -- N10 [label="1.93", len=5.7887097140]
N13 -- A23P214821 [label="1.15", len=3.4621749204]
N183 -- N172 [label="0.25", len=0.7478610004]
N12 -- A23P400945 [label="0.16", len=0.4676061491]
N12 -- A24P140621 [label="0.75", len=2.2442231046]
N11 -- A23P22027 [label="3.75", len=11.2475707056]
N11 -- A32P112279 [label="1.03", len=3.1043312021]
N10 -- N9 [label="0.18", len=0.5447624184]
N10 -- A24P28722 [label="0.53", len=1.5835513056]
N9 -- N8 [label="0.18", len=0.5533709848]
N9 -- A23P139786 [label="0.56", len=1.6741233524]
N8 -- N7 [label="0.89", len=2.6784140701]
N8 -- A23P35412 [label="0.28", len=0.8459444551]
N183 -- A23P306211 [label="0.21", len=0.6170791186]
N7 -- N6 [label="0.25", len=0.7599523917]
N7 -- A23P24004 [label="1.05", len=3.1391252093]
N6 -- N5 [label="0.56", len=1.6875808881]
N6 -- A23P6263 [label="0.55", len=1.6631366570]
N5 -- N4 [label="0.65", len=1.9443452018]
N5 -- A23P14863 [label="1.53", len=4.5990662800]
N4 -- N3 [label="0.30", len=0.8905987604]
N4 -- A23P20814 [label="0.16", len=0.4803869958]
N3 -- N2 [label="0.11", len=0.3309125959]
N3 -- A23P17663 [label="0.14", len=0.4260057274]
N200 -- N199 [label="0.05", len=0.1446374230]
N182 -- A23P127013 [label="0.20", len=0.5908382448]
N2 -- N1 [label="1.54", len=4.6064058491]
N2 -- A23P45871 [label="0.21", len=0.6171271532]
N1 -- A23P48513 [label="0.25", len=0.7648760876]
N1 -- A23P52266 [label="2.67", len=8.0057904424]
N182 -- N181 [label="0.04", len=0.1274330976]
N181 -- A23P348992 [label="0.15", len=0.4547495553]
N181 -- N179 [label="0.07", len=0.1994774801]
N180 -- N158 [label="0.31", len=0.9265879949]
N180 -- N157 [label="0.20", len=0.5978519629]
N179 -- N177 [label="0.06", len=0.1842346647]
N179 -- N178 [label="0.04", len=0.1080975358]
N178 -- A24P215804 [label="0.32", len=0.9516525807]
N178 -- N175 [label="0.06", len=0.1768989934]
N200 -- N198 [label="0.05", len=0.1481315071]
N177 -- A23P144096 [label="0.16", len=0.4706994367]
N177 -- N173 [label="0.12", len=0.3551376916]
N176 -- N174 [label="0.04", len=0.1155096453]
N176 -- N159 [label="0.09", len=0.2844443184]
N175 -- A24P761130 [label="0.29", len=0.8693591447]
N175 -- N170 [label="0.15", len=0.4627093279]
N174 -- A24P915675 [label="0.11", len=0.3293285397]
N174 -- A23P501634 [label="0.23", len=0.6887159712]
N173 -- A32P234294 [label="0.34", len=1.0245872158]
N173 -- N168 [label="0.13", len=0.3953926792]
N199 -- A32P220152 [label="0.10", len=0.2945490579]
N172 -- A24P66932 [label="0.18", len=0.5522027274]
N172 -- N171 [label="0.03", len=0.0950097777]
N171 -- N169 [label="0.10", len=0.2940660018]
N171 -- N165 [label="0.17", len=0.5122455741]
N170 -- N162 [label="0.15", len=0.4544391162]
N170 -- A24P25040 [label="0.30", len=0.9135875625]
N169 -- N166 [label="0.08", len=0.2418611608]
N169 -- N164 [label="0.12", len=0.3621102955]
N168 -- N167 [label="0.04", len=0.1161467970]
N168 -- A24P941946 [label="0.06", len=0.1825274312]
N199 -- A32P34970 [label="0.05", len=0.1393736426]
N167 -- A24P281730 [label="0.08", len=0.2401850779]
N167 -- A32P233735 [label="0.07", len=0.2152651041]
N166 -- N161 [label="0.13", len=0.3925246801]
N166 -- N163 [label="0.08", len=0.2298428295]
N165 -- N155 [label="0.19", len=0.5788423625]
N165 -- N154 [label="0.26", len=0.7937359006]
N164 -- A32P139302 [label="0.05", len=0.1549359546]
N164 -- A24P75543 [label="0.20", len=0.5893629795]
N163 -- N160 [label="0.12", len=0.3458728739]
N163 -- N136 [label="0.71", len=2.1398773663]
N198 -- N195 [label="0.13", len=0.3763192205]
N162 -- A23P353316 [label="0.21", len=0.6412617516]
N162 -- A23P390032 [label="0.12", len=0.3479121082]
N161 -- A24P201936 [label="0.15", len=0.4532913959]
N161 -- N144 [label="0.43", len=1.3034980614]
N160 -- A24P391574 [label="0.07", len=0.2055646431]
N160 -- A24P924251 [label="0.21", len=0.6237078937]
N159 -- N150 [label="0.23", len=0.6957992516]
N159 -- A24P247536 [label="0.23", len=0.7011280863]
N158 -- N156 [label="0.08", len=0.2502725089]
N158 -- A32P206561 [label="0.29", len=0.8607748339]
N198 -- N196 [label="0.08", len=0.2299226796]
N157 -- N152 [label="0.11", len=0.3359745291]
N157 -- A24P350017 [label="0.15", len=0.4575294890]
N156 -- A32P396186 [label="0.45", len=1.3507753768]
N156 -- N137 [label="0.61", len=1.8387515502]
N155 -- N147 [label="0.24", len=0.7066082660]
N155 -- A24P170384 [label="0.12", len=0.3541231196]
N154 -- N153 [label="0.06", len=0.1900579832]
N154 -- A23P10091 [label="0.17", len=0.5221628729]
N153 -- N145 [label="0.25", len=0.7621343697]
N153 -- A23P391443 [label="0.36", len=1.0724572933]
}
```

The following clusters were estimated ...

 * A24P246591, N38, A23P133263, N32
 * N167, N132, N150, A24P915675, N161, A23P122210, N169, N162, A23P127013, N187, A23P348992, A24P144337, N126, A24P924251, N194, N164, A24P911648, N134, N171, A24P58187, A24P392505, A32P234294, A24P215804, N153, A23P26314, N191, N155, A32P118481, A23P353316, A24P298604, N148, A32P233735, A23P144096, A24P101601, N183, N201, A32P34970, A24P400751, A23P390032, N199, N165, N181, N142, N200, N154, A24P170384, A24P237661, A23P306211, A24P350017, N146, A23P202361, N151, N138, N192, A23P501634, N141, N173, N193, N189, N166, N149, N185, N180, N176, A24P358337, A24P247536, A24P391574, A24P152855, A32P139302, N172, N186, A24P350160, N152, A24P66932, A24P201936, N182, A24P136161, N195, A24P25040, N198, A32P234202, A32P220152, N177, A32P20582, A24P941946, N160, A24P290188, N147, N139, N178, A32P112401, A24P281730, A32P4792, A23P10091, A32P94199, A32P224666, A23P401361, A24P761130, N188, N170, N174, A32P73452, N159, A24P298099, N190, A24P75543, A24P315474, N145, N163, N184, N196, N129, A24P884376, N197, N168, A32P230196, N157, A23P391443, N179, N175
 * A23P397671, N39, N34, A32P12355, A32P203917, N33, N35, A23P133949, N41, N49, A24P738168, A24P927770, A24P476247, N43, N46, A23P385067, A24P937039, A24P922139, N42
 * A24P119813, N73, A24P38722, N68, N70, N72, A24P344251, N66, A32P25243
 * N78, N76, N71, A23P117873, N75, N74, A24P931030, A23P46070, A23P119448, A24P162393
 * A24P289067, N86, N85, A23P384551, A23P69606, N82, A24P25437, N83, A32P206344, N84, N87, A24P922979, A24P923534
 * A23P125278, A23P98622, A24P871687, N44, N52, N47
 * A32P387648, N81, A24P112730
 * N51, A24P925673, A32P207096, N54
 * N40, A24P400180, A23P21990
 * A23P416434, N122, N128, A24P837537, A24P220984, N125
 * N140, N135, A24P67364, N131, A23P500844, A24P162211
 * A24P109111, A24P59554, A32P82119, N96, N99, N101, A24P558750, N93, N92, A24P54863, N95, A32P26401, N102
 * A32P186038, N112, N111, A24P917866, A24P711050, A24P812018, N110, N113
 * A24P350771, A23P258633, N118, N116
 * N2, A23P20814, A23P17663, N3, N4, A23P45871
 * N144, N143, A24P914102, A32P211048
 * N61, A23P13465, A23P328145, N53
 * A32P332551, N56, A24P66780, A23P326700, A23P47904, N69, N64, N63, N65, A23P82567, A24P928156
 * N98, A23P69768, A23P424727
 * A23P64828, N20, N18, A23P4283, N19
 * A32P396186, N156, A32P206561, N158
 * N45, N50, A24P934145, A24P927304, A24P889237, N48, A23P101636
 * A23P95417, N59, N55, A23P396934, A24P68088, N62, N60, A23P170050, A24P887239
 * N89, A23P140475, A24P943866
 * A32P15128, A24P316965, N25, N26, A24P343929

</div>

`{bm-enable-all}`

