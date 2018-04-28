from django import forms

class Zhuce(forms.Form):
    username = forms.CharField(
        max_length=12,
        min_length=6
    )
    password = forms.CharField(
        max_length=12,
        min_length=6,
        widget=forms.PasswordInput()
    )