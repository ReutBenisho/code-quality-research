#include <atomic>

class Wrapper {
public:
    class MyImmutable { };

    class MyThreadSafe { };

    class Main {
    private:
        std::atomic<MyImmutable*> x;
        std::atomic<MyThreadSafe*> y;
    };
};