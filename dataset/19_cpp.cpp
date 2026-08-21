#include <memory>

class Test {
    void closeConnection(std::shared_ptr<Connection> c) {
        if (c != nullptr) c->close();
    }

    void process(Pool& pool) {
        std::shared_ptr<Connection> c = pool.getConnection();
        try {
            // Business logic
        } catch (...) {
            closeConnection(c);
            throw;
        }
        closeConnection(c);
    }

    class Pool {
    public:
        virtual ~Pool() = default;
        virtual std::shared_ptr<Connection> getConnection() = 0;
    };
};