from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
   firstname = models.CharField(max_length=50)
   lastname = models.CharField(max_length=50)
   email = models.CharField(max_length=50,primary_key=True)
   password = models.CharField(max_length=100)

   def __unicode__(self):
    	return self.email

class Audio(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.FileField(upload_to="audio")
	email = models.ForeignKey(User)

	def __unicode__(self):
		return self.name.name

def get_upload_to(instance, filename):
    return 'upload/%d/%s' % (instance.profile, filename)

class Summary(models.Model):
	summaryId = models.ForeignKey(Audio)
	name = models.FileField(upload_to=get_upload_to)
	
	def __unicode__(self):
	   	return self.name.name

class Sentiment(models.Model):
	sentimentId = models.ForeignKey(Audio)
	name = models.FileField(upload_to=get_upload_to)
	
	def __unicode__(self):
	   	return self.name.name