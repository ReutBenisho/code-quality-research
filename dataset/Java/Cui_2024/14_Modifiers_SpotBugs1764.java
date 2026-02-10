/**
 * Source: Cui et al. 2024, Fig 5(h)
 * Issue: SpotBugs #1764
 * Category: Modifiers (Final Strings)
 * Ground Truth: False Negative (FN)
 */
public class ModifierSample {
    public boolean compareStrings() {
        String s1 = "str1";
        final String s2 = "str2";
        // SpotBugs fails to warn about "==" comparison 
        // because s2 is marked as final.
        return s1 == s2; 
    }
}
