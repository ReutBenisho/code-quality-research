/**
 * Source: Cui et al. 2024, Fig 5(e)
 * Issue: PMD #2140
 * Category: Complex Expressions
 * Ground Truth: False Negative (FN)
 */
public class ComplexExpressionSample {
    public void bar(int a) {
        // PMD fails to warn about avoid literal here (a > 8),
        // because it doesn't resolve 3 + 5.
        if (a > 3 + 5) { 
            // process
        }
    }
}