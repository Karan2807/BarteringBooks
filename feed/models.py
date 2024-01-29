from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models import Max
from django.contrib.postgres.fields import ArrayField



class Post(models.Model):
	description = models.CharField(max_length=255, blank=True)
	pic = models.ImageField(upload_to='path/to/img')
	date_posted = models.DateTimeField(default=timezone.now)
	user_name = models.ForeignKey(User, on_delete=models.CASCADE)
	tags = models.CharField(max_length=100, blank=True)
	genre_choice = (
        ("G.k and Learning", "G.k and Learning"),
        ("Government Jobs", "Government Jobs"),
		("Engineering", "Engineering"),
		("Medical", "Medical"),
		("Science and Arts", "Science and Arts"),
		("School Level", "School Level"),
		("International Exams", "International Exams"),
		("Finance", "Finance"),
		("Commerce", "Commerce"),
		("Dictionary", "Dictionary"),
		("Children Books", "Children Books"),
		("Fiction", "Fiction"),
		("Non Fiction", "Non Fiction"),
		("Motivation and Self Help", "Motivation and Self Help"),
		("Religion And Spirituality", "Religion And Siprituality"),
		("Others", "Others"),
    )
	genre = models.CharField(choices=genre_choice, max_length=100, null=True)

	def __str__(self):
		return self.description

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})
 

class Comments(models.Model):
	post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
	username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
	comment = models.CharField(max_length=255)
	comment_date = models.DateTimeField(default=timezone.now)

class Like(models.Model):
	user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
	post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

class ThreadModel(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
#   has_unread = models.BooleanField(default=False)

class MessageModel(models.Model):
  thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
  sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  body = models.CharField(max_length=1000)
  image = models.ImageField(upload_to='', blank=True, null=True)
  date = models.DateTimeField(default=timezone.now)
  is_read = models.BooleanField(default=False)