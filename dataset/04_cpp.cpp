#include <vector>
#include <cstdint>

class Wrapper {
public:
    std::vector<uint8_t> foo(std::vector<uint8_t> a1, std::vector<uint8_t> a2) {
        if (a1.size() != a2.size()) {
            return {};
        }
        return a1;
    }
};