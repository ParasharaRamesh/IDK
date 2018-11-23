from enum import Enum
from IDK_commons import utils

class IDKUser:
    def __init__(self,username,questions,answers,comments,tags,givenVotes,receivedVotes,unreadNotifications,reputation, followers, following, userId = None):
        self.userId = userId
        self.username = username
        self.questions = questions #list of questionDT's
        self.answers = answers #list of answerDT's
        self.comments = comments #list of commentDT's
        self.tags = tags # list of tag names from db
        self.givenVotes = givenVotes # the number of upvotes
        self.receivedVotes = receivedVotes #the number of downvotes
        self.unreadNotifications = unreadNotifications#the number of unreadnotifications for this user in the DB
        self.reputation = reputation# a computed value => f(q,a,c,v,t,u,d,un)
        self.followers = followers# a list of all the user ids who are the followers for this user
        self.following = following# a list of all user ids who this user is following