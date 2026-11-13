package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import java.io.Closeable;
import java.io.IOException;
import java.io.Writer;
import static java.lang.String.format;
import java.text.DecimalFormat;
import static java.util.stream.Collectors.joining;
import java.util.stream.IntStream;

public final class MarkdownWriter implements Closeable {
    private final Writer writer;
    
    public MarkdownWriter(Writer writer) {
        Preconditions.checkNotNull(writer);
        this.writer = writer;
    }
    
    public MarkdownWriter out(String str) {
        try {
            writer.write(str);
        } catch (IOException ioe) {
            throw new IllegalStateException(ioe);
        }
        return this;
    }

    public MarkdownWriter out(long l) {
        out("" + l);
        return this;
    }
    
    public MarkdownWriter out(double d) {
        out("" + d);
        return this;
    }
    
    public MarkdownWriter out(double d, int maxDecimalPlaces) {
        out(d, maxDecimalPlaces, false);
        return this;
    }
    
    public MarkdownWriter out(double d, int decimalPlaces, boolean trailingZeros) {
        if (trailingZeros) {
            out("" + format("%." + decimalPlaces + "f", d));
        } else {
            DecimalFormat df = new DecimalFormat("#." + IntStream.range(0, decimalPlaces).mapToObj(_d -> "#").collect(joining()));
            out("" + df.format(d));
        }
        return this;
    }
    
    public MarkdownWriter out(Object obj) {
        out("" + obj);
        return this;
    }

    public MarkdownWriter out(ChemicalEquation ce) {
        out("`{kt} ");
        rawChemicalEquationSet(ce.reactants);
        switch (ce.direction) {
            case UNIDIRECTIONAL:
                out(" \\rightarrow ");
                break;
            case BIDIRECTIONAL:
                out(" \\rightleftharpoons ");
                break;
            default:
                throw new IllegalStateException();
        }
        rawChemicalEquationSet(ce.products);
        out("`");
        return this;
    }
    
    public MarkdownWriter out(Bond b) {
        out("`{kt} ");
        rawBond(b);
        out("`");
        return this;
    }
    
    private void rawChemicalEquationSet(ChemicalEquationSet ces) {
        int remaining = ces.items.size();
        for (ChemicalEquationUnit ceu : ces.items) {
            out(ceu.count == 1 ? "" : "" + ceu.count);
            rawBond(ceu.bond);
            remaining--;
            if (remaining > 0) {
                out(" + ");
            }
        }
    }
    
    private void rawBond(Bond b) {
        for (BondUnit bu : b.items) {
            rawBondUnit(bu);
        }
    }
    
    private void rawBondUnit(BondUnit bu) {
        out(bu.element.symbol);
        if (bu.count > 1) {
            out("_" + bu.count);
        }
    }

    @Override
    public void close() throws IOException {
        writer.close();
    }
}
