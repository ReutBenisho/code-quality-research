import java.util.Scanner;

public class Main {
    public static void function() {
        short[] p = null;
        try {
            p = new short[1000];
        } catch (OutOfMemoryError e) {
            System.out.println("Error allocating memory.");
        }

        System.out.print(p);
        return;
    }

    public static void main(String[] args) {
        int i, j;
        Scanner scanner = new Scanner(System.in);
        System.out.println("Please enter two numbers: ");
        i = scanner.nextInt();
        j = scanner.nextInt();

        while (i == j) function();
        return;
    }
}