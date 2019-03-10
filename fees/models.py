from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	grade=models.IntegerField()
	board=models.CharField(max_length=100)
	join_date=models.DateField(default=timezone.now)
	last_paid=models.DateTimeField(null=True)
	next_due_date=models.DateTimeField(null=True)
	def __str__(self):
		return self.user.username


class FeeHistory(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	paid_date=models.DateTimeField()
	amount=models.IntegerField(null=True)
	# paiddate=models.DateTimeField(null=True)


	class Meta:
		verbose_name_plural = "Students' Fee History"


	def __str__(self):
		return f"{self.user.username} | {self.paid_date}"