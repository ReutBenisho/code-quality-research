
/**
 * Source: Cui et al. 2024, Table 3(b)
 * Mutation Operator: Converting an anonymous class to a lambda expression.
 * Ground Truth: Semantic Neutral.
 */
public class LambdaMutation {
    public void runTask() {
        // המוטציה: שימוש בלמדא במקום Runnable אנונימי
        Runnable r = () -> {
            System.out.println("Running task via lambda");
        };
        r.run();
    }
}