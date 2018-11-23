from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(FollowTable)
admin.site.register(QuestionTable)
admin.site.register(AnswerTable)
admin.site.register(CommentTable)
admin.site.register(NotificationTable)
admin.site.register(ScoreTable)
admin.site.register(TagTable)


