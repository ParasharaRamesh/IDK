from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer
from IDK_commons.serializers.entities.MinifiedQuestion import MinQuestionSerializer


class FeedRequestSerializer(commonserializer.CommonSerializer):
    userId = serializers.IntegerField()

class FeedResponseSerializer(commonserializer.CommonSerializer):
    featured = serializers.ListField(child = MinQuestionSerializer(),default = [])
    unanswered = serializers.ListField(child = MinQuestionSerializer(),default = [])