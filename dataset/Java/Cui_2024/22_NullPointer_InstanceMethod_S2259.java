
/**
 * Source: Cui et al. 2024, Fig 6(d)
 * Issue: SonarQube S2259 FN
 * Category: Symbolic Execution / Null Pointer
 * Ground Truth: False Negative (FN) - Potential NullPointerException.
 */
public class MetamorphicNullPointer {
    // המוטציה: המתודה הפכה ל-Instance method
    public void hasArguments(String name) {
        int length = name.length(); // פוטנציאל ל-NPE
        System.out.println("Length: " + length);
    }

    public static void main(String[] args) {
        String name = null;
        MetamorphicNullPointer mnp = new MetamorphicNullPointer();
        // Sonar FN: נכשל במעקב אחר ה-null במבנה של אובייקט
        mnp.hasArguments(name); 
    }
}