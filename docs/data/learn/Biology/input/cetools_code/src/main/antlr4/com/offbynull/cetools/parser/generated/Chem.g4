grammar Chem;

chemEq:
        chemEqSet '->' chemEqSet                 #UnidirChemEq     // e.g. 2H2 + O2 ->  2H2O
        | chemEqSet '<->' chemEqSet              #BidirChemEq      // e.g. 2H2 + O2 <-> 2H2O
        ;

chemEqSet: (chemEqUnit '+')* chemEqUnit;                           // e.g. 2H2O + NaCl
chemEqUnit: COUNT? bond;                                           // e.g. 2H2O

bond: bondUnit+ bondCharge? bondPhase?;                            // e.g. Fe2(HO)3^-3 (s)
bondUnit:
        SYMBOL COUNT?                           # SingleBondUnit   // e.g. Fe2
        | '(' bondUnit+ ')' COUNT?              # GroupedBondUnit  // e.g. (H2O)3
        ;
bondCharge: '^' COUNT (PLUS|MINUS);
bondPhase: '(' PHASE ')';

UNIDIRECTIONAL: '->';
BIDIRECTIONAL: '<->';
OPEN_BRACKET: '(';
CLOSE_BRACKET: ')';
PLUS: '+';
MINUS: '-';
CARET: '^';
COUNT: [0-9]+;
SYMBOL: [A-Z] [a-z]*;
PHASE: [a-z]*;
WS: [ \t\n\r]+ -> skip;