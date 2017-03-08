from django.contrib import admin
from .models import User, Audio, Summary, Sentiment

# Register your models here.

admin.site.register(User)
admin.site.register(Audio)
admin.site.register(Summary)
admin.site.register(Sentiment)