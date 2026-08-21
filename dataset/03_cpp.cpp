#include <string>

class Wrapper {
private:
    class Logger {
    public:
        void trace(const std::string& m, void* p) {}
    };

    static inline Logger logger = Logger();

public:
    void foo() {
        if (true) {
            const std::string logMessage = "Message with three params: {}, {}, {}";
        }
        if (true) {
            const std::string logMessage = "Message with one parameter: {}";
            void* param = nullptr;
            logger.trace(logMessage, param);
        }
    }
};