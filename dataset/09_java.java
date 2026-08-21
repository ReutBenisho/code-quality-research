public class NestedClassSample {
    public void foo() {
        InnerClass.doSomething();
    }

    static class InnerClass {
        private static void doSomething() { } 
    }
}
