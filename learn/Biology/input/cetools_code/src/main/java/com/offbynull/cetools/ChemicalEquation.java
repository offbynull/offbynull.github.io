package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import java.util.Objects;

public final class ChemicalEquation {
    
    public final ChemicalEquationSet reactants;
    public final ChemicalEquationSet products;
    public final ChemicalEquationDirection direction;

    public ChemicalEquation(ChemicalEquationSet reactants, ChemicalEquationSet products, ChemicalEquationDirection direction) {
        Preconditions.checkNotNull(reactants);
        Preconditions.checkNotNull(products);
        Preconditions.checkNotNull(direction);

        this.reactants = reactants;
        this.products = products;
        this.direction = direction;
    }

    @Override
    public String toString() {
        String dir;
        switch (direction) {
            case UNIDIRECTIONAL:
                dir = "->";
                break;
            case BIDIRECTIONAL:
                dir = "<->";
                break;
            default:
                throw new IllegalStateException();
        }
        return reactants + " " + dir + " " + products;
    }

    @Override
    public int hashCode() {
        int hash = 5;
        hash = 43 * hash + Objects.hashCode(this.reactants);
        hash = 43 * hash + Objects.hashCode(this.products);
        hash = 43 * hash + Objects.hashCode(this.direction);
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
        final ChemicalEquation other = (ChemicalEquation) obj;
        if (!Objects.equals(this.reactants, other.reactants)) {
            return false;
        }
        if (!Objects.equals(this.products, other.products)) {
            return false;
        }
        if (this.direction != other.direction) {
            return false;
        }
        return true;
    }
    
    
    public enum ChemicalEquationDirection {
        UNIDIRECTIONAL,
        BIDIRECTIONAL
    }
}
