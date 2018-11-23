import datetime
from django.shortcuts import render
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

#util functions import 
from IDK_commons.utils import *
#intelligence import
from IDK_rest.intelligence import *
#datatypes import
from IDK_commons.datatypes.entities.MinifiedQuestion import *
from IDK_commons.datatypes.entities.Question import *
from IDK_commons.datatypes.rest.Question import *
from IDK_commons.datatypes.entities.Comment import *
from IDK_commons.datatypes.rest.Comment import *
from IDK_commons.datatypes.rest.Vote import *
from IDK_commons.datatypes.rest.IDK_user import *
from IDK_commons.datatypes.entities.Answer import *
from IDK_commons.datatypes.rest.Answer import *
from IDK_commons.datatypes.rest.Search import *
from IDK_commons.datatypes.rest.Feed import *
#serializers import
from IDK_commons.serializers.entities.MinifiedQuestion import *
from IDK_commons.serializers.entities.Question import *
from IDK_commons.serializers.rest.Question import *
from IDK_commons.serializers.entities.Comment import *
from IDK_commons.serializers.rest.Comment import *
from IDK_commons.serializers.rest.Vote import *
from IDK_commons.serializers.rest.IDK_user import *
from IDK_commons.serializers.entities.Answer import *
from IDK_commons.serializers.rest.Answer import *
from IDK_commons.serializers.rest.Search import *
from IDK_commons.serializers.rest.Feed import *
#models and managers import
from IDK_rest.models import *

MAX_FEED = 30
MAX_SEARCH_RESULTS = 10


#util functions 
# for minification of questionDT to miniQuestionDT with only title, body and questionId
def minify(questions):
    minifiedQuestions = []
    for question in questions:
        questionId = question.questionId
        owner = question.owner
        body = question.body
        title = question.title
        tags = QuestionTable.objects.getRelatedTags(questionId)
        score = ScoreTable.objects.computeTotalScore(questionId,"question")
        numanswers = len(QuestionTable.objects.getRelatedAnswers(questionId))
        minQuestion = MinifiedQuestion(questionId = questionId,owner = owner,body = body,
            title = title,tags = tags,score = score, numanswers = numanswers)
        minifiedQuestions.append(minQuestion)
    return minifiedQuestions

# if not RealEstateListing.objects.filter(slug_url=slug).exists():
#     do stuff... 

def getQuestionsFromRelatedTags(tags):
    searchResults = set()
    #get the tag ids from the db and skip if no tag is found in the db
    tag_ids =[]
    for tag in tags:
        try:
            tag_id = TagTable.objects.get(name = tag).id
            tag_ids.append(tag_id)
        except Exception:
            print("continued...")
            continue 

    #check if all tags have been skipped
    if len(tag_ids)==0:
        print("in here")
        return Response({"error": "no results found!"}, status=status.HTTP_404_NOT_FOUND)

    for tagId in tag_ids:
        relatedQuestions = TagTable.objects.getRelatedQuestions(tagId)
        for relatedQuestion in relatedQuestions:
            searchResults.add(relatedQuestion)

    searchResults = list(searchResults)
    return searchResults

# Create your views here.

# question related

#done
class AddQuestionAPI(APIView):
    def post(self,request):
        serializer = AddQuestionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        addQuestionRequest = AddQuestionRequest(**serializer.data['question'])
        if not collapseCheck(addQuestionRequest.question.title) or not collapseCheck(addQuestionRequest.question.body):
            owner = addQuestionRequest.question.owner
            title = addQuestionRequest.question.title
            body = addQuestionRequest.question.body
            creationTime = addQuestionRequest.question.creationTime
            modificationTime = addQuestionRequest.question.modificationTime
            reputationThreshold = addQuestionRequest.question.reputationThreshold
            #extract all the tags and save in the manytomany field
            tags = extractTags(body)
            tagRows = []
            for tag in tags :
                try:
                    tagObj = TagTable.objects.get(name = tag)
                    print("already there macha....") 
                except Exception:
                    print("in add question puttting for the first time")
                    tagObj = TagTable(name = tag)
                    tagObj.save()     
                tagRows.append(tagObj)

            questionRow = QuestionTable(owner_id = owner, title = title, body = body, 
                creationTime = creationTime, modificationTime = modificationTime, 
                reputationThreshold = reputationThreshold)
            questionRow.save()
            questionRow.tags.add(*tagRows)#for many to many field use the "add" function
            questionRow.save()

            defaultscore = ScoreTable(user_id = owner, question_id = questionRow.id, answer_id = None)
            defaultscore.save()
        else:        
            addQuestionResponse = AddQuestionResponse(status = "collapsed",questionId = None)
            return Response(AddQuestionResponseSerializer(addQuestionResponse).data,status=status.HTTP_200_OK)

        addQuestionResponse = AddQuestionResponse(status = "success",questionId = questionRow.id)
        return Response(AddQuestionResponseSerializer(addQuestionResponse).data,status=status.HTTP_200_OK)

#done
class DeleteQuestionAPI(APIView):
    def delete(self,request):
        serializer = DeleteQuestionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        deleteQuestionRequest = DeleteQuestionRequest(**serializer.data)
        
        try:
            questionTableRowObj = QuestionTable.objects.get(id=deleteQuestionRequest.questionId)
            questionTableRowObj.delete()
        except Exception:
            deleteQuestionResponse = DeleteQuestionResponse(status = "failure")
            return Response(DeleteQuestionResponseSerializer(deleteQuestionResponse).data,status=status.HTTP_200_OK)    
    
        deleteQuestionResponse = DeleteQuestionResponse(status = "success")
        return Response(DeleteQuestionResponseSerializer(deleteQuestionResponse).data,status=status.HTTP_200_OK)

#done
class GetQuestionAPI(APIView):
    def post(self,request):
        serializer = GetQuestionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        getQuestionRequest = GetQuestionRequest(**serializer.data)
        questionId = getQuestionRequest.questionId
        try:
            questionTableRowObj = QuestionTable.objects.get(id=questionId)
        except:
            return Response({"error": "question not present in the database"}, status=status.HTTP_404_NOT_FOUND)
        questionObj = convert_question_table_to_question_dt(questionTableRowObj)
        getQuestionResponse = GetQuestionResponse(question = questionObj)
        return Response(GetQuestionResponseSerializer(getQuestionResponse).data,status=status.HTTP_200_OK)

class GetSimilarQuestionsAPI(APIView):
    def post(self,request):
        serializer = GetSimilarQuestionsRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        getSimilarQuestionsRequest = GetSimilarQuestionsRequest(**serializer.data)

        questionId = getSimilarQuestionsRequest.questionId
        query = None
        try:
            query = QuestionTable.objects.get(id = questionId).title
        except:
           return Response({"error":"this question does'nt exist!"},status= status.HTTP_404_NOT_FOUND)

        similarQuestions  = QuestionTable.objects.getSimilarQuestions(query,MAX_SEARCH_RESULTS)
        minifiedQuestions = minify(similarQuestions)
        print("making into a set",len(minifiedQuestions))
        minifiedQuestions = list(set(minifiedQuestions))
        print("made into a set",len(minifiedQuestions))
        getSimilarQuestionsResponse = GetSimilarQuestionsResponse(minifiedQuestions = minifiedQuestions)
        return Response(GetSimilarQuestionsResponseSerializer(getSimilarQuestionsResponse).data,status=status.HTTP_200_OK)        


#answer related

#done
class AddAnswerAPI(APIView):
    def post(self,request):
        serializer = AddAnswerRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        addAnswerRequest = AddAnswerRequest(**serializer.data['answer'])
        if not collapseCheck(addAnswerRequest.answer.body):
            creationTime = addAnswerRequest.answer.creationTime
            modificationTime = addAnswerRequest.answer.modificationTime
            owner = addAnswerRequest.answer.owner
            body = addAnswerRequest.answer.body
            parentId  = addAnswerRequest.answer.parentId
            answerId = addAnswerRequest.answer.answerId

            reputationThreshold = QuestionTable.objects.get(id = parentId).reputationThreshold
            ownerReputation = IDKUserManager().calculateReputation(owner)
            if ownerReputation < reputationThreshold:
                return Response({"error": "you are not allowed to answer! increase your reputation first!!"}, status=status.HTTP_404_NOT_FOUND)
            #extract all the tags and save in the manytomany field
            tags = extractTags(body)
            tagRows = []
            for tag in tags :
                try:
                    tagObj = TagTable.objects.get(name = tag)
                    print("already there bro...")
                except Exception:
                    print("in add answer..saving for the first time.")
                    tagObj = TagTable(name = tag)
                    tagObj.save()     
                tagRows.append(tagObj)

            answerRow = AnswerTable(owner_id = owner,body = body, 
                creationTime = creationTime,parent_id = parentId, modificationTime = modificationTime)
            answerRow.save()
            answerRow.tags.add(*tagRows)#for many to many field use the "add" function
            answerRow.save()
            # add a default
            defaultscore = ScoreTable(user_id = owner, question_id = None, answer_id = answerRow.id)
            defaultscore.save()
        else:        
            addAnswerResponse = AddAnswerResponse(status = "collapsed",answerId = None)
            return Response(AddAnswerResponseSerializer(addAnswerResponse).data,status=status.HTTP_200_OK)

        addAnswerResponse = AddAnswerResponse(status = "success",answerId = answerRow.id)
        return Response(AddAnswerResponseSerializer(addAnswerResponse).data,status=status.HTTP_200_OK)

#done
class DeleteAnswerAPI(APIView):
    def delete(self,request):
        serializer = DeleteAnswerRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        deleteAnswerRequest = DeleteAnswerRequest(**serializer.data)
        
        try:
            AnswerTableRowObj = AnswerTable.objects.get(id=deleteAnswerRequest.answerId)
            AnswerTableRowObj.delete()
        except Exception:
            deleteAnswerResponse = DeleteAnswerResponse(status = "failure")
            return Response(DeleteAnswerResponseSerializer(deleteAnswerResponse).data,status=status.HTTP_200_OK)    
    
        deleteAnswerResponse = DeleteAnswerResponse(status = "success")
        return Response(DeleteAnswerResponseSerializer(deleteAnswerResponse).data,status=status.HTTP_200_OK)

#done
class GetAnswerAPI(APIView):
    def post(self,request):
        serializer = GetAnswerRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        getAnswerRequest = GetAnswerRequest(**serializer.data)
        answerId = getAnswerRequest.answerId
        try:
            answerTableRowObj = AnswerTable.objects.get(id=answerId)
        except:
            return Response({"error": "answer not present in the database"}, status=status.HTTP_404_NOT_FOUND)
        answerObj = convert_answer_table_to_answer_dt(answerTableRowObj)
        getAnswerResponse = GetAnswerResponse(answer = answerObj)
        return Response(GetAnswerResponseSerializer(getAnswerResponse).data,status=status.HTTP_200_OK)

        
# comment related
#done
class AddCommentAPI(APIView):
    def post(self,request):
        serializer = AddCommentRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        commentparam = Comment(**serializer.data["comment"])
        parentIdparam = serializer.data["parentId"]
        parentTypeparam = serializer.data["parentType"]
        typeparam = serializer.data["type"]
        addCommentRequest = AddCommentRequest(comment = commentparam,parentId = parentIdparam,
                            parentType = parentTypeparam,type = typeparam)
        #check the serializer data
        comment = addCommentRequest.comment
        type = addCommentRequest.type
        parentId = addCommentRequest.parentId
        parentType = addCommentRequest.parentType
        if not collapseCheck(addCommentRequest.comment.body):
            try:
                commentTableObj = convert_comment_dt_to_comment_table(comment,parentType,parentId)
            except Exception:
                return Response({"error":"parent id doesnt exist in the database"},status= status.HTTP_400_BAD_REQUEST)
            if type == "normal":
                commentTableObj.save()
                addCommentResponse = AddCommentResponse(status = "success",commentId = commentTableObj.id ,parentId = parentId,parentType= parentType,collapsestatus = "normal")
                return Response(AddCommentResponseSerializer(addCommentResponse).data,status=status.HTTP_200_OK)
            elif type == "notify":
                commentTableObj.save()
                ownerId = comment.owner #the id of the owner
                notifiedUserName = comment.notifiedUser
                try:
                    notifiedUserId = User.objects.get(username=notifiedUserName).id
                except Exception:
                    return Response({"error":"the notified user doesnt exist but comment is saved!"},status= status.HTTP_400_BAD_REQUEST)
                notificationTableRowObj = NotificationTable(fromUser_id = ownerId,toUser_id = notifiedUserId ,comment_id = commentTableObj.id) 
                notificationTableRowObj.save()
                addCommentResponse = AddCommentResponse(status = "success",commentId = commentTableObj.id ,parentId = parentId,parentType= parentType,collapsestatus = "normal",notificationId = notificationTableRowObj.id)
                return Response(AddCommentResponseSerializer(addCommentResponse).data,status=status.HTTP_200_OK)
            else:
                return Response({"error":"the type must be either normal or notify only"},status= status.HTTP_400_BAD_REQUEST)
        else:
            addCommentResponse = AddCommentResponse(status = "failure",commentId = None,parentId = None,parentType= None,collapsestatus = "collapsed")
            return Response(AddCommentResponseSerializer(addCommentResponse).data,status=status.HTTP_200_OK)

#done
class DeleteCommentAPI(APIView):
    def delete(self,request):
        serializer = DeleteCommentRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        deleteCommentRequest = DeleteCommentRequest(**serializer.data)
        
        try:
            commentTableRowObj = CommentTable.objects.get(id=deleteCommentRequest.commentId)
            commentTableRowObj.delete()         
        except Exception:
            deleteCommentResponse = DeleteCommentResponse(status = "failure")
            return Response(DeleteCommentResponseSerializer(deleteCommentResponse).data,status=status.HTTP_200_OK)    
    
        deleteCommentResponse = DeleteCommentResponse(status = "success")
        return Response(DeleteCommentResponseSerializer(deleteCommentResponse).data,status=status.HTTP_200_OK)

#done
class DeleteNotificationAPI(APIView):
    def delete(self,request):
        serializer = DeleteNotificationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        deleteNotificationRequest = DeleteNotificationRequest(**serializer.data)
        
        try:
            notificationTableRowObj = NotificationTable.objects.get(id=deleteNotificationRequest.notificationId)
            notificationTableRowObj.delete()         
        except Exception:
            deleteNotificationResponse = DeleteNotificationResponse(status = "failure")
            return Response(DeleteCommentResponseSerializer(deleteNotificationResponse).data,status=status.HTTP_200_OK)    
    
        deleteNotificationResponse = DeleteNotificationResponse(status = "success")
        return Response(DeleteCommentResponseSerializer(deleteNotificationResponse).data,status=status.HTTP_200_OK)

#done
class GetNotificationAPI(APIView):
    def post(self,request):
        serializer = GetNotificationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        getNotificationRequest = GetNotificationRequest(**serializer.data)
        
        notificationId = getNotificationRequest.notificationId
        notifyTableObj = NotificationTable.objects.get(id=notificationId)

        fromUserId = notifyTableObj.fromUser_id
        toUserId = notifyTableObj.toUser_id
        commentId = notifyTableObj.comment_id


        try:
            commentTableObj = CommentTable.objects.get(id=commentId)
        except Exception:
            return Response({"error":"comment having this notification was not found!!"},status = status.HTTP_404_NOT_FOUND)

        questionId = commentTableObj.question_id
        answerId = commentTableObj.answer_id

        getNotificationResponse = GetNotificationResponse(status = "success",commentId = commentId, user1 = fromUserId,user2 = toUserId,questionId=
            questionId,answerId=answerId)
        return Response(GetNotificationResponseSerializer(getNotificationResponse).data,status=status.HTTP_200_OK)        
        
#done
#NOTE: here the returned notifiedUser is the string id rather than name , so typecast it in the client side
class GetCommentAPI(APIView):
    def post(self,request):
        serializer = GetCommentRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        getCommentRequest = GetCommentRequest(**serializer.data)
        commentId = getCommentRequest.commentId
        try:
            commentTableRowObj = CommentTable.objects.get(id=commentId)
        except:
            return Response({"error": "comment not present in the database"}, status=status.HTTP_404_NOT_FOUND)
        commentObj = convert_comment_table_to_comment_dt(commentTableRowObj)
        getCommentResponse = GetCommentResponse(comment = commentObj)
        return Response(GetCommentResponseSerializer(getCommentResponse).data,status=status.HTTP_200_OK)

# user related
#done
class GetUserDetailsAPI(APIView):
    def post(self,request):
        serializer = GetUserDetailsRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        getUserRequest = GetUserDetailsRequest(**serializer.data)
        userId = getUserRequest.userId
        if userId == -1:
            loggedInUserId =  request.user.id
            loggedInUserName = User.objects.get(id = loggedInUserId).username
            userObj = create_idk_user_dt(loggedInUserId,loggedInUserName)
            getUserResponse = GetUserDetailsResponse(idkuser = userObj)
            print("current user details are retreived..")
            return Response(GetUserDetailsResponseSerializer(getUserResponse).data,status=status.HTTP_200_OK)
        else:
            try:
                username = User.objects.get(id = userId).username
            except:
                return Response({"error":"user with this id doesnt exist!"},status=status.HTTP_400_BAD_REQUEST)
            userObj = create_idk_user_dt(userId,username)
            getUserResponse = GetUserDetailsResponse(idkuser = userObj)
            print("other user details are retreived..")
            return Response(GetUserDetailsResponseSerializer(getUserResponse).data,status=status.HTTP_200_OK)

#done
class FollowAPI(APIView):
    #user1 follows user2 and user2 has user1 as one of his many followers
    def post(self,request):
        serializer = FollowRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        followRequest = FollowRequest(**serializer.data)

        user1 = followRequest.user1
        user2 = followRequest.user2
        try:#those users are there
            followTableRowObj = FollowTable.objects.get(follower_id=user1,following_id = user2)
            return Response({"error":"user 1 already follows user 2"},status=status.HTTP_404_NOT_FOUND)
        except:#those users are not there
            try:
                followTableRowObj = FollowTable(follower_id = user1 , following_id = user2)
                followTableRowObj.save()
                followResponse = FollowResponse(status = "success")
            except:
                followResponse = FollowResponse(status = "failure")
            return Response(FollowResponseSerializer(followResponse).data,status=status.HTTP_200_OK)

#done
class UnfollowAPI(APIView):
    #user1 follows user2 and user2 has user1 as one of his many followers
    def delete(self,request):
        serializer = UnfollowRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        unfollowRequest = UnfollowRequest(**serializer.data)

        user1 = unfollowRequest.user1
        user2 = unfollowRequest.user2
        try:
            followTableRowObj = FollowTable.objects.get(follower_id=user1,following_id = user2)
            followTableRowObj.delete()
            unfollowResponse = UnfollowResponse(status = "success")
        except:
            unfollowResponse = UnfollowResponse(status = "failure")
        return Response(UnfollowResponseSerializer(unfollowResponse).data,status=status.HTTP_200_OK)


# vote related
#done
class VoteAPI(APIView):
    def post(self,request):
        serializer = VoteRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        voteRequest = VoteRequest(**serializer.data)
        userId = voteRequest.userId
        questionId = None
        answerId = None
        scoreVal = voteRequest.scoreVal
        if voteRequest.type == "question":
            questionId = voteRequest.parentId

            try:
                questionTableRowObj = QuestionTable.objects.get(id=questionId)
            except:
                return Response({"error": "question not present in the database"}, status=status.HTTP_404_NOT_FOUND)

            scoreTableRowObj = ScoreTable(user_id = userId,question_id = questionId ,answer_id = answerId ,scoreVal = scoreVal)
            scoreTableRowObj.save()
        elif voteRequest.type == "answer":
            answerId = voteRequest.parentId

            try:
                answerTableRowObj = AnswerTable.objects.get(id=answerId)
            except:
                return Response({"error": "answer not present in the database"}, status=status.HTTP_404_NOT_FOUND)

            scoreTableRowObj = ScoreTable(user_id = userId,question_id = questionId ,answer_id = answerId ,scoreVal = scoreVal)
            scoreTableRowObj.save()
        else:
            return Response({"error": "type must be question or answer"}, status=status.HTTP_404_NOT_FOUND)
        #score to compute the total no of votes the question has received
        newscore = ScoreTable.objects.computeTotalScore(voteRequest.parentId,voteRequest.type)
        voteResponse = VoteResponse(scoreVal = newscore)
        return Response(VoteResponseSerializer(voteResponse).data,status=status.HTTP_200_OK)

# search related
class SearchAPI(APIView):
    def post(self,request):
        serializer = SearchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        searchRequest = SearchRequest(**serializer.data)
        searchquery = searchRequest.searchquery
        searchtype = searchRequest.searchtype
        tags = None
        print("searchquery",searchquery)
        #extract tags section
        if searchtype == "tag":
            tags = searchquery.split(",")
            print("in tag , tags is",tags)
        elif searchtype == "normal":
            #if query matches the title of some question then return questionId
            similarQuestions = QuestionTable.objects.getSimilarQuestions(searchquery,MAX_FEED)
            minifiedSimilarQuestions = minify(similarQuestions)
            tags = extractTags(searchquery)
            print("in normal, tags is",tags)
        else:        
            return Response({"error": "type must be tag or normal!"}, status=status.HTTP_404_NOT_FOUND)

        searchResults = getQuestionsFromRelatedTags(tags)
        # print("search results is",searchResults)
        results = minify(searchResults)
        results.extend(minifiedSimilarQuestions)

        unique_qids = dict()
        minifiedQuestions = []
        for question in results:
            if question.questionId not in unique_qids:
                unique_qids[question.questionId] = 0 
                minifiedQuestions.append(question) 
        del results
        del unique_qids
        searchResponse = SearchResponse(minifiedQuestions = minifiedQuestions)#fill later
        return Response(SearchResponseSerializer(searchResponse).data,status=status.HTTP_200_OK)
        
# feed related
class FeedAPI(APIView):
    def post(self,request):
        serializer = FeedRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("serialiser is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        feedRequest = FeedRequest(**serializer.data)

        userId = feedRequest.userId
        featuredQuestions = IDKUserManager().getFeaturedQuestions(userId)[:MAX_FEED]
        unansweredQuestions = IDKUserManager().getUnansweredQuestions(userId)[:MAX_FEED]

        featuredMiniQuestions = minify(featuredQuestions)
        unansweredMiniQuestions = minify(unansweredQuestions)

        unique_featured_qids = dict()
        unique_unanswered_qids = dict()
        featuredResults = []
        unansweredResults = []
        for question in featuredMiniQuestions:
            if question.questionId not in unique_featured_qids:
                unique_featured_qids[question.questionId] = 0 
                featuredResults.append(question) 


        for question in unansweredMiniQuestions:
            if question.questionId not in unique_unanswered_qids:
                unique_unanswered_qids[question.questionId] = 0 
                unansweredResults.append(question)

        feedResponse = FeedResponse(featured = featuredResults, unanswered = unansweredResults)
        return Response(FeedResponseSerializer(feedResponse).data,status=status.HTTP_200_OK)
        

