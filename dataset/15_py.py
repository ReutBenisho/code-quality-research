class NestedMutation:
    def outerMethod(self) -> None:
        class NestedClass:
            def foo(self) -> None:
                print("Inner logic execution.")
        
        NestedClass().foo()