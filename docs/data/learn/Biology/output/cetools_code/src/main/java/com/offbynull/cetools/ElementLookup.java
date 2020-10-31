package com.offbynull.cetools;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.Range;
import java.io.FileReader;
import java.io.Reader;
import static java.lang.Double.parseDouble;
import static java.lang.Integer.parseInt;
import java.util.List;
import java.util.Objects;
import static java.util.stream.Collectors.toList;
import java.util.stream.IntStream;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.apache.commons.lang3.RegExUtils;
import org.apache.commons.lang3.StringUtils;
import static org.apache.commons.lang3.math.NumberUtils.toDouble;

public final class ElementLookup {
    public static ImmutableList<Element> ELEMENTS;

    static {
        try {
            // Data extracted from https://ciaaw.org/
            // Data extracted from https://en.wikipedia.org/w/index.php?title=Electronegativities_of_the_elements_(data_page)&oldid=931213836
            List<CSVRecord> isotopeMassRecs;
            try (Reader in = new FileReader("isotope_masses.csv")) {
                isotopeMassRecs = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(in).getRecords();
            }
            List<CSVRecord> isotopeAbundanceRecs;
            try (Reader in = new FileReader("isotope_abundances.csv")) {
                isotopeAbundanceRecs = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(in).getRecords();
            }
            List<CSVRecord> weightRecs;
            try (Reader in = new FileReader("weights.csv")) {
                weightRecs = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(in).getRecords();
            }
            List<CSVRecord> electronegativityRecs;
            try (Reader in = new FileReader("electronegativity.csv")) {
                electronegativityRecs = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(in).getRecords();
            }
            
            ImmutableList.Builder<Element> elementsBuilder = ImmutableList.builder();
            for (CSVRecord weightRec : weightRecs) {
                String zVal = weightRec.get("Z").replaceAll("[^\\d]", "");
                String symbol = weightRec.get("Symbol");
                String name = weightRec.get("Element");

                Double electronegativity = electronegativityRecs.stream()
                        .filter(e -> e.get("Symbol").equals(symbol))
                        .limit(1L)
                        .map(e -> e.get("use"))
                        .map(n -> toDouble(n, Double.NaN))
                        .filter(n -> !Double.isNaN(n))
                        .findAny().orElse(null);
                
                int protonCount = parseInt(zVal);
                Range<Double> atomicWeightRange = parseRange(weightRec.get("Standard Atomic Weight"));
                
                ImmutableList.Builder<ElementIsotope> isotopesBuilder = ImmutableList.builder();
                int isotopesStartIdx = IntStream.range(0, isotopeMassRecs.size())
                        .filter(i -> isotopeMassRecs.get(i).get("Z").equals(zVal))
                        .findFirst().orElse(-1);
                int isotopeAbundancesStartIdx = IntStream.range(0, isotopeAbundanceRecs.size())
                        .filter(i -> isotopeAbundanceRecs.get(i).get("Z").equals(zVal))
                        .findFirst().orElse(-1);
                if (isotopesStartIdx != -1 && isotopeAbundancesStartIdx != -1) {
                    List<CSVRecord> foundIsotopeMasses = isotopeMassRecs.subList(isotopesStartIdx, isotopeMassRecs.size()).stream()
                            .takeWhile(r -> r.get("Z").replaceAll("[^\\d]", "").equals(zVal) || r.get("Z").isBlank())
                            .collect(toList());
                    List<CSVRecord> foundIsotopeAbundances = isotopeAbundanceRecs.subList(isotopeAbundancesStartIdx, isotopeAbundanceRecs.size()).stream()
                            .takeWhile(r -> r.get("Z").replaceAll("[^\\d]", "").equals(zVal) || r.get("Z").isBlank())
                            .collect(toList());
                    for (CSVRecord isotopeMassRec : foundIsotopeMasses) {
                        String aVal = isotopeMassRec.get("A").replaceAll("[^\\d]", "");
                        String massVal = isotopeMassRec.get("Atomic mass, m a /Da").replaceAll("[^\\d]", "");
                        CSVRecord isotopeAbundanceRec = foundIsotopeAbundances.stream()
                                .filter(r -> r.get("A").replaceAll("[^\\d]", "").equals(aVal))
                                .findFirst().orElse(null);
                        
                        if (isotopeAbundanceRec == null) {
                            System.err.println("No abundances found for A=" + aVal);
                            continue;
                        }
                        
                        int protonNeutronCount = parseInt(aVal);
                        int neutronCount = protonNeutronCount - protonCount;
                        double atomicMass = parseDouble(massVal);
                        Range<Double> relativeAbundanceRange = parseRange(isotopeAbundanceRec.get("Representative isotopic composition"));
                        
                        ElementIsotope elementIsotope = new ElementIsotope(protonCount, neutronCount, atomicMass, relativeAbundanceRange);
                        isotopesBuilder.add(elementIsotope);
                    }
                }
                ImmutableList<ElementIsotope> isotopes = isotopesBuilder.build();
                
                Element element = new Element(name, symbol, protonCount, isotopes, atomicWeightRange, electronegativity);
                elementsBuilder.add(element);
            }
            ELEMENTS = elementsBuilder.build();
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }
    
    private static Range<Double> parseRange(String input) {
        Range<Double> ret;
        input = RegExUtils.removeAll(input, "[^\\d\\[\\]\\.,]"); // remove spaces and brackets
        if (input.isBlank()) {
            return null;
        }
        if (input.matches("\\[[\\d+\\.]+,[\\d+\\.]+\\]")) {
            String[] relativeAbundanceRangeSplit = input.split(",");
            relativeAbundanceRangeSplit[0] = StringUtils.removeStart(relativeAbundanceRangeSplit[0], "[");
            relativeAbundanceRangeSplit[1] = StringUtils.removeEnd(relativeAbundanceRangeSplit[1], "]");
            double relativeAbundanceStart = parseDouble(relativeAbundanceRangeSplit[0]);
            double relativeAbundanceEnd = parseDouble(relativeAbundanceRangeSplit[1]);
            ret = Range.closed(relativeAbundanceStart, relativeAbundanceEnd);
        } else {
            double relativeAbundance = parseDouble(input);
            ret = Range.closed(relativeAbundance, relativeAbundance);
        }
        return ret;
    }

    private ElementLookup() {
        // do nothing
    }
    
    public static Element byName(String name) {
        return ELEMENTS.stream().filter(e -> e.name.equals(name)).findAny().orElse(null);
    }
    
    public static Element bySymbol(String symbol) {
        return ELEMENTS.stream().filter(e -> e.symbol.equals(symbol)).findAny().orElse(null);
    }
    
    public static Element byAtomicNumber(int protonCount) {
        return ELEMENTS.stream().filter(e -> e.protonCount == protonCount).findAny().orElse(null);
    }
}
