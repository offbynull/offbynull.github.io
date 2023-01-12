package com.offbynull.kthelper;

import static com.google.common.base.Throwables.getStackTraceAsString;
import static com.offbynull.kthelper.Parameterizer.parameterize;
import java.io.IOException;
import java.io.StringWriter;
import java.io.Writer;
import java.util.List;

public final class LongDivision {
    public static String run(String input) throws IOException {
        try (Writer mdOut = new StringWriter()) {
            try {
                List<String> parameters = parameterize(input);
                String quotient = parameters.remove(0);
                String divisor = parameters.remove(0);
                String dividend = parameters.remove(0);
                
                String output = "";
                output += "`{kt}";
                output += "\\begin{array}{l}";
                output += "\\phantom{{" + divisor + "\\smash{)}}}{" + quotient + "} \\\\";
                output += "{" + divisor + "}\\overline{\\smash{)}" + dividend + "} \\\\";
                
                while (!parameters.isEmpty()) {
                    String under = parameters.remove(0);
                    output += "\\phantom{{" + divisor + "\\smash{)}}}" + under + " \\\\";
                }
                
                output += "\\end{array}";
                output += "`";

                mdOut.write(output);
            } catch (Exception e) {
                mdOut.append("`{bm-disable-all}`\n\n");
                mdOut.append(getStackTraceAsString(e));
                mdOut.append("`{bm-enable-all}`");
            }
            return mdOut.toString();
        }
    }
}
