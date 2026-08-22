public static boolean XNor(boolean a, boolean b) {
    if (a == true) {
        if (b == true) {
            return true;
        }
    }
    if (a == false) {
        if (b == false) {
            return true;
        }
    }
    else {
        return false;
    }
}