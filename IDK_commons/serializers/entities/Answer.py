from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer
from IDK_commons.serializers.entities.Comment import CommentSerializer
import datetime

class AnswerSerializer(commonserializer.CommonSerializer):
    answerId = serializers.IntegerField(default = -1)
    parentId = serializers.IntegerField()
    owner = serializers.IntegerField()
    body  = serializers.CharField(max_length=2000)
    creationTime = serializers.DateTimeField(default = datetime.datetime.now())
    modificationTime = serializers.DateTimeField(default = datetime.datetime.now())
    score_val = serializers.IntegerField(default = 0)
    comments  = serializers.ListField(child=CommentSerializer(),default = [])