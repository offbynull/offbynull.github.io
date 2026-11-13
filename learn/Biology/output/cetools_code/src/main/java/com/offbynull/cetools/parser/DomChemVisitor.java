package com.offbynull.cetools.parser;

import com.offbynull.cetools.ChemicalEquationUnit;
import com.offbynull.cetools.Bond;
import com.offbynull.cetools.ChemicalEquation;
import com.offbynull.cetools.BondUnit;
import com.offbynull.cetools.ChemicalEquationSet;
import com.google.common.collect.ImmutableList;
import static com.google.common.collect.ImmutableList.toImmutableList;
import com.offbynull.cetools.Element;
import com.offbynull.cetools.ElementLookup;
import com.offbynull.cetools.ChemicalEquation.ChemicalEquationDirection;
import com.offbynull.cetools.Phase;
import com.offbynull.cetools.parser.generated.ChemBaseVisitor;
import com.offbynull.cetools.parser.generated.ChemParser;
import static java.lang.Integer.parseInt;
import java.util.List;
import static java.util.stream.Collectors.toList;


public final class DomChemVisitor extends ChemBaseVisitor<Object> {

    @Override
    public Object visitUnidirChemEq(ChemParser.UnidirChemEqContext ctx) {
        ChemicalEquationSet reactants = (ChemicalEquationSet) visit(ctx.chemEqSet(0));
        ChemicalEquationDirection direction = ChemicalEquationDirection.UNIDIRECTIONAL;
        ChemicalEquationSet products = (ChemicalEquationSet) visit(ctx.chemEqSet(1));
        return new ChemicalEquation(reactants, products, direction);
    }

    @Override
    public Object visitBidirChemEq(ChemParser.BidirChemEqContext ctx) {
        ChemicalEquationSet reactants = (ChemicalEquationSet) visit(ctx.chemEqSet(0));
        ChemicalEquationDirection direction = ChemicalEquationDirection.BIDIRECTIONAL;
        ChemicalEquationSet products = (ChemicalEquationSet) visit(ctx.chemEqSet(1));
        return new ChemicalEquation(reactants, products, direction);
    }

    @Override
    public Object visitChemEqSet(ChemParser.ChemEqSetContext ctx) {
        ImmutableList<ChemicalEquationUnit> formulaUnits = ctx.chemEqUnit().stream()
                .map(fu -> (ChemicalEquationUnit) visit(fu))
                .collect(toImmutableList());
        return new ChemicalEquationSet(formulaUnits);
    }
 
    @Override
    public Object visitChemEqUnit(ChemParser.ChemEqUnitContext ctx) {
        int count = ctx.COUNT() == null ? 1 : parseInt(ctx.COUNT().getText());
        Bond bond = (Bond) visit(ctx.bond());
        return new ChemicalEquationUnit(count, bond);
    }
    
    @Override
    public Object visitBond(ChemParser.BondContext ctx) {
        ImmutableList<BondUnit> bondUnits = ctx.bondUnit().stream()
                .map(bul -> (List<BondUnit>) visit(bul))
                .flatMap(l -> l.stream())
                .collect(toImmutableList());
        int charge = ctx.bondCharge() == null ? 0 : (Integer) visit(ctx.bondCharge());
        Phase phase = ctx.bondPhase() == null ? null : (Phase) visit(ctx.bondPhase());
        return new Bond(bondUnits, charge, phase);
    }

    @Override
    public Object visitGroupedBondUnit(ChemParser.GroupedBondUnitContext ctx) {
        int count = ctx.COUNT() == null ? 1 : parseInt(ctx.COUNT().getText());
        return ctx.bondUnit().stream()
                .map(bul -> (List<BondUnit>) visit(bul))
                .flatMap(l -> l.stream())
                .map(bu -> new BondUnit(bu.element, bu.count * count))
                .collect(toList());
    }

    @Override
    public Object visitSingleBondUnit(ChemParser.SingleBondUnitContext ctx) {
        Element element = ElementLookup.bySymbol(ctx.SYMBOL().getText());
        int count = ctx.COUNT() == null ? 1 : parseInt(ctx.COUNT().getText());
        return List.of(new BondUnit(element, count));
    }

    @Override
    public Phase visitBondPhase(ChemParser.BondPhaseContext ctx) {
        switch (ctx.PHASE().toString()) {
            case "g":
                return Phase.GAS;
            case "l":
                return Phase.LIQUID;
            case "s":
                return Phase.SOLID;
            case "aq":
                return Phase.AQUEOUS;
            default:
                throw new IllegalArgumentException("Unrecognized phase");
        }
    }

    @Override
    public Integer visitBondCharge(ChemParser.BondChargeContext ctx) {
        int charge = ctx.COUNT() == null ? 1 : Integer.parseInt(ctx.COUNT().getText());
        if (ctx.MINUS() != null) {
            charge = -charge;
        }
        return charge;
    }    
}
