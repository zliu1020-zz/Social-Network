import mysql.connector
import time

USERNAME = ""
ID = -1
TIMESTAMP = time.gmtime(0)

class DatabaseConnector:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="lzy971020"
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
        userName = input("what is your user name? ")
        userID = input("what is your ID ")
        searchQuery = "select * from NetworkUser where name = '" + userName + "' and uID = " + userID + ";"
        result = DBConnector.query(searchQuery)

        if result:
            ID = result[0][0]
            USERNAME = result[0][1]
            TIMESTAMP = time.time()
            print("Hello, " + USERNAME + " !")
            return True

        else:
            print("you are not present in our database, please try again")
            return False
      
    @staticmethod
    def getCurrentUserInformation():
        sql = "select * from NetworkUser WHERE uid = %i" % ID
        result = DBConnector.query(sql)
        return result

    @staticmethod
    def getNewPostsFromFolloweesSinceLastLogin():
        print("getNewPostsFromFolloweesSinceLastLogin")
        
    @staticmethod
    def getNewPostsFromTopicsUserFollowsSinceLastLogin():
        print("getNewPostsFromFolloweesSinceLastLogin")
        
    @staticmethod
    def getAllFollowers():
        sql = "select UsersFollowUsers.followerID as followerID,\
         (select name from NetworkUser where uID = followerID) as followerName\
         from NetworkUser inner join UsersFollowUsers on NetworkUser.uID = UsersFollowUsers.followeeID\
         where uID = %i" % ID
        result = DBConnector.query(sql)
        return result
    
    @staticmethod
    def getAllFollowees():
        sql = "select UsersFollowUsers.followeeID,\
         (select name from NetworkUser where NetworkUser.uID = UsersFollowUsers.followeeID) as followeeName\
          from UsersFollowUsers inner join NetworkUser\
           on UsersFollowUsers.followerID = NetworkUser.uID where followerID = %i" % ID
        result = DBConnector.query(sql)
        return result
        
    @staticmethod
    def getTopicsCurrentUserFollows():
        print("getTopicsCurrentUserFollows")

    @staticmethod
    def getGroupsUserJoins():
        sql = "select UsersBelongToGroups.groupID, SocialGroup.name from UsersBelongToGroups\
         inner join SocialGroup on UsersBelongToGroups.groupID = SocialGroup.gID\
          where userID = %i" % ID
        result = DBConnector.query(sql)
        return result
        
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
    Util.login()
    
    # while True:
    #     var = input("Please enter something: ")
    #     print("You entered: " + var)
    #     if int(var) == 123:
    #         print("Terminating the program. Bye.")
    #         break

            
    
    
    