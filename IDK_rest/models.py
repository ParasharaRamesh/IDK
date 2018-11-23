from django.db import connection, models
from django.contrib.auth.models import User
from IDK_rest.intelligence import *
#NOTE: all the models ,managers , conversion functions HAVE to come here itself, if seperated into seprate files you get circular import errors.believe me i tried!!

# MODEL MANAGERS
class ScoreManager(models.Manager):
    def computeTotalScore(self,parentId,type):
        parentType = "\""+ type.lower() + "_id\""
        with connection.cursor() as cursor:
            query = "SELECT SUM(\"scoreVal\") FROM \"IDK_rest_scoretable\" " + \
                    "WHERE "+parentType+"="+str(parentId)+";"
            cursor.execute(query)
            row = cursor.fetchone()
        return row[0]

class QuestionManager(models.Manager):
    def getRelatedTags(self, questionId):
        tagid_list = []
        tag_list = []
        with connection.cursor() as cursor:
            query = "SELECT t1.\"tagtable_id\" FROM \"IDK_rest_questiontable_tags\" as t1 " + \
                    "WHERE t1.\"questiontable_id\" = "+str(questionId)+";"
            cursor.execute(query)
            for row in cursor.fetchall():
                tagid_list.append(row[0])

        for tagid in tagid_list:
            with connection.cursor() as cursor:
                query = "SELECT t1.\"name\" FROM \"IDK_rest_tagtable\" as t1 " + \
                        "WHERE t1.\"id\" = "+str(tagid)+";"
                cursor.execute(query)
                for row in cursor.fetchall():
                    tag_list.append(row[0])

        return tag_list  


    def getSimilarQuestions(self,query,N):
        threshold = 0.0
        thisele = None  
        title = query      
        try:
            thisObj = QuestionTable.objects.get(title = query)
            title = thisObj.title
            thisObjId = thisObj.id
            thisele = (thisObjId,title,100000)
        except Exception:
            pass

        allQuestionTitles=[i[0] for i in QuestionTable.objects.values_list('title')]
        allQuestionIds=[i[0] for i in QuestionTable.objects.values_list('id')]
        allQuestions = zip(allQuestionIds,allQuestionTitles)
        similarQuestions = set()
        for question in allQuestions:
            score = getSimilarityScore(title,question[1])
            if score>=threshold :
                ele = (question[0],question[1],score)
                similarQuestions.add(ele)

        # print("added this ele")
        similarQuestions = list(similarQuestions)
        similarQuestions.sort(key = lambda x : x[2],reverse = True)
        # print("similar questions is",similarQuestions)
        topQuestions = similarQuestions[:N]
        # print("top questions is",similarQuestions)
        question_tables = []
        for question in topQuestions:
            questionTableObj = QuestionTable.objects.get(id = question[0])
            question_tables.append(questionTableObj)

        return convert_question_tables_to_question_dts(question_tables)  


    def getRelatedAnswers(self,questionId):
        with connection.cursor() as cursor:
            query = "SELECT (t1).* FROM \"IDK_rest_answertable\" as t1 " + \
                    "WHERE t1.\"parent_id\" = "+str(questionId)+";"
            cursor.execute(query)
            result_list = []
            for row in cursor.fetchall():
                result_list.append(row)     
        return result_list

    def getRelatedComments(self,questionId):
        with connection.cursor() as cursor:
            query = "SELECT (t1).* FROM \"IDK_rest_commenttable\" as t1 " + \
                    "WHERE t1.\"question_id\" = "+str(questionId)+";"
            cursor.execute(query)
            result_list = []
            for row in cursor.fetchall():
                result_list.append(row)     
        return result_list

class AnswerManager(models.Manager):
    def getRelatedComments(self,answerId):
        with connection.cursor() as cursor:
            query = "SELECT (t1).* FROM \"IDK_rest_commenttable\" as t1 " + \
                    "WHERE t1.\"answer_id\" = "+str(answerId)+";"
            cursor.execute(query)
            result_list = []
            for row in cursor.fetchall():
                result_list.append(row)     
        return result_list

class TagManager(models.Manager):
    def getUnansweredQuestions(self,tagId):
        questionids = set()
        answeredids = set()
        answeredQids = set()
        
        questionids = set([i[0] for i in QuestionTable.objects.values_list('id')])
        with connection.cursor() as cursor:
            query = "SELECT t1.\"answertable_id\" FROM \"IDK_rest_answertable_tags\" as t1 " + \
                    "WHERE t1.\"tagtable_id\" = "+str(tagId)+";"
            cursor.execute(query)
            for row in cursor.fetchall():
                answeredids.add(row[0])

        for answerid in answeredids:
            answerTableObj =  AnswerTable.objects.get(id=answerid)
            answeredQids.add(answerTableObj.parent_id)
        
        unanswered = questionids.difference(answeredQids)
        questionDtList = []                                    
        for questionId in unanswered:
            questionTableObj = QuestionTable.objects.get(id=questionId)
            questionDT = convert_question_table_to_question_dt(questionTableObj)
            questionDtList.append(questionDT)
        
        questionDtList.sort(key = lambda obj:obj.score_val,reverse = True)
        return questionDtList                            

    def getAnsweredQuestions(self,tagId):
        answeredids = set()
        answeredQids = set()
        
        with connection.cursor() as cursor:
            query = "SELECT t1.\"answertable_id\" FROM \"IDK_rest_answertable_tags\" as t1 " + \
                    "WHERE t1.\"tagtable_id\" = "+str(tagId)+";"
            cursor.execute(query)
            for row in cursor.fetchall():
                answeredids.add(row[0])
        
        for answerid in answeredids:
            answerTableObj =  AnswerTable.objects.get(id=answerid)
            answeredQids.add(answerTableObj.parent_id)
        
        questionDtList = []   
        for questionId in answeredQids:
            questionTableObj = QuestionTable.objects.get(id=questionId)
            questionDT = convert_question_table_to_question_dt(questionTableObj)
            questionDtList.append(questionDT)
        
        return questionDtList

    def getRelatedAnswers(self,tagId):
        answer_list = []
        answerid_list = set()
        with connection.cursor() as cursor:
            query = "SELECT t1.\"answertable_id\" FROM \"IDK_rest_answertable_tags\" as t1 " + \
                    "WHERE t1.\"tagtable_id\" = "+str(tagId)+";"
            cursor.execute(query)
            for row in cursor.fetchall():
                answerid_list.add(row[0])
        # answerid_list = list(answerid_list)
        for answerid in answerid_list:
            with connection.cursor() as cursor:
                query = "SELECT (t1).* FROM \"IDK_rest_answertable\" as t1 " + \
                        "WHERE t1.\"id\" = "+str(answerid)+";"
                cursor.execute(query)
                for row in cursor.fetchall():
                    answer_list.append(row)
        relatedAnswers = convert_answer_rows_to_answer_dts(answer_list)
        return relatedAnswers

    def getRelatedQuestions(self,tagId):
        question_list = []
        questionid_list = set()
        with connection.cursor() as cursor:
            query = "SELECT t1.\"questiontable_id\" FROM \"IDK_rest_questiontable_tags\" as t1 " + \
                    "WHERE t1.\"tagtable_id\" = "+str(tagId)+";"
            cursor.execute(query)
            for row in cursor.fetchall():
                questionid_list.add(row[0])

        for questionid in questionid_list:
            with connection.cursor() as cursor:
                query = "SELECT (t1).* FROM \"IDK_rest_questiontable\" as t1 " + \
                        "WHERE t1.\"id\" = "+str(questionid)+";"
                cursor.execute(query)
                for row in cursor.fetchall():
                    question_list.append(row)
        # print("the tag names list from question is",question_list)
        result = convert_question_rows_to_question_dts(question_list)        
        result.sort(key = lambda obj:obj.score_val,reverse = True)
        return result                            

# MODEL SCHEMA
class TagTable(models.Model):
    name = models.CharField(max_length=128,unique=True)
    objects = TagManager()
    class Meta:
        verbose_name_plural = "TagTable"

class QuestionTable(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reputationThreshold = models.IntegerField(default=0)#added
    tags = models.ManyToManyField(TagTable)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=30000)
    creationTime = models.DateTimeField(null=True)
    modificationTime = models.DateTimeField(null=True)

    objects = QuestionManager()
    class Meta:
        verbose_name_plural = "QuestionTable"

class AnswerTable(models.Model):
    parent = models.ForeignKey(QuestionTable, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(TagTable)
    body = models.CharField(max_length=30000)
    creationTime = models.DateTimeField(null=True)
    modificationTime = models.DateTimeField(null=True)

    objects = AnswerManager()
    class Meta:
        verbose_name_plural = "AnswerTable"
   
class CommentTable(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    body = models.CharField(max_length=1024)
    creationTime = models.DateTimeField(null=True)
    modificationTime = models.DateTimeField(null=True)
    question =  models.ForeignKey(QuestionTable, on_delete=models.CASCADE, null =True,blank = True)
    answer = models.ForeignKey(AnswerTable, on_delete=models.CASCADE, null =True,blank = True)
    class Meta:
        verbose_name_plural = "CommentTable"

class NotificationTable(models.Model):
    fromUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fromUser")
    toUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="toUser")
    comment = models.ForeignKey(CommentTable, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "NotificationTable"

class FollowTable(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    class Meta:
        verbose_name_plural = "FollowTable"

class ScoreTable(models.Model):#+
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionTable, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(AnswerTable, on_delete=models.CASCADE, null=True, blank =True)
    scoreVal = models.IntegerField(default=0)

    objects = ScoreManager()

    class Meta:
        verbose_name_plural = "ScoreTable"


#CONVERSION FUNCTIONS

from IDK_commons.datatypes.entities.Answer import *
from IDK_commons.datatypes.entities.Comment import *
from IDK_commons.datatypes.entities.Question import *
from IDK_commons.datatypes.entities.User import *

#change datatype functions
def convert_question_tables_to_question_dts(relatedQuestionTables):
    question_dts = []
    for questionTable in relatedQuestionTables:
        question_dts.append(convert_question_table_to_question_dt(questionTable))
    return question_dts

def convert_question_table_to_question_dt(questionTableRowObj):
    questionId = questionTableRowObj.id
    owner = questionTableRowObj.owner_id
    reputationThreshold = questionTableRowObj.reputationThreshold
    title = questionTableRowObj.title
    body = questionTableRowObj.body
    creationTime = questionTableRowObj.creationTime
    modificationTime = questionTableRowObj.modificationTime
    score_val = ScoreTable.objects.computeTotalScore(questionId,"question")
    answerTableRows = QuestionTable.objects.getRelatedAnswers(questionId)
    commentTableRows = QuestionTable.objects.getRelatedComments(questionId)
    answers = convert_answer_rows_to_answer_dts(answerTableRows)
    comments = convert_comment_rows_to_comment_dts(commentTableRows)
    questiondt = Question(questionId = questionId,owner = owner, title = title, body = body, 
                creationTime = creationTime,modificationTime = modificationTime,
                score_val = score_val,reputationThreshold = reputationThreshold,answers = answers, comments = comments)
    return questiondt

def convert_comment_table_to_comment_dt(commentTableRowObj):
    commentId = commentTableRowObj.id
    owner = commentTableRowObj.owner_id
    body = commentTableRowObj.body
    creationTime = commentTableRowObj.creationTime
    modificationTime = commentTableRowObj.modificationTime
    notifiedUserId = None
    try:
        notifiedUserId = NotificationTable.objects.get(comment_id = commentId).toUser_id
    except Exception:
        pass   
    commentdt= Comment(commentId = commentId,owner = owner ,body = body,creationTime = creationTime , modificationTime = modificationTime,notifiedUser = notifiedUserId)
    return commentdt

def convert_comment_dt_to_comment_table(comment,parentType,parentId):
    question = None
    answer = None
    if parentType == "question":
        question = parentId
        try:
            qt = QuestionTable.objects.get(id = question)
        except Exception:
            raise Exception("Question table does not have question with this id")
    else:
        answer = parentId
        try:
            at = AnswerTable.objects.get(id = answer)
        except Exception:
            raise Exception("Answer table does not have question with this id")

    owner = comment.owner
    body = comment.body
    creationTime = comment.creationTime
    modificationTime = comment.modificationTime
    commentTableObj = CommentTable(owner_id = owner,body = body,
                    creationTime = creationTime, modificationTime = modificationTime,
                    question_id= question,answer_id = answer)
    return commentTableObj

def convert_answer_table_to_answer_dt(answerTableRowObj):
    answerId = answerTableRowObj.id
    parentId = answerTableRowObj.parent_id
    owner = answerTableRowObj.owner_id
    body = answerTableRowObj.body
    creationTime = answerTableRowObj.creationTime
    modificationTime = answerTableRowObj.modificationTime
    score_val = ScoreTable.objects.computeTotalScore(answerId,"answer")
    commentTableRows = AnswerTable.objects.getRelatedComments(answerId)
    comments = convert_comment_rows_to_comment_dts(commentTableRows)
    answerdt = Answer(answerId=answerId, parentId=parentId, owner=owner,
        body = body,creationTime = creationTime,modificationTime= modificationTime,
        score_val = score_val,comments = comments)
    return answerdt

#convert sql returned rows to dts function
def convert_question_rows_to_question_dts(relatedQuestionTableRows):
    questionObjs = []
    for questionTableRow in relatedQuestionTableRows:
        questionObjs.append(convert_question_row_to_question_dt(questionTableRow))
    return questionObjs

def convert_question_row_to_question_dt(questionTableRow):
    questionId = questionTableRow[0]
    # print("\t\tquestionID in the convert function is",questionId)
    owner = questionTableRow[-1]
    reputationThreshold = questionTableRow[1]
    creationTime = questionTableRow[4]
    modificationTime = questionTableRow[5]
    title = questionTableRow[2]
    body = questionTableRow[3]
    score_val = ScoreTable.objects.computeTotalScore(questionId,"question")
    answerTableRows = QuestionTable.objects.getRelatedAnswers(questionId)
    commentTableRows = QuestionTable.objects.getRelatedComments(questionId)
    answers = convert_answer_rows_to_answer_dts(answerTableRows)
    comments = convert_comment_rows_to_comment_dts(commentTableRows)
    questiondt = Question(owner = owner, title = title, body = body, 
                creationTime = creationTime,modificationTime = modificationTime,
                score_val = score_val,reputationThreshold = reputationThreshold,
                answers = answers, comments = comments,questionId = questionId)
    return questiondt

def convert_answer_rows_to_answer_dts(relatedAnswerTableRows):
    answerObjs = []
    for answerTableRow in relatedAnswerTableRows:
        answerObjs.append(convert_answer_row_to_answer_dt(answerTableRow))
    return answerObjs

def convert_answer_row_to_answer_dt(answerTableRow):
    parentId = answerTableRow[-1]
    answerId = answerTableRow[0]
    owner = answerTableRow[4]
    body = answerTableRow[1]
    creationTime = answerTableRow[2]
    modificationTime = answerTableRow[3]
    score_val = ScoreTable.objects.computeTotalScore(answerId,"answer")
    commentTableRows = AnswerTable.objects.getRelatedComments(answerId)
    comments = convert_comment_rows_to_comment_dts(commentTableRows)
    answerdt=Answer(answerId=answerId,parentId = parentId ,owner = owner ,body = body, creationTime = creationTime , 
        modificationTime = modificationTime,score_val=score_val,comments=comments)
    return answerdt

def convert_comment_rows_to_comment_dts(relatedCommentTableRows):
    commentObjs = []
    for commentTableRow in relatedCommentTableRows:
        commentObjs.append(convert_comment_row_to_comment_dt(commentTableRow))
    return commentObjs

def convert_comment_row_to_comment_dt(commentTableRow):
    commentId = commentTableRow[0]
    owner = commentTableRow[-2]
    body = commentTableRow[1]
    creationTime = commentTableRow[2]
    modificationTime = commentTableRow[3]
    notifiedUserId = None
    try:
        notifiedUserId = NotificationTable.objects.get(comment_id = commentId).toUser_id
    except Exception:
        pass   
    commentdt= Comment(commentId=commentId,owner = owner ,body = body,creationTime = creationTime , modificationTime = modificationTime,notifiedUser = notifiedUserId)
    return commentdt



# USER Manager (Not exactly a django model but just a class with functions for queryinf user details)
class IDKUserManager():
    #feed functions
    def getFeaturedQuestions(self,userId):
        '''
            extract tags of this user from his questions and for each tag extract answered questions 
        '''
        tag_list = list(set(self.getTagsFromQuestion(userId)))
        
        featuredQuestions = []
        for tagname in tag_list:
            tagId = TagTable.objects.get(name = tagname).id       
            questions = TagTable.objects.getAnsweredQuestions(tagId)
            featuredQuestions.extend(questions)
        return featuredQuestions
        
    def getUnansweredQuestions(self,userId):
        '''
            extract tags of this user from his answers and for each tag extract unanswered questions 
        '''
        tag_list = list(set(self.getTagsFromAnswer(userId)))
        unansweredQuestions = []
        for tagname in tag_list:
            tagId = TagTable.objects.get(name = tagname).id
            questions = TagTable.objects.getUnansweredQuestions(tagId)
            unansweredQuestions.extend(questions)
        return unansweredQuestions


    #util functions
    def getTagsFromQuestion(self,userId):#tag list
        #check it later might be incorrect!
        tag_list = []
        tagid_list = []
        questions  = self.getQuestions(userId)
        for question in questions:
            #ids are questiontable_id & tagtable_id 
            with connection.cursor() as cursor:
                query = "SELECT t1.\"tagtable_id\" FROM \"IDK_rest_questiontable_tags\" as t1 " + \
                        "WHERE t1.\"questiontable_id\" = "+str(question.questionId)+";"
                cursor.execute(query)
                for row in cursor.fetchall():
                    tagid_list.append(row[0])

        for tagid in tagid_list:
            with connection.cursor() as cursor:
                query = "SELECT t1.\"name\" FROM \"IDK_rest_tagtable\" as t1 " + \
                        "WHERE t1.\"id\" = "+str(tagid)+";"
                cursor.execute(query)
                for row in cursor.fetchall():
                    tag_list.append(row[0])
        # print("the tag names list from question is",tag_list)
        return tag_list        


    def getTagsFromAnswer(self,userId):#tag list
        tag_list = []
        tagid_list = []
        answers  = self.getAnswers(userId)

        for answer in answers:
            with connection.cursor() as cursor:
                query = "SELECT t1.\"tagtable_id\" FROM \"IDK_rest_answertable_tags\" as t1 " + \
                        "WHERE t1.\"answertable_id\" = "+str(answer.answerId)+";"
                cursor.execute(query)
                for row in cursor.fetchall():
                    tagid_list.append(row[0])
        for tagid in tagid_list:
            with connection.cursor() as cursor:
                query = "SELECT t1.\"name\" FROM \"IDK_rest_tagtable\" as t1 " + \
                        "WHERE t1.\"id\" = "+str(tagid)+";"
                cursor.execute(query)
                for row in cursor.fetchall():
                    tag_list.append(row[0])
        return tag_list    
    
    #all appropriate sql quesries come here 
    def getGivenVotes(self,userId):#number
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) FROM \"IDK_rest_scoretable\" as t1 " + \
                    "WHERE t1.\"user_id\" = "+str(userId)+";"
            cursor.execute(query)
            votes = cursor.fetchone()[0]
        return votes

    def getReceivedVotes(self,userId):#number
        questions = self.getQuestions(userId)
        answers = self.getAnswers(userId)
        votes = 0
        with connection.cursor() as cursor:
            for question in questions:
                query = "SELECT COUNT(*) FROM \"IDK_rest_scoretable\" as t1 " + \
                        "WHERE t1.\"question_id\" = "+ str(question.questionId) +";"
                cursor.execute(query)
                votes += cursor.fetchone()[0]

        with connection.cursor() as cursor:
            for answer in answers:
                query = "SELECT COUNT(*) FROM \"IDK_rest_scoretable\" as t1 " + \
                        "WHERE t1.\"answer_id\" = "+ str(answer.answerId) +";"
                cursor.execute(query)
                votes += cursor.fetchone()[0]
        return votes
                                        

    def getFollowers(self,userId):#list of tuples (username,userId)
        with connection.cursor() as cursor:
            query = "SELECT (t1).\"follower_id\" FROM \"IDK_rest_followtable\" as t1 " + \
                    "WHERE t1.\"following_id\" = "+str(userId)+";"
            cursor.execute(query)
            id_list = []
            name_list = []
            for row in cursor.fetchall():
                id_list.append(row[0])
                name_list.append(User.objects.get(id=row[0]).username)
        result = list(zip(id_list,name_list))
        return result
    
    def getFollowing(self,userId):#list of tuples (username,userId)
        with connection.cursor() as cursor:
            query = "SELECT (t1).\"following_id\" FROM \"IDK_rest_followtable\" as t1 " + \
                    "WHERE t1.\"follower_id\" = "+str(userId)+";"
            cursor.execute(query)
            id_list = []
            name_list = []
            for row in cursor.fetchall():
                id_list.append(row[0])
                name_list.append(User.objects.get(id=row[0]).username)

        result = list(zip(id_list,name_list))
        return result

    def getQuestions(self,userId):#list of questionDTs
        related_list = []
        with connection.cursor() as cursor:
            query = "SELECT (t1).* FROM \"IDK_rest_questiontable\" as t1 " + \
                    "WHERE t1.\"owner_id\" = "+str(userId)+";"
            cursor.execute(query)
            for row in cursor.fetchall():
                related_list.append(row)    
        return convert_question_rows_to_question_dts(related_list)
        

    def getAnswers(self,userId):#list of answerDTs
        related_list = []
        with connection.cursor() as cursor:
            query = "SELECT (t1).* FROM \"IDK_rest_answertable\" as t1 " + \
                    "WHERE t1.\"owner_id\" = "+str(userId)+";"
            cursor.execute(query)
            for row in cursor.fetchall():
                related_list.append(row)     
        return convert_answer_rows_to_answer_dts(related_list)
    
    def getComments(self,userId):#list of commentDTs
        related_list = []
        with connection.cursor() as cursor:
            query = "SELECT (t1).* FROM \"IDK_rest_commenttable\" as t1 " + \
                    "WHERE t1.\"owner_id\" = "+str(userId)+";"
            cursor.execute(query)
            for row in cursor.fetchall():
                related_list.append(row)     
        return convert_comment_rows_to_comment_dts(related_list)

    def getTags(self,userId):
        questionTags = self.getTagsFromQuestion(userId)
        answerTags = self.getTagsFromAnswer(userId)
        questionTags.extend(answerTags)
        #combined list of all the tag names
        return questionTags

    def getUnreadNotifications(self,userId):#only see the toUser part , return number only
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) FROM \"IDK_rest_notificationtable\" as t1 " + \
                    "WHERE t1.\"toUser_id\" = "+str(userId)+" ;"
            cursor.execute(query)
            result = cursor.fetchone()[0]   
            return result
    
    #calculate reputation of this user based on all the count of objects from each of the above functions!
    def calculateReputation(self,userId):
        q = len(self.getQuestions(userId))
        a = len(self.getAnswers(userId))
        c = len(self.getComments(userId))
        t = len(self.getTags(userId))
        un = self.getUnreadNotifications(userId)
        gv = self.getGivenVotes(userId)
        rv = self.getReceivedVotes(userId)
        f1 = len(self.getFollowers(userId))
        f2 = len(self.getFollowing(userId))
        #weighted sum
        rep = int((q*1.0) + (a*1.0) + (c*0.75) + (t*0.2) + (un*(-0.45)) + (gv*0.3) + (rv*0.7) + (f1*0.5) + (f2*0.4))
        print("no of questions==>",q)
        print("no of answers==>",a)
        print("no of comments==>",c)
        print("no of tags==>",t)
        print("no of unread notifications==>",un)
        print("no of given votes==>",gv)
        print("no of received votes==>",rv)
        print("no of followers==>",f1)
        print("no of people followed==>",f2)
        print("reputation score of user==>",rep)
        return rep
    

#IDK user functions
def create_idk_user_dt(userId,username):
    #use the idkmanager functions and do it 
    UserManager=IDKUserManager()
    questions = UserManager.getQuestions(userId)
    answers = UserManager.getAnswers(userId)
    comments = UserManager.getComments(userId)
    tags = UserManager.getTags(userId)
    unreadNotifications = UserManager.getUnreadNotifications(userId)
    givenVotes = UserManager.getGivenVotes(userId)
    receivedVotes = UserManager.getReceivedVotes(userId)
    reputation = UserManager.calculateReputation(userId)
    followers = UserManager.getFollowers(userId)#list of tuples where each tuple is (id,name)
    following = UserManager.getFollowing(userId)#list of tuples where each tuple is (id,name)
    userObj = IDKUser(userId=userId, username= username, questions = questions, answers = answers
        , comments= comments,tags = tags, givenVotes = givenVotes,receivedVotes = receivedVotes,
        unreadNotifications = unreadNotifications, reputation=reputation,
        followers = followers,following= following)
    return userObj



