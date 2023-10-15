from django import forms

from app.tube.models import Video


class FormVideoCreateFirstStep(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_file']

class FormVideoCreateSecondStep(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'category']