class NestedClassSample {
public:
    void foo() {
        InnerClass::doSomething();
    }

    class InnerClass {
    private:
        static void doSomething() { }
    };
};