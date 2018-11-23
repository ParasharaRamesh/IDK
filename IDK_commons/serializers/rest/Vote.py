from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer


class VoteRequestSerializer(commonserializer.CommonSerializer):
    userId = serializers.IntegerField()
    #dont give one of it or specify as empty check it out!!
    parentId = serializers.IntegerField()
    type = serializers.CharField()#question/answer
    scoreVal = serializers.IntegerField()

class VoteResponseSerializer(commonserializer.CommonSerializer):
    scoreVal = serializers.IntegerField()