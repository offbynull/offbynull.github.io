<div style="border:1px solid black;">

`{bm-disable-all}`

````{latex}

        \documentclass{standalone}
        \usepackage{tikz, pagecolor}
        \begin{document}
            \pagecolor{white}
            \begin{tikzpicture}

\begin{scope}[shift={(0.0,0.0)}]
\node[anchor=west] at (0, 1.5) (Oheader) {Original};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, 0.0) (NO0_0) {0.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -3.75) (NO0_1) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -7.5) (NO0_2) {-2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -11.25) (NO0_3) {-3.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -15.0) (NO0_4) {-4.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -18.75) (NO0_5) {-5.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, 0.0) (NO1_0) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -3.75) (NO1_1) {0.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -7.5) (NO1_2) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -11.25) (NO1_3) {-2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -15.0) (NO1_4) {-3.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -18.75) (NO1_5) {-3.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, 0.0) (NO2_0) {-2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -3.75) (NO2_1) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -7.5) (NO2_2) {1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -11.25) (NO2_3) {0.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -15.0) (NO2_4) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -18.75) (NO2_5) {-2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, 0.0) (NO3_0) {-3.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -3.75) (NO3_1) {-2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -7.5) (NO3_2) {0.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -11.25) (NO3_3) {2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -15.0) (NO3_4) {1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -18.75) (NO3_5) {0.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, 0.0) (NO4_0) {-4.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -3.75) (NO4_1) {-3.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -7.5) (NO4_2) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -11.25) (NO4_3) {1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -15.0) (NO4_4) {2.0};
        \node[draw = gray, fill = yellow, thick, circle, minimum size = 2px] at (15.0, -18.75) (NO4_5) {2.0};
        \draw[->, >=stealth, line width = 2px, green] (NO0_0) to [] node [align=center, midway, color=black] {T\\ G\\ 0.0} (NO1_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_0) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NO0_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_0) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO1_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_1) to [] node [align=center, midway, color=black] {T\\ A\\ 0.0} (NO1_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (NO0_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_1) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO1_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_2) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO1_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_2) to [] node [align=center, midway, color=black] {T\\ C\\ 0.0} (NO1_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (NO0_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_3) to [] node [align=center, midway, color=black] {T\\ G\\ 0.0} (NO1_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_3) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO1_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_3) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NO0_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_4) to [] node [align=center, midway, color=black] {T\\ T\\ 1.0} (NO1_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_4) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO1_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_4) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (NO0_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO0_5) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO1_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_0) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NO2_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_0) to [] node [align=center, midway, color=black] {A\\ G\\ 0.0} (NO2_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_0) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NO1_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (NO1_2);
        \draw[->, >=stealth, line width = 2px, green] (NO1_1) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (NO2_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_1) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NO2_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_2) to [] node [align=center, midway, color=black] {A\\ C\\ 0.0} (NO2_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_2) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NO2_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (NO1_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_3) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NO2_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_3) to [] node [align=center, midway, color=black] {A\\ G\\ 0.0} (NO2_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_3) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NO1_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_4) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NO2_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_4) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (NO1_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_4) to [] node [align=center, midway, color=black] {A\\ T\\ 0.0} (NO2_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO1_5) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NO2_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_0) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NO2_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_0) to [] node [align=center, midway, color=black] {C\\ G\\ 0.0} (NO3_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_0) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NO3_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (NO2_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_1) to [] node [align=center, midway, color=black] {C\\ A\\ 0.0} (NO3_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_1) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NO3_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (NO2_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_2) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NO3_2);
        \draw[->, >=stealth, line width = 2px, green] (NO2_2) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (NO3_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_3) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NO2_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_3) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NO3_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_3) to [] node [align=center, midway, color=black] {C\\ G\\ 0.0} (NO3_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_4) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (NO2_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_4) to [] node [align=center, midway, color=black] {C\\ T\\ 0.0} (NO3_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_4) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NO3_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO2_5) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NO3_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_0) to [] node [align=center, midway, color=black] {T\\ G\\ 0.0} (NO4_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_0) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NO3_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_0) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO4_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (NO3_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_1) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO4_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_1) to [] node [align=center, midway, color=black] {T\\ A\\ 0.0} (NO4_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_2) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO4_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_2) to [] node [align=center, midway, color=black] {T\\ C\\ 0.0} (NO4_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (NO3_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_3) to [] node [align=center, midway, color=black] {T\\ G\\ 0.0} (NO4_4);
        \draw[->, >=stealth, line width = 2px, green] (NO3_3) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NO3_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_3) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO4_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_4) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO4_4);
        \draw[->, >=stealth, line width = 2px, green] (NO3_4) to [] node [align=center, midway, color=black] {T\\ T\\ 1.0} (NO4_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_4) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (NO3_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO3_5) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NO4_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO4_0) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NO4_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO4_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (NO4_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO4_2) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (NO4_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO4_3) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NO4_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NO4_4) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (NO4_5);

\end{scope}


\begin{scope}[shift={(19.92,0.0)}]
\node[anchor=west] at (0, 1.5) (REheader) {Reversed Edge};
        \node[draw = gray, fill = yellow, thick, circle, minimum size = 2px] at (0.0, 0.0) (NRE0_0) {2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -3.75) (NRE0_1) {1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -7.5) (NRE0_2) {0.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -11.25) (NRE0_3) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -15.0) (NRE0_4) {-2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -18.75) (NRE0_5) {-4.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, 0.0) (NRE1_0) {1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -3.75) (NRE1_1) {2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -7.5) (NRE1_2) {1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -11.25) (NRE1_3) {0.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -15.0) (NRE1_4) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -18.75) (NRE1_5) {-3.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, 0.0) (NRE2_0) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -3.75) (NRE2_1) {0.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -7.5) (NRE2_2) {1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -11.25) (NRE2_3) {1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -15.0) (NRE2_4) {0.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -18.75) (NRE2_5) {-2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, 0.0) (NRE3_0) {-3.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -3.75) (NRE3_1) {-2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -7.5) (NRE3_2) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -11.25) (NRE3_3) {0.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -15.0) (NRE3_4) {1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -18.75) (NRE3_5) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, 0.0) (NRE4_0) {-5.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -3.75) (NRE4_1) {-4.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -7.5) (NRE4_2) {-3.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -11.25) (NRE4_3) {-2.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -15.0) (NRE4_4) {-1.0};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -18.75) (NRE4_5) {0.0};
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE0_1) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NRE0_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE0_2) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (NRE0_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE0_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (NRE0_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE0_4) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NRE0_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE0_5) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (NRE0_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_0) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE0_0);
        \draw[->, >=stealth, line width = 2px, green] (NRE1_1) to [] node [align=center, midway, color=black] {T\\ G\\ 0.0} (NRE0_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_1) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NRE1_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_1) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE0_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_2) to [] node [align=center, midway, color=black] {T\\ A\\ 0.0} (NRE0_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_2) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE0_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_2) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (NRE1_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_3) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE0_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (NRE1_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_3) to [] node [align=center, midway, color=black] {T\\ C\\ 0.0} (NRE0_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_4) to [] node [align=center, midway, color=black] {T\\ G\\ 0.0} (NRE0_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_4) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE0_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_4) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NRE1_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_5) to [] node [align=center, midway, color=black] {T\\ T\\ 1.0} (NRE0_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_5) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (NRE1_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE1_5) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE0_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_0) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NRE1_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_1) to [] node [align=center, midway, color=black] {A\\ G\\ 0.0} (NRE1_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_1) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NRE2_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_1) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NRE1_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_2) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (NRE2_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_2) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NRE1_2);
        \draw[->, >=stealth, line width = 2px, green] (NRE2_2) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (NRE1_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_3) to [] node [align=center, midway, color=black] {A\\ C\\ 0.0} (NRE1_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (NRE2_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_3) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NRE1_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_4) to [] node [align=center, midway, color=black] {A\\ G\\ 0.0} (NRE1_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_4) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NRE1_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_4) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NRE2_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_5) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (NRE1_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_5) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (NRE2_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE2_5) to [] node [align=center, midway, color=black] {A\\ T\\ 0.0} (NRE1_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_0) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NRE2_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_1) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NRE3_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_1) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NRE2_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_1) to [] node [align=center, midway, color=black] {C\\ G\\ 0.0} (NRE2_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_2) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (NRE3_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_2) to [] node [align=center, midway, color=black] {C\\ A\\ 0.0} (NRE2_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_2) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NRE2_2);
        \draw[->, >=stealth, line width = 2px, green] (NRE3_3) to [] node [align=center, midway, color=black] {C\\ C\\ 1.0} (NRE2_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (NRE3_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_3) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NRE2_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_4) to [] node [align=center, midway, color=black] {C\\ G\\ 0.0} (NRE2_3);
        \draw[->, >=stealth, line width = 2px, green] (NRE3_4) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NRE3_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_4) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NRE2_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_5) to [] node [align=center, midway, color=black] {C\\ T\\ 0.0} (NRE2_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_5) to [] node [align=center, midway, color=black] {C\\ —\\ -1.0} (NRE2_5);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE3_5) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (NRE3_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_0) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE3_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_1) to [] node [align=center, midway, color=black] {T\\ G\\ 0.0} (NRE3_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_1) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE3_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_1) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NRE4_0);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_2) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE3_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_2) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (NRE4_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_2) to [] node [align=center, midway, color=black] {T\\ A\\ 0.0} (NRE3_1);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_3) to [] node [align=center, midway, color=black] {T\\ C\\ 0.0} (NRE3_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_3) to [] node [align=center, midway, color=black] {—\\ C\\ -1.0} (NRE4_2);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_3) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE3_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_4) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE3_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_4) to [] node [align=center, midway, color=black] {T\\ G\\ 0.0} (NRE3_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_4) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (NRE4_3);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_5) to [] node [align=center, midway, color=black] {—\\ T\\ -1.0} (NRE4_4);
        \draw[->, >=stealth, line width = 2px, gray!40] (NRE4_5) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (NRE3_5);
        \draw[->, >=stealth, line width = 2px, green] (NRE4_5) to [] node [align=center, midway, color=black] {T\\ T\\ 1.0} (NRE3_4);

\end{scope}

                    \draw[line width = 4px, blue!50] (NO3_4) to [bend right, looseness=0.6] node [align=center, midway, draw=blue!50, fill=blue!50, text=white] {$1.0 + 1.0 = 2.0$} (NRE3_4);
        \draw[line width = 4px, blue!50] (NO0_0) to [bend right, looseness=0.6] node [align=center, midway, draw=blue!50, fill=blue!50, text=white] {$0.0 + 2.0 = 2.0$} (NRE0_0);
        \draw[line width = 4px, blue!50] (NO1_1) to [bend right, looseness=0.6] node [align=center, midway, draw=blue!50, fill=blue!50, text=white] {$0.0 + 2.0 = 2.0$} (NRE1_1);
        \draw[line width = 4px, blue!50] (NO4_5) to [bend right, looseness=0.6] node [align=center, midway, draw=blue!50, fill=blue!50, text=white] {$2.0 + 0.0 = 2.0$} (NRE4_5);
        \draw[line width = 4px, blue!50] (NO3_3) to [bend right, looseness=0.6] node [align=center, midway, draw=blue!50, fill=blue!50, text=white] {$2.0 + 0.0 = 2.0$} (NRE3_3);
        \draw[line width = 4px, blue!50] (NO2_2) to [bend right, looseness=0.6] node [align=center, midway, draw=blue!50, fill=blue!50, text=white] {$1.0 + 1.0 = 2.0$} (NRE2_2);

            \end{tikzpicture}
        \end{document}

````

</div>

`{bm-enable-all}`

