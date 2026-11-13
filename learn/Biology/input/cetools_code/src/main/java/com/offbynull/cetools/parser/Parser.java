package com.offbynull.cetools.parser;

import com.offbynull.cetools.Bond;
import com.offbynull.cetools.ChemicalEquation;
import com.offbynull.cetools.parser.generated.ChemLexer;
import com.offbynull.cetools.parser.generated.ChemParser;
import static com.offbynull.cetools.parser.generated.ChemParser.VOCABULARY;
import static java.util.stream.Collectors.joining;
import org.antlr.v4.runtime.BailErrorStrategy;
import org.antlr.v4.runtime.BaseErrorListener;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.RecognitionException;
import org.antlr.v4.runtime.Recognizer;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.misc.ParseCancellationException;
import org.apache.commons.lang3.Validate;

public final class Parser {

    public ChemicalEquation parseChemicalEquation(String input) {
        Validate.notNull(input);

        ChemParser parser = initParser(input);
        DomChemVisitor visitor = new DomChemVisitor();
        
        try {
            return (ChemicalEquation) visitor.visit(parser.chemEq());
        } catch (ParseCancellationException pce) { // throws by BailErrorStrategy
            RecognitionException re = (RecognitionException) pce.getCause();
            throw new IllegalArgumentException(
                    String.format("Parser syntax error: token [%s] but expected one of [%s] (line %d pos %d)",
                            re.getOffendingToken() == null ? "" : VOCABULARY.getDisplayName(re.getOffendingToken().getType()),
                            re.getExpectedTokens().toList().stream().map(i -> VOCABULARY.getDisplayName(i)).collect(joining(",")),
                            re.getOffendingToken().getLine(),
                            re.getOffendingToken().getCharPositionInLine()),
                    re);
        }
    }

    public Bond parseBond(String input) {
        Validate.notNull(input);

        ChemParser parser = initParser(input);
        DomChemVisitor visitor = new DomChemVisitor();
        
        try {
            return (Bond) visitor.visit(parser.bond());
        } catch (ParseCancellationException pce) { // throws by BailErrorStrategy
            RecognitionException re = (RecognitionException) pce.getCause();
            throw new IllegalArgumentException(
                    String.format("Parser syntax error: token [%s] but expected one of [%s] (line %d pos %d)",
                            re.getOffendingToken() == null ? "" : VOCABULARY.getDisplayName(re.getOffendingToken().getType()),
                            re.getExpectedTokens().toList().stream().map(i -> VOCABULARY.getDisplayName(i)).collect(joining(",")),
                            re.getOffendingToken().getLine(),
                            re.getOffendingToken().getCharPositionInLine()),
                    re);
        }
    }

    private ChemParser initParser(String input) {
        input = input.trim();

        CharStream charStream = CharStreams.fromString(input);
        
        ChemLexer lexer = new ChemLexer(charStream);
        TokenStream tokenStream = new CommonTokenStream(lexer);
        ChemParser parser = new ChemParser(tokenStream);
        
        parser.setErrorHandler(new BailErrorStrategy());
        parser.addErrorListener(new BaseErrorListener() {
            @Override
            public void syntaxError(
                    Recognizer<?, ?> recognizer,
                    Object offendingSymbol,
                    int line,
                    int charPositionInLine,
                    String msg,
                    RecognitionException re) {
                throw new IllegalArgumentException(
                        String.format("Parser syntax error: token [%s] but expected one of [%s] (line %d pos %d)",
                                re.getOffendingToken() == null ? "" : VOCABULARY.getDisplayName(re.getOffendingToken().getType()),
                                re.getExpectedTokens().toList().stream().map(i -> VOCABULARY.getDisplayName(i)).collect(joining(",")),
                                re.getOffendingToken().getLine(),
                                re.getOffendingToken().getCharPositionInLine()),
                        re);
            }
        });
        
        return parser;
    }
}