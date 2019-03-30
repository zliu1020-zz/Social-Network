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

- `show_new_posts_from_followees_since_last_login`:
    - Prints out the information of new posts from people that current user follows since their last login.
    - Example output:

- `show_new_posts_from_topics_user_follows_since_last_login`:
    - Prints out the information of new posts from topics that current user follows since their last login.
    - Example output:
    
- `show_all_followers`:
    - Prints out IDs and names of all people that follow the current user.
    - Example output:
    
- `show_all_followees`:
    - Prints out IDs and names of all people that the current user follows.
    - Example output:
 
- `show_topics_user_follows`:
    - Prints out IDs and names of all topics that the current user follows.
    - Example output:

- `show_groups_user_joins`:
    - Prints out IDs and names of all groups that the current user follows.
    - Example output:
    
- `show_posts_user_owns`:
    - Prints out ID, content, timestamp and total number of thumbs of all posts created by the current user.
    - Example output:

- `make_new_post_with_topic`:
    - Takes two inputs: post content and topic name.
    - If the topic name does not exist, a new topic with this name will be created.
    - A new post with provided content will be created and assigned under a topic with the provided topic name.
    - User will be told whether actions have successed or actions are aborted due to invalid inputs from them.
    - Example output:
    
- `thumb_up_post`:
    - Takes one input: post id.
    - User will see errors if the post id does not exist;
    - The number of thumb ups will increment by 1 provided that the id exists.
    
    
- `thumb_down_post`:
    - Takes one input: post id.
    - User will see errors if the post id does not exist;
    - The number of thumb ups will decrement by 1 provided that the id exists.
    - Example output:
    
- `reply_to_post`:
    - Takes two inputs: post id and reply content.
    - User will see errors if the post id does not exist or the content is invalid.
    - A new post will be created successfully in the response to an existing post.
    - Example output:
    
- `join_group`:
    - Takes one input: group id
    - User will see errors if the group id does not exist.
    - User will join the group successully if the group id is valid.
    - Example output:
    
- `create_group`:
    - Takes two inputs: group name, id of another user that's been invited
    - User will see errors if the user id does not exist or group name is invalid.
    - User and their friend will join the new group successully if both arguments are valid.
    - Example output:
    
- `follow_topic`:
    - Takes one input: topic id.
    - User will see errors if the topic id does not exist.
    - User will follow the topic successully if the argument is valid.
    - Example output:
   
