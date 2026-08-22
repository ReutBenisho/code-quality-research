package testcases.javatestcases.t51;

public class TestClass {
    private static final int PRIVATE_STATIC_FINAL_FIVE = 5;

    public static void func() {
        int data; 
        
        if (PRIVATE_STATIC_FINAL_FIVE == 5) {
            data = Short.MAX_VALUE;
        } else {
            data = 0;
        }

        if (PRIVATE_STATIC_FINAL_FIVE == 5) {
            int result = ++data; 
            System.out.println("result: " + result);
        }
    }

    public static void main(String[] args) {
        func();
    }
}