import secrets

class TestClass:
    def func(self):
        match 7:
            case 7:
                x = secrets.randbelow(2**32) - 2**31
                if x == 0:
                    IO.writeLine("Inside the if statement")
                else:
                    pass
                IO.writeLine("Hello from func()")
            case _:
                IO.writeLine("Benign, fixed string")