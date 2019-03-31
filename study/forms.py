from django import forms
from .models import Subject, Note
from django.contrib import auth

class SubjectForm(forms.ModelForm):

	class Meta:
		model = Subject
		exclude = ('user',)

class NoteForm(forms.ModelForm):

	class Meta:
		model = Note
		exclude = ('user',)

	def __init__(self, user, *args, **kwargs):
		super(NoteForm, self).__init__(*args, **kwargs)
		self.fields['subject'].queryset = Subject.objects.filter(user=user)


class LoginForm(forms.Form):
	username = forms.CharField(max_length=100, required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

	def clean(self):
		try:
			u = self.cleaned_data['username']
			p = self.cleaned_data['password']
		except KeyError:
			raise forms.ValidationError('Correct the errors below')
		user = auth.authenticate(username=u, password=p)
		if user is not None:
			return self.cleaned_data
		else:
			raise forms.ValidationError('Incorrect Username or Password!')


class UserRegisterForm(auth.forms.UserCreationForm):
	# first_name = forms.CharField(max_length=100, required=True)
	# last_name = forms.CharField(max_length=100, required=True)
	# email = forms.EmailField(max_length=100, required=True)
	# username = forms.CharField(max_length=100, required=True)

	class Meta:
		model = auth.models.User
		fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

	def clean(self):
		try:
			u = self.cleaned_data['username']
			e = self.cleaned_data['email']
			p = self.cleaned_data['password1']
			cp = self.cleaned_data['password2']
		except KeyError:
			raise forms.ValidationError('Correct the errors below')
		if auth.models.User.objects.filter(email=e).exists():
			raise forms.ValidationError('Email already exists!')
		if auth.models.User.objects.filter(username=u).exists():
			raise forms.ValidationError('Username already exists!')
		if p != cp:
			raise forms.ValidationError('Passwords Mismatch')
		return self.cleaned_data


class UserEditForm(auth.forms.UserChangeForm):
	password = None

	class Meta:
		model = auth.models.User
		fields = ['first_name', 'last_name', 'email', 'username']


