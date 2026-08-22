class Outerclass:
    def __init__(self):
        self.__arr = []

    def getArr(self):
        return self.__arr

    class Innerclass:
        def __init__(self):
            self.__arr2 = []

        def getArr(self):
            return self.__arr2