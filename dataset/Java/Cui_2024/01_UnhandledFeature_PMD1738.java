/**
 * Source: Cui et al. 2024, Fig 3(a)
 * Issue: PMD #1749
 * Category: Security / Data Leakage (Nested Classes)
 * Ground Truth: False Negative (FN)
 */
public class Outerclass {
    private int[] arr;
    public int[] getArr() { return arr; } // PMD detects this (True Positive)

    public static class Innerclass {
        private int[] arr2;
        // PMD fails to detect this exposure due to nested class structure
        public int[] getArr() { return arr2; } 
    }
}