from IDK_commons import utils

class FeedRequest:
    def __init__(self,userId):
        self.userId = userId

class FeedResponse:
    def __init__(self,featured,unanswered):
        self.featured = featured
        self.unanswered = unanswered