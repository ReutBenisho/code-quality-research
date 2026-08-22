double factorSum(int num) {
    /**
     * the funcation get number and return the sum of the the prime numbers
     */
    double temp = num;
    double sum = 0;

    if ((int)temp % 2 == 0) {
        sum = 2;
        while ((int)temp % 2 == 0) {
            temp = temp / 2;
        }
    }
    else {
        sum = 0;
    }

    if ((int)temp % 3 == 0) {
        sum = sum + 3;
        while ((int)temp % 3 == 0) {
            temp = temp / 3;
        }
    }
    else {
        // pass
    }

    if (temp != 1) {
        for (int i = 5; i <= num; i++) {
            if (i % 2 != 0 && i % 3 != 0) {
                if ((int)temp % i == 0) {
                    sum = sum + i;
                    while ((int)temp % i == 0) {
                        temp = temp / i;
                        if (temp == 1) {
                            return sum;
                        }
                    }
                }
            }
        }
    }
    else {
        return sum;
    }

    return sum;
}