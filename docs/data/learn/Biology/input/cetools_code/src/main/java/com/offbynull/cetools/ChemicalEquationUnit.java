package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import java.util.Objects;

public final class ChemicalEquationUnit {
    
    public final int count;
    public final Bond bond;

    public ChemicalEquationUnit(int count, Bond bond) {
        Preconditions.checkNotNull(bond);
        Preconditions.checkArgument(count > 0);

        this.count = count;
        this.bond = bond;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 61 * hash + this.count;
        hash = 61 * hash + Objects.hashCode(this.bond);
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
        final ChemicalEquationUnit other = (ChemicalEquationUnit) obj;
        if (this.count != other.count) {
            return false;
        }
        if (!Objects.equals(this.bond, other.bond)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return count + bond.toString();
    }
    
}
