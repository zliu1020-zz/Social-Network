import mysql.connector
import time
from tabulate import tabulate
from datetime import datetime

### Global var - the name of the current user
USERNAME = ""
### Global var - the id of the current user
ID = -1
### Global var - the timestamp of which the current user logs in
TIMESTAMP = 0


class DatabaseConnector:
    def __init__(self):
        ### Connect to your local DB server, by default auto_commit is OFF
        ### Replace the following information with the data of your own MySQL instance
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="lzy971020"
        )
        self.cursor = self.db.cursor()

    ### Run a query and return all matching results
    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    ### Execute a statement and return False/True depending on if the mutation succeeds
    def execute(self, sql, val=None):
        self.cursor.execute(sql, val or ())
        self.db.commit()

        if self.cursor.rowcount == 0:
            return False
        else:
            return True

    ### Roll back current transaction
    def rollback(self):
        self.db.rollback()

    ### Commit current transaction
    def commit(self):
        self.db.commit()

    ### Execute a statement without committing
    ### Return False/True depending on if the mutation succeeds
    def executeWithoutCommitting(self, sql, val=None):
        self.cursor.execute(sql, val or ())

        if self.cursor.rowcount == 0:
            return False
        else:
            return True

    ### Execute a MySQL script
    ### Used for db initial setup
    def runScript(self, path):
        file = open(path, 'r')
        sqlStatements = file.read()
        file.close()

        for statement in sqlStatements.split(';'):
            try:
                self.execute(statement)
            except OperationalError:
                print("Error found when executing sql statement: ", statement , " Skipping.")

    ### get the auto_increment ID from database
    def getLastInsertionID(self):
        return self.cursor.lastrowid

    ### Clean up and close database connection
    def closeConnection(self):
        self.db.close()
        self.cursor.close()

### Global var - the database connection
DBConnector = DatabaseConnector()

class Util:

    ### called when the application starts up
    @staticmethod
    def login():
        ### Collect user name and ID from the input prompt
        userName = input("what is your user name? ")
        userID = input("what is your ID? ")
        searchQuery = "select * from NetworkUser where name = '" + userName + "' and uID = " + userID + ";"

        ### Check if such user exists
        result = DBConnector.query(searchQuery)

        if result:
            ### if the user exists, rewrites what's stored in memory
            global ID
            ID = result[0][0]
            global USERNAME
            USERNAME = result[0][1]
            global TIMESTAMP
            TIMESTAMP = time.time()

            ### Print welcome message
            print("Hello, " + USERNAME + "!\n")
            return True

        else:
            ### Failed to log in if the user credentials are falsy
            print("You are not present in our database, please try again")
            return False

    ### Prints out the ID, name and date of birth information of the current user.
    @staticmethod
    def getCurrentUserInformation():
        sql = "select * from NetworkUser WHERE uid = %i" % ID
        result = DBConnector.query(sql)
        return result

    ### get the information of new posts from people that current user follows since their last login.
    @staticmethod
    def getNewPostsFromFolloweesSinceLastLogin():
        lastLoginResult = Util.getCurrentUserLastLoginTime()
        lastLogin = lastLoginResult[0][0]
        sql_query = "select NetworkUser.name,pID, content, ts, thumbNum, tID, Topic.name from Post inner " \
                    "join ((select followeeID from UsersFollowUsers where followerID = %i) as followees " \
                    "inner join UsersOwnPosts on (userID = followees.followeeID))on (Post.pID = postID ) inner join " \
                    "PostsBelongToTopics on(Post.pID = PostsBelongToTopics.postID) inner join Topic on(topicID = tID) " \
                    "inner join NetworkUser on (followees.followeeID = NetworkUser.uID);" %ID
        posts = DBConnector.query(sql_query)
        new_posts = []
        for post in posts:
            if post[3] >= lastLogin:
                new_posts.append(post)
        return new_posts

    ### get the information of new posts from topics that current user follows since their last login.
    @staticmethod
    def getNewPostsFromTopicsUserFollowsSinceLastLogin():
        lastLoginResult = Util.getCurrentUserLastLoginTime()
        lastLogin = lastLoginResult[0][0]
        sql_query = "select Post.pID, Post.content, Post.ts, Post.thumbNum, Topic.tID, Topic.name from Post " \
                    "inner join ((select topicID from UsersFollowTopics where userID = %i) as topics " \
                    "inner join PostsBelongToTopics on (PostsBelongToTopics.topicID = topics.topicID))" \
                    "on (Post.pID = postID) inner join Topic on (PostsBelongToTopics.topicID = Topic.tID);"%ID
        posts = DBConnector.query(sql_query)
        new_posts = []
        for post in posts:
            if post[2] >= lastLogin:
                new_posts.append(post)
        return new_posts

    ### get a list of people that follow the current user
    @staticmethod
    def getAllFollowers():
        sql = "select UsersFollowUsers.followerID as followerID,\
         (select name from NetworkUser where uID = followerID) as followerName\
         from NetworkUser inner join UsersFollowUsers on NetworkUser.uID = UsersFollowUsers.followeeID\
         where uID = %i" % ID
        result = DBConnector.query(sql)
        return result

    ### get a list of people that the current user follows
    @staticmethod
    def getAllFollowees():
        sql = "select UsersFollowUsers.followeeID,\
         (select name from NetworkUser where NetworkUser.uID = UsersFollowUsers.followeeID) as followeeName\
          from UsersFollowUsers inner join NetworkUser\
           on UsersFollowUsers.followerID = NetworkUser.uID where followerID = %i" % ID
        result = DBConnector.query(sql)
        return result

    ### get a list of topics that the current user follows
    @staticmethod
    def getTopicsCurrentUserFollows():
            sql = "select Topic.tID, Topic.name from Topic \
                    inner join UsersFollowTopics as U \
                        on Topic.tID = U.topicID and U.userID = " + str(ID) +";"
            result = DBConnector.query(sql)
            return result

    ### get a list of groups that the current user joins
    @staticmethod
    def getGroupsUserJoins():
        sql = "select UsersBelongToGroups.groupID, SocialGroup.name from UsersBelongToGroups\
         inner join SocialGroup on UsersBelongToGroups.groupID = SocialGroup.gID\
          where userID = %i" % ID
        result = DBConnector.query(sql)
        return result

    ### get a list of posts written by the current user
    @staticmethod
    def getPostsUserOwns():
        sql = "select postID, content, ts, thumbNum from UsersOwnPosts\
         inner join Post on UsersOwnPosts.postID = Post.pID where userID = %i" % ID
        result = DBConnector.query(sql)
        return result

    ### Create a new post with a topic
    @staticmethod
    def makeNewPostWithTopic():

        ### Collect post content and topic name from input prompt
        ### Exit immediately upon invalid inputs
        content = input("Please enter post content (text only):")
        topicName = input("Please enter the topic name associated with the current post:")
        if (not content) or (not topicName):
            print("Input is invalid. Please try again.")
            return False
        else:
            ### Check if a topic with provided name exists
            ### Create a new topic if it does not exist
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

            ### Insert into Post, UsersOwnPosts and PostsBelongToTopics
            ### Roll back immediately if any of them failed
            ### commit the transaction if all of them succeeds
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

    ### Takes one input: post id.
    ### User will see errors if the post id does not exist;
    ### The number of thumb ups will increment by 1 provided that the id exists.
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

    ### Takes one input: post id.
    ### User will see errors if the post id does not exist;
    ### The number of thumb ups will decrement by 1 provided that the id exists.
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
                print("thumb down added to the the post!")
                return True
            else:
                DBConnector.rollback()
                print("something wrong happened to the machine, please try again!")
                return False
        except mysql.connector.Error as err:
            DBConnector.rollback()
            print("Encountered issues when inserting into database. Transaction aborted. Message: ", err.msg)
            return False

    ### Takes two inputs: post id and reply content.
    ### User will see errors if the post id does not exist or the content is invalid.
    ### A new post will be created successfully in the response to an existing post.
    @staticmethod
    def replyToPost():
        ### Collect post content and ID from input prompt
        ### Exit immediately upon invalid inputs
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
            ### Insert into Post, UsersOwnPosts, PostsRespondToPosts and PostsBelongToTopics
            ### Roll back immediately if any of them failed
            ### commit the transaction if all of them succeed
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

    ### Takes one input: group id
    ### User will see errors if the group id does not exist.
    ### User will join the group successully if the group id is valid.
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

    ### Takes two inputs: group name, id of another user that's been invited
    ### User will see errors if the user id does not exist or group name is invalid.
    ### User and their friend will join the new group successully if both arguments are valid.
    @staticmethod
    def createGroup():
        ### Collect groupName and friendID from input prompt
        ### Exit immediately upon invalid inputs
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
            ### Insert into SocialGroup and UsersBelongToGroups
            ### Roll back immediately if any of them failed
            ### commit the transaction if both of them succeed
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

    ### Takes one input: topic id.
    ### User will see errors if the topic id does not exist.
    ### User will follow the topic successully if the argument is valid.
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

    ### get all existing users in the database
    @staticmethod
    def getAllUsers():
        sql  = "select uID, name from NetworkUser;"
        result = DBConnector.query(sql)
        return result

    ### get all existing groups in the database
    @staticmethod
    def getAllGroups():
        sql  = "select gID, name from SocialGroup;"
        result = DBConnector.query(sql)
        return result

    ### get all posts with topics in the database
    @staticmethod
    def getAllPostsWithTopics():
        sql  = "select pID, content, ts, thumbNum, name from Post inner join PostsBelongToTopics on(Post.pId = PostsBelongToTopics.postID) inner join Topic on(topicID = tID);"
        result = DBConnector.query(sql)
        return result

    ### get all topics in the database
    @staticmethod
    def getAllTopics():
        sql  = "select tID, name from Topic;"
        result = DBConnector.query(sql)
        return result

    ### get the last time at which the current user logged in
    @staticmethod
    def getCurrentUserLastLoginTime():
        sql = "select lastLogin from NetworkUser where uId = %i;" % ID
        result = DBConnector.query(sql)
        return result

    ### called upon application exiting
    @staticmethod
    def logout():
        global USERNAME
        global ID
        global TIMESTAMP

        ### Write the timestamp at which the user logged in this time as "LastLogin" into database
        dt_obj = datetime.fromtimestamp(TIMESTAMP)
        date_time = dt_obj.strftime("%Y-%m-%d %H:%M:%S")

        sql = "update NetworkUser set lastLogin = '" + date_time + "' where uID = " + str(ID)
        try:
            result = DBConnector.execute(sql)
            if not result:
                DBConnector.rollback()
                print("Logout failed due to internal error. Try again.")
                return False
            else:
                ### Clear global variables and exit
                DBConnector.commit()
                USERNAME = ""
                ID = -1
                TIMESTAMP = 0
                print("You've logged out. Bye.")
                return True
        except mysql.connector.Error as err:
            DBConnector.rollback()
            print("Encountered issues when inserting into database. Transaction aborted. Message: ", err.msg)
            return False

    ### called upon application startup
    @staticmethod
    def setupDatabse():
        ### run the script if no db named "SocialNetwork" exists
        sql = "show databases like 'SocialNetwork'"
        result = DBConnector.query(sql)
        if not result:
            DBConnector.runScript("./createTable.sql")
            print("Finished initializing database.")
        else:
            DBConnector.execute("use SocialNetwork;")
            print("Use existing database SocialNetwork.")

    ### Print a list of instructions supported by this application
    @staticmethod
    def printInstructions():
        print("***********************************************")
        print("A list of instructions supported by this tool:\n")
        print("show_instructions: display the aviable instruction for this program\n")
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

    ### Keep making the user log in until they succeed
    @staticmethod
    def continuousLogin():
        success = Util.login()
        if not success:
            while True:
                success = Util.login()
                if success:
                    break

    ### Display the output in tabular format
    @staticmethod
    def prettyPrint(content, header):
        print("\n")
        print(tabulate(content, headers=header))
        print("\n")


class Main:
    ### Initial setup
    Util.setupDatabse()
    Util.continuousLogin()
    Util.printInstructions()

    ### Keep asking instruction from the user until they logs out
    while True:
        instruction = input("Please enter your instruction:")

        if instruction == "logout":
            Util.logout()
            DBConnector.closeConnection()
            break

        if instruction == "show_current_user_info":
            info = Util.getCurrentUserInformation()
            Util.prettyPrint(info, ['ID', 'Name', 'Date of Birth', 'Last Login'])
        elif instruction == "show_instructions":
            Util.printInstructions()
        elif instruction == "show_new_posts_from_followees_since_last_login":
            info = Util.getNewPostsFromFolloweesSinceLastLogin()
            Util.prettyPrint(info, ['User name','Post ID', 'Content', 'Created Time', 'Thumb Number', 'Topic ID', 'Topic Name'])
        elif instruction == "show_new_posts_from_topics_user_follows_since_last_login":
            info = Util.getNewPostsFromTopicsUserFollowsSinceLastLogin()
            Util.prettyPrint(info, ['Post ID', 'Content', 'Created Time', 'Thumb Number', 'Topic ID', 'Topic Name'])
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