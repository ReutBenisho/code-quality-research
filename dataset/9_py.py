class NestedClassSample:
    def foo(self):
        NestedClassSample.InnerClass._doSomething()

    class InnerClass:
        @staticmethod
        def _doSomething():
            pass