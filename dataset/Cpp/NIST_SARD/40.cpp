#include <iostream>
#include <new>

using namespace std;

void function() {
    short *p = nullptr;
    try {
        p = new short[1000];
        cout << "Memory allocated at: " << p << endl;
    }
    catch (const bad_alloc& e) {
        cerr << "Error allocating memory: " << e.what() << endl;
        return;
    }

    delete[] p;
}

int main() {
    int i, j;
    cout << "Please enter two numbers: " << endl;
    if (!(cin >> i >> j)) return 1;

    while (i == j) {
        function();
        cout << "Running again... (Press Ctrl+C to stop or change logic)" << endl;
    }

    return 0;
}