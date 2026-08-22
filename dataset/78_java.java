public class Main {
    public static void CalcUpperCalcLower(String s) {
        /**
         * printing number of upper and lower letters in the string that been given:
         * :param s: string
         * :return: none
         */
        int upper_count = 0, lower_count = 0; // counters of upper and lower letters
        for (char i : s.toCharArray()) {
            if (Character.isUpperCase(i)) { // if the char is upper increase upper_count
                upper_count += 1;
            }
            else if (Character.isLowerCase(i)) { // if the char is lower increase lower_count
                lower_count += 1;
            }
        }
        System.out.println(String.format("Number of Upper cases: %d \nNumber of Lower cases: %d", upper_count, lower_count));
    }
}