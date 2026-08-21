
public class NestedMutation {
    public void outerMethod() {
        class NestedClass {
            void foo() {
                System.out.println("Inner logic execution.");
            }
        }
        new NestedClass().foo();
    }
}
