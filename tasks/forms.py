from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "due_date", "priority"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
