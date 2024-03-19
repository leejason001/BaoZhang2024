#coding:utf8
from django import forms
from django.forms import fields, widgets
from django.core.validators import RegexValidator

class registerForm(forms.Form):
    username = fields.CharField(max_length=32)
    email    = fields.EmailField(max_length=64)
    password = fields.CharField( max_length=8, min_length=8,
                                error_messages={
                                    'c1':'A-Za-z\d@%',
                                },
                                 validators=[RegexValidator(
        r'(?![A-Za-z]{8})(?![A-Z,\d]{8})(?![A-Z,@,%]{8})(?![a-z,\d]{8})(?![a-z,@,%]{8})(?![\d,@,%]{8})[A-Z,\d,a-z,@,%]{8}',
            code='c1')] , widget=widgets.PasswordInput(attrs={"placeholder":"Please input passowrd"}))

    confirmPassword = fields.CharField( max_length=8, min_length=8, validators=[RegexValidator(
        r'(?![A-Za-z]{8})(?![A-Z,\d]{8})(?![A-Z,@,%]{8})(?![a-z,\d]{8})(?![a-z,@,%]{8})(?![\d,@,%]{8})[A-Z,\d,a-z,@,%]{8}',
        'Password format is error!' )] , widget=widgets.PasswordInput(attrs={"placeholder":"Please confirm the passowrd"}))
    checkCode        = fields.CharField( max_length=6, min_length=6)
    headPicture_path = fields.CharField( max_length=128)
    def clean(self):
        if self.cleaned_data.get("password") == self.cleaned_data.get("confirmPassword"):
            return self.cleaned_data
        else:
            from django.core.exceptions import ValidationError
            raise ValidationError("两次输入的密码不一致")






    

