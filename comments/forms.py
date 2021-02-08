from django import forms
from comments.models import Comment


class CommentForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "class": "form-control",}), label='')
	class Meta:
		model = Comment
		fields = ('content',)
