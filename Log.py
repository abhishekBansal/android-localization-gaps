class Logger:
    logEnabled = False;

    def __init__(self):
        logEnabled = False

    def d(self, logStr):
        if self.logEnabled:
            print logStr
