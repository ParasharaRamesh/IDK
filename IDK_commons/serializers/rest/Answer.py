from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer
from IDK_commons.serializers.entities.Answer import AnswerSerializer
from IDK_commons.datatypes.entities.Answer import Answer

#add question request,response
class AddAnswerRequestSerializer(commonserializer.CommonSerializer):
    answer = AnswerSerializer()

class AddAnswerResponseSerializer(commonserializer.CommonSerializer):
    status = serializers.CharField()
    answerId = serializers.IntegerField()

#delete question request,response
class DeleteAnswerRequestSerializer(commonserializer.CommonSerializer):
    answerId = serializers.IntegerField()

class DeleteAnswerResponseSerializer(commonserializer.CommonSerializer):
    status = serializers.CharField()


#get question request,response
class GetAnswerRequestSerializer(commonserializer.CommonSerializer):
    answerId = serializers.IntegerField()

class GetAnswerResponseSerializer(commonserializer.CommonSerializer):
    answer = AnswerSerializer()