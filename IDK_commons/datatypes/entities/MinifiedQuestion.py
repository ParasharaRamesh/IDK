from enum import Enum
from IDK_commons import utils

class MinifiedQuestion:
    def __init__(self,questionId,title,body,owner,tags,score,numanswers):
        self.questionId = questionId
        self.title = title
        self.body = body
        self.owner = owner
        self.tags = tags
        self.score = score
        self.numanswers = numanswers