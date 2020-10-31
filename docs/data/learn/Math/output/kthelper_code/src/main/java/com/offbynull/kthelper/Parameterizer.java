package com.offbynull.kthelper;

import com.google.common.base.Preconditions;
import java.util.ArrayList;
import java.util.List;
import java.util.PrimitiveIterator;

public final class Parameterizer {
    
    private Parameterizer() {
        // do nothing
    }

    public static List<String> parameterize(String input) {
        PrimitiveIterator.OfInt intIt = input.chars().iterator();
        
        List<String> ret = new ArrayList<>();
        String current = null;
        int nest = 0;
        while (intIt.hasNext()) {
            int chr = intIt.nextInt();
            if (nest == 0) {
                switch (chr) {
                    case '{':
                        nest = 1;
                        current = "{";
                        break;
                    case ' ':
                    case '\r':
                    case '\n':
                    case '\t':
                        break;
                    default:
                        throw new IllegalArgumentException("Unrecognized charater: " + (char) chr);
                }
            } else {
                switch (chr) {
                    case '{':
                        nest++;
                        current += "{";
                        break;
                    case '}':
                        nest--;
                        current += "}";
                        if (nest == 0) {
                            ret.add(current);
                            current = null;
                        }
                        break;
                    case '\\':
                        current += "\\" + (intIt.hasNext() ? "" + (char) intIt.nextInt() : "");
                        break;
                    default:
                        current += (char) chr;
                }                
            }
        }
        
        Preconditions.checkArgument(current == null, "Unterminated parameter: " + current);
        
        return ret;
    }
}
