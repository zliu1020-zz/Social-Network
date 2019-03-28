-- Project: Social Network
drop database if exists SocialNetwork;
create database SocialNetwork;
use SocialNetwork;

drop table if exists NetworkUser;
drop table if exists SocialGroup;
drop table if exists Post;
drop table if exists Topic;
drop table if exists UsersFollowUsers;
drop table if exists UsersFollowTopics;
drop table if exists UsersBelongToGroups;
drop table if exists UsersOwnPosts;
drop table if exists PostsBelongToTopics;
drop table if exists PostsRespondToPosts;

create table NetworkUser(
    uID int(10) auto_increment,
    name varchar(20),
    DOB date,
    primary key pk_networkuser(uID)
);
alter table NetworkUser auto_increment = 1;
insert into NetworkUser values (NULL, "Alice", "1988-01-01"),
(NULL, "Bob", "1999-12-12"),
(NULL, "Cindy", "1963-11-11");

create table SocialGroup (
    gID int(10) auto_increment,
    name varchar(20),
    primary key pk_socialgroup(gID)
);
alter table SocialGroup auto_increment = 1;
insert into SocialGroup values(NULL, "Evil"), (NULL, "Goose");

create table Post (
    pID int(10) auto_increment,
    content varchar(200),
    ts timestamp,
    thumbNum int(10) default 0,
    primary key pk_post(pID)
);
alter table Post auto_increment = 1;
insert into Post values
(NULL, "qwer", current_timestamp(), default), 
(NULL, "asdf", current_timestamp(), default), 
(NULL, "zxcv", current_timestamp(), default);

create table Topic (
    tID int(10) auto_increment,
    name varchar(20),
    primary key pk_topic(tID)
);
alter table Topic auto_increment = 1;
insert into Topic values(NULL, "Dark souls"), (NULL, "Civilization");

create table UsersFollowUsers (
    followeeID int(10),
    followerID int(10),
    primary key pk_usersfollowusers(followeeID, followerID),
    constraint fk_followeeid foreign key (followeeID) references NetworkUser(uID),
    constraint fk_followerid foreign key (followerID) references NetworkUser(uID)
);
insert into UsersFollowUsers values(1, 3), (1,2), (3, 2);

create table UsersFollowTopics (
    userID int(10),
    topicID int(10),
    primary key pk_usersfollowtopics(userID, topicID),
    constraint fk_userid foreign key (userID) references NetworkUser(uID),
    constraint fk_topicid foreign key (topicID) references Topic(tID)
);
insert into UsersFollowTopics values(1, 1), (1, 2);

create table UsersBelongToGroups (
    userID int(10),
    groupID int(10),
    primary key pk_usersbelongtogroups(userID, groupID),
    constraint fk_userid_2 foreign key (userID) references NetworkUser(uID),
    constraint fk_groupid foreign key (groupID) references SocialGroup(gID)
);
insert into UsersBelongToGroups values(1, 1), (3,1), (1, 2), (2, 2);

create table UsersOwnPosts (
    userID int(10),
    postID int(10),
    primary key pk_usersownposts(userID, postID),
    constraint fk_userid_3 foreign key (userID) references NetworkUser(uID),
    constraint fk_postid foreign key (postID) references Post(pID) 
);
insert into UsersOwnPosts values(1, 1), (1, 2), (2, 3);

create table PostsBelongToTopics (
    postID int(10),
    topicID int(10),
    primary key pk_postsbelongtotopics(postID, topicID),
    constraint fk_postid_2 foreign key (postID) references Post(pID),
    constraint fk_topicid_2 foreign key (topicID) references Topic(tID)
);
insert into PostsBelongToTopics values(1, 1), (3, 1), (2, 2);

create table PostsRespondToPosts (
    respondedPostID int(10),
    respondingPostID int(10),
    primary key pk_postrespondtoposts(respondedPostID, respondingPostID),
    constraint fk_respondedpostiD foreign key (respondedPostID) references Post(pID),
    constraint fk_respondingpostiD foreign key (respondingPostID) references Post(pID)
);
insert into PostsRespondToPosts values(1, 3);