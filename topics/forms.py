from django import forms
from .models import Topic
from .models import Comment


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
