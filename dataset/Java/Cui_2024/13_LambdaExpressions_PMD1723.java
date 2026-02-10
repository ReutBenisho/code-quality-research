/**
 * Source: Cui et al. 2024, Fig 5(g)
 * Issue: PMD #1723
 * Category: Lambda Expressions
 * Ground Truth: False Positive (FP)
 */
import java.util.ArrayList;

public class LambdaSample {
    Runnable someAction = () -> {
        // PMD incorrectly flags this for "use diamond operator" 
        // inside the lambda, although foo is not explicitly typed.
        var foo = new ArrayList<String>(5);
        System.err.println(foo);
    };
}