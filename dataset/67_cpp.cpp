bool XNor(bool a, bool b) {
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