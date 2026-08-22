class MinMax_s {
    public int min;
    public int max;

    public MinMax_s(int min, int max) {
        this.min = min;
        this.max = max;
    }
}

public class SnippetManager {
    public MinMax_s GetMinAndMaxSnippetLength(List<String> snippets) {
        int min_len = 100;
        int max_len = 0;
        // ... inner logic to calculate lengths (can assume it's correct)
        MinMax_s minMax = new MinMax_s(min_len, max_len);
        return minMax;
    }
}