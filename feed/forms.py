from django import forms
from .models import Comments, Post

class NewPostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['description', 'pic', 'tags', 'genre']

class NewCommentForm(forms.ModelForm):

	class Meta:
		model = Comments
		fields = ['comment']

class ThreadForm(forms.Form):
  username = forms.CharField(label='', max_length=100)
class MessageForm(forms.Form):
  message = forms.CharField(label='', max_length=1000)