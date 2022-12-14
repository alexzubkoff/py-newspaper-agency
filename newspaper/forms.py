from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from newspaper.models import Newspaper, Redactor, Topic


class NewspaperForm(forms.ModelForm):
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        initial=0
    )
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Newspaper
        fields = ["title", "content", "topic", "publishers"]


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )

    def clean_years_of_experience_number(self):
        return validate_years_of_experience_number(self.cleaned_data["years_of_experience"])


class RedactorExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["username", "first_name", "last_name", "years_of_experience"]

    def clean_license_number(self):
        return validate_years_of_experience_number(self.cleaned_data["years_of_experience"])


def validate_years_of_experience_number(years_of_experience):
    if years_of_experience < 0 or years_of_experience > 75:
        raise ValidationError("Years of experience are not real!")

    return years_of_experience
