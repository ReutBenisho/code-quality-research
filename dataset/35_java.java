import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        char[] input = new char[100];
        int i, n;
        long[] l;

        Scanner scanner = new Scanner(System.in);

        System.out.print("How many numbers do you want to type in? ");
        String line = scanner.nextLine();
        i = Integer.parseInt(line);

        l = new long[i];
        if (l == null) {
            System.exit(1);
        }

        for (n = 0; n < i; n++) {
            System.out.print("Enter number: ");
            line = scanner.nextLine();
            l[n] = Long.parseLong(line);
        }

        System.out.print("You have entered: ");
        for (n = 0; n < i; n++) {
            System.out.print(l[n] + ", ");
        }

        l = null;
    }
}