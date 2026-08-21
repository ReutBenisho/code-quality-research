class Test:
    def __init__(self):
        self._b = 10

    def b(self) -> None:
        print(f"Method b called. Field b value: {self._b}")