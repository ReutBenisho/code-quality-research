
/**
 * Source: Cui et al. 2024, Table 3(a)
 * Mutation Operator: Wrapping a method with a nested class.
 * Ground Truth: Semantic Neutral (Should not change analysis results).
 */
public class NestedMutation {
    public void outerMethod() {
        // המוטציה: המתודה foo הועברה לתוך מחלקה פנימית
        class NestedClass {
            void foo() {
                System.out.println("Inner logic execution.");
            }
        }
        new NestedClass().foo();
    }
}