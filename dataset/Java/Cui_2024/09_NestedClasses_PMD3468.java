/**
 * Source: Cui et al. 2024, Fig 5(c)
 * Issue: PMD #3468
 * Category: Nested Classes
 * Ground Truth: False Positive (FP)
 */
public class NestedClassSample {
    public void foo() {
        InnerClass.doSomething(); // doSomething() is used here
    }

    static class InnerClass {
        // PMD FP: Claims this is an unused private method
        private static void doSomething() { } 
    }
}