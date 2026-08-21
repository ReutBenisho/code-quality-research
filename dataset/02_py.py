from typing import Optional

def immutable(cls):
    return cls

def thread_safe(cls):
    return cls


class Wrapper:
    @immutable
    class MyImmutable:
        pass

    @thread_safe
    class MyThreadSafe:
        pass

    class Main:
        def __init__(self):
            self.__x: Optional['Wrapper.MyImmutable'] = None
            self.__y: Optional['Wrapper.MyThreadSafe'] = None