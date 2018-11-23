from enum import Enum
from IDK_commons import utils

class Comment:
    def __init__(self,owner,body,creationTime,modificationTime,notifiedUser=None,commentId=None):
        self.commentId = commentId
        self.owner = owner#user id
        self.body = body#body string
        self.creationTime = creationTime#time
        self.modificationTime = modificationTime#time
        self.notifiedUser = notifiedUser#user_name if user is tagged notification
    
