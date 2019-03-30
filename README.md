# Simple Social Network

This application resembles a simple social network written in Python with MySQL as the data storage solution. 
The user interface is command-line based and supports a list of instructions to emulate social interactions between users.

## Getting Started
### Prerequisites
- `Python3`
- `MySQL8.0`
- `mysql-connector-python`
- `python-tabulate`

### Installing
1. Install `Python3` by following this [article](https://realpython.com/installing-python/).

2. Make sure Python3 is installed by typing `python3 --version` in your terminal. 

3. Install `MySQL8.0` by following this [article](https://dev.mysql.com/doc/refman/8.0/en/installing.html).

4. Make sure Python3 is installed by typing `mysql --version` in your terminal. 

5. Install `mysql-connector-python` by typing `pip3 install mysql-connector-python`. Refer to this [guide](https://pynative.com/install-mysql-connector-python/) if the above command fails.

5. Install `tabulate` by typing `pip3 install tabulate`. Refer to this [guide](https://pypi.org/project/tabulate/) if the above command fails.

## Functionalities
- A person can initial a post on a topic.
- A person can join a group with another person.
- A person can follow a topic.
- A person can determine what posts have been added by people and/or topics that they are following since they last read from those people/topics.
- A person can respond to a post with thumbs up/down and/or a response post.

## Instruction Usage
- `show_current_user_info`: 
    - Prints out the ID, name and date of birth information of the current user.
    - Example output:
    ```
      ID  Name    Date of Birth    Last Login
       1  Alice   1988-01-01       2019-03-30 13:46:22
    ```

- `show_new_posts_from_followees_since_last_login`:
    - Prints out the information of new posts from people that current user follows since their last login.
    - Example output:
    ```
    User name      Post ID  Content    Created Time           Thumb Number    Topic ID  Topic Name
    Alice                1  qwer       2019-03-30 14:11:13               0           1  Dark souls
    Alice                2  asdf       2019-03-30 14:11:13               0           2  Civilization
    ```

- `show_new_posts_from_topics_user_follows_since_last_login`:
    - Prints out the information of new posts from topics that current user follows since their last login.
    - Example output:
    ```
      Post ID  Content    Created Time           Thumb Number    Topic ID  Topic Name
            1  qwer       2019-03-30 14:12:54               0           1  Dark souls
            3  zxcv       2019-03-30 14:12:54               0           1  Dark souls
            2  asdf       2019-03-30 14:12:54               0           2  Civilization
    ```


    
- `show_all_followers`:
    - Prints out IDs and names of all people that follow the current user.
    - Example output:
    ```
      ID  Name
       2  Bob
       3  Cindy
    ```
    
- `show_all_followees`:
    - Prints out IDs and names of all people that the current user follows.
    - Example output:
    ```
      ID  Name
       1  Alice
       3  Cindy
    ```
 
- `show_topics_user_follows`:
    - Prints out IDs and names of all topics that the current user follows.
    - Example output:
    ```
      ID  Name
       1  Dark souls
       2  Civilization
    ```

- `show_groups_user_joins`:
    - Prints out IDs and names of all groups that the current user follows.
    - Example output:
    ```
      group ID  group name
             1  Evil
             2  Goose
    ```
    
- `show_posts_user_owns`:
    - Prints out ID, content, timestamp and total number of thumbs of all posts created by the current user.
    - Example output:
    ```
      postID  content    created time           thumb number
           1  qwer       2019-03-30 13:46:22               0
           2  asdf       2019-03-30 13:46:22               0
    ```

- `make_new_post_with_topic`:
    - Takes two inputs: post content and topic name.
    - If the topic name does not exist, a new topic with this name will be created.
    - A new post with provided content will be created and assigned under a topic with the provided topic name.
    - User will be told whether actions have successed or actions are aborted due to invalid inputs from them.
    - Example output:
    ```
  Please enter your instruction:make_new_post_with_topic


  Topic ID  Topic Name
           1  Dark souls
           2  Civilization


  Please enter post content (text only): aloha
  Please enter the topic name associated with the current post:1
  A new topic named 1 is created successfully. ID = 3
  Post created successfully. ID = 4
    ```
    
- `thumb_up_post`:
    - Takes one input: post id.
    - User will see errors if the post id does not exist;
    - The number of thumb ups will increment by 1 provided that the id exists.
    - Example output:
    ```
    Please enter your instruction:thumb_up_post


  Post ID  Content    Created Time           Thumb Number  Topic Name
          1  qwer       2019-03-30 13:46:22               0  Dark souls
          3  zxcv       2019-03-30 13:46:22               0  Dark souls
          2  asdf       2019-03-30 13:46:22               0  Civilization
          4  aloha      2019-03-30 13:55:22               0  1


  what is the ID of the post you want to thumb up? 1
  thumb up added to the the post!
    ```
    
    
- `thumb_down_post`:
    - Takes one input: post id.
    - User will see errors if the post id does not exist;
    - The number of thumb ups will decrement by 1 provided that the id exists.
    - Example output:
    ```
  Please enter your instruction:thumb_down_post


  Post ID  Content    Created Time           Thumb Number  Topic Name
          1  qwer       2019-03-30 13:46:22               1  Dark souls
          3  zxcv       2019-03-30 13:46:22              -1  Dark souls
          5  mie        2019-03-30 14:00:58               0  Dark souls
          2  asdf       2019-03-30 13:46:22               0  Civilization
          4  aloha      2019-03-30 13:55:22               1  1


  what is the ID of the post you want to thumb down? 3
  thumb down added to the the post!
    ```
    
- `reply_to_post`:
    - Takes two inputs: post id and reply content.
    - User will see errors if the post id does not exist or the content is invalid.
    - A new post will be created successfully in the response to an existing post.
    - Example output:
    ```
    Please enter your instruction:reply_to_post


  Post ID  Content    Created Time           Thumb Number  Topic Name
          1  qwer       2019-03-30 13:46:22               1  Dark souls
          3  zxcv       2019-03-30 13:46:22              -1  Dark souls
          2  asdf       2019-03-30 13:46:22               0  Civilization
          4  aloha      2019-03-30 13:55:22               1  1


  what is the ID of the post you want to reply? 1
  what is the content to reply? mie
  A new post with content "mie" is created successfully. post ID = 5
  You have replied to post id 1 successfully!
    ```
    
- `join_group`:
    - Takes one input: group id
    - User will see errors if the group id does not exist.
    - User will join the group successully if the group id is valid.
    - Example output:
    ```
    Please enter your instruction:join_group


  Group ID  Group Name
           1  Evil
           2  Goose
           3  jaksldfjla


  Please enter the id of the group that you would like to join:3
  You've joined group 3 successfully.
    ```
    
- `create_group`:
    - Takes two inputs: group name, id of another user that's been invited
    - User will see errors if the user id does not exist or group name is invalid.
    - User and their friend will join the new group successully if both arguments are valid.
    - Example output:
    ```
    Please enter your instruction:create_group


  User ID  User Name
          1  Alice
          2  Bob
          3  Cindy


  Please enter the name of the new group:jaksldfjla
  Please enter the ID of another user that you'd like to join the new group with:3
  A new group named jaksldfjla is created successfully. ID = 3
  You and user 3 have joined group 3.
    ```
    
- `follow_topic`:
    - Takes one input: topic id.
    - User will see errors if the topic id does not exist.
    - User will follow the topic successully if the argument is valid.
    - Example output:
    ```
    Please enter your instruction:follow_topic


  Topic ID  Topic Name
           1  Dark souls
           2  Civilization
           3  1


  Please enter the id of the topic that you would like to follow:1
  You've followed topic 1 successfully.
    ```
   
