#include <utility>
#include <string>
#include <vector>

struct MinMax_s
{
	int min;
	int max;
};

class SnippetManager {
public:
    MinMax_s GetMinAndMaxSnippetLength(const std::vector<std::string>& snippets) {
        int min_len = 100;
        int max_len = 0;
        // Logic to calculate lengths...
		MinMax_s minMax{min_len, max_len};
        return minMax;
    }
};
