#include <string>
#include <vector>
#include <stdexcept>
#include <cassert>

std::vector<uint8_t> get_url_to_bytes(const std::string& url, bool allow_file_url = false) {
    if (!allow_file_url && url.rfind("file://", 0) == 0) {
        throw std::invalid_argument("File URL not explicitly allowed: " + url);
    }
    return {'f', 'a', 'k', 'e', '_', 'd', 'a', 't', 'a'};
}

class TestUrlLoading {
public:
    void test_file_url_not_allowed() {
        std::string fake_file_url = "file://fake_image.png";
        try {
            get_url_to_bytes(fake_file_url, false);
            assert(false);
        } catch (const std::invalid_argument&) {
        }
    }
};