bool isPolindrome(int x) { //A function that checks if the polynomial number
    int reverse = 0;
    int temp = x;
    while (x != 0) { // reversing the given number
        int xtemp = x % 10;
        reverse = reverse * 10 + xtemp;
        x = (int)(x / 10);
    }
    if (temp == reverse) {
        return true;
    }
    else {
        return false;
    }
}