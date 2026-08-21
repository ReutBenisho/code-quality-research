class Wrapper:
    class Logger:
        def trace(self, m: str, p: object) -> None:
            pass

    logger = Logger()

    def foo(self) -> None:
        if True:
            logMessage = "Message with three params: {}, {}, {}"
        if True:
            logMessage = "Message with one parameter: {}"
            param = None
            self.logger.trace(logMessage, param)