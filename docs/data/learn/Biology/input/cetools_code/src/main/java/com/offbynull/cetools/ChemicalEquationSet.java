package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import com.google.common.collect.ImmutableList;
import static com.google.common.collect.ImmutableList.toImmutableList;
import java.util.Objects;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.summingInt;

public final class ChemicalEquationSet {
    
    public ImmutableList<ChemicalEquationUnit> items;

    public ChemicalEquationSet(ImmutableList<ChemicalEquationUnit> items) {
        Preconditions.checkNotNull(items);

        // consolidate repeated + sort because consolidation will have swapped things around
        this.items = items.stream()
                .collect(
                        groupingBy(
                                e -> e.bond,
                                summingInt(e -> e.count)
                        )
                )
                .entrySet().stream()
                .map(e -> new ChemicalEquationUnit(e.getValue(), e.getKey()))
                .sorted((x,y) -> x.bond.toString().compareTo(y.bond.toString()))
                .collect(toImmutableList());
    }

    @Override
    public int hashCode() {
        int hash = 5;
        hash = 89 * hash + Objects.hashCode(this.items);
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
        final ChemicalEquationSet other = (ChemicalEquationSet) obj;
        if (!Objects.equals(this.items, other.items)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return items.toString();
    }
    
}
