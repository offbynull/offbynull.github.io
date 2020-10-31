package com.offbynull.cetools;

import static com.google.common.base.Throwables.getStackTraceAsString;
import java.io.IOException;
import java.io.PrintWriter;
import static java.lang.Integer.parseInt;
import static java.util.Locale.ENGLISH;
import java.util.Objects;
import java.util.Scanner;
import static java.util.stream.Collectors.toList;
import java.util.stream.Stream;
import static org.apache.commons.lang3.StringUtils.capitalize;
import static org.apache.commons.lang3.math.NumberUtils.toInt;

public final class MainElementInformation {
    public static void main(String[] args) throws IOException {
        try (Scanner s = new Scanner(System.in);
                PrintWriter pw = new PrintWriter(System.out, true);
                MarkdownWriter mdw = new MarkdownWriter(pw)) {
            mdw.out("`{bm-disable-all}`\n\n");
            mdw.out("<div style=\"border:1px solid black;\">\n\n");
            try {
                String input = s.nextLine();

                String[] splitInput = input.replaceAll("\\s+", "").split("-", 2);
                String elementInput = splitInput[0].toLowerCase(ENGLISH);
                int isotopeMassNum = splitInput.length >= 2 && !splitInput[1].isEmpty() ? parseInt(splitInput[1]) : -1;

                Element element = Stream.of(
                        ElementLookup.bySymbol(capitalize(elementInput)),
                        ElementLookup.byName(elementInput),
                        toInt(elementInput, -1) == -1 ? null : ElementLookup.byAtomicNumber(toInt(input))
                ).filter(Objects::nonNull).findAny().orElse(null);
                if (element == null) {
                    throw new IllegalArgumentException("Element not found. Search by name/symbol/atomic number -- for specific istope,"
                            + "follow by dash and mass number of isotope");
                }
                
                mdw.out("Pulling information for ").out(element.name);
                if (isotopeMassNum != -1) {
                    mdw.out(" (isotope " + isotopeMassNum + ")");
                } else {
                    mdw.out(" (no isotope specified)");
                }
                mdw.out("\n\n");
                
                mdw.out(" * name= ").out(element.name).out("\n");
                mdw.out(" * symbol = ").out(element.symbol).out("\n");
                mdw.out(" * atomic weight = [");
                mdw.out(element.atomicWeight.lowerEndpoint(), 5).out(" amu, ");
                mdw.out(element.atomicWeight.upperEndpoint(), 5).out(" amu");
                mdw.out("]\n");
                mdw.out(" * atomic number / proton count = ").out(element.atomicNumber()).out("\n");
                mdw.out(" * electronegativity = ").out(element.electronegativity).out("\n");
                if (isotopeMassNum != -1) {
                    ElementIsotope isotope = element.isotopes.stream().filter(i -> i.massNumber() == isotopeMassNum).findAny().orElse(null);
                    if (isotope == null) {
                        throw new IllegalArgumentException("Element ISOTOPE not found. Search by name/symbol/atomic number -- for specific"
                                + " istope, follow by dash and mass number of isotope");
                    }
                    mdw.out(" * neutrons = ").out(isotope.neutronCount);
                    mdw.out(" * mass number / (proton + neutron count) = ").out(isotope.massNumber()).out("\n");
                    mdw.out(" * relative abundance = ").out(isotope.relativeAbundance).out("\n");
                } else {
                    mdw.out(" * isotope mass numbers = ")
                            .out(element.isotopes.stream().map(i -> "" + i.massNumber()).collect(toList())).out("\n");
                }
            } catch (Exception e) {
                mdw.out(getStackTraceAsString(e));
            }
            mdw.out("\n\n</div>\n\n");
            mdw.out("`{bm-enable-all}`\n\n");
        }
    }
}
