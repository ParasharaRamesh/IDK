from IDK_commons import utils
from IDK_commons.datatypes.entities.User import IDKUser

#user details API
class GetUserDetailsRequest:
    def __init__(self,userId):
        self.userId = userId

class GetUserDetailsResponse:
    def __init__(self, idkuser):
        utils.objTypeCheck(idkuser ,IDKUser, "idkuser")
        self.idkuser = idkuser


#follow API
class FollowRequest:
    def __init__(self,user1,user2):
        self.user1 = user1
        self.user2 = user2

class FollowResponse:
    def __init__(self,status):
        self.status = status

#unfollow API
class UnfollowRequest:
    def __init__(self,user1,user2):
        self.user1 = user1
        self.user2 = user2

class UnfollowResponse:
    def __init__(self,status):
        self.status = status

