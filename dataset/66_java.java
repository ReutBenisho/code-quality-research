public static boolean XNor(boolean num1, boolean num2) {
    if (num1 == false && num2 == false) { //Checking conditions
        return true;
    }
    else if (num1 == false && num2 == true) {
        return false;
    }
    else if (num1 == true && num2 == false) {
        return false;
    }
    else if (num1 == true && num2 == true) {
        return true;
    }
}