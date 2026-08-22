public class Test {
    public void func(float data) {
        if (Math.abs(data) < 1e-9f) {
            System.err.println("Error: Division by zero");
            return;
        }

        double raw_result = 100.0 / data;

        if (raw_result > Integer.MAX_VALUE || 
            raw_result < Integer.MIN_VALUE) {
            System.err.println("Error: Result exceeds integer range");
            return;
        }

        int result = (int) raw_result;
        System.out.println("result: " + result);
    }
}