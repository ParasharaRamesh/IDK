from IDK_commons.datatypes.entities.Comment import Comment
from IDK_commons import utils


#add comment API
class AddCommentRequest:
    def __init__(self,comment,parentId,parentType,type):
        utils.objTypeCheck(comment,Comment,"comment")
        self.comment = comment
        self.parentId = parentId
        self.parentType = parentType
        self.type = type

class AddCommentResponse:
    def __init__(self,status,commentId,parentId,parentType,collapsestatus,notificationId = None):
        self.status = status
        self.commentId = commentId
        self.notificationId = notificationId
        self.parentId = parentId
        self.parentType = parentType
        self.collapsestatus = collapsestatus

# delete comment API
class DeleteCommentRequest:
    def __init__(self,commentId):
        self.commentId = commentId

class DeleteCommentResponse:
    def __init__(self,status):
        self.status = status

# delete notification API
class DeleteNotificationRequest:
    def __init__(self,notificationId):
        self.notificationId = notificationId

class DeleteNotificationResponse:
    def __init__(self,status):
        self.status = status

# get notification API
class GetNotificationRequest:
    def __init__(self,notificationId):
        self.notificationId = notificationId

class GetNotificationResponse:
    def __init__(self,status,commentId,user1,user2,questionId,answerId):
        self.status = status
        self.commentId = commentId
        self.user1 = user1
        self.user2 = user2
        self.questionId = questionId
        self.answerId = answerId

# get comment  API
class GetCommentRequest:
    def __init__(self,commentId):
        self.commentId = commentId

class GetCommentResponse:
    def __init__(self,comment):
        utils.objTypeCheck(comment,Comment,"comment")
        self.comment = comment