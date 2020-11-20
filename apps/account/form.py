from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={ 'class' : 'form-control'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={ 'class' : 'form-control'})) # PasswordInput表示密文输入