
/**
 * Source: Cui et al. 2024, Fig 6(c)
 * Issue: SonarQube S2384 FP
 * Category: Mutable Members Storage
 * Ground Truth: False Positive (FP) - Storage is safe due to cloning.
 */
public class SecureStorage {
    private byte[] buf;

    // קונסטרקטור פרטי
    private SecureStorage(final byte[] buf) {
        // Sonar FP: טוען לאחסון לא בטוח של מערך מוטבילי
        this.buf = buf; 
    }

    public static SecureStorage of(final byte[] buf) {
        // כאן מתבצע ה-Clone, לכן הקונסטרקטור הפרטי מקבל עותק בטוח
        return new SecureStorage(buf.clone());
    }
}