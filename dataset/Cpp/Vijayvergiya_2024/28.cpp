/**
 * Source: Vijayvergiya et al. (2024), Figure 3
 * Language: C++
 * Category: Style / Maintainability
 * Description: Use of std::pair instead of a struct. 
 * AI Suggestion: Prefer a 'struct' instead of a pair so elements can have meaningful names.
 */
#include <utility>
#include <string>
#include <vector>

class SnippetManager {
public:
    // שימוש ב-pair המקשה על הבנת משמעות הערכים המוחזרים
    std::pair<int, int> GetMinAndMaxSnippetLength(const std::vector<std::string>& snippets) {
        int min_len = 100;
        int max_len = 0;
        // Logic to calculate lengths...
        return std::make_pair(min_len, max_len);
    }
};