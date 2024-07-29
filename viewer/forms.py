import re
from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.transaction import atomic

from viewer.models import Genre, Movie, Profile


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Value must be capitalized.')


class PastMonthField(forms.DateField):

    def validate(self, value):
        super().validate(value)
        if value >= date.today():
            raise ValidationError('Only past dates allowed here.')

    def clean(self, value):
        result = super().clean(value)
        return date(year=result.year, month=result.month, day=1)


class MovieForm(forms.Form):
    title = forms.CharField(max_length=128)
    genre = forms.ModelChoiceField(queryset=Genre.objects)
    rating = forms.IntegerField(min_value=1, max_value=10)
    released = forms.DateField()
    description = forms.CharField(widget=forms.Textarea, required=False)

    def clean_description(self):
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        if result['genre'].name == 'commedy' and result['rating'] > 5:
            self.add_error('genre' '')
            self.add_error('rating' '')
            raise ValidationError(
                "Commedies aren't so good to be rated over 5."
            )
        return result


class MovieModelForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

    title = forms.CharField(validators=[capitalized_validator])
    rating = forms.IntegerField(min_value=1, max_value=10)
    released = PastMonthField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_description(self):
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        cleaned = '. '.join(sentence.capitalize() for sentence in sentences)
        return cleaned

    def clean(self):
        result = super().clean()
        if result['genre'].name == 'commedy' and result['rating'] > 5:
            raise ValidationError(
                "Commedies aren't so good to be rated over 5."
            )
        return result


class GenreModelForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'

    name = forms.CharField(validators=[capitalized_validator])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name']

    biography = forms.CharField(
        label='Tell us your story with movies', widget=forms.Textarea, min_length=40
    )

    @atomic
    def save(self, commit=True):
        self.instance.is_active = False
        result = super().save(commit)
        biography = self.cleaned_data['biography']
        profile = Profile(biography=biography, user=result)
        if commit:
            profile.save()
        return result
