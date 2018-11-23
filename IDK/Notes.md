Note: whereever you see (done) that means that it is implemented!!


#try adding editquestion,editanswer,editcomment,getsimilarquestions apis


In IDK_commons/datatypes/entities:

1.QuestionDT(done):
	- owner , title, body, creationTime, modificationTime, score_val, AnswerList, CommentList, reputation_threshold(a field to set the min threshold for answering questions)

2.AnswerDT(done):
	- owner , body , creationTime, modifiedTime , commentList , score_val

3.CommentDT(done):
	- owner, body, creationTime, modifiedTime , notifiedUser

4.UserDT(done):
	- name , phone , emmail and all those stuff
	- followers and following
	- reputation function (calculation of it is shown in 2a)
	- answerList,questionList,commentList,tagList
	- just show all his numbers in a fancy way in the UI (#questions, #votes, #tags,#answers,#comments,#unreadnotifications)

Notes:

- write utility functions for ANY reusable code!(Note to Pillai!)


Functional API docs:

1. In IDK_commons/rest/Questions(done):

	a. addQuestion(done):
		Request:
		*set score_val,AnswerList,CommentList as None
		{Question: QuestionDT}

		Response:
		{success+return ID/failure/collapse}

		Logic:
			- check for collapse
			- extract tags
			- save QuestionTable row with extracted tags + set creation_time same as modification_time

	b. deleteQuestion(done):
		Request:
		{questionId: id_to_be_deleted}

		Response:
		{sucess/failure}

		Logic:
			- delete it from the questiontable

	c. getQuestionDetails(done):
		Request:
		{questionId: id}

		Response:
		{Question:QuestionDT}

		Logic:
		- write an sql query to scoreTable and get the total score for this question
		-for this id get the appropriate row in question table
		- get all the related comments from commentTable and convert to commentDT and add it to the commentList in the QuestionDT response
		- get all the related answers from answerTable and for each answer get all related comments and add to the commentList for each AnswerDT object
		- for all related answers also compute the score from the score table using another similar sql query to step 1
		- add all the answerDT objects to the answerList in the QuestionDT response 

2. In IDK_commons/rest/Answers(done):
	
	a. addAnswer(done):
		Request:
		- for Answer set commentList as None
		- parentQuestionId should be given from the clientside
		{Answer: AnswerDT,parentId : parentQuestionId}

		Response:
		{sucess+return (questionid+answerid)/failure/collapse}

		Logic:
		- check for collapse
		- compute reputation of user and check with reputation threshold:
			-(where q = #questions, a= #answers, v = #votes,c=#comments , t= #tags, un = #unreadnotifications)
			- score = ((q+a+v+c)/(q*a*v*c))+(t/2)-un
			- if a notification is read that means it is removed from the table , we only store the unread notifications
		- extract tags from answer and add the row in the answerTable along with other info
		- return (questionId,answerId) 
		-#need both coordinates to uniquely identify in the UI, or maybe just one is enough (maru you should only tell)

	b. deleteAnswer(done):
		Request:#maybe just answerId is enough, review later
		{questionId:parentQuestionId ,answerId:its corresponding answerId}

		Response:
		{sucess/failure}

		Logic:
		- get the answerId and delete from answerTable
		-return success/failure

	c. getAnswerDetails(done):
		Request:
		{answerId: answerId}

		Response:
		{Answer:AnswerDT, parentId : question_id}

		Logic:
		- get corresponding row from answerTable
		- get all the corresponding comments for this question
		- compute the score for this answer from the comment table
		- return the question id which happens to be its parent and also return the answer details



3. In IDK_commons/rest/Comments(done):

	a. addComment(done):
		Preconditions:
		 	- in client side do a simple regex match to verify if a comment has the "~USER_NAME" notification pattern and if so set the type as "notify" else set type as "normal"
		Request:
			{comment:commentDT, parentId: just the id,parentType:question/answer, type:normal/notify}
		Response:#(probably just one comment id is enough to navigate in ui , if so have to change this return)
			{success + comment ID + parentId + parentTypes/failure,collapsestatus:success/collapsed}
		Logic:
			-check for collapse
			- if type == normal:
				- add a row in the comment table.
			  elif type == notify:
			  	- add the text as it is a new row in the comment table
				- extract the to_user from the text and search for this user in USER table + show error if not found
				- add a new row in the notify table.

	b. deleteComment(done):
		Request:
			{commentId: commentId}
		Response:
			{success/failure}
		Logic:
			- delete it i say!!


	d. getComment(done):
		Request: just the id
		Response:{comment:commentDT}
		Note: the returned notifiedUser in this case is that user's id in string form rather than the name
		Logic:
			just fetch the details i say!!

	e. deletenotification(done):
		Preconditions:
		 - have logic in client side such that if the notified user happens to clicck on the notification he is routed to that comment, and onclick this api gets called
		Request:just the id
		response : success / failure
		Logic:
			just delete it man!!


4. In IDK_commons/rest/IDK_user(done):
	a. getUserDetails(done) :given id return UserDT
	b. follow api(done): given current user and the followed insert into the table
	c. unfollow api(done):given current user and the followed guy remove from the table


5. In IDK_commons/rest/search 
	request: {query:inputstring , type: tag-search/sentence-search}
	response: list of questions similar to list of tuples for user_feed api
	Logic:
		- if type is tag search we use each tag and compute the intersection of all referenced questions , and we show that intersection list as output , else we show that search resulted in nothing
		- if type is question search, search DB directly if found return that directly, else extract the tags and then show intersection
		- (if possible) sort the returned "intersection list" (only if it is a list i.e.) using the siamese LSTM score, as this is a similarity index and is an "intelligence component"

6. In IDK_commons/rest/vote(done):
	Request:
	-potential to do medium clap feature
	{questionId : questionId, answerId: answerid, userId :userId , score:+1/-1}

	Response:
	{score_val:new score_val}

	Logic:
	- go to score table and add a new row with these input fields
	- compute total score for this specific question/answer and return that

7. In IDK_commons/rest/user_feed:
	a. getFeed:
		request: use request.user
		response : {featured:[list of tuples], unanswered:[list of tuples]}
		logic:
			- get all tags asked by user in a question call it askedTags
			- get all tags answered by user in an answer call it answeredTags
			- for featured tab , use all tags in askedTags and get union of all questions.
			- from this pick the top N questions by sorting based on score.(if it proves to be computationally heavy we can choose to just have a score attribute in each table for precomputation purposes) / pick questions with score > some K ..choose the easier path
			- same as the previous step except this time it is for the unsanswered tab , use the answeredTags and get all the question ids.
			- for each tab category return a list of tuples where each tuple has ( questionid, question title, question score) #this is done to show stuff in a more better way in the UI/ maru can suggest any changes to this structure
			- can sort on f(similarity index, question score)
	




Intelligence API docs:

fill the code in /intelligence.py all logic goes there. in api we just call those functions


1. GetTags:
	- refer https://github.com/E-tanok/NLTK_stackoverflow_tags_recommender
	- use that tag generator tool for stackoverflow data
	- write a function to get tags
	- write an api which calls this function internally

2. Collapse:
	- refer https://github.com/adityagaydhani14/Toxic-Language-Detection-in-Online-Content
	- build a model using sklearn GaussianNB
	- scrape some offensive data and train on server init
	- return offensive/ not offensive

3. similarity

