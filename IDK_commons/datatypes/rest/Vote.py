from IDK_commons import utils

class VoteRequest:
    def __init__(self,userId,parentId,type,scoreVal):
        self.userId = userId
        self.parentId =  parentId
        self.type = type
        self.scoreVal = scoreVal

class VoteResponse:
    def __init__(self,scoreVal):
        self.scoreVal = scoreVal