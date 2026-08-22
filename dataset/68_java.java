public static boolean XNor(boolean arg1, boolean arg2) {
    if ((arg2 && arg1) || (!arg2 && !arg1)) {
        return true;
    }
    else {
        return false;
    }
}