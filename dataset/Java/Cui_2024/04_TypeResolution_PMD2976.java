/**
 * Source: Cui et al. 2024, Fig 3(f)
 * Issue: SonarJava-3619
 * Category: Symbolic Execution / Logic
 * Ground Truth: False Positive (FP)
 */
public class Wrapper {
    public byte[] foo(byte[] a1, byte[] a2) {
        // Sonar incorrectly suggests comparing byte arrays with equals() 
        // instead of checking length, leading to logic flaws.
        if (a1.length != a2.length) {
            return null;
        }
        return a1;
    }
}
