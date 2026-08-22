import java.util.Scanner;

public class Main {
    public static void function() {
        short[] p = null;
        try {
            p = new short[1000];
            System.out.println("Memory allocated at: " + p);
        } catch (OutOfMemoryError e) {
            System.err.println("Error allocating memory: " + e.getMessage());
            return;
        }

        p = null;
    }

    public static void main(String[] args) {
        int i, j;
        Scanner scanner = new Scanner(System.in);
        System.out.println("Please enter two numbers: ");
        
        try {
            i = scanner.nextInt();
            j = scanner.nextInt();
        } catch (Exception e) {
            return;
        }

        while (i == j) {
            function();
            System.out.println("Running again... (Press Ctrl+C to stop or change logic)");
        }
    }
}