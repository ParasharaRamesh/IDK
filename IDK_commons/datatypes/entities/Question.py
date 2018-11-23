from enum import Enum
from IDK_commons import utils
from IDK_commons.datatypes.entities.Comment import Comment
from IDK_commons.datatypes.entities.Answer import Answer

class Question:
    def __init__(self,owner,title,body,creationTime,modificationTime,answers,comments,reputationThreshold=0,score_val=0,questionId = None):
        self.questionId = questionId
        self.owner = owner#id
        self.title = title# title string
        self.body = body#body string
        self.creationTime = creationTime#time
        self.modificationTime = modificationTime#time
        self.score_val = score_val#integer
        self.reputationThreshold = reputationThreshold#int representing the minimum reputation needed to answer this question
        self.answers = answers#list of all answer datatypes
        self.comments = comments#list of all comment datatypes

