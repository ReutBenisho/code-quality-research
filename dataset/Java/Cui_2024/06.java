/**
 * Source: Cui et al. 2024, Fig 3(c)
 * Issue: PMD #3284
 * Category: Logical Logic / Boolean Evaluation
 * Ground Truth: False Positive (FP)
 */
public class Wrapper {
    public void foo(Boolean b) {
        if (b == Boolean.TRUE) {
            // Do something
        } else if (b == Boolean.FALSE) { 
            // PMD incorrectly claims this expression is always "true" 
            // because it fails to account for the 'null' possibility in boxed Boolean.
        }
    }
}