<div style="border:1px solid black;">

`{bm-disable-all}`

````{latex}

\documentclass{standalone}
\usepackage{pgf, tikz, pagecolor}
\usetikzlibrary{arrows, automata}
\pgfdeclarelayer{bg}    % declare background layer
\pgfsetlayers{bg,main}  % set the order of the layers (main is the standard layer)
\begin{document}
    \pagecolor{white}
    \begin{tikzpicture}
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, 0.0) (Nhigh_0_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -3.75) (Nhigh_0_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -7.5) (Nhigh_0_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (30.0, -11.25) (Nhigh_0_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, 0.0) (Nhigh_1_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -3.75) (Nhigh_1_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -7.5) (Nhigh_1_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (33.75, -11.25) (Nhigh_1_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, 0.0) (Nhigh_2_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, -3.75) (Nhigh_2_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, -7.5) (Nhigh_2_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (37.5, -11.25) (Nhigh_2_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, 0.0) (Nhigh_3_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, -3.75) (Nhigh_3_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, -7.5) (Nhigh_3_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (41.25, -11.25) (Nhigh_3_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -15.0) (Nmid_0_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -18.75) (Nmid_0_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -22.5) (Nmid_0_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (15.0, -26.25) (Nmid_0_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -15.0) (Nmid_1_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -18.75) (Nmid_1_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -22.5) (Nmid_1_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (18.75, -26.25) (Nmid_1_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -15.0) (Nmid_2_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -18.75) (Nmid_2_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -22.5) (Nmid_2_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (22.5, -26.25) (Nmid_2_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -15.0) (Nmid_3_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -18.75) (Nmid_3_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -22.5) (Nmid_3_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (26.25, -26.25) (Nmid_3_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -30.0) (Nlow_0_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -33.75) (Nlow_0_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -37.5) (Nlow_0_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0.0, -41.25) (Nlow_0_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -30.0) (Nlow_1_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -33.75) (Nlow_1_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -37.5) (Nlow_1_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (3.75, -41.25) (Nlow_1_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -30.0) (Nlow_2_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -33.75) (Nlow_2_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -37.5) (Nlow_2_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (7.5, -41.25) (Nlow_2_3) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -30.0) (Nlow_3_0) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -33.75) (Nlow_3_1) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -37.5) (Nlow_3_2) {};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (11.25, -41.25) (Nlow_3_3) {};
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
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_0) to [] node [align=center, midway, color=black] {A\\ —\\ -0.1} (Nhigh_2_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_1) to [] node [align=center, midway, color=black] {A\\ —\\ -0.1} (Nhigh_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_2) to [] node [align=center, midway, color=black] {A\\ —\\ -0.1} (Nhigh_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_1_3) to [] node [align=center, midway, color=black] {A\\ —\\ -0.1} (Nhigh_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_1_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_2_0) to [] node [align=center, midway, color=black] {A\\ —\\ -0.1} (Nhigh_3_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_2_1) to [] node [align=center, midway, color=black] {A\\ —\\ -0.1} (Nhigh_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_2_2) to [] node [align=center, midway, color=black] {A\\ —\\ -0.1} (Nhigh_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_2_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nhigh_2_3) to [] node [align=center, midway, color=black] {A\\ —\\ -0.1} (Nhigh_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_0) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_1) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_2) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, purple] (Nhigh_3_3) to [bend left, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_0) to [] node [align=center, midway, color=black] {T\\ G\\ 0.0} (Nmid_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_0) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_0) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (Nlow_0_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_1) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_1) to [] node [align=center, midway, color=black] {T\\ A\\ 0.0} (Nmid_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (Nlow_0_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_2) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (Nlow_0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_2) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_2) to [] node [align=center, midway, color=black] {T\\ G\\ 0.0} (Nmid_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_0_3) to [] node [align=center, midway, color=black] {T\\ —\\ -1.0} (Nhigh_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_0) to [] node [align=center, midway, color=black] {A\\ G\\ 0.0} (Nmid_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_0) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (Nhigh_2_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_0) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (Nlow_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_1) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (Nmid_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (Nlow_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_1) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (Nhigh_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_2) to [] node [align=center, midway, color=black] {A\\ G\\ 0.0} (Nmid_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_2) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (Nhigh_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_2) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (Nlow_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_1_3) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (Nhigh_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_0) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (Nlow_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_0) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (Nhigh_3_0);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_0) to [] node [align=center, midway, color=black] {A\\ G\\ 0.0} (Nmid_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_1) to [] node [align=center, midway, color=black] {A\\ A\\ 1.0} (Nmid_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_1) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (Nhigh_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (Nlow_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_2) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (Nlow_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_2) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (Nhigh_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_2) to [] node [align=center, midway, color=black] {A\\ G\\ 0.0} (Nmid_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_2_3) to [] node [align=center, midway, color=black] {A\\ —\\ -1.0} (Nhigh_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_0) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (Nlow_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_1) to [] node [align=center, midway, color=black] {—\\ A\\ -1.0} (Nlow_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nmid_3_2) to [] node [align=center, midway, color=black] {—\\ G\\ -1.0} (Nlow_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_0_0) to [] node [align=center, midway, color=black] {—\\ G\\ -0.1} (Nlow_0_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_0_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_0_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_0_1) to [] node [align=center, midway, color=black] {—\\ A\\ -0.1} (Nlow_0_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_0_2) to [] node [align=center, midway, color=black] {—\\ G\\ -0.1} (Nlow_0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_0_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_0_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_0_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_0_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_1_0) to [] node [align=center, midway, color=black] {—\\ G\\ -0.1} (Nlow_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_1_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_1_1) to [] node [align=center, midway, color=black] {—\\ A\\ -0.1} (Nlow_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_1_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_1_2) to [] node [align=center, midway, color=black] {—\\ G\\ -0.1} (Nlow_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_1_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_1_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_2_0) to [] node [align=center, midway, color=black] {—\\ G\\ -0.1} (Nlow_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_2_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_2_1) to [] node [align=center, midway, color=black] {—\\ A\\ -0.1} (Nlow_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_2_2) to [] node [align=center, midway, color=black] {—\\ G\\ -0.1} (Nlow_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_2_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_2_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_2_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_3_0) to [] node [align=center, midway, color=black] {—\\ G\\ -0.1} (Nlow_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_3_1) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_1);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_3_1) to [] node [align=center, midway, color=black] {—\\ A\\ -0.1} (Nlow_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 2px, gray!40] (Nlow_3_2) to [] node [align=center, midway, color=black] {—\\ G\\ -0.1} (Nlow_3_3);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_3_2) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_2);
        \end{pgfonlayer}
        \begin{pgfonlayer}{bg}
        \draw[->, >=stealth, line width = 1px, orange] (Nlow_3_3) to [bend right, looseness=0.3] node [align=center, midway, color=black] {} (Nmid_3_3);
        \end{pgfonlayer}

    \end{tikzpicture}
\end{document}

````

NOTE: Orange edges are "free rides" from source / Purple edges are "free rides" to sink.

</div>

`{bm-enable-all}`

