public class Wrapper {
    private static final Logger logger = new Logger();

    public void foo() {
        if (true) {           // Scope 1
            final String logMessage = "Message with three para: {}, {}, {}";
        }
        if (true) {           // Scope 2
            final String logMessage = "Message with one parameter: {}";
            final Object param = null; 
            logger.trace(logMessage, param); 
        }
    }

    private static class Logger {
        void trace(String m, Object p) {}
    }
}
