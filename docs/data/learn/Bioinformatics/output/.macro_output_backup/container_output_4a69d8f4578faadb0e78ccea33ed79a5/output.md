<div style="border:1px solid black;">

`{bm-disable-all}`

Given the sequences AGAC and TAAGAACT and the score matrix...

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
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, 0.0) (N0_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -3.75) (N0_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -7.5) (N0_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -11.25) (N0_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -15.0) (N0_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -18.75) (N0_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -22.5) (N0_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -26.25) (N0_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -30.0) (N0_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, 0.0) (N1_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -3.75) (N1_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -7.5) (N1_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -11.25) (N1_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -15.0) (N1_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -18.75) (N1_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -22.5) (N1_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -26.25) (N1_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -30.0) (N1_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, 0.0) (N2_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -3.75) (N2_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -7.5) (N2_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -11.25) (N2_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -15.0) (N2_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -18.75) (N2_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -22.5) (N2_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -26.25) (N2_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -30.0) (N2_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, 0.0) (N3_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -3.75) (N3_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -7.5) (N3_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -11.25) (N3_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -15.0) (N3_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -18.75) (N3_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -22.5) (N3_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -26.25) (N3_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -30.0) (N3_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, 0.0) (N4_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -3.75) (N4_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -7.5) (N4_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -11.25) (N4_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -15.0) (N4_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -18.75) (N4_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -22.5) (N4_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -26.25) (N4_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -30.0) (N4_8) {};
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (N0_0) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (N0_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (N0_0) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (N0_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (N0_0) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (N0_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (N0_0) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (N0_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, green] (N0_0) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (N0_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (N0_0) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (N0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (N0_0) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (N0_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_0) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N1_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_0) to [] node [align=center, midway, color=black] {A\\ T\\ -1.0} (N1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N0_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (N0_0) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (N0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N0_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_1) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_1) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_2) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N1_2);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (N0_2) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N1_3);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_2) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_3) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (N0_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_3) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_3) to [] node [align=center, midway, color=black] {A\\ G\\ -1.0} (N1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_4) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_4) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N0_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_4) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_5) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_5) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_5) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_6) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_6) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N0_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_7) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N0_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_7) to [] node [align=center, midway, color=black] {A\\ T\\ -1.0} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_7) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_8) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_0) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N2_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_0) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (N2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_1) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_1) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_2) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_2) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_2) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N1_3);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (N1_3) to [] node [align=center, midway, color=black] {G\\ G\\ 1.0} (N2_4);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_3) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_3) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (N1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_4) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_4) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_4) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_5) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_5) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_5) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_6) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_6) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_7) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_7) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_7) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_8) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_0) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N3_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_0) to [] node [align=center, midway, color=black] {A\\ T\\ -1.0} (N3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_1) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_1) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_2) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_2) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_2) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_3) to [] node [align=center, midway, color=black] {A\\ G\\ -1.0} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_3) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_3) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (N2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_4) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_4) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N3_5);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (N2_4) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N2_5);
        \draw[->, >=stealth, line width = 2px, green] (N2_5) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N3_6);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_5) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_5) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_6) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_6) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_7) to [] node [align=center, midway, color=black] {A\\ T\\ -1.0} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_7) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_7) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_8) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_0) to [] node [align=center, midway, color=black] {C\\ T\\ -1.0} (N4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_0) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N4_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_1) to [] node [align=center, midway, color=black] {C\\ A\\ -1.0} (N4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_1) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_2) to [] node [align=center, midway, color=black] {C\\ A\\ -1.0} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_2) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_2) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_3) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_3) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_3) to [] node [align=center, midway, color=black] {C\\ G\\ -1.0} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_4) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_4) to [] node [align=center, midway, color=black] {C\\ A\\ -1.0} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_4) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_5) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_5) to [] node [align=center, midway, color=black] {C\\ A\\ -1.0} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_5) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_6) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N4_6);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (N3_6) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (N4_7);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_7) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_7) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_7) to [] node [align=center, midway, color=black] {C\\ T\\ -1.0} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_8) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_2) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (N4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_3) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_4) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (N4_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (N4_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_5) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (N4_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, green] (N4_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_7) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N4_8);
        \end{pgfonlayer}

    \end{tikzpicture}
\end{document}

````

````
AG-AC
AGAAC
````

Weight: 3.0
</div>

`{bm-enable-all}`

