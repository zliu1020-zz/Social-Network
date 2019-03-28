import mysql.connector

class DatabaseConnector:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mappleleaf12"
        )
        self.cursor = self.db.cursor()
    
    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def execute(self, sql, val=None):
        self.cursor.execute(sql, val or ())
        self.db.commit()
        
    def runScript(self, path):
        file = open(path, 'r')
        sqlStatements = file.read()
        file.close()

        for statement in sqlStatements.split(';'):
            try:
                self.execute(statement)
            except OperationalError:
                print("Error found when executing sql statement: ", statement , " Skipping.")


class Main:
    dbConnector = DatabaseConnector();
    dbConnector.runScript("./createTable.sql")
    print("Finished initializing database.")
    
    while True:
        var = input("Please enter something: ")
        print("You entered: " + var)
        if int(var) == 123:
            print("Terminating the program. Bye.")
            break
            
    
    
    