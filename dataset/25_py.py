import sys

class TestClass:
    def func(self, request, response):
        data = -sys.maxsize - 1

        cookieSources = request.getCookies()
        if cookieSources is not None:
            stringNumber = cookieSources[0].getValue()
            try:
                data = int(stringNumber.strip())
            except ValueError as exceptNumberFormat:
                IO.logger.log(Level.WARNING, "Number format exception reading data from cookie", exceptNumberFormat)

        array = [0, 1, 2, 3, 4]

        if data < len(array):
            IO.writeLine(array[data])
        else:
            IO.writeLine("Array index out of bounds")