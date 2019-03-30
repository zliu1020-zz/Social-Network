import mysql.connector
import time
from tabulate import tabulate

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
        userID = input("what is your ID? ")
        searchQuery = "select * from NetworkUser where name = '" + userName + "' and uID = " + userID + ";"
        result = DBConnector.query(searchQuery)

        if result:
            global ID
            ID = result[0][0]
            global USERNAME
            USERNAME = result[0][1]
            global TIMESTAMP
            TIMESTAMP = time.time()
            print("Hello, " + USERNAME + "!\n")
            return True

        else:
            print("You are not present in our database, please try again")
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
        posts = DBConnector.query(sql_query)
        new_posts = []
        for post in posts:
            # convert datetime.datetime to local timestamp
            post_timestamp = post[1].replace().timestamp()
            if post_timestamp > TIMESTAMP:
                new_posts.append(post)
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
        posts = DBConnector.query(sql_query)
        new_posts = []
        for post in posts:
            # convert datetime.datetime to local timestamp
            post_timestamp = post[1].replace().timestamp()
            if post_timestamp > TIMESTAMP:
                new_posts.append(post)
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
            sql = "select Topic.tID, Topic.name from Topic \
                    inner join UsersFollowTopics as U \
                        on Topic.tID = U.topicID and U.userID = " + str(ID) +";"
            result = DBConnector.query(sql)
            return result

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
                    print("Failed to create a new topic named " + topicName + ". Please try again later.")
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

        sql = "select * from Post where pID = " + str(postNumber)
        result = DBConnector.query(sql)

        if not result:
            print("Failure: The post with ID " + str(postNumber) + " does not exist. ")
            return False
        try:
            sql = "update Post set thumbNum = thumbNum + 1 where pID = " + postNumber
            result = DBConnector.executeWithoutCommitting(sql)

            if result:
                DBConnector.commit()
                print("thumb up added to the the post!")
                return True
            else:
                DBConnector.rollback()
                print("something wrong happened to the machine, please try again!")
                return False
        except mysql.connector.Error as err:
            DBConnector.rollback()
            print("Encountered issues when inserting into database. Transaction aborted. Message: ", err.msg)
            return False
        
    @staticmethod
    def thumbDownPost():
        postNumber = input("what is the ID of the post you want to thumb down? ")

        sql = "select * from Post where pID = " + str(postNumber)
        result = DBConnector.query(sql)

        if not result:
            print("Failure: The post with ID " + str(postNumber) + " does not exist. ")
            return False
        try:
            sql = "update Post set thumbNum = thumbNum - 1 where pID = " + postNumber
            result = DBConnector.executeWithoutCommitting(sql)

            if result:
                DBConnector.commit()
                print("thumb up added to the the post!")
                return True
            else:
                DBConnector.rollback()
                print("something wrong happened to the machine, please try again!")
                return False
        except mysql.connector.Error as err:
            DBConnector.rollback()
            print("Encountered issues when inserting into database. Transaction aborted. Message: ", err.msg)
            return False
        
    @staticmethod
    def replyToPost():
        postID = input("what is the ID of the post you want to reply? ")

        checkPostExistence = "select * from Post where pID = %s " %postID
        postInfo = DBConnector.query(checkPostExistence)

        if len(postInfo) == 0:
            print("The post does not exist!")
            return False

        content = input("what is the content to reply? ")
        if content == "":
            print("Please enter the reply content!")
            return False

        selectTopicsID = "select topicID from PostsBelongToTopics where PostsBelongToTopics.postID = %s " %postID
        topic = DBConnector.query(selectTopicsID)
        topicID = topic[0][0]

        if topicID == "":
            print("The post you want to reply does not belong to any topics!")
            return False
        try:
            sql = "insert into Post (content) values ('" + content + "')"
            postResult = DBConnector.executeWithoutCommitting(sql)

            if not postResult:
                DBConnector.rollback()
                print("Failed to create a new post with content " + content + ". Please try again later.")
                return False
            else:
                newPostID = DBConnector.getLastInsertionID()
                print("A new post with content \"" + content + "\" is created successfully. post ID = " + str(newPostID))

                usersOwnPostsResult = DBConnector.executeWithoutCommitting("insert into UsersOwnPosts(userID, postID) values(" + str(ID) + "," + str(newPostID) + ");")
                postsBelongToTopicsResult = DBConnector.executeWithoutCommitting("insert into PostsBelongToTopics(postID, topicID) values(" + str(newPostID) + "," + str(topicID) + ");")
                postsRespondToPostsResult = DBConnector.executeWithoutCommitting("insert into PostsRespondToPosts(respondedPostID, respondingPostID) values(" + str(postID) + "," + str(newPostID) + ");")

                if usersOwnPostsResult and postsBelongToTopicsResult and postsRespondToPostsResult:
                    DBConnector.commit()
                    print("You have replied to post id " + str(postID) + " successfully!")
                    return True
                else:
                    DBConnector.rollback()
                    print("Encountered issues when inserting into database. Transaction aborted.")

        except mysql.connector.Error as err:
            DBConnector.rollback()
            print("Encountered issues when inserting a new post into database. Transaction aborted. Message: ", err.msg)
            return False

    @staticmethod
    def joinGroup():
        groupID = input("Please enter the id of the group that you would like to join:")
        sql = "select * from SocialGroup where gID = " + str(groupID)
        result = DBConnector.query(sql)

        if not result:
            print("Failure: The group with group ID " + str(groupID) + " does not exist. ")
            return False

        try:
            sql = "insert into UsersBelongToGroups(userID, groupID) values(" + str(ID) + "," + str(groupID) + ")"
            result = DBConnector.executeWithoutCommitting(sql)

            if not result:
                DBConnector.rollback()
                print("Encountered issues when inserting into database. Transaction aborted.")
                return False
            else:
                DBConnector.commit()
                print("You've joined group " + str(groupID) + " successfully.")
                return True
        except mysql.connector.Error as err:
            DBConnector.rollback()
            print("Encountered issues when inserting into database. Transaction aborted. Message: ", err.msg)
            if "Duplicate entry" in err.msg:
                print("You have already joined the group id " + str(groupID) + "!")
            return False

    @staticmethod
    def createGroup():
        groupName = input("Please enter the name of the new group:")
        friendID = input("Please enter the ID of another user that you'd like to join the new group with:")

        if ID == int(friendID):
            print("Failed to invite a friend. Please don't invite yourself.")
            return False

        sql = "select * from NetworkUser where uID = " + str(friendID)
        result = DBConnector.query(sql)

        if (not result) or (not groupName):
            print("Failure: Nonexistent user id or invalid group name.")
            return False

        try:
            groupSql = "insert into SocialGroup(name) values('" + groupName + "')"
            groupResult = DBConnector.executeWithoutCommitting(groupSql)

            if not groupResult:
                DBConnector.rollback()
                print("Failed to create a new group named " + groupName + ". Please try again later.")
                return False
            else:
                groupID = DBConnector.getLastInsertionID()
                print("A new group named " + groupName + " is created successfully. ID = " + str(groupID))

                relationSql = "insert into UsersBelongToGroups(userID, groupID)\
                values(" + str(ID) + ","  + str(groupID) + "), " + "(" + str(friendID) + ","  + str(groupID) + ")"
                relationResult = DBConnector.executeWithoutCommitting(relationSql)

                if groupResult and relationResult:
                    DBConnector.commit()
                    print("You and user " + str(friendID) + " have joined group " + str(groupID) + ".")
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
    def followTopic():
        topicID = input("Please enter the id of the topic that you would like to follow:")
        sql = "select * from Topic where tID = " + str(topicID)
        result = DBConnector.query(sql)

        if not result:
            print("Failure: The topic with topic ID " + str(topicID) + " does not exist. ")
            return False

        try:
            sql = "insert into UsersFollowTopics(userID, topicID) values(" + str(ID) + "," + str(topicID) + ")"
            result = DBConnector.executeWithoutCommitting(sql)

            if not result:
                DBConnector.rollback()
                print("Encountered issues when inserting into database. Transaction aborted.")
                return False
            else:
                DBConnector.commit()
                print("You've followed topic " + str(topicID) + " successfully.")
                return True
        except mysql.connector.Error as err:
            DBConnector.rollback()
            print("Encountered issues when inserting into database. Transaction aborted. Message: ", err.msg)
            if "Duplicate entry" in err.msg:
                print("You have already followed the topic id " + str(topicID) + "!")
            return False

    @staticmethod
    def getAllUsers():
        sql  = "select uID, name from NetworkUser;"
        result = DBConnector.query(sql)
        return result

    @staticmethod
    def getAllGroups():
        sql  = "select gID, name from SocialGroup;"
        result = DBConnector.query(sql)
        return result

    @staticmethod
    def getAllPostsWithTopics():
        sql  = "select pID, content, ts, thumbNum, name from Post inner join PostsBelongToTopics on(Post.pId = PostsBelongToTopics.postID) inner join Topic on(topicID = tID);"
        result = DBConnector.query(sql)
        return result

    @staticmethod
    def getAllTopics():
        sql  = "select tID, name from Topic;"
        result = DBConnector.query(sql)
        return result
        
    @staticmethod
    def logout():
        global USERNAME
        USERNAME = ""
        global ID
        ID = -1
        global TIMESTAMP
        TIMESTAMP = 0

        print("You've logged out. Bye.")

    @staticmethod
    def setupDatabse():
        sql = "show databases like 'SocialNetwork'"
        result = DBConnector.query(sql)
        if not result:
            DBConnector.runScript("./createTable.sql")
            print("Finished initializing database.")
        else:
            DBConnector.execute("use SocialNetwork;")
            print("Use existing database SocialNetwork.")

    @staticmethod
    def printInstructions():
        print("***********************************************")
        print("A list of instructions supported by this tool:\n")
        print("show_current_user_info\n")
        print("show_new_posts_from_followees_since_last_login\n")
        print("show_new_posts_from_topics_user_follows_since_last_login\n")
        print("show_all_followers\n")
        print("show_all_followees\n")
        print("show_topics_user_follows\n")
        print("show_groups_user_joins\n")
        print("show_posts_user_owns\n")
        print("make_new_post_with_topic: takes two inputs, post content and topic name\n")
        print("thumb_up_post: takes one input, the post id\n")
        print("thumb_down_post: takes one input, the post id\n")
        print("reply_to_post: takes twos inputs, the post id and content\n")
        print("join_group: takes one input, the group id\n")
        print("create_group: takes two inputs, the group name and friend id\n")
        print("follow_topic: takes one input, the topic id\n")
        print("logout")
        print("***********************************************")

    @staticmethod
    def continuousLogin():
        success = Util.login()
        if not success:
            while True:
                success = Util.login()
                if success:
                    break

    @staticmethod
    def prettyPrint(content, header):
        print("\n")
        print(tabulate(content, headers=header))
        print("\n")


class Main:
    Util.setupDatabse();
    Util.continuousLogin()

    while True:
        time.sleep(0.5)
        Util.printInstructions()
        instruction = input("Please enter your instruction:")

        if instruction == "logout":
            Util.logout()
            DBConnector.closeConnection()
            break

        if instruction == "show_current_user_info":
            info = Util.getCurrentUserInformation()
            Util.prettyPrint(info, ['ID', 'Name', 'DOB'])
        elif instruction == "show_new_posts_from_followees_since_last_login":
            Util.getNewPostsFromFolloweesSinceLastLogin()
        elif instruction == "show_new_posts_from_topics_user_follows_since_last_login":
            Util.getNewPostsFromTopicsUserFollowsSinceLastLogin()
        elif instruction == "show_all_followers":
            followers = Util.getAllFollowers()
            Util.prettyPrint(followers, ['ID', 'Name'])
        elif instruction == "show_all_followees":
            followees = Util.getAllFollowees()
            Util.prettyPrint(followees, ['ID', 'Name'])
        elif instruction == "show_topics_user_follows":
            topics = Util.getTopicsCurrentUserFollows()
            Util.prettyPrint(topics, ['ID', 'Name'])
        elif instruction == "show_groups_user_joins":
            info = Util.getGroupsUserJoins()
            Util.prettyPrint(info, ['group ID', 'group name'])
        elif instruction == "show_posts_user_owns":
            info = Util.getPostsUserOwns()
            Util.prettyPrint(info, ['postID', 'content', 'created time', 'thumb number'])
        elif instruction == "make_new_post_with_topic":
            info = Util.getAllTopics()
            Util.prettyPrint(info, ['Topic ID', 'Topic Name'])
            Util.makeNewPostWithTopic()
        elif instruction == "thumb_up_post":
            info = Util.getAllPostsWithTopics()
            Util.prettyPrint(info, ['Post ID', 'Content', 'Created Time', 'Thumb Number', 'Topic Name'])
            Util.thumbUpPost()
        elif instruction == "thumb_down_post":
            info = Util.getAllPostsWithTopics()
            Util.prettyPrint(info, ['Post ID', 'Content', 'Created Time', 'Thumb Number', 'Topic Name'])
            Util.thumbDownPost()
        elif instruction == "reply_to_post":
            info = Util.getAllPostsWithTopics()
            Util.prettyPrint(info, ['Post ID', 'Content', 'Created Time', 'Thumb Number', 'Topic Name'])
            Util.replyToPost()
        elif instruction == "join_group":
            info = Util.getAllGroups()
            Util.prettyPrint(info, ['Group ID', 'Group Name'])
            Util.joinGroup()
        elif instruction == "create_group":
            info = Util.getAllUsers()
            Util.prettyPrint(info, ['User ID', 'User Name'])
            Util.createGroup()
        elif instruction == "follow_topic":
            info = Util.getAllTopics()
            Util.prettyPrint(info, ['Topic ID', 'Topic Name'])
            Util.followTopic()
        else:
            print("The instruction you provide cannot be recognized. Please try again.")