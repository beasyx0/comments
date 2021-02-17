from django import forms
from comments.models import Comment, CommentFlags


class CommentForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "class": "form-control",}), label='')
	class Meta:
		model = Comment
		fields = ('content',)


class CommentFlagForm(forms.ModelForm):
	class Meta:
		model = CommentFlags
		fields = ('reason',)
