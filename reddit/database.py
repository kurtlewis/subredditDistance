import mysql.connector
from configparser import ConfigParser


class DatabaseConnection:

    def __init__(self, tableName):
        self.tableName = tableName
        config = self.readConfigFile()
        self.cnx = mysql.connector.connect(user=config['user'],
                                           password=config['password'],
                                           host=config['host'],
                                           database=config['database'])
        self.cursor = self.cnx.cursor()

        self.createTable(tableName)

    def createTable(self, tableName):
        tableCreateString = (
            " CREATE TABLE " + tableName + " ("
            "  from_sub VARCHAR(21) NOT NULL,"
            "  to_sub VARCHAR(21) NOT NULL,"
            "  occurences INT NOT NULL,"
            "  PRIMARY KEY (from_sub)"
            ") Engine=InnoDB")
        try:
            self.cursor.execute(tableCreateString)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
                print('Table already exists')
            else:
                print(err.msg)
            raise err

    def readConfigFile(self):
        parser = ConfigParser()
        parser.read('config.ini')

        db = {}
        if parser.has_section('mysql'):
            items = parser.items('mysql')
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception('mysql missing from config file')

        return db

    def close(self):
        self.cnx.close()