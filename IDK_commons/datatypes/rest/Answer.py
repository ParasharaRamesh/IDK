from IDK_commons.datatypes.entities.Answer import Answer
from IDK_commons import utils


#add question API
class AddAnswerRequest:
    def __init__(self,**kwargs):
        self.answer = Answer(**kwargs)

class AddAnswerResponse:
    def __init__(self,status,answerId):
        self.status = status
        self.answerId = answerId#will be set only if the status is success

# delete Question API
class DeleteAnswerRequest:
    def __init__(self,answerId):
        self.answerId = answerId

class DeleteAnswerResponse:
    def __init__(self,status):
        self.status = status

# get Question  API
class GetAnswerRequest:
    def __init__(self,answerId):
        self.answerId = answerId

class GetAnswerResponse:
    def __init__(self,answer):
        utils.objTypeCheck(answer,Answer,"answer")
        self.answer = answer