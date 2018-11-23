from IDK_commons.datatypes.entities.Question import Question
from IDK_commons import utils


#add question API
class AddQuestionRequest:
    def __init__(self,**kwargs):
        self.question = Question(**kwargs)

class AddQuestionResponse:
    def __init__(self,status,questionId):
        self.status = status
        self.questionId = questionId#will be set only if the status is success

# delete Question API
class DeleteQuestionRequest:
    def __init__(self,questionId):
        self.questionId = questionId

class DeleteQuestionResponse:
    def __init__(self,status):
        self.status = status

# get Question  API
class GetQuestionRequest:
    def __init__(self,questionId):
        self.questionId = questionId

class GetQuestionResponse:
    def __init__(self,question):
        utils.objTypeCheck(question,Question,"question")
        self.question = question

#getSimilarQuestion API
class GetSimilarQuestionsResponse:
    def __init__(self,minifiedQuestions):
        self.minifiedQuestions= minifiedQuestions

class GetSimilarQuestionsRequest:
    def __init__(self,questionId):
        self.questionId = questionId
