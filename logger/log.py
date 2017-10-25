class Log:
    """ Object containing configuration and data for logging."""

    def __init__(self, filename, size):
        self.filename = filename
        self.size = size
        # Treat output like queue, but it is implemented as a list
        self.output = list()
        self.linesSinceLastLog = 0

    def log(self, strToLog):
        self.output.append(strToLog)
        self.linesSinceLastLog += 1

        if len(self.output) > self.size:
            self.output.pop(0)

    def writeToFile(self):
        file = open(self.filename, 'w')
        for line in self.output:
            file.write(line + '\n')
        file.close()
        self.linesSinceLastLog = 0

    def logAndAutoWrite(self, strToLog):
        self.log(strToLog)
        if self.linesSinceLastLog >= self.size:
            self.writeToFile()
