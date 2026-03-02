public class NestedClassSample {
    public void foo() {
        InnerClass.doSomething(); // doSomething() is used here
    }

    static class InnerClass {
        private static void doSomething() { } 
    }
}
