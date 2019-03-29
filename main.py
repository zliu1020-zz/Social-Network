import mysql.connector
import time
import datetime

USERNAME = ""
ID = -1
TIMESTAMP = 0


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

        if self.cursor.rowcount == 0:
            return False
        else:
            return True

    def rollback(self):
        self.db.rollback()

    def commit(self):
        self.db.commit()

    def executeWithoutCommitting(self, sql, val=None):
        self.cursor.execute(sql, val or ())

        if self.cursor.rowcount == 0:
            return False
        else:
            return True

    def runScript(self, path):
        file = open(path, 'r')
        sqlStatements = file.read()
        file.close()

        for statement in sqlStatements.split(';'):
            try:
                self.execute(statement)
            except OperationalError:
                print("Error found when executing sql statement: ", statement , " Skipping.")

    def getLastInsertionID(self):
        return self.cursor.lastrowid

    def closeConnection(self):
        self.db.close()
        self.cursor.close()

DBConnector = DatabaseConnector()

class Util:  
    @staticmethod
    def login():
        userName = input("what is your user name? ")
        userID = input("what is your ID ")
        searchQuery = "select * from NetworkUser where name = '" + userName + "' and uID = " + userID + ";"
        result = DBConnector.query(searchQuery)

        if result:
            global ID
            ID = result[0][0]
            global USERNAME
            USERNAME = result[0][1]
            global TIMESTAMP
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
        sql_query = "select content, ts " \
                "from Post " \
                "   inner join ((select followeeID " \
                "       from UsersFollowUsers " \
                "       where followerID = %i) as followees " \
                "       inner join UsersOwnPosts " \
                "           on (userID = followees.followeeID)) " \
                "   on (Post.pID = postID );" % ID
        new_posts = DBConnector.query(sql_query)
        for post in new_posts:
            # convert datetime.datetime to UTC timestamp
            post_timestamp = post[1].replace(tzinfo=datetime.timezone.utc).timestamp()
            if post_timestamp < TIMESTAMP:
                new_posts.remove(post)
        return new_posts
        
    @staticmethod
    def getNewPostsFromTopicsUserFollowsSinceLastLogin():
        sql_query = "select content, ts " \
                    "from Post " \
                    "   inner join ((select topicID " \
                    "       from UsersFollowTopics " \
                    "       where userID = %i) as topics " \
                    "       inner join PostsBelongToTopics " \
                    "           on (PostsBelongToTopics.topicID = topics.topicID)) " \
                    "   on (Post.pID = postID );" % ID
        new_posts = DBConnector.query(sql_query)
        for post in new_posts:
            # convert datetime.datetime to UTC timestamp
            post_timestamp = post[1].replace(tzinfo=datetime.timezone.utc).timestamp()
            if post_timestamp < TIMESTAMP:
                new_posts.remove(post)
        return new_posts
        
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
            sql = "select Topic.name from Topic \
                    inner join UsersFollowTopics as U \
                        on Topic.tID = U.topicID and U.userID = " + str(ID) +";"
            print(sql)
            result = DBConnector.query(sql)
            print(result)

    @staticmethod
    def getGroupsUserJoins():
        sql = "select UsersBelongToGroups.groupID, SocialGroup.name from UsersBelongToGroups\
         inner join SocialGroup on UsersBelongToGroups.groupID = SocialGroup.gID\
          where userID = %i" % ID
        result = DBConnector.query(sql)
        return result
        
    @staticmethod
    def getPostsUserOwns():
        sql = "select postID, content, ts, thumbNum from UsersOwnPosts\
         inner join Post on UsersOwnPosts.postID = Post.pID where userID = %i" % ID
        result = DBConnector.query(sql)
        return result
        
    @staticmethod
    def makeNewPostWithTopic():
        content = input("Please enter post content (text only):")
        topicName = input("Please enter the topic name associated with the current post:")
        if (not content) or (not topicName):
            print("Input is invalid. Please try again.")
            return False
        else:
            sql = "select * from Topic where name = '%s'" % topicName
            result = DBConnector.query(sql)
            if not result:
                sql = "INSERT INTO Topic (name) VALUES ('" + topicName + "')"
                insertionResult = DBConnector.executeWithoutCommitting(sql)
                if not insertionResult:
                    DBConnector.rollback()
                    print("Failed to create a new topic named %s. Please try again later.", topicName)
                    return False
                else:
                    topicID = DBConnector.getLastInsertionID()
                    print("A new topic named " + topicName + " is created successfully. ID = " + str(topicID))
            else:
                topicID = result[0][0]

            try:
                postSql = "INSERT INTO Post (content) VALUES ('" + content + "')"
                postResult = DBConnector.executeWithoutCommitting(postSql)
                postID = DBConnector.getLastInsertionID()

                usersOwnPostsSql = "INSERT INTO UsersOwnPosts (userID, postID) VALUES (" + str(ID) + "," + str(postID) + ")"
                usersOwnPostsResult = DBConnector.executeWithoutCommitting(usersOwnPostsSql)

                postsBelongToTopicsSql = "INSERT INTO PostsBelongToTopics (postID, topicID) VALUES (" + str(postID) + "," + str(topicID) + ")"
                postsBelongToTopicsResult = DBConnector.executeWithoutCommitting(postsBelongToTopicsSql)

                if postResult and usersOwnPostsResult and postsBelongToTopicsResult:
                    DBConnector.commit()
                    print("Post created successfully. ID = " + str(postID))
                    return True
                else:
                    DBConnector.rollback()
                    print("Encountered issues when inserting into database. Transaction aborted.")
                    return False
            except mysql.connector.Error as err:
                DBConnector.rollback()
                print("Encountered issues when inserting into database. Transaction aborted. Message: ", err.msg)
                return False

    
    @staticmethod
    def thumbUpPost():
        postNumber = input("what is the ID of the post you want to thumb up? ")

        sql = "update Post set thumbNum = thumbNum + 1 where pID = " + postNumber
        result = DBConnector.execute(sql)

        if result:
            print("thumb up added to the the post!")
        else:
            print("something wrong happened to the machine, please try again!")
        
    @staticmethod
    def thumbDownPost():
        postNumber = input("what is the ID of the post you want to thumb down? ")

        sql = "update Post set thumbNum = thumbNum - 1 where pID = " + postNumber
        result = DBConnector.execute(sql)

        if result:
            print("thumb down added to the the post!")
        else:
            print("something wrong happened to the machine, please try again!")
        
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
    #Util.makeNewPostWithTopic()
    DBConnector.closeConnection()

    # while True:
    #     var = input("Please enter something: ")
    #     print("You entered: " + var)
    #     if int(var) == 123:
    #         Util.getNewPostsFromFolloweesSinceLastLogin()
    #         break

    
    
    