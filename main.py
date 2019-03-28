import mysql.connector
import time
from datetime import timezone

USER_NAME = "Alice"
USER_ID = 1
TIMESTAMP = time.time()

class DatabaseConnector:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            #lzy971020
            password="htp19950715"
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
        sql_query = "select content, ts " \
                "from Post " \
                "   inner join ((select followeeID " \
                "       from UsersFollowUsers " \
                "       where followerID = 2) as followees " \
                "       inner join UsersOwnPosts " \
                "           on (userID = followees.followeeID)) " \
                "   on (Post.pID = postID );"
        new_posts = DBConnector.query(sql_query)
        for post in new_posts:
            # convert datetime.datetime to UTC timestamp
            post_timestamp = post[1].replace(tzinfo=timezone.utc).timestamp()
            if post_timestamp > TIMESTAMP:
                new_posts.remove(post)
        print(new_posts)
        return new_posts
        
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
            Util.getNewPostsFromFolloweesSinceLastLogin()
            break
            
    
    
    