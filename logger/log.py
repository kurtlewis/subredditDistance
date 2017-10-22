class Log:
    """ Object containing configuration and data for logging."""
    filename = './log.txt'
    output
    size = 200
    linesSinceLastLog

    def __init__(self, filename, size):
        self.filename = filename
        self.size = size
        output = list()
        linesSinceLastLog = 0

    def log(self, strToLog):
        output.append(strToLog)
        linesSinceLastLog += 1

        if output.size > size:
            output.popLeft()

    def writeToFile(self):
        file = open(filename, 'w')
        file.writeLines(output)
        file.close()
        linesSinceLastLog = 0

    def logAndAutoWrite(self, strToLog):
        self.log(strToLog)
        if linesSinceLastLog >= size:
            self.writeToFile()
