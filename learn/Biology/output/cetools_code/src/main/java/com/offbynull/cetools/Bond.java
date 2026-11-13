package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import com.google.common.collect.ImmutableList;
import static com.google.common.collect.ImmutableList.toImmutableList;
import com.google.common.collect.Range;
import java.util.Objects;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.summingInt;

public final class Bond {

    public final ImmutableList<BondUnit> items;
    public final int charge;
    public final Phase phase;  // null means unknown/not specified

    public Bond(ImmutableList<BondUnit> items, int charge, Phase phase) {
        Preconditions.checkNotNull(items);
        // phase can be null
        
        this.charge = charge;
        this.phase = phase;
        
        // consolidate repeated (e.g. FeOFeOO -> Fe2O3) + sort because consolidation will have swapped things around
        this.items = items.stream()
                .collect(
                        groupingBy(
                                e -> e.element,
                                summingInt(e -> e.count)
                        )
                )
                .entrySet().stream()
                .map(e -> new BondUnit(e.getKey(), e.getValue()))
                .sorted((x, y) -> x.element.symbol.compareTo(y.element.symbol))
                .collect(toImmutableList());
    }
    
    public Range<Double> atomicWeight() {
        return Range.closed(
                items.stream().mapToDouble(bu -> bu.element.atomicWeight.lowerEndpoint() * bu.count).sum(),
                items.stream().mapToDouble(bu -> bu.element.atomicWeight.upperEndpoint() * bu.count).sum()
        );
    }

    @Override
    public String toString() {
        return items.toString();
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 37 * hash + Objects.hashCode(this.items);
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
        final Bond other = (Bond) obj;
        if (!Objects.equals(this.items, other.items)) {
            return false;
        }
        return true;
    }

}
