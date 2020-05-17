from django import forms

from comments.models import CommentReview


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentReview
        fields = [
            'content'
        ]
