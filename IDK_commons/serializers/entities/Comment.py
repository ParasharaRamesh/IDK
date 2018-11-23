from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer
import datetime

class CommentSerializer(commonserializer.CommonSerializer):
    commentId = serializers.IntegerField(default = -1)
    owner = serializers.IntegerField()
    body  = serializers.CharField(max_length=2000)
    creationTime = serializers.DateTimeField(default = datetime.datetime.now())
    modificationTime = serializers.DateTimeField(default = datetime.datetime.now())
    notifiedUser = serializers.CharField(default = "null")#this is for saying no notified user