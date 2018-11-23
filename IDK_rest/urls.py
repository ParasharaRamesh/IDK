from django.urls import path, re_path, include
from IDK_rest import views

urlpatterns = [
    #for user rest_auth
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path('auth/registration/', include('rest_auth.registration.urls')),
    #user related apis
    re_path('^user/follow/$', views.FollowAPI.as_view()),
    re_path('^user/unfollow/$', views.UnfollowAPI.as_view()),
    re_path('^user/getuserdetails/$', views.GetUserDetailsAPI.as_view()),
    #question related apis
    re_path('^question/addquestion/$', views.AddQuestionAPI.as_view()),
    re_path('^question/deletequestion/$', views.DeleteQuestionAPI.as_view()),
    re_path('^question/getquestion/$', views.GetQuestionAPI.as_view()),
    re_path('^question/getsimilarquestions/$', views.GetSimilarQuestionsAPI.as_view()),
    #answer related apis
    re_path('^answer/addanswer/$', views.AddAnswerAPI.as_view()),
    re_path('^answer/deleteanswer/$', views.DeleteAnswerAPI.as_view()),
    re_path('^answer/getanswer/$', views.GetAnswerAPI.as_view()),
    #comment related apis
    re_path('^comment/addcomment/$', views.AddCommentAPI.as_view()),
    re_path('^comment/deletecomment/$', views.DeleteCommentAPI.as_view()),
    re_path('^comment/getcomment/$', views.GetCommentAPI.as_view()),
    re_path('^comment/getnotification/$', views.GetNotificationAPI.as_view()),
    re_path('^comment/deletenotification/$', views.DeleteNotificationAPI.as_view()),
    #search related apis
    re_path('^search/$', views.SearchAPI.as_view()),
    #user feed related apis
    re_path('^feed/$', views.FeedAPI.as_view()),
    #vote api
    re_path('^vote/$', views.VoteAPI.as_view()),
    
]