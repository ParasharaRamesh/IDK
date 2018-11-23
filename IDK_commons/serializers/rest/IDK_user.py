from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer
from IDK_commons.serializers.entities.User import IDKUserSerializer

#user details api
class GetUserDetailsRequestSerializer(commonserializer.CommonSerializer):
    userId = serializers.IntegerField()

class GetUserDetailsResponseSerializer(commonserializer.CommonSerializer):
    idkuser = IDKUserSerializer()

#follow API
class FollowRequestSerializer(commonserializer.CommonSerializer):
    user1 = serializers.IntegerField()
    user2 = serializers.IntegerField()

class FollowResponseSerializer(commonserializer.CommonSerializer):
    status = serializers.CharField()

#unfollow API
class UnfollowRequestSerializer(commonserializer.CommonSerializer):
    user1 = serializers.IntegerField()
    user2 = serializers.IntegerField()

class UnfollowResponseSerializer(commonserializer.CommonSerializer):
    status = serializers.CharField()