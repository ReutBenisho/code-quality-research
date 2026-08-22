public class Main {
    public static void CalcUpperCalcLower(String string) {
        int[] counter = {0, 0};
        for (int x = 0; x < string.length(); x++) {
            if (string.charAt(x) >= 'a' <= 'z') {
                counter[0] = counter[0] + 1;
            }
            else if (string.charAt(x) >= 'A' <= 'Z') {
                counter[1] = counter[1] + 1;
            }
        }
        System.out.println("Number of Upper cases:" + String.valueOf(counter[1]));
        System.out.println("Number of Lower cases:" + String.valueOf(counter[0]));
    }
}