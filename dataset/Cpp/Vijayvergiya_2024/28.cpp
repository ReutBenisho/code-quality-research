#include <utility>
#include <string>
#include <vector>

class SnippetManager {
public:
    std::pair<int, int> GetMinAndMaxSnippetLength(const std::vector<std::string>& snippets) {
        int min_len = 100;
        int max_len = 0;
        // ... inner logic to calculate lengths (can assume it's correct)
        return std::make_pair(min_len, max_len);
    }
};
