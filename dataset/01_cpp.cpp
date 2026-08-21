#include <vector>

class Outerclass {
private:
    std::vector<int> arr;

public:
    std::vector<int> getArr() { return arr; }

    class Innerclass {
    private:
        std::vector<int> arr2;

    public:
        std::vector<int> getArr() { return arr2; }
    };
};