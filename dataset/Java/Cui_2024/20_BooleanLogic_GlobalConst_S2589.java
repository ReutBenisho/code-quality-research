
/**
 * Source: Cui et al. 2024, Fig 6(b)
 * Issue: SonarQube S2589 FN
 * Category: Variable Scope Analysis
 * Ground Truth: False Negative (FN) - Expression is always false.
 */
public class GlobalConstantLogic {
    // הקבוע מוגדר מחוץ למתודה
    public static final int c = 0;

    public static void booleanExpressionMethod() {
        // Sonar FN: נכשל בזיהוי ש-c הוא 0, ולא מתריע שהתנאי תמיד שקרי
        if (c != 0) { 
            System.out.println("This will never print");
        }
    }
}