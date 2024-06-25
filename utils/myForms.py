#coding:utf8
from django import forms
from django.forms import fields, widgets
from django.core.validators import RegexValidator
from django.forms import widgets as django_widgets
from django.forms import fields as django_fields

from repository import models

class registerForm(forms.Form):
    username = fields.CharField(max_length=32, widget=widgets.TextInput(attrs={'placeholder':'Input username'}))
    email    = fields.EmailField(max_length=64)
    # password = fields.CharField( max_length=8, min_length=8,
    #                             error_messages={
    #                                 'ZiDingYiCuoWuTiShi':'A-Za-z\d@%',
    #                             },
    #                              validators=[RegexValidator(
    #     r'(?![A-Za-z]{8})(?![A-Z,\d]{8})(?![A-Z,@,%]{8})(?![a-z,\d]{8})(?![a-z,@,%]{8})(?![\d,@,%]{8})[A-Z,\d,a-z,@,%]{8}',
    #         code='ZiDingYiCuoWuTiShi')] , widget=widgets.PasswordInput(attrs={"placeholder":"Please input passowrd"}))
    #
    # confirmPassword = fields.CharField( max_length=8, min_length=8, validators=[RegexValidator(
    #     r'(?![A-Za-z]{8})(?![A-Z,\d]{8})(?![A-Z,@,%]{8})(?![a-z,\d]{8})(?![a-z,@,%]{8})(?![\d,@,%]{8})[A-Z,\d,a-z,@,%]{8}',
    #     'Password format is error!' )] , widget=widgets.PasswordInput(attrs={"placeholder":"Please confirm the passowrd"}))
    password        = fields.CharField(max_length=8, min_length=8, widget=widgets.PasswordInput(attrs={'placeholder':'Please input password'}))
    confirmPassword = fields.CharField(max_length=8, min_length=8, widget=widgets.PasswordInput(attrs={'placeholder':'Please confirm password'}))

    checkCode        = fields.CharField( max_length=6, min_length=6, widget=widgets.TextInput(attrs={'placeholder':'CheckCode'}))
    headPicture_path = fields.CharField( max_length=128)
    def clean(self):
        if self.cleaned_data.get("password") == self.cleaned_data.get("confirmPassword"):
            return self.cleaned_data
        else:
            from django.core.exceptions import ValidationError
            raise ValidationError("两次输入的密码不一致")

class loginForm(forms.Form):
    username = fields.CharField(max_length=32, widget=widgets.TextInput(attrs={'placeholder':'Input username'}))
    password = fields.CharField(max_length=8, min_length=8, widget=widgets.PasswordInput())
    checkCode= fields.CharField(max_length=4, min_length=4)

class articleForm(forms.Form):
    title   = fields.CharField(max_length=32, required=True, error_messages={'required':'required,null is error','max_length':'max_length is not enough'},\
                             validators=[RegexValidator(r'\D','Number is not allowed!')])
    summary = fields.CharField(max_length=32, required=True, error_messages={'required':'required,null is error'})
    content = fields.CharField(widget=widgets.Textarea(attrs={'id':'articleContent','class':'kind-content'}), required=False, error_messages={'required':'required,null is error content'})

    articleType     = django_fields.IntegerField(widget=django_widgets.RadioSelect(choices=models.articles.type_choices))
    classifications = django_fields.ChoiceField(choices=[], widget=django_widgets.RadioSelect)
    labels          = django_fields.ChoiceField(choices=[], widget=django_widgets.RadioSelect)

    def __init__(self, request, *args, **kwargs):
        super(articleForm, self).__init__(*args, **kwargs)
        try:
            blog_id = request.session['blog_id']
            self.fields['classifications'].choices = models.classifications.objects.filter(owner__id=blog_id).values_list('id', 'className')
            self.fields['labels'].choices          = models.labels.objects.filter(toBlog__id=blog_id).values_list('id', 'labelName')[0:]
        except:
            print('')

class TroubleMaker(forms.Form):
    title = fields.CharField(max_length=64, error_messages={'required':'Null title is not allowed!'})
    summary = fields.CharField(max_length=256)
    detail  = fields.CharField(widget=widgets.Textarea(
        attrs={'id':'detail'}
    ))








    

