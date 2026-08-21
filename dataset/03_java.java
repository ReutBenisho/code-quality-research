public class Wrapper {
    private static final Logger logger = new Logger();

    public void foo() {
        if (true) {           
            final String logMessage = "Message with three params: {}, {}, {}";
        }
        if (true) {           
            final String logMessage = "Message with one parameter: {}";
            final Object param = null; 
            logger.trace(logMessage, param); 
        }
    }

    private static class Logger {
        void trace(String m, Object p) {}
    }
}
