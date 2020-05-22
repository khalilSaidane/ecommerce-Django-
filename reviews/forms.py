from django import forms

from reviews.models import Review


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'content',
            'rate',
        ]

    def clean_rate(self):
        rate = self.cleaned_data['rate']
        if 0 <= rate <= 10:
            raise forms.ValidationError('Rate must be between 0 and 10')
        return rate
