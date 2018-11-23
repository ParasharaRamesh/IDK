from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer

class StringListField(serializers.ListField):
    child = serializers.CharField()

class MinQuestionSerializer(commonserializer.CommonSerializer):
    questionId = serializers.IntegerField()
    title = serializers.CharField()
    body = serializers.CharField()
    owner = serializers.IntegerField()
    tags  = StringListField()
    score = serializers.IntegerField()
    numanswers = serializers.IntegerField()
