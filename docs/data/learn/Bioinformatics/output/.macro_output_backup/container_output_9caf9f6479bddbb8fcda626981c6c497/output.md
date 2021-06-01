<div style="border:1px solid black;">

`{bm-disable-all}`

Applying 2-breaks on circular genome until red_p_list=[['+A', '-B', '-C', '+D'], ['+E']] matches blue_p_list=[['+A', '+B', '-D'], ['-C', '-E']] (show_graph=True)...

 * Initial red_p_list=[['+A', '-B', '-C', '+D'], ['+E']]

   ```{dot}
   graph G {
   layout=neato
   node [shape=plain];
   _A_h_ [pos="2.5,-6.123233995736766e-16!"];
   _A_t_ [pos="2.022542485937368,-1.4694631307311834!"];
   _B_h_ [pos="0.7725424859373681,-2.377641290737884!"];
   _B_t_ [pos="-0.7725424859373689,-2.3776412907378837!"];
   _D_t_ [pos="-2.022542485937369,-1.4694631307311825!"];
   _D_h_ [pos="-2.5,3.061616997868383e-16!"];
   _C_h_ [pos="-2.022542485937368,1.4694631307311832!"];
   _C_t_ [pos="-0.7725424859373684,2.377641290737884!"];
   _E_h_ [pos="0.7725424859373686,2.3776412907378837!"];
   _E_t_ [pos="2.0225424859373686,1.469463130731183!"];
   _A_h_ -- _A_t_ [style=dashed, dir=forward];
   _B_h_ -- _B_t_ [style=dashed, dir=forward];
   _D_t_ -- _D_h_ [style=dashed, dir=back];
   _C_h_ -- _C_t_ [style=dashed, dir=forward];
   _E_h_ -- _E_t_ [style=dashed, dir=forward];
   _A_h_ -- _D_h_ [color=blue];
   _C_h_ -- _E_t_ [color=blue];
   _A_t_ -- _B_h_ [color=blue];
   _B_t_ -- _D_t_ [color=blue];
   _C_t_ -- _E_h_ [color=blue];
   _B_h_ -- _C_t_ [color=red];
   _A_h_ -- _D_t_ [color=red];
   _E_h_ -- _E_t_ [color=red];
   _C_h_ -- _D_h_ [color=red];
   _A_t_ -- _B_t_ [color=red];
   }
   ```
 * red_p_list=[['+A', '+B', '-C', '+D'], ['+E']]

   ```{dot}
   graph G {
   layout=neato
   node [shape=plain];
   _A_h_ [pos="2.5,-6.123233995736766e-16!"];
   _A_t_ [pos="2.022542485937368,-1.4694631307311834!"];
   _B_h_ [pos="0.7725424859373681,-2.377641290737884!"];
   _B_t_ [pos="-0.7725424859373689,-2.3776412907378837!"];
   _D_t_ [pos="-2.022542485937369,-1.4694631307311825!"];
   _D_h_ [pos="-2.5,3.061616997868383e-16!"];
   _C_h_ [pos="-2.022542485937368,1.4694631307311832!"];
   _C_t_ [pos="-0.7725424859373684,2.377641290737884!"];
   _E_h_ [pos="0.7725424859373686,2.3776412907378837!"];
   _E_t_ [pos="2.0225424859373686,1.469463130731183!"];
   _A_h_ -- _A_t_ [style=dashed, dir=forward];
   _B_h_ -- _B_t_ [style=dashed, dir=forward];
   _D_t_ -- _D_h_ [style=dashed, dir=back];
   _C_h_ -- _C_t_ [style=dashed, dir=forward];
   _E_h_ -- _E_t_ [style=dashed, dir=forward];
   _A_h_ -- _D_h_ [color=blue];
   _C_h_ -- _E_t_ [color=blue];
   _A_t_ -- _B_h_ [color=blue];
   _B_t_ -- _D_t_ [color=blue];
   _C_t_ -- _E_h_ [color=blue];
   _A_h_ -- _D_t_ [color=red];
   _E_h_ -- _E_t_ [color=red];
   _C_h_ -- _D_h_ [color=red];
   _A_t_ -- _B_h_ [color=red];
   _B_t_ -- _C_t_ [color=red];
   }
   ```
 * red_p_list=[['+A', '+B', '-C', '-D'], ['+E']]

   ```{dot}
   graph G {
   layout=neato
   node [shape=plain];
   _A_h_ [pos="2.5,-6.123233995736766e-16!"];
   _A_t_ [pos="2.022542485937368,-1.4694631307311834!"];
   _B_h_ [pos="0.7725424859373681,-2.377641290737884!"];
   _B_t_ [pos="-0.7725424859373689,-2.3776412907378837!"];
   _D_t_ [pos="-2.022542485937369,-1.4694631307311825!"];
   _D_h_ [pos="-2.5,3.061616997868383e-16!"];
   _C_h_ [pos="-2.022542485937368,1.4694631307311832!"];
   _C_t_ [pos="-0.7725424859373684,2.377641290737884!"];
   _E_h_ [pos="0.7725424859373686,2.3776412907378837!"];
   _E_t_ [pos="2.0225424859373686,1.469463130731183!"];
   _A_h_ -- _A_t_ [style=dashed, dir=forward];
   _B_h_ -- _B_t_ [style=dashed, dir=forward];
   _D_t_ -- _D_h_ [style=dashed, dir=back];
   _C_h_ -- _C_t_ [style=dashed, dir=forward];
   _E_h_ -- _E_t_ [style=dashed, dir=forward];
   _A_h_ -- _D_h_ [color=blue];
   _C_h_ -- _E_t_ [color=blue];
   _A_t_ -- _B_h_ [color=blue];
   _B_t_ -- _D_t_ [color=blue];
   _C_t_ -- _E_h_ [color=blue];
   _A_h_ -- _D_h_ [color=red];
   _E_h_ -- _E_t_ [color=red];
   _A_t_ -- _B_h_ [color=red];
   _B_t_ -- _C_t_ [color=red];
   _C_h_ -- _D_t_ [color=red];
   }
   ```
 * red_p_list=[['+A', '+B', '-D'], ['+E'], ['+C']]

   ```{dot}
   graph G {
   layout=neato
   node [shape=plain];
   _A_h_ [pos="2.5,-6.123233995736766e-16!"];
   _A_t_ [pos="2.022542485937368,-1.4694631307311834!"];
   _B_h_ [pos="0.7725424859373681,-2.377641290737884!"];
   _B_t_ [pos="-0.7725424859373689,-2.3776412907378837!"];
   _D_t_ [pos="-2.022542485937369,-1.4694631307311825!"];
   _D_h_ [pos="-2.5,3.061616997868383e-16!"];
   _C_h_ [pos="-2.022542485937368,1.4694631307311832!"];
   _C_t_ [pos="-0.7725424859373684,2.377641290737884!"];
   _E_h_ [pos="0.7725424859373686,2.3776412907378837!"];
   _E_t_ [pos="2.0225424859373686,1.469463130731183!"];
   _A_h_ -- _A_t_ [style=dashed, dir=forward];
   _B_h_ -- _B_t_ [style=dashed, dir=forward];
   _D_t_ -- _D_h_ [style=dashed, dir=back];
   _C_h_ -- _C_t_ [style=dashed, dir=forward];
   _E_h_ -- _E_t_ [style=dashed, dir=forward];
   _A_h_ -- _D_h_ [color=blue];
   _C_h_ -- _E_t_ [color=blue];
   _A_t_ -- _B_h_ [color=blue];
   _B_t_ -- _D_t_ [color=blue];
   _C_t_ -- _E_h_ [color=blue];
   _A_h_ -- _D_h_ [color=red];
   _E_h_ -- _E_t_ [color=red];
   _A_t_ -- _B_h_ [color=red];
   _B_t_ -- _D_t_ [color=red];
   _C_h_ -- _C_t_ [color=red];
   }
   ```
 * red_p_list=[['+A', '+B', '-D'], ['+C', '+E']]

   ```{dot}
   graph G {
   layout=neato
   node [shape=plain];
   _A_h_ [pos="2.5,-6.123233995736766e-16!"];
   _A_t_ [pos="2.022542485937368,-1.4694631307311834!"];
   _B_h_ [pos="0.7725424859373681,-2.377641290737884!"];
   _B_t_ [pos="-0.7725424859373689,-2.3776412907378837!"];
   _D_t_ [pos="-2.022542485937369,-1.4694631307311825!"];
   _D_h_ [pos="-2.5,3.061616997868383e-16!"];
   _C_h_ [pos="-2.022542485937368,1.4694631307311832!"];
   _C_t_ [pos="-0.7725424859373684,2.377641290737884!"];
   _E_h_ [pos="0.7725424859373686,2.3776412907378837!"];
   _E_t_ [pos="2.0225424859373686,1.469463130731183!"];
   _A_h_ -- _A_t_ [style=dashed, dir=forward];
   _B_h_ -- _B_t_ [style=dashed, dir=forward];
   _D_t_ -- _D_h_ [style=dashed, dir=back];
   _C_h_ -- _C_t_ [style=dashed, dir=forward];
   _E_h_ -- _E_t_ [style=dashed, dir=forward];
   _A_h_ -- _D_h_ [color=blue];
   _C_h_ -- _E_t_ [color=blue];
   _A_t_ -- _B_h_ [color=blue];
   _B_t_ -- _D_t_ [color=blue];
   _C_t_ -- _E_h_ [color=blue];
   _A_h_ -- _D_h_ [color=red];
   _C_h_ -- _E_t_ [color=red];
   _A_t_ -- _B_h_ [color=red];
   _B_t_ -- _D_t_ [color=red];
   _C_t_ -- _E_h_ [color=red];
   }
   ```


Recall that the the breakpoint graph is undirected. A permutation may have been walked in either direction (clockwise vs counter-clockwise) and there are multiple nodes to start walking from. If the output looks like it's going backwards, that's just as correct as if it looked like it's going forward.

Also, recall that a genome is represented as a set of permutations -- sets are not ordered.
</div>

`{bm-enable-all}`

