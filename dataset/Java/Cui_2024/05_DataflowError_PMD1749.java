/**
 * Source: Cui et al. 2024, Fig 3(b)
 * Issue: SonarJava-3804
 * Category: Dataflow Anomaly
 * Ground Truth: False Positive (FP)
 */
public class Wrapper {
    public void test() {
        int a = 0;
        // Sonar incorrectly flags this as a DD-Anomaly (Double Declaration)
        a = a + 3; 
    }
}