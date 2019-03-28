import mysql.connector
import time

USERNAME = "Alice"
ID = 1
TIMESTAMP = time.time()

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

DBConnector = DatabaseConnector()

class Util:  
    @staticmethod
    def login():
        print("login")
      
    @staticmethod
    def getCurrentUserInformation():
        print("getCurrentUserInformation")

    @staticmethod
    def getNewPostsFromFolloweesSinceLastLogin():
        print("getNewPostsFromFolloweesSinceLastLogin")
        
    @staticmethod
    def getNewPostsFromTopicsUserFollowsSinceLastLogin():
        print("getNewPostsFromFolloweesSinceLastLogin")
        
    @staticmethod
    def getAllFollowers():
        print("getAllFollowers")
    
    @staticmethod
    def getAllFollowees():
        print("getAllFollowees")
        
    @staticmethod
    def getTopicsCurrentUserFollows():
        print("getTopicsCurrentUserFollows")

    @staticmethod
    def getGroupsUserJoins():
        print("getGroupsUserJoins")
        
    @staticmethod
    def getPostsUserOwns():
        print("getPostsUserOwns")
        
    @staticmethod
    def makeNewPostWithTopic():
        print("makeNewPostWithTopic")
    
    @staticmethod
    def thumbUpPost():
        print("thumbUpPost")
        
    @staticmethod
    def thumbDownPost():
        print("thumbDownPost")
        
    @staticmethod
    def replyToPost():
        print("replyToPost")
        
    @staticmethod
    def joinGroup():
        print("joinGroup")
        
    @staticmethod
    def createGroup():
        print("createGroup")
        
    @staticmethod
    def followTopic():
        print("followTopic")
        
    @staticmethod
    def logout():
        print("logout")


class Main:
    DBConnector.runScript("./createTable.sql")
    print("Finished initializing database.")
    
    while True:
        var = input("Please enter something: ")
        print("You entered: " + var)
        if int(var) == 123:
            print("Terminating the program. Bye.")
            break
            
    
    
    