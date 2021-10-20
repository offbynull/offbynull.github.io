<div style="border:1px solid black;">

`{bm-disable-all}`

Given the sequences TGGCGG and TCCCCC and the score matrix...

```
INDEL=-1.0
    A   C   T   G
A   1  -1  -1  -1
C  -1   1  -1  -1
T  -1  -1   1  -1
G  -1  -1  -1   1

````

... the global alignment is...

````{latex}

\documentclass{standalone}
\usepackage{pgf, tikz, pagecolor}
\usetikzlibrary{arrows, automata}
\pgfdeclarelayer{bg}    % declare background layer
\pgfsetlayers{bg,main}  % set the order of the layers (main is the standard layer)
\begin{document}
    \pagecolor{white}
    \begin{tikzpicture}
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -26.25) (Nmid_0_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -30.0) (Nmid_0_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -33.75) (Nmid_0_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -37.5) (Nmid_0_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -41.25) (Nmid_0_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -45.0) (Nmid_0_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -48.75) (Nmid_0_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -26.25) (Nmid_1_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -30.0) (Nmid_1_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -33.75) (Nmid_1_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -37.5) (Nmid_1_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -41.25) (Nmid_1_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -45.0) (Nmid_1_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -48.75) (Nmid_1_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -26.25) (Nmid_2_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -30.0) (Nmid_2_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -33.75) (Nmid_2_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -37.5) (Nmid_2_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -41.25) (Nmid_2_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -45.0) (Nmid_2_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -48.75) (Nmid_2_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, -26.25) (Nmid_3_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, -30.0) (Nmid_3_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, -33.75) (Nmid_3_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, -37.5) (Nmid_3_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, -41.25) (Nmid_3_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, -45.0) (Nmid_3_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, -48.75) (Nmid_3_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, -26.25) (Nmid_4_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, -30.0) (Nmid_4_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, -33.75) (Nmid_4_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, -37.5) (Nmid_4_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, -41.25) (Nmid_4_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, -45.0) (Nmid_4_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, -48.75) (Nmid_4_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (45.0, -26.25) (Nmid_5_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (45.0, -30.0) (Nmid_5_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (45.0, -33.75) (Nmid_5_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (45.0, -37.5) (Nmid_5_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (45.0, -41.25) (Nmid_5_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (45.0, -45.0) (Nmid_5_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (45.0, -48.75) (Nmid_5_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (48.75, -26.25) (Nmid_6_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (48.75, -30.0) (Nmid_6_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (48.75, -33.75) (Nmid_6_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (48.75, -37.5) (Nmid_6_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (48.75, -41.25) (Nmid_6_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (48.75, -45.0) (Nmid_6_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (48.75, -48.75) (Nmid_6_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -52.5) (Nlow_0_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -56.25) (Nlow_0_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -60.0) (Nlow_0_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -63.75) (Nlow_0_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -67.5) (Nlow_0_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -71.25) (Nlow_0_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -75.0) (Nlow_0_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -52.5) (Nlow_1_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -56.25) (Nlow_1_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -60.0) (Nlow_1_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -63.75) (Nlow_1_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -67.5) (Nlow_1_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -71.25) (Nlow_1_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -75.0) (Nlow_1_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -52.5) (Nlow_2_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -56.25) (Nlow_2_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -60.0) (Nlow_2_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -63.75) (Nlow_2_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -67.5) (Nlow_2_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -71.25) (Nlow_2_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -75.0) (Nlow_2_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -52.5) (Nlow_3_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -56.25) (Nlow_3_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -60.0) (Nlow_3_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -63.75) (Nlow_3_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -67.5) (Nlow_3_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -71.25) (Nlow_3_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -75.0) (Nlow_3_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -52.5) (Nlow_4_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -56.25) (Nlow_4_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -60.0) (Nlow_4_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -63.75) (Nlow_4_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -67.5) (Nlow_4_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -71.25) (Nlow_4_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -75.0) (Nlow_4_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -52.5) (Nlow_5_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -56.25) (Nlow_5_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -60.0) (Nlow_5_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -63.75) (Nlow_5_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -67.5) (Nlow_5_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -71.25) (Nlow_5_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -75.0) (Nlow_5_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -52.5) (Nlow_6_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -56.25) (Nlow_6_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -60.0) (Nlow_6_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -63.75) (Nlow_6_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -67.5) (Nlow_6_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -71.25) (Nlow_6_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -75.0) (Nlow_6_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (52.5, 0.0) (Nhigh_0_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (52.5, -3.75) (Nhigh_0_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (52.5, -7.5) (Nhigh_0_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (52.5, -11.25) (Nhigh_0_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (52.5, -15.0) (Nhigh_0_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (52.5, -18.75) (Nhigh_0_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (52.5, -22.5) (Nhigh_0_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (56.25, 0.0) (Nhigh_1_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (56.25, -3.75) (Nhigh_1_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (56.25, -7.5) (Nhigh_1_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (56.25, -11.25) (Nhigh_1_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (56.25, -15.0) (Nhigh_1_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (56.25, -18.75) (Nhigh_1_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (56.25, -22.5) (Nhigh_1_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (60.0, 0.0) (Nhigh_2_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (60.0, -3.75) (Nhigh_2_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (60.0, -7.5) (Nhigh_2_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (60.0, -11.25) (Nhigh_2_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (60.0, -15.0) (Nhigh_2_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (60.0, -18.75) (Nhigh_2_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (60.0, -22.5) (Nhigh_2_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (63.75, 0.0) (Nhigh_3_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (63.75, -3.75) (Nhigh_3_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (63.75, -7.5) (Nhigh_3_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (63.75, -11.25) (Nhigh_3_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (63.75, -15.0) (Nhigh_3_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (63.75, -18.75) (Nhigh_3_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (63.75, -22.5) (Nhigh_3_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (67.5, 0.0) (Nhigh_4_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (67.5, -3.75) (Nhigh_4_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (67.5, -7.5) (Nhigh_4_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (67.5, -11.25) (Nhigh_4_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (67.5, -15.0) (Nhigh_4_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (67.5, -18.75) (Nhigh_4_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (67.5, -22.5) (Nhigh_4_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (71.25, 0.0) (Nhigh_5_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (71.25, -3.75) (Nhigh_5_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (71.25, -7.5) (Nhigh_5_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (71.25, -11.25) (Nhigh_5_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (71.25, -15.0) (Nhigh_5_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (71.25, -18.75) (Nhigh_5_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (71.25, -22.5) (Nhigh_5_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (75.0, 0.0) (Nhigh_6_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (75.0, -3.75) (Nhigh_6_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (75.0, -7.5) (Nhigh_6_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (75.0, -11.25) (Nhigh_6_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (75.0, -15.0) (Nhigh_6_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (75.0, -18.75) (Nhigh_6_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (75.0, -22.5) (Nhigh_6_6) {};
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_0) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_0);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (Nmid_0_0) to [] node [align=center, midway, color=black] {T\\ T\\ 1.0} (Nmid_1_1);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (Nlow_0_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_1) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_0_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_1) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_1) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (Nmid_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_2) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (Nmid_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_2) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_0_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_3) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (Nmid_1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_3) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_4) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_4) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (Nmid_1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_0_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_5) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (Nmid_1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_5) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_6) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_0) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_2_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (Nlow_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_0) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (Nmid_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_1) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, green] (Nmid_1_1) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_1) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_2) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_2) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_3) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_3) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_4) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_4) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_5) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_5) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_6) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_0) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_3_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_0) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (Nmid_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (Nlow_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_1) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_1) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_1) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_2) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_2) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_3) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_3) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_4) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_4) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_5) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_5) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_6) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_0) to [] node [align=center, midway, color=black] {C\\ T\\ -1.0} (Nmid_4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_0) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (Nhigh_4_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (Nlow_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_1) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_1) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (Nhigh_4_1);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (Nmid_3_1) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (Nmid_4_2);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_2) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (Nhigh_4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_2) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (Nmid_4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_3) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (Nhigh_4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_3) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (Nmid_4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_4) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (Nmid_4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_4) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (Nhigh_4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_5) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (Nmid_4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_5) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (Nhigh_4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_6) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (Nhigh_4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (Nlow_4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_0) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_5_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_0) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (Nmid_5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_1) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_1) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_1) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_2) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_2) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, green] (Nmid_4_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_3) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_3) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_4) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_4) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_5) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_5) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_4_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, green] (Nmid_4_6) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (Nlow_5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_0) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (Nmid_6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_0) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_6_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_1) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_1) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_1) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_2) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_2) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_3) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_3) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_4) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_4) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_5) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (Nmid_6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_5) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_5_6) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (Nhigh_6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_6_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (Nlow_6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_6_1) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_6_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_6_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_6_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_6_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (Nlow_6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_0_0) to [] node [align=center, midway, color=black] {—\\ T\\ -0.1} (Nlow_0_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_0_1) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_0_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_0_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_0_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_0_2) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_0_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_0_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_0_3) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_0_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_0_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_0_4) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_0_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_0_4) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_0_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_0_5) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_0_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_0_5) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_0_6) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_1_0) to [] node [align=center, midway, color=black] {—\\ T\\ -0.1} (Nlow_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_1_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_1_1) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_1_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_1_2) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_1_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_1_3) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_1_4) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_1_4) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_1_5) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_1_5) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_1_6) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_2_0) to [] node [align=center, midway, color=black] {—\\ T\\ -0.1} (Nlow_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_2_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_2_1) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_2_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_2_2) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_2_3) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_2_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_2_4) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_2_4) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_2_5) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_2_5) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_2_6) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_3_0) to [] node [align=center, midway, color=black] {—\\ T\\ -0.1} (Nlow_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_3_1) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_3_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_3_2) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_3_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_3_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_3_3) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_3_4) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_3_4) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_3_5) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_3_5) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_3_6) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_4_0) to [] node [align=center, midway, color=black] {—\\ T\\ -0.1} (Nlow_4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_4_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_4_1) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_4_2) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_4_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_4_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_3);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (Nlow_4_3) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_4_4);
        \draw[->, >=stealth, line width = 2px, green] (Nlow_4_4) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_4_5);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_4_4) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_4_5) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_5);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (Nlow_4_5) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_4_6);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_4_6) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_5_0) to [] node [align=center, midway, color=black] {—\\ T\\ -0.1} (Nlow_5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_5_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_5_1) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_5_2) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_5_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_5_3) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_5_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_5_4) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_5_4) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_5_5) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_5_5) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_5_6) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_6_0) to [] node [align=center, midway, color=black] {—\\ T\\ -0.1} (Nlow_6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_6_1) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_6_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_6_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_6_2) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_6_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_6_3) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_6_4) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_6_4) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_6_5) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_6_5) to [] node [align=center, midway, color=black] {—\\ C\\ -0.1} (Nlow_6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_6_6) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_0_0) to [] node [align=center, midway, color=black] {T\\ —\\ -0.1} (Nhigh_1_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_0_1) to [] node [align=center, midway, color=black] {T\\ —\\ -0.1} (Nhigh_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_0_2) to [] node [align=center, midway, color=black] {T\\ —\\ -0.1} (Nhigh_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_0_3) to [] node [align=center, midway, color=black] {T\\ —\\ -0.1} (Nhigh_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_0_4) to [] node [align=center, midway, color=black] {T\\ —\\ -0.1} (Nhigh_1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_0_5) to [] node [align=center, midway, color=black] {T\\ —\\ -0.1} (Nhigh_1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_0_6) to [] node [align=center, midway, color=black] {T\\ —\\ -0.1} (Nhigh_1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_0) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_2_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_1) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_2) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_3) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_4) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_5) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_6) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_2_0) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_3_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_1);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (Nhigh_2_1) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_3_1);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_2_2) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_2_3) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_2_4) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_2_5) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_2_6) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_3_0) to [] node [align=center, midway, color=black] {C\\ —\\ -0.1} (Nhigh_4_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_3_1) to [] node [align=center, midway, color=black] {C\\ —\\ -0.1} (Nhigh_4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_3_2) to [] node [align=center, midway, color=black] {C\\ —\\ -0.1} (Nhigh_4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_3_3) to [] node [align=center, midway, color=black] {C\\ —\\ -0.1} (Nhigh_4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_3_4) to [] node [align=center, midway, color=black] {C\\ —\\ -0.1} (Nhigh_4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_3_5) to [] node [align=center, midway, color=black] {C\\ —\\ -0.1} (Nhigh_4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_3_6) to [] node [align=center, midway, color=black] {C\\ —\\ -0.1} (Nhigh_4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_4_0) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_5_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_4_1) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_4_2) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_4_3) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_4_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_4_4) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_4_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_4_5) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_4_6) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_4_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_5_0) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_6_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_5_1) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_5_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_5_2) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_5_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_5_3) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_5_4) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_5_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_5_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_5_5) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_6_5);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (Nhigh_5_6) to [] node [align=center, midway, color=black] {G\\ —\\ -0.1} (Nhigh_6_6);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_5_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_6_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_6_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_6_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_6_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_6_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_6_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_6_6);
        \end{pgfonlayer}

    \end{tikzpicture}
\end{document}

````

````
TGGC----GG
T--CCCCC--
````

Weight: -1.5
</div>

`{bm-enable-all}`

