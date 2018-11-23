import csv
import os
import random
import time
import os
from django.contrib.auth.models import User

from IDK_commons import utils
from IDK_rest.models import *


'''
order of init:
profile
question
answer
tag
comment
vote
notification

csv schema:

questions: Id,OwnerUserId,CreationDate,ClosedDate,Score,Title,Body
tags:qid,tag_name
answers:Id,OwnerUserId,CreationDate,ParentId,Score,Body


'''



class TableSetup:
    def __init__(self,randomSeed=1):
        # self.question_csv_ids = []#holds list of tuples of (csv qid,real qid) 
        self.numComments = 150
        self.questions = []#question id in DB, 
        self.tag_questions = []##csv qid,tag id in DB
        self.comments = []#commentId in db,commentRow from csv
        self.answers = []#answerId in db , answerRow
        self.numTags = None
        self.numUsers = 50
        self.numQuestions = 10
        self.numAnswers = 0
        self.numNotifications = int(self.numUsers * 1.3)
        random.seed(randomSeed)

    #utility functions
    def _read_csv(self, filename, skipHeader=True):
        rows = []
        dataDir = os.path.join(os.path.abspath(os.path.dirname(__name__)), "IDK_rest", "data")
        with open(os.path.join(dataDir, filename),encoding="ISO-8859-1") as f:
            reader = csv.reader(f)
            if skipHeader:
                next(reader)
            for row in reader:
                if len(row)==0:
                    continue
                else:
                    rows.append(row)
            return rows

    def Randomize(self):
        return random.randint(1,60)

    def CoinToss(self,thres = 0.5):
        if random.random() > thres:
            return True
        else:
            return False

    #init and clear all tables functions
    def initTables(self):
        self.init_Tag_Table()
        self.init_Comment_Table()
        self.init_Answer_Table()
        # self.init_Question_Table()
        # self.init_Profile_Table()
        # self.init_Notification_Table()
        self.stats()
        print("done creating everything..")

    def clearTables(self):
        self.clearNotificationTable()
        self.clearProfileTable()
        self.clearQuestionTable()
        self.clearAnswerTable()
        self.clearCommentTable()
        self.clearTagTable()
        
    def stats(self):
        print("Tag Table = ", self.numTags)
        print("Comment Table = ", self.numComments)
        print("Answer Table = ", self.numAnswers)

    #clear table functions
    def clearCommentTable(self):
        CommentTable.objects.all().delete()
        print("destroyed commenttable contents..")   
    
    def clearAnswerTable(self):
        AnswerTable.objects.all().delete()
        print("destroyed answertable contents..")   

    def clearTagTable(self):
        TagTable.objects.all().delete()
        print("destroyed tagtable contents..")   

    def clearQuestionTable(self):
        QuestionTable.objects.all().delete()
        print("destroyed question contents..") 

    def clearNotificationTable(self):
        NotificationTable.objects.all().delete()
        print("destroyed notification table contents..") 

    def clearProfileTable(self):
        ProfileTable.objects.all().delete()
        print("destroyed profile contents..") 

    
    #init table functions
    #works
    def init_Tag_Table(self):#1
        tagRows = self._read_csv("Tags-min.csv")
        count = 0
        for tagRow in tagRows:
            tagObj = TagTable.objects.create(TagName = tagRow[1])
            self.tag_questions.append((tagRow[0],tagObj.Tag))
            count+=1
        self.numTags=count
        print("tag table done...")    

    #works
    def init_Comment_Table(self):
        commentRows = self._read_csv("Answers-min.csv")
        count = 0
        #for all the questionIds of the corresponding tags get the corresponding answer set
        for csv_questionId, tagId in self.tag_questions:
            commentRows = list(filter(lambda row : row[3] ==  csv_questionId , commentRows))
            if len(commentRows)==0:
                print("no comments....")
            for commentRow in commentRows:
                commentObj=CommentTable.objects.create(CommentBody = commentRow[-1])
                self.comments.append((commentObj.Comment,commentRow))
                count += 1
        self.numComments = count
        print("finished init comment table..")

    #works
    def init_Answer_Table(self):
        answerRows_orig = self._read_csv("Answers-min.csv")
        for commentId,comment_row in self.comments:
            #get other anwers with the same parentID, and should not be empty(there can be empty lines in the csv file)
            answerRows=list(filter(lambda row:len(row)!=0 and row[3]==comment_row[3],answerRows_orig))
            # print("answers len",len(answerRows))
            for answerRow in answerRows:
                if self.CoinToss(thres=0.4):#create with comments attached to this answer
                    Upvotes = self.Randomize()
                    Downvotes = self.Randomize()
                    answerObj=AnswerTable.objects.create(AnswerBody = answerRow[-1] , Comment_id = commentId,Upvotes = Upvotes, Downvotes = Downvotes)
                else:#create an empty answer
                    Upvotes = self.Randomize()
                    Downvotes = self.Randomize()
                    answerObj=AnswerTable.objects.create(AnswerBody = answerRow[-1] , Comment = None ,Upvotes = Upvotes, Downvotes = Downvotes)
                self.answers.append((answerObj.Answer,answerRow))
        self.numAnswers = len(answerRows)
        print("done answer Table..")

    #works
    def init_Question_Table(self):
        #all questions belonging to the tags have no answers or comments
        questionsRows_orig = self._read_csv("Questions-min.csv")
                
        #all other questions corresponding to answer
        questionTableObjs = set()
        for answerId,answerRow in self.answers:
            questionsRows = list(filter(lambda row : row[0] == answerRow[3] ,questionsRows_orig))
            for questionRow in questionsRows:
                Upvotes = self.Randomize()
                Downvotes = self.Randomize()
                Reputation = self.Randomize()
                Title = questionRow[-2]
                Body = questionRow[-1]
                Comment = None
                Tags = list(filter(lambda row : row[0]==questionRow[0], self.tag_questions))
                assert (len(tags)>0)
                Tag = random.choice(Tags)[1]
                questionObj = QuestionTable(Answer_id = answer_id, Comment_id = Comment , Tag_id = Tag, QuestionTitle = Title, QuestionBody = Body, Reputation= Reputation , Upvotes = Upvotes , Downvotes= Downvotes)                
                questionTableObjs.add(questionObj)

        #all questions based on comments
        for commentId,commentRow in self.comments:
            questionsRows = list(filter(lambda row : row[0] == commentRow[3] ,questionsRows_orig))
            for questionRow in questionsRows:
                Upvotes = self.Randomize()
                Downvotes = self.Randomize()
                Reputation = self.Randomize()
                Title = questionRow[-2]
                Body = questionRow[-1]
                Answer = None
                Tags = list(filter(lambda row : row[0]==questionRow[0], self.tag_questions))
                assert (len(Tags)>0)
                Tag = random.choice(Tags)[1]
                if self.CoinToss(thres=0.4):#all questions with only comments and no answers
                    questionObj = QuestionTable(Answer_id = Answer, Comment_id = commentId , Tag_id = Tag, QuestionTitle = Title, QuestionBody = Body, Reputation= Reputation , Upvotes = Upvotes , Downvotes= Downvotes)
                else:#all questions without any answers or comments
                    questionObj = QuestionTable(Answer_id = Answer, Comment_id = None , Tag_id = Tag, QuestionTitle = Title, QuestionBody = Body, Reputation= Reputation , Upvotes = Upvotes , Downvotes= Downvotes)
                                
                questionTableObjs.add(questionObj)

        QuestionTable.objects.bulk_create(list(questionTableObjs))
        print("Question Table done....")

    #works
    def init_Notification_Table(self):#6
        for i in range(self.numNotifications):
            randomUsers = random.sample(list(range(0,self.numUsers)),2)
            randomCommentId = random.choice(list(range(0,self.numComments)))
            NotificationTable.objects.create(FromUser_id=randomUsers[0],ToUser_id = randomUsers[1],Comment_id = randomCommentId)
        print("notification tables are done..")

    #Incomplete have to make sure all tags,comments,answers and questions are taken by every user
    def init_Profile_Table(self):#2
        maleNames = self._read_csv("male-first-names.csv")
        femaleNames = self._read_csv("female-first-names.csv")
        pokemon = self._read_csv("pokemon.csv")
        randomFirstNames = random.choices(maleNames + femaleNames,
                                          weights=[95] * len(maleNames) + [5] * len(femaleNames),
                                          k=self.numUsers)
        randomPokemon = random.choices(pokemon, k=self.numUsers)

        profileRowObjs = []

        mult = self.numQuestions // self.numUsers
        mod = self.numQuestions % self.numUsers


        for i in range(self.numUsers):    

            name = randomFirstNames[i][0].capitalize() + " " + randomPokemon[i][0]
            user = User.objects.create_user(username=name,
            email=name+'@gmail.com',
            password=name+"passwrd")
            user.save()

            for k in range(mult):
                Upvotes = self.Randomize()
                Downvotes = self.Randomize()
                profileRowObj = ProfileTable(Profile = i,User = user,Question = i +(k*self.numUsers),Upvotes = randomUpvotes,Downvotes = randomDownvotes)
                profileRowObjs.append(profileRowObj)
            
            for j in range(mod):
                Upvotes = self.Randomize()
                Downvotes = self.Randomize()
                profileRowObj = ProfileTable(Profile = i+j,User = user,Question = j + 1 + (mult*self.numUsers),Upvotes = randomUpvotes,Downvotes = randomDownvotes)
                profileRowObjs.append(profileRowObj)         

        ProfileTable.objects.bulk_create(profileRowObjs)
        print("created profile table")



