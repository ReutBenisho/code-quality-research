
/**
 * Source: Cui et al. 2024, Fig 6(a)
 * Issue: PMD CloseResource FP
 * Category: Data-flow analysis / Method calls
 * Ground Truth: False Positive (FP) - Resource is actually closed.
 */
import java.sql.Connection;

public class ResourceHoisting {
    // סגירת הקונקשן מתבצעת כאן
    void closeConnection(Connection c) throws Exception {
        if (c != null) c.close();
    }

    void process(Pool pool) throws Exception {
        Connection c = pool.getConnection();
        try {
            // Business logic
        } finally {
            // PMD FP: טוען שהמשאב לא נסגר כי הוא לא מנתח את מה שקורה בתוך המתודה
            closeConnection(c); 
        }
    }

    interface Pool { Connection getConnection(); }
}