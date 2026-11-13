package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import com.google.common.collect.BoundType;
import com.google.common.collect.Range;
import java.util.Objects;

public final class ElementIsotope {
    public final int protonCount;
    public final int neutronCount;
    public final double atomicMass;
    public final Range<Double> relativeAbundance;

    public ElementIsotope(int protonCount, int neutronCount, double atomicMass, Range<Double> relativeAbundance) {
        Preconditions.checkArgument(protonCount >= 0);
        Preconditions.checkArgument(neutronCount >= 0);
        Preconditions.checkArgument(atomicMass > 0.0);
        if (relativeAbundance != null) {
            Preconditions.checkArgument(relativeAbundance.lowerEndpoint() >= 0.0);
            Preconditions.checkArgument(relativeAbundance.upperEndpoint() >= 0.0);
            Preconditions.checkArgument(relativeAbundance.lowerBoundType() == BoundType.CLOSED);
            Preconditions.checkArgument(relativeAbundance.upperBoundType() == BoundType.CLOSED);
        }
        this.protonCount = protonCount;
        this.neutronCount = neutronCount;
        this.atomicMass = atomicMass;
        this.relativeAbundance = relativeAbundance;
    }

    public int massNumber() {
        return protonCount + neutronCount;
    }

    @Override
    public int hashCode() {
        int hash = 5;
        hash = 89 * hash + this.protonCount;
        hash = 89 * hash + this.neutronCount;
        hash = 89 * hash + (int) (Double.doubleToLongBits(this.atomicMass) ^ (Double.doubleToLongBits(this.atomicMass) >>> 32));
        hash = 89 * hash + Objects.hashCode(this.relativeAbundance);
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
        final ElementIsotope other = (ElementIsotope) obj;
        if (this.protonCount != other.protonCount) {
            return false;
        }
        if (this.neutronCount != other.neutronCount) {
            return false;
        }
        if (Double.doubleToLongBits(this.atomicMass) != Double.doubleToLongBits(other.atomicMass)) {
            return false;
        }
        if (!Objects.equals(this.relativeAbundance, other.relativeAbundance)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "ElementIsotope{" + "protonCount=" + protonCount + ", neutronCount=" + neutronCount + ", atomicMass=" + atomicMass + ", relativeAbundance=" + relativeAbundance + '}';
    }
}
