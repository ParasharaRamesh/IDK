from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer
from IDK_commons.serializers.entities.Question import QuestionSerializer
from IDK_commons.datatypes.entities.Question import Question
from IDK_commons.serializers.entities.MinifiedQuestion import MinQuestionSerializer

#add question request,response
class AddQuestionRequestSerializer(commonserializer.CommonSerializer):
    question = QuestionSerializer()

class AddQuestionResponseSerializer(commonserializer.CommonSerializer):
    status = serializers.CharField()
    questionId = serializers.IntegerField()

#delete question request,response
class DeleteQuestionRequestSerializer(commonserializer.CommonSerializer):
    questionId = serializers.IntegerField()

class DeleteQuestionResponseSerializer(commonserializer.CommonSerializer):
    status = serializers.CharField()


#get question request,response
class GetQuestionRequestSerializer(commonserializer.CommonSerializer):
    questionId = serializers.IntegerField()

class GetQuestionResponseSerializer(commonserializer.CommonSerializer):
    question = QuestionSerializer()

class GetSimilarQuestionsRequestSerializer(commonserializer.CommonSerializer):
    questionId = serializers.IntegerField()

class GetSimilarQuestionsResponseSerializer(commonserializer.CommonSerializer):
    minifiedQuestions = serializers.ListField(child = MinQuestionSerializer() , default = [])