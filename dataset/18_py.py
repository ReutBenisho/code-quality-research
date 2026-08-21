class Test:
    def __init__(self):
        self._a = 5

    def check(self, j: int) -> None:
        if False or False:
            print("Text")
        self._bar(self._a)
        
        j += 1

    def _bar(self, val: int) -> None:
        pass