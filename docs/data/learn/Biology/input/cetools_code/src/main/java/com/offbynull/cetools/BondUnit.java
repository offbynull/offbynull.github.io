package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import com.offbynull.cetools.Element;
import java.util.Objects;

public final class BondUnit {
    
    public final Element element;
    public final int count;

    public BondUnit(Element element, int count) {
        Preconditions.checkNotNull(element);
        Preconditions.checkArgument(count > 0);
        
        this.element = element;
        this.count = count;
    }

    @Override
    public String toString() {
        return element.symbol + count;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 53 * hash + Objects.hashCode(this.element);
        hash = 53 * hash + this.count;
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
        final BondUnit other = (BondUnit) obj;
        if (this.count != other.count) {
            return false;
        }
        if (!Objects.equals(this.element, other.element)) {
            return false;
        }
        return true;
    }
    
}
