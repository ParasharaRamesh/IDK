from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer
from IDK_commons.serializers.entities.Comment import CommentSerializer
from IDK_commons.serializers.entities.Answer import AnswerSerializer
from IDK_commons.serializers.entities.Question import QuestionSerializer


class StringListField(serializers.ListField):
    child = serializers.CharField()

class FollowListField(serializers.ListField):
    userId = serializers.IntegerField()
    username = serializers.CharField()


class IDKUserSerializer(commonserializer.CommonSerializer):
    #negativeid as a hack
    userId = serializers.IntegerField(default = -1)
    username = serializers.CharField(max_length = 40)
    questions = serializers.ListField(child = QuestionSerializer(),default = [])
    comments  = serializers.ListField(child = CommentSerializer(),default = [])
    answers  = serializers.ListField(child = AnswerSerializer(),default = [])
    tags  = StringListField()
    givenVotes = serializers.IntegerField()
    receivedVotes = serializers.IntegerField()
    unreadNotifications = serializers.IntegerField()
    reputation = serializers.IntegerField()
    followers = FollowListField()
    following = FollowListField()

    