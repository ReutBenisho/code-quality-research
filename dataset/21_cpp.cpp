#include <vector>
#include <cstdint>

class Storage {
private:
    std::vector<uint8_t> buf;

    Storage(const std::vector<uint8_t>& buf) : buf(buf) {}

public:
    static Storage of(const std::vector<uint8_t>& buf) {
        return Storage(buf);
    }
};