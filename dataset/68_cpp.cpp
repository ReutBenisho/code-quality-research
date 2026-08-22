bool XNor(bool arg1, bool arg2) {
    if ((arg2 && arg1) || (!arg2 && !arg1)) {
        return true;
    }
    else {
        return false;
    }
}