package com.offbynull.cetools;

import static com.google.common.base.Throwables.getStackTraceAsString;
import com.offbynull.cetools.parser.Parser;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;

public final class MainBondInformation {
    public static void main(String[] args) throws IOException {
        try (Scanner s = new Scanner(System.in);
                PrintWriter pw = new PrintWriter(System.out, true);
                MarkdownWriter mdw = new MarkdownWriter(pw)) {
            mdw.out("`{bm-disable-all}`\n\n");
            mdw.out("<div style=\"border:1px solid black;\">\n\n");
            try {
                String input = s.nextLine();

                mdw.out("Pulling information for ").out(input).out("\n\n");

                Bond bond = new Parser().parseBond(input);
                bond.items.forEach(bu -> mdw.out(" * ").out(bu.count).out(bu.element.name).out("\n"));
                mdw.out(" * atomic weight = [");
                mdw.out(bond.atomicWeight().lowerEndpoint(), 5).out(" amu, ");
                mdw.out(bond.atomicWeight().upperEndpoint(), 5).out(" amu");
                mdw.out("]\n");
                mdw.out(" * charge = ").out(bond.charge).out("\n");
                mdw.out(" * phase = ").out(bond.phase + "").out("\n"); // bond.phase + "" because bond.phase can be null
            } catch (Exception e) {
                mdw.out(getStackTraceAsString(e));
            }
            mdw.out("\n\n</div>\n\n");
            mdw.out("`{bm-enable-all}`\n\n");
        }
    }
}
