from rest_framework import serializers
from IDK_commons import utils
from IDK_commons.serializers import commonserializer
from IDK_commons.serializers.entities.Comment import CommentSerializer
from IDK_commons.datatypes.entities.Comment import Comment

#add question request,response
class AddCommentRequestSerializer(commonserializer.CommonSerializer):
    comment = CommentSerializer()
    parentId = serializers.IntegerField()
    parentType = serializers.CharField()
    type = serializers.CharField()

class AddCommentResponseSerializer(commonserializer.CommonSerializer):
    status = serializers.CharField()
    commentId = serializers.IntegerField()
    notificationId = serializers.IntegerField()
    parentId = serializers.IntegerField()
    parentType = serializers.CharField()
    collapsestatus = serializers.CharField()

#delete question API
class DeleteCommentRequestSerializer(commonserializer.CommonSerializer):
    commentId = serializers.IntegerField()

class DeleteCommentResponseSerializer(commonserializer.CommonSerializer):
    status = serializers.CharField()

#get comment API
class GetCommentRequestSerializer(commonserializer.CommonSerializer):
    commentId = serializers.IntegerField()

class GetCommentResponseSerializer(commonserializer.CommonSerializer):
    comment = CommentSerializer()

#delete notification API
class DeleteNotificationRequestSerializer(commonserializer.CommonSerializer):
    notificationId = serializers.IntegerField()

class DeleteNotificationResponseSerializer(commonserializer.CommonSerializer):
    status = serializers.CharField()

#get notification API
class GetNotificationRequestSerializer(commonserializer.CommonSerializer):
    notificationId = serializers.IntegerField()

class GetNotificationResponseSerializer(commonserializer.CommonSerializer):
    status = serializers.CharField()
    commentId = serializers.IntegerField()
    user1 = serializers.IntegerField()
    user2 = serializers.IntegerField()
    questionId = serializers.IntegerField()
    answerId = serializers.IntegerField()