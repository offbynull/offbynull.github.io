package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import static com.google.common.base.Throwables.getStackTraceAsString;
import static com.google.common.collect.ImmutableList.toImmutableList;
import com.google.common.collect.Streams;
import static com.google.common.collect.Streams.mapWithIndex;
import static com.offbynull.cetools.InternalUtils.isCharged;
import static com.offbynull.cetools.InternalUtils.isPhasePresent;
import com.offbynull.cetools.parser.Parser;
import java.io.IOException;
import java.io.PrintWriter;
import static java.util.Arrays.stream;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import org.ejml.simple.SimpleMatrix;

public final class MainEquationBalance {
    public static void main(String[] args) throws Throwable {
        try (Scanner s = new Scanner(System.in);
                PrintWriter pw = new PrintWriter(System.out, true);
                MarkdownWriter mdw = new MarkdownWriter(pw)) {
            mdw.out("`{bm-disable-all}`\n\n");
            mdw.out("<div style=\"border:1px solid black;\">\n\n");
            try {
                String input = s.nextLine();

                mdw.out("Balancing ").out(input).out("\n\n");

                ChemicalEquation ce = new Parser().parseChemicalEquation(input);
                balanceEquation(mdw, ce);
            } catch (Exception e) {
                mdw.out(getStackTraceAsString(e));
            }
            mdw.out("\n\n</div>\n\n");
            mdw.out("`{bm-enable-all}`\n\n");
        }
    }
    
    
    
    
    public static ChemicalEquation balanceEquation(MarkdownWriter mdw, ChemicalEquation ce) throws IOException {
        Preconditions.checkNotNull(mdw);
        Preconditions.checkNotNull(ce);        
        
        if (isCharged(ce)) {
            mdw.out("Equation is charged! Ions not supported!!\n\n");
            return null;
        }
        
        if (isPhasePresent(ce)) {
            mdw.out("Equation has phases present! Remove before using!!\n\n");
            return null;
        }
        
        
        // unbalance
        mdw.out("Removing stoichiometric coefficients: ");
        ChemicalEquation unbalancedCe = new ChemicalEquation(
                new ChemicalEquationSet(
                        ce.reactants.items.stream()
                               .map(i -> new ChemicalEquationUnit(1, i.bond))
                               .collect(toImmutableList())
                ),
                new ChemicalEquationSet(
                        ce.products.items.stream()
                               .map(i -> new ChemicalEquationUnit(1, i.bond))
                               .collect(toImmutableList())
                ),
                ce.direction
        );
        mdw.out(unbalancedCe);
        mdw.out("\n\n");
        
        
        
        // get all elements used
        mdw.out("Determining unique elements: [");
        Set<Element> elements = new HashSet<>();
        unbalancedCe.reactants.items.stream()
                .flatMap(i -> i.bond.items.stream())
                .forEach(bu -> elements.add(bu.element));
        unbalancedCe.products.items.stream()
                .flatMap(i -> i.bond.items.stream())
                .forEach(bu -> elements.add(bu.element));
        mdw.out(elements.stream().map(e -> e.symbol).collect(joining(", ")));
        mdw.out("]\n");

        int eqCount = elements.size();
        mdw.out("\n\n");
        
        
        
        // list equations to solve
        mdw.out("Determining equation for each element: \n\n");
        var bondMapping = Streams.zip(
                Stream.concat(unbalancedCe.reactants.items.stream(), unbalancedCe.products.items.stream()),
                IntStream.range('a', 'z').mapToObj(i -> i),
                (a,b) -> new VariableToBond("" + ((char) b.intValue()), a.bond))
                .sorted((a,b) -> a.var.compareTo(b.var))
                .collect(toList());
        for (var e : elements) {
            mdw.out(" * " + e.symbol + ": ");
            mdw.out("`{kt} ");
            int remainingReactants = unbalancedCe.reactants.items.size();
            for (var ceu : unbalancedCe.reactants.items) {
                var bondElemCount = ceu.bond.items.stream().mapToInt(bu -> bu.element.equals(e) ? bu.count : 0).sum();
                var bondVarName = bondMapping.stream().filter(bm -> bm.bond.equals(ceu.bond)).findFirst().get().var;
                mdw.out(bondVarName + "(" + bondElemCount + ")");
                remainingReactants--;
                if (remainingReactants > 0) {
                    mdw.out(" + ");
                }
            }
            mdw.out(" = ");
            int remainingProducts = unbalancedCe.products.items.size();
            for (var ceu : unbalancedCe.products.items) {
                var bondElemCount = ceu.bond.items.stream().mapToInt(bu -> bu.element.equals(e) ? bu.count : 0).sum();
                var bondVarName = bondMapping.stream().filter(bm -> bm.bond.equals(ceu.bond)).findFirst().get().var;
                mdw.out(bondVarName + "(" + bondElemCount + ")");
                remainingProducts--;
                if (remainingProducts > 0) {
                    mdw.out(" + ");
                }
            }
            mdw.out("`\n");
        }
        mdw.out("\n\n... where ...\n\n");
        for (var bondMap : bondMapping) {
            mdw.out(" * " + bondMap.var);
            mdw.out(" maps to ");
            mdw.out(bondMap.bond);
            mdw.out("\n");
        }
        mdw.out("\n\n");
        
        int varCount = bondMapping.size();
        
        
        
        // solve system of linear equations
          // solving using matrix instead of substitution: https://chemistry.stackexchange.com/a/66805
        mdw.out("Solving system of linear equations: \n\n");
        if (eqCount != varCount - 1) {
            mdw.out("Not enough equations to solve for variables.\n\n");
            return null;
        }
        double[][] matrixA = new double[varCount][varCount];
        int rowIdx = 0;
        for (var e : elements) {
            int colIdx = 0;
            for (var ceu : unbalancedCe.reactants.items) {
                var bondElemCount = ceu.bond.items.stream().mapToInt(bu -> bu.element.equals(e) ? bu.count : 0).sum();
                matrixA[rowIdx][colIdx] = -bondElemCount;
                colIdx++;
            }
            for (var ceu : unbalancedCe.products.items) {
                var bondElemCount = ceu.bond.items.stream().mapToInt(bu -> bu.element.equals(e) ? bu.count : 0).sum();
                matrixA[rowIdx][colIdx] = bondElemCount;
                colIdx++;
            }
            rowIdx++;
        }
        matrixA[varCount - 1][0] = 1.0;
        SimpleMatrix simpleMatrixA = new SimpleMatrix(matrixA);
        double[][] matrixB = new double[varCount][1];
        matrixB[varCount - 1][0] = 1.0;
        SimpleMatrix simpleMatrixB = new SimpleMatrix(matrixB);
        SimpleMatrix simpleMatrixRes = simpleMatrixA.solve(simpleMatrixB);
        double[] stoichiometricRatios = new double[varCount];
        for (var i = 0; i < varCount; i++) {
            double stoichiometricCoefficient = simpleMatrixRes.get(i, 0);
            stoichiometricRatios[i] = stoichiometricCoefficient;
            mdw.out(" * " + bondMapping.get(i).var + " (mapped to ");
            mdw.out(bondMapping.get(i).bond);
            mdw.out(") = ").out(stoichiometricCoefficient, 5).out("\n");
        }
        mdw.out("\n\n");
        
        
        
        // get it to whole numbers the cheap-and-easy but inefficient way
        mdw.out("Getting it to whole numbers: \n\n");
        double[] newRatios = stoichiometricRatios;
        for (int i = 1; i < 1000; i++) {
            boolean isWholeNums = stream(newRatios).allMatch(d -> isWholeNumber(d, 0.0001));
            if (isWholeNums) {
                break;
            }
            int finalI = i;
            newRatios = stream(stoichiometricRatios).map(d -> d * finalI).toArray();
            int newRatiosLen = newRatios.length;
            mdw.out(" * Scaling by " + i + ": [");
            mapWithIndex(stream(newRatios), (d, _i) -> new IndexedItem<>(d, _i)).forEach(ii -> mdw.out(ii.item, 5).out(ii.idx < newRatiosLen - 1 ? " : " : ""));
            mdw.out("]\n");
        }
        stoichiometricRatios = newRatios;
        if (newRatios == stoichiometricRatios) {
            mdw.out("Already in whole numbers.\n");
        }
        mdw.out("\n\n");
        boolean isWholeNums = stream(newRatios).allMatch(d -> isWholeNumber(d, 0.0001));
        if (!isWholeNums) {
            mdw.out("Unable to get to whole nums");
            return null;
        }

        
        // print it back out
        ChemicalEquation balancedCe = new ChemicalEquation(
                new ChemicalEquationSet(
                        Streams.zip(
                                ce.reactants.items.stream(),
                                stream(stoichiometricRatios).limit(ce.reactants.items.size()).boxed(), // limited to reactants
                                (a,b) -> new ChemicalEquationUnit(b.intValue(), a.bond))
                               .collect(toImmutableList())
                ),
                new ChemicalEquationSet(
                        Streams.zip(
                                ce.products.items.stream(),
                                stream(stoichiometricRatios).skip(ce.reactants.items.size()).boxed(), // skips past reactants
                                (a,b) -> new ChemicalEquationUnit(b.intValue(), a.bond))
                               .collect(toImmutableList())
                ),
                ce.direction
        );
        mdw.out("Balanced chemical equation: ");
        mdw.out(balancedCe);
        mdw.out("\n\n");
        
        return balancedCe;
    }
    
    // https://stackoverflow.com/a/23975512
    private static boolean isWholeNumber(double n, double tolerance) {
        double absN = Math.abs(n);
        return Math.abs(absN - Math.round(absN)) <= tolerance;
    }

    private static final class VariableToBond {
        private final String var;
        private final Bond bond;

        public VariableToBond(String var, Bond bond) {
            this.var = var;
            this.bond = bond;
        }
    }
    
    private static final class IndexedItem<T> {
        private final T item;
        private final long idx;

        public IndexedItem(T item, long idx) {
            this.item = item;
            this.idx = idx;
        }
    }
}
