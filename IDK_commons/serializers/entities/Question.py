from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer
from IDK_commons.serializers.entities.Comment import CommentSerializer
from IDK_commons.serializers.entities.Answer import AnswerSerializer
import datetime

class QuestionSerializer(commonserializer.CommonSerializer):
    questionId = serializers.IntegerField(default = -1)
    owner = serializers.IntegerField()
    title = serializers.CharField(max_length = 100)
    body  = serializers.CharField(max_length=2000)
    creationTime = serializers.DateTimeField(default = datetime.datetime.now())
    modificationTime = serializers.DateTimeField(default = datetime.datetime.now())
    score_val = serializers.IntegerField(default = 0)
    reputationThreshold = serializers.IntegerField(default = 0)
    answers = serializers.ListField(child =AnswerSerializer() , default = [])
    comments  = serializers.ListField(child=CommentSerializer(), default = [])