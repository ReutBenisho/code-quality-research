/**
 * Source: Cui et al. 2024, Fig 5(a)
 * Issue: SonarJava-3320
 * Category: Annotations / Lombok
 * Ground Truth: False Positive (FP)
 */
import lombok.Value;

@Value
public class CustomException extends Exception {
    // Sonar incorrectly warns that 'final' is missing, 
    // but @Value makes all fields final by default.
    private String customValue; 
}