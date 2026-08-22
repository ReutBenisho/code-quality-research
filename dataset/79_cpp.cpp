bool PerfectNumber(int number) {
    int Sum = 0;
    for (int i = 1; i < number; i++) {
        if (number % i == 0) {
            Sum = Sum + i;
        }
    }
    return Sum == number;
}