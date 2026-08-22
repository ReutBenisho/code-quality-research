import java.util.Scanner;

public class Main {
    public static final int MAXSIZE = 40;

    public static void process_input_safe() {
        char[] buffer = new char[MAXSIZE];
        Scanner scanner = new Scanner(System.in);
        String input = scanner.next();
        if (input.length() > MAXSIZE - 1) {
            input = input.substring(0, MAXSIZE - 1);
        }
        buffer = input.toCharArray();
        System.out.println("Data received safely: " + String.valueOf(buffer));
    }

    public static void main(String[] args) {
        process_input_safe();
    }
}