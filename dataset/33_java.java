import java.util.Scanner;

public class Main {
    public static final int MAXSIZE = 40;

    public static void process_input() {
        char[] buffer = new char[MAXSIZE];
        Scanner scanner = new Scanner(System.in);
        String input = scanner.next();
        buffer = input.toCharArray();
        System.out.println("Data received: " + String.valueOf(buffer));
    }

    public static void main(String[] args) {
        process_input();
    }
}