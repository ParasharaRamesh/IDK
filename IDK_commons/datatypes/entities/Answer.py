from enum import Enum
from IDK_commons import utils
from IDK_commons.datatypes.entities.Comment import Comment

class Answer:
    def __init__(self,owner,body,creationTime,modificationTime,score_val,comments,parentId,answerId=None):
        self.answerId = answerId
        self.parentId = parentId
        self.owner = owner#id
        self.body = body#body string
        self.creationTime = creationTime#time
        self.modificationTime = modificationTime#time
        self.score_val = score_val#integer
        self.comments = comments#list of all comment datatypes
