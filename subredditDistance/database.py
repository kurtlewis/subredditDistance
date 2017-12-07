import mysql.connector
from configparser import ConfigParser


class DatabaseConnection:

    def __init__(self, tableName, forceNewTable=True):
        self.tableName = tableName
        config = self.readConfigFile()
        self.cnx = mysql.connector.connect(user=config['user'],
                                           password=config['password'],
                                           host=config['host'],
                                           database=config['database'])

        self.tableCreateString = (" CREATE TABLE " + tableName + " ("
                                  "  from_sub VARCHAR(50) NOT NULL,"
                                  "  to_sub VARCHAR(50) NOT NULL,"
                                  "  occurences INT NOT NULL,"
                                  "  PRIMARY KEY (from_sub, to_sub)"
                                  ") Engine=InnoDB")

        self.subQuery = ("SELECT occurences FROM " + tableName + " "
                         "WHERE from_sub=%s and to_sub=%s")

        self.subUpdate = ("UPDATE " + tableName + " SET occurences = %s "
                          "WHERE from_sub=%s and to_sub=%s")

        self.subInsert = ("INSERT INTO " + tableName + " "
                          "(from_sub, to_sub, occurences) "
                          "VALUES (%s, %s, %s)")

        self.checkForTable = ("Select * "
                              "FROM information_schema.tables "
                              "WHERE TABLE_SCHEMA='" + config['database'] + "'"
                              " AND TABLE_NAME='" + tableName + "' "
                              "LIMIT 1;")
        
        self.createTable(forceNewTable)

    def createTable(self, forceNewTable):
        try:
            cursor = self.cnx.cursor()
            cursor.execute(self.checkForTable)
            cursor.fetchall()
            if (cursor.rowcount == 0 or forceNewTable):
                cursor.execute(self.tableCreateString)
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

    def addSubredditLink(self, from_sub, to_sub, numLinks):
        cursor = self.cnx.cursor()
        cursor.execute(self.subQuery, (from_sub, to_sub))
        row = cursor.fetchone()
        if row is not None:
            cursor.execute(self.subUpdate, (row[0] + numLinks, from_sub, to_sub))
        else:
            # no result, so insert sub
            try:
                cursor.execute(self.subInsert, (from_sub, to_sub, numLinks))
            except mysql.connector.errors.DataError as err:
                # the subreddit name is probably too long for the table -
                # skip this link
                print("Error: " + str(err))

        # commit changes
        self.cnx.commit()
        if cursor.rowcount > 1:
            raise Exception("More than one result returned")

    def close(self):
        self.cnx.close()