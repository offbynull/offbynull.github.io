package com.offbynull.kthelper;

import com.google.common.base.Preconditions;
import static com.google.common.base.Throwables.getStackTraceAsString;
import static com.offbynull.kthelper.Parameterizer.parameterize;
import java.io.IOException;
import java.io.StringWriter;
import java.io.Writer;
import java.util.List;
import static java.util.regex.Pattern.matches;
import static java.util.stream.Collectors.joining;

public final class VerticalAddition {
    public static String run(String input) throws IOException {
        try (Writer mdOut = new StringWriter()) {
            try {
                String[] lines = input.split("[\r\n]+");
                
                Integer colLen = null;
                String innerOutput = "";
                for (int i = 0; i < lines.length; i++) {
                    String line = lines[i];
                    
                    List<String> cols = parameterize(line);
                    if (i < lines.length - 1 && matches("-+", lines[i+1])) {
                        Preconditions.checkArgument(i == lines.length - 3, line + " must be the 3rd last line");
                        innerOutput += toCols(cols) + " \\enspace + \\\\ \\hline";
                        i++; // skip the next line
                    } else if (i > 0 && matches("-+", lines[i-1])) {
                        Preconditions.checkArgument(i == lines.length - 1, line + " must be the last line");
                        innerOutput += toCols(cols);
                    } else {
                        innerOutput += toCols(cols) + " \\\\";
                    }

                    // ensure all col sizes match
                    if (colLen == null) {
                        colLen = cols.size();
                    } else {
                        Preconditions.checkArgument(colLen == cols.size(), "Column sizes must all equal");
                    }
                }

                String output = "";
                output += "`{kt}";
                output += "\\begin{alignedat}{" + colLen + "}";
                output += innerOutput;
                output += "\\end{alignedat}";
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
    
    private static final String toCols(List<String> col) {
        return col.stream().collect(joining("&  \\enspace", "", "&"));
    }
}
