import os
import importlib

class TestClass:
    def bad(self):
        data = None
        if IO.STATIC_FINAL_FIVE == 5:
            data = os.getenv("ADD")
        else:
            data = None

        tempClass = importlib.import_module(data)
        tempClassObject = tempClass()

        IO.writeLine(str(tempClassObject))