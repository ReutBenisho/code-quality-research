
/**
 * Source: Cui et al. 2024, Table 3(c)
 * Mutation Operator: Renaming symbols to create same identifiers.
 * Ground Truth: Semantic Neutral.
 */
public class IdentifierMutation {
    // המוטציה: למשתנה b ולמתודה b יש אותו שם
    private int b = 10;

    public void b() {
        System.out.println("Method b called. Field b value: " + this.b);
    }
}