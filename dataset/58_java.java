public class Program {
    public static void assignData(String data) {
        Scanner scanner = new Scanner(System.in);
        data = scanner.next();
    }

    public static void main(String[] args) {
        String data1 = "";
        String data2 = "";
        assignData(data1);
        assignData(data2);
        System.out.println(data1);
        System.out.println(data2);
    }
}