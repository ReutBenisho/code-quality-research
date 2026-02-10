/**
 * Source: Cui et al. 2024, Fig 5(d)
 * Issue: PMD #1474
 * Category: Same Identifiers
 * Ground Truth: False Positive (FP)
 */
public class IdentifierConflict {
    public double energy(int x) { return 0.0; }

    private void process(double[] energy) {
        // PMD mistakes method call energy(1) as array energy, 
        // flagging it for insecure array storage.
        energy = energy(1); 
    }
}