
/**
 * Source: Cui et al. 2024, Table 3(d)
 * Mutation Operator: Replacing with equivalent statements/expressions.
 * Ground Truth: Semantic Neutral.
 */
public class EquivalenceMutation {
    private int a = 5;

    public void check(int j) {
        // המוטציה: false || false שקול ל-false, ושימוש ב-this.a
        if (false || false) {
            System.out.println("Unreachable");
        }
        this.bar(this.a);
        
        // המוטציה: ++j במקום j++
        ++j;
    }

    private void bar(int val) {}
}
