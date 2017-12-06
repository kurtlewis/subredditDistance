import pickle
from pathlib import Path


class PicklingUtil:
    """ 'Pickles' the given queue/set for recovering from errors """
    def __init__(self, tableName, path):
        self.tableName = tableName
        self.path = path
        if not path.endswith('/'):
            self.path = self.path + '/'
        self.filename = self.path + self.tableName
        self.fileExt = '.pickle'

    def pickle(self, datastruct, desc):
        outFile = open(self.buildFilename(desc), 'wb')
        pickle.dump(datastruct, outFile)
        outFile.close()

    def load(self, desc):
        inFile = open(self.buildFilename(desc), 'rb')
        out = pickle.load(inFile)
        inFile.close()
        return out

    def buildFilename(self, desc):
        return self.filename + '-' + desc + self.fileExt

    def doesFileExist(self, desc):
        return Path(self.buildFilename(desc)).exists()