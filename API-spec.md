
TODOS:
. retest with intelligence

Datatypes examples:
1. IDK_User
        {
            "userId":int,
            "username":name,
            "questions":[questionDts],
            "comments":[commentDts],
            "answers":[answerDts],
            "tags":[tagnames],
            "givenVotes":int,
            "receivedVotes":int,
            "unreadNotifications":int,
            "reputation":int,
            "followers":[(userId,username)..],
            "following":[(userId,username)..]
        }
2. Question
        {
            "questionId": int,
            "owner": int,
            "title": title,
            "body": body,
            "creationTime": "2018-11-21T11:53:49Z",#eg format
            "modificationTime": "2018-11-21T11:53:50Z",
            "score_val": int/null,
            "reputationThreshold": int,
            "answers": [answerDts],
            "comments": [commentDts]
        }
3. Answer
        {
            "answerId": 1,
            "parentId": 3,
            "owner": 2,
            "body": "how to blow out all the gonne!",
            "creationTime": "2018-11-21T10:33:15Z",
            "modificationTime": "2018-11-21T10:33:16Z",
            "score_val": 0,
            "comments": [commentDts]
        }
4. Comment  
    .notes: notifiedUser field is a string which you have to typecast to int to get the notitfieduser id
        {
            "commentId": 1,
            "owner": 2,
            "body": "commentTest2",
            "creationTime": "2018-11-21T10:59:10Z",
            "modificationTime": "2018-11-21T10:59:12Z",
            "notifiedUser": username of the tagged guy(when adding a comment notification),"returned notification id as a string"
        }
5. MinifiedQuestion #todo
    {
        "questionId": int,
        "title": title,
        "body":body,
        "answers":no of answers,
        "tags:[list],
        "votes":score
    }

Apis:

. Question APIs

    .AddQuestionAPI:
        url:(POST)
            . http://localhost:8000/IDK/question/addquestion/
        notes:
            . if status == collapsed , collapse in the UI
        request:
            {
                "question":{
                    "owner":UserId,
                    "title":title,
                    "body":body,
                    "reputationThreshold":int
                }
            }
        response:
            {
                "status":success/collapsed,
                "questionId": int
            }
        errors:
            .

    .DeleteQuestionAPI:
        url:(DELETE)
            . http://localhost:8000/IDK/question/deletequestion/
        notes:
            . 
        request:
            {
                "questionId":int
            }
        response:
            {
                "status":success/failure
            }
        errors:
            . 

    .GetQuestionAPI:
        url:(POST)
            . http://localhost:8000/IDK/question/getquestion/
        notes:
            . 
        request:
            {
                "questionId":int
            }
        response:
            {
                "question": questionDt
            }
            
        errors:
            . "question not present in the database"

. AnswerAPIs

    .AddAnswerAPI:
        url:(POST)
            . http://localhost:8000/IDK/answer/addanswer/
        notes:
            . if status == collapsed , collapse in the UI
        request:
            {
                "question":{
                    "owner":UserId,
                    "title":title,
                    "body":body,
                    "reputationThreshold":int
                }
            }
        response:
            {
                "status":success/collapsed,
                "questionId": int
            }
        errors:
            .

    .DeleteAnswerAPI:
        url:(DELETE)
            . http://localhost:8000/IDK/answer/deleteanswer/
        notes:
            . 
        request:
            {
                "answerId":int
            }
        response:
            {
                "status":success/failure
            }
        errors:
            . 

    .GetAnswerAPI:
        url:(POST)
            . http://localhost:8000/IDK/answer/getanswer/
        notes:
            . 
        request:
            {
                "answerId":int
            }
        response:
            {
                "answer": answerDt
            }
            
        errors:
            . "answer not present in the database"


. CommentAPIs
    .AddCommentAPI:
        url:(POST)
            . http://localhost:8000/IDK/comment/addcomment/
        notes:
            . if collapsestatus == collapsed , collapse in the UI else it is normal
        request:
            {
                "comment" : {
                    "owner":1,
                    "body":"generic comment 2!!!!"
                },
                "parentId" : 1,
                "parentType" : "question"/"answer",
                "type" : "normal"/"notify"
            }
        response:
            {
                "status": "success" or "failure",
                "commentId": 3,
                "notificationId": 3,
                "parentId": 1,
                "parentType": "question",
                "collapsestatus": "normal" or "collapsed"
            }
        errors:
            ."parent id doesnt exist in the database"
            ."the notified user doesnt exist but comment is saved!"
            ."the type must be either normal or notify only"


    .DeleteCommentAPI:
        url:(DELETE)
            . http://localhost:8000/IDK/comment/deletecomment/
        notes:
            . 
        request:
            {
                "commentId":int
            }
        response:
            {
                "status":success/failure
            }
        errors:
            . 

    .GetCommentAPI:
        url:(POST)
            . http://localhost:8000/IDK/comment/getcomment/
        notes:
            . 
        request:
            {
                "commentId":int
            }
        response:
            {
                "comment": commentDt
            }
            
        errors:
            . "comment not present in the database"

    .GetNotificationAPI:
        url:(POST)
            . http://localhost:8000/IDK/comment/getnotification/
        notes:
            .
        request:
            {
                "notificationId":int
            }
        response:
            {
                "status":success/failure,
                "commentId" : its commentId,
                "user1":user Id,
                "user2":user Id
                "questionId": parent id,
                "answerId: null/answerParent Id
            }
        errors:
            .
    .DeleteNotificationAPI:
        url:(DELETE)
            . http://localhost:8000/IDK/comment/deletenotification/
        notes:
            .
        request:
            {
                "notificationId":int
            }
        response:
            {
                "status":success/failure
            }
        errors:
            .

. UserAPIs #change
    . Login / Logout / Register : user rest_auth
    . GetUserDetailsAPI:
        url:(POST)
            . http://localhost:8000/IDK/user/getuserdetails/
        notes:
            .
        request:
            . request.user
        response:
            {
                "idkuser":userDt
            }
        errors:
            . "user with this id doesnt exist!"

    . FollowAPI:
        url:(POST)
            . http://localhost:8000/IDK/user/follow/
        notes:
            . user1 follows user2 , user2 is followed by user1
        request:
            {
                "user1":int,
                "user2":int
            }
        response:
            {
                "status":success/failure
            }
        errors:
            . "user 1 already follows user 2"

    . UnFollowAPI:
        url:(POST)
            . http://localhost:8000/IDK/user/unfollow/
        notes:
            .
        request:
            {
                "user1":int,
                "user2":int
            }
        response:
        response:
            {
                "status":success/failure
            }
        errors:
            .

. VoteAPIs
    .VoteAPI:
        url:(POST)
            . http://localhost:8000/IDK/vote/
        notes:
            .
        request:
            {
                "userId":int,
                "parentId":int,
                "type":question/answer,
                "scoreVal":1/-1
            }
        response:
            {
                "scoreVal":updatedscore val
            }
        errors:
            .


. FeedAPIs
    .FeedAPI:
        url:(POST)
            . http://localhost:8000/IDK/feed/
        notes:
            .
        request:
            {
                "userId":int
            }
        response:
            {
                "featured":[minquestiondts],
                "unanswered":[minquestiondts]
            }
        errors:
            .

. SearchAPIs
    .SearchAPI:
        url:(POST)
            . http://localhost:8000/IDK/search/
        notes:
            . if tag put all the tags seperated by comma, and in ui show as floating tiles or something
        request:
            {
                "searchquery":text,
                "searchtype":tag/normal
            }
        response:
            {
                "minifiedQuestions":[minfiedQuestionDts]
            }
        errors:
            ."no results found!"
            ."type must be tag or normal!"

