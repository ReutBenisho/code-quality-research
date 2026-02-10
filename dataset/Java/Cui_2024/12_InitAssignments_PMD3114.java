/**
 * Source: Cui et al. 2024, Fig 5(f)
 * Issue: PMD #3114
 * Category: Variable Initialization and Assignments
 * Ground Truth: False Positive (FP)
 */
public class InitializationSample {
    public int getStart() {
        int start; // PMD FP: unused variable 'start'
        if (true) start = 1;
        else start = 2;
        return start;
    }
}