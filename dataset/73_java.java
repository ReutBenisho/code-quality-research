public class Main {
    public static int RemoveMinDigit(int num) {
        /**
         * Decription
         * Take number and remove all the appearance of the minimum digit in the number.
         * :param num: positive decimal number.
         * :return: the num after we removed all the appearance of the minimum digit in the number.
         */
        if (num <= 0) {
            System.out.println("Error, number must be positive");
            return num;
        }

        String numStr = String.valueOf(num);
        char minimum = numStr.charAt(0);
        for (int i = 1; i < numStr.length(); i++) {
            minimum = (char) Math.min(numStr.charAt(i), minimum);
        }
        numStr = numStr.replace(String.valueOf(minimum), "");
        int numRes = Integer.parseInt(numStr);
        return numRes;
    }
}