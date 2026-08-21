import sys

class Test:
    def __init__(self):
        def _action():
            foo = []
            print(foo, file=sys.stderr)
        self.someAction = _action