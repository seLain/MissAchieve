from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

'''
Automatically create token for new user
ref: django-rest-framework.org/api-guide/authentication
'''
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Mission(models.Model):
	key = models.CharField(max_length=128, unique=True, default=uuid.uuid4)
	name = models.CharField(max_length=128)
	content = models.TextField(blank=True)
	desired_score = models.IntegerField(default=0)
	success_message = models.CharField(max_length=256, blank=True)

	def meet_desired_score(self, score):
		return True if score >= self.desired_score else False

	def __str__(self):
		return self.name if self.name else 'Mission without name.'

class KeywordMission(Mission):
	keyword = models.CharField(max_length=64)

class MissionProxy(models.Model):
	key = models.CharField(max_length=128, unique=True, default=uuid.uuid4)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
	score = models.IntegerField(default=0)
	achieved = models.BooleanField(default=False)

	def evaluate(self):
		if self.mission.meet_desired_score(self.score) and self.achieved is False:
			self.achieved = True
			self.save()
			return True
		else:
			return False

	def __str__(self):
		return 'A <%s> mission instance assigned to user <%s>' % (self.mission.__class__.__name__, self.owner.username)
