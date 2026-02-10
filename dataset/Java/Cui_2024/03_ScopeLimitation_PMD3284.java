/**
 * Source: Cui et al. 2024, Fig 3(a)
 * Issue: PMD #1738
 * Category: Logic Error / Scope Analysis
 * Ground Truth: False Positive (FP)
 */
public class Wrapper {
    private static final Logger logger = new Logger();

    public void foo() {
        if (true) {           // Scope 1
            final String logMessage = "Message with three para: {}, {}, {}";
        }
        if (true) {           // Scope 2
            final String logMessage = "Message with one parameter: {}";
            final Object param = null; 
            // PMD incorrectly expects 3 arguments here based on Scope 1
            logger.trace(logMessage, param); 
        }
    }

    private static class Logger {
        void trace(String m, Object p) {}
    }
}