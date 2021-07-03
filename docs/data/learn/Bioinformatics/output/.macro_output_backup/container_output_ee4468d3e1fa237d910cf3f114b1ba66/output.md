<div style="border:1px solid black;">

`{bm-disable-all}`

Given the sequences TAGGCGGAT and TACCCCCAT and the score matrix...

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
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -33.75) (N0_9) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, 0.0) (N1_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -3.75) (N1_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -7.5) (N1_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -11.25) (N1_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -15.0) (N1_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -18.75) (N1_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -22.5) (N1_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -26.25) (N1_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -30.0) (N1_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -33.75) (N1_9) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, 0.0) (N2_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -3.75) (N2_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -7.5) (N2_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -11.25) (N2_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -15.0) (N2_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -18.75) (N2_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -22.5) (N2_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -26.25) (N2_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -30.0) (N2_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -33.75) (N2_9) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, 0.0) (N3_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -3.75) (N3_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -7.5) (N3_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -11.25) (N3_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -15.0) (N3_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -18.75) (N3_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -22.5) (N3_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -26.25) (N3_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -30.0) (N3_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -33.75) (N3_9) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, 0.0) (N4_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -3.75) (N4_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -7.5) (N4_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -11.25) (N4_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -15.0) (N4_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -18.75) (N4_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -22.5) (N4_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -26.25) (N4_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -30.0) (N4_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -33.75) (N4_9) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, 0.0) (N5_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -3.75) (N5_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -7.5) (N5_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -11.25) (N5_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -15.0) (N5_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -18.75) (N5_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -22.5) (N5_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -26.25) (N5_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -30.0) (N5_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -33.75) (N5_9) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, 0.0) (N6_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -3.75) (N6_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -7.5) (N6_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -11.25) (N6_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -15.0) (N6_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -18.75) (N6_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -22.5) (N6_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -26.25) (N6_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -30.0) (N6_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -33.75) (N6_9) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, 0.0) (N7_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -3.75) (N7_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -7.5) (N7_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -11.25) (N7_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -15.0) (N7_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -18.75) (N7_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -22.5) (N7_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -26.25) (N7_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -30.0) (N7_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -33.75) (N7_9) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, 0.0) (N8_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -3.75) (N8_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -7.5) (N8_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -11.25) (N8_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -15.0) (N8_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -18.75) (N8_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -22.5) (N8_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -26.25) (N8_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -30.0) (N8_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -33.75) (N8_9) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, 0.0) (N9_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -3.75) (N9_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -7.5) (N9_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -11.25) (N9_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -15.0) (N9_4) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -18.75) (N9_5) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -22.5) (N9_6) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -26.25) (N9_7) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -30.0) (N9_8) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -33.75) (N9_9) {};
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_0) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N1_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_0);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (N0_0) to [] node [align=center, midway, color=black] {T\\ T\\ 1.0} (N1_1);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N0_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N0_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_1) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_1) to [] node [align=center, midway, color=black] {T\\ A\\ -1.0} (N1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_2) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (N1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_2) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N0_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_3) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_3) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (N1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_4) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (N1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N0_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_4) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_5) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N0_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_5) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_6) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_6) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N0_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_7) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N0_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N0_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N0_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_7) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_7) to [] node [align=center, midway, color=black] {T\\ A\\ -1.0} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_8) to [] node [align=center, midway, color=black] {T\\ T\\ 1.0} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_8) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N0_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_8) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N0_9) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N0_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_0) to [] node [align=center, midway, color=black] {A\\ T\\ -1.0} (N2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_0) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N2_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_1) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_4);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (N1_1) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N2_2);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_2) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_2) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_3) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N1_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_3) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_4) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N1_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_4) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N1_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_5) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_5) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_6) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_6) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N1_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_7) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_7) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N1_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N1_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_7) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_8) to [] node [align=center, midway, color=black] {A\\ T\\ -1.0} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_8) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_8) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N1_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N1_9) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N1_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_0) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N3_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_0) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (N3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_1) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_1) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, green] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_2) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_2) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_3) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_3) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N2_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N2_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_4) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_4) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_5) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N2_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_5) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N2_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_6) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_6) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, green] (N2_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N2_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_7) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_7) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N2_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_7) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_8) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_8) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_8) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N2_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N2_9) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N2_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_0) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (N4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_0) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N4_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_1) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_1) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_2) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_2) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N3_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_3) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_3) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N3_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_4) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_4) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_5) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_5) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N3_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_6) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_6) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N3_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_7) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N3_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_7) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N3_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_7) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_8) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N3_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_8) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_8) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N3_9) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N3_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N4_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_0) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N5_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_0) to [] node [align=center, midway, color=black] {C\\ T\\ -1.0} (N5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_1) to [] node [align=center, midway, color=black] {C\\ A\\ -1.0} (N5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N4_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_1) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_2) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (N5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_2) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N4_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N4_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_3) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (N5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_3) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N4_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_4) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_4) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_5) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N4_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_5) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (N4_6) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (N5_7);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N4_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_6) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_7) to [] node [align=center, midway, color=black] {C\\ A\\ -1.0} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_7) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_7) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N4_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N4_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_8) to [] node [align=center, midway, color=black] {C\\ T\\ -1.0} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_8) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N4_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_8) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N4_9) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N4_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_0) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N6_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N5_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_0) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (N6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_1) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N5_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_1) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_2) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_2) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N5_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_3) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_3) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N5_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_4) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N5_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_4) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N5_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_5) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_5) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_6) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N5_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_6) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_7) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N5_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_7) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N5_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, green] (N5_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_7) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_8) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_8) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N5_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_8) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N5_9) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N5_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_0) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N7_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_0) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (N7_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N6_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_1) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N7_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N6_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_1) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N7_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_2) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N7_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N6_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_2) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N6_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_3) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_3) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_4) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N6_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_4) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N6_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_5) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_5) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_6) to [] node [align=center, midway, color=black] {G\\ C\\ -1.0} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_6) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N6_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_7) to [] node [align=center, midway, color=black] {G\\ A\\ -1.0} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_7) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N6_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_7) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N6_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_8) to [] node [align=center, midway, color=black] {G\\ T\\ -1.0} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_8) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N6_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_8) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N6_9) to [] node [align=center, midway, color=black] {G\\ —\\ -1.0} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N6_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_0) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N8_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N7_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N7_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_0) to [] node [align=center, midway, color=black] {A\\ T\\ -1.0} (N8_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N7_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_1) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N7_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_1) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N8_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N7_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N7_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_2) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_2) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_3) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N7_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_3) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N7_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_4) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N7_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_4) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N7_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N7_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N7_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_5) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_5) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N7_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N7_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_6) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_6) to [] node [align=center, midway, color=black] {A\\ C\\ -1.0} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_7) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N7_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N7_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N7_9);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (N7_7) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (N8_8);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_7) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N7_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_8) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N7_8) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_8) to [] node [align=center, midway, color=black] {A\\ T\\ -1.0} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_8) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N7_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, magenta] (N7_9) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N7_9) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_0) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N9_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N8_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_0) to [] node [align=center, midway, color=black] {T\\ T\\ 1.0} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N8_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_1) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_1) to [] node [align=center, midway, color=black] {T\\ A\\ -1.0} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_2) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_2) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N8_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_3) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N8_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_3) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_4) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N8_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_4) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N8_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_5) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_5) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_6) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_6) to [] node [align=center, midway, color=black] {T\\ C\\ -1.0} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N8_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_7) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N8_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N8_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_7) to [] node [align=center, midway, color=black] {T\\ A\\ -1.0} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_7) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_8) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N8_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_8) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N9_8);
        \end{pgfonlayer}
        \draw[->, >=stealth, line width = 2px, green] (N8_8) to [] node [align=center, midway, color=black] {T\\ T\\ 1.0} (N9_9);
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N8_9) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N9_0) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N9_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N9_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N9_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N9_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N9_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N9_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N9_4);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N9_4) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N9_5);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_4) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_5) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N9_5) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N9_6);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_6) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N9_6) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (N9_7);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, red] (N9_7) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (N9_9);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N9_7) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (N9_8);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (N9_8) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (N9_9);
        \end{pgfonlayer}

    \end{tikzpicture}
\end{document}

````

````
TA----GGCGGAT
TACCCC--C--AT
````

Weight: 1.4999999999999998
</div>

`{bm-enable-all}`

