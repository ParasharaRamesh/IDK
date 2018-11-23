from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer
from IDK_commons.serializers.entities.MinifiedQuestion import MinQuestionSerializer


class SearchRequestSerializer(commonserializer.CommonSerializer):
    searchquery = serializers.CharField() 
    searchtype = serializers.CharField()

class SearchResponseSerializer(commonserializer.CommonSerializer):
    minifiedQuestions = serializers.ListField(child = MinQuestionSerializer(),default = [])