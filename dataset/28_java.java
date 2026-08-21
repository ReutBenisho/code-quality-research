import java.util.List;
import java.util.AbstractMap;

public class SnippetManager {
    public AbstractMap.SimpleEntry<Integer, Integer> GetMinAndMaxSnippetLength(List<String> snippets) {
        int min_len = 100;
        int max_len = 0;
        // ... inner logic to calculate lengths (can assume it's correct)
        return new AbstractMap.SimpleEntry<>(min_len, max_len);
    }
}