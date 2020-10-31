package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import com.google.common.collect.BoundType;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.Range;
import java.util.Objects;

public final class Element {
    public final String name;
    public final String symbol;
    public final int protonCount;
    public final ImmutableList<ElementIsotope> isotopes;
    public final Range<Double> atomicWeight; // aka relative atomic mass
    public final Double electronegativity;

    public Element(String name, String symbol, int protonCount, ImmutableList<ElementIsotope> isotopes, Range<Double> atomicWeight, Double electronegativity) {
        Preconditions.checkNotNull(name);
        Preconditions.checkNotNull(symbol);
        Preconditions.checkNotNull(isotopes);
        Preconditions.checkArgument(protonCount >= 1);
        if (atomicWeight != null) {
            Preconditions.checkArgument(atomicWeight.lowerEndpoint() >= 0.0);
            Preconditions.checkArgument(atomicWeight.upperEndpoint() >= 0.0);
            Preconditions.checkArgument(atomicWeight.lowerBoundType() == BoundType.CLOSED);
            Preconditions.checkArgument(atomicWeight.upperBoundType() == BoundType.CLOSED);
        }
        if (electronegativity != null) {
            Preconditions.checkArgument(electronegativity >= 0.0);
        }
        this.name = name;
        this.symbol = symbol;
        this.protonCount = protonCount;
        this.isotopes = ImmutableList.copyOf(isotopes);
        this.atomicWeight = atomicWeight;
        this.electronegativity = electronegativity;
    }

    public int atomicNumber() {
        return protonCount;
    }

    @Override
    public String toString() {
        return "Element{" + "name=" + name + ", symbol=" + symbol + ", protonCount=" + protonCount + ", isotopes=" + isotopes + ", atomicWeight=" + atomicWeight + ", electronegativity=" + electronegativity + '}';
    }

    @Override
    public int hashCode() {
        int hash = 5;
        hash = 59 * hash + Objects.hashCode(this.name);
        hash = 59 * hash + Objects.hashCode(this.symbol);
        hash = 59 * hash + this.protonCount;
        hash = 59 * hash + Objects.hashCode(this.isotopes);
        hash = 59 * hash + Objects.hashCode(this.atomicWeight);
        hash = 59 * hash + Objects.hashCode(this.electronegativity);
        return hash;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final Element other = (Element) obj;
        if (this.protonCount != other.protonCount) {
            return false;
        }
        if (!Objects.equals(this.name, other.name)) {
            return false;
        }
        if (!Objects.equals(this.symbol, other.symbol)) {
            return false;
        }
        if (!Objects.equals(this.isotopes, other.isotopes)) {
            return false;
        }
        if (!Objects.equals(this.atomicWeight, other.atomicWeight)) {
            return false;
        }
        if (!Objects.equals(this.electronegativity, other.electronegativity)) {
            return false;
        }
        return true;
    }

}
