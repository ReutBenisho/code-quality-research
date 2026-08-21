#include <vector>

class Test {
public:
    double energy(int x) { return 0.0; }

private:
    void process(std::vector<double> energy) {
        energy = energy(1);
    }
};