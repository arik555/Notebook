from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Subject, Note
from .forms import SubjectForm, NoteForm, LoginForm, UserRegisterForm, UserEditForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import custom_pagination
# Create your views here.

def login(request):
	form = LoginForm(request.POST or None)
	if form.is_valid():
		u = form.cleaned_data['username']
		p = form.cleaned_data['password']
		user = auth.authenticate(username=u, password=p)
		auth.login(request, user)
		return redirect('items')
	context = {'form': form, 'login': 'Yeah'}
	return render(request, 'login_register.html', context)

def register(request):
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('login')
	context = {'form': form}
	return render(request, 'login_register.html', context)


@login_required(login_url='/login')
def upload(request, typ):
	if typ == 'note':
		if request.method == 'POST':
			form = NoteForm(request.user, request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = request.user
				# print(form.cleaned_data)
				instance.save()
		else:
			form = NoteForm(request.user)
		context = {'form': form, 'note': 'Yeah'}
		return render(request, 'upload.html', context)
	if typ == 'subject':
		if request.method == 'POST':
			form = SubjectForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = request.user
				# print(form.cleaned_data)
				instance.save()
		else:
			form = SubjectForm()
		context = {'form': form, }
		return render(request, 'upload.html', context)


def list_items(request, sub_id=None):
	qs = None
	page_range = None
	if request.method == 'GET':
		qs = request.GET.get('srch_query')
	if sub_id is None:
		if qs:
			instance = Subject.objects.filter(
				Q(name__contains=qs) | Q(desc__contains=qs)
				)
		else:
			instance = Subject.objects.all()
			instance, page_range = custom_pagination(request, instance)
		context = {'subjects': instance, 'page_range': page_range,}
	else:
		subj_object = Subject.objects.get(id=sub_id)
		instance = Note.objects.filter(subject=subj_object)
		if qs:
			instance = instance.filter(
				Q(title__contains=qs) | Q(desc__contains=qs)
				)
		else:
			instance, page_range = custom_pagination(request, instance)
		context = {'notes': instance, 'page_range': page_range,}
	return render(request, 'items.html', context)


def display(request, note_id):
	instance = Note.objects.get(id=note_id)
	context = {'instance': instance}
	return render(request, 'display.html', context)

@login_required(login_url='/login')
def action(request, typ, topic, id):
	if typ == 'edit':
		if topic == 'note':
			instance = Note.objects.get(id=id)
			if instance.user != request.user:
				return HttpResponse('Unauthorized Access')
			form = NoteForm(request.user, request.POST or None, instance=instance)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.save()
				return redirect('myuploads')
			context = {'form': form, 'note': 'Yeah'}
			return render(request, 'upload.html', context)
		if topic == 'subject':
			instance = Subject.objects.get(id=id)
			if instance.user != request.user:
				return HttpResponse('Unauthorized Access')
			form = SubjectForm(request.POST or None, instance=instance)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.save()
				return redirect('myuploads')
			context = {'form': form, 'subject': 'Yeah', 'placeholder': 'https://getuikit.com/v2/docs/images/placeholder_600x400.svg'}
			return render(request, 'upload.html', context)
	elif typ == 'del':
		if topic == 'note':
			instance = Note.objects.get(id=id)
			if instance.user != request.user:
				return HttpResponse('Unauthorized Access')
			instance.delete()
			return redirect('myuploads')
		if topic == 'subject':
			instance = Subject.objects.get(id=id)
			if instance.user != request.user:
				return HttpResponse('Unauthorized Access')
			instance.delete()
			return redirect('myuploads')
	else:
		return HttpResponse('<h4>Something went wrong!</h4>')

@login_required(login_url='/login')
def profile(request):
	context = {'instance': request.user, 'profile': 'Yeah'}
	return render(request, 'profile.html', context)

@login_required(login_url='/login')
def myuploads(request):
	instance = Subject.objects.filter(user=request.user)
	context = {'instance': instance}
	return render(request, 'database.html', context)

@login_required(login_url='/login')
def user_edit(request):
	instance = auth.models.User.objects.get(username=request.user)
	form = UserEditForm(request.POST or None, instance=instance)
	if form.is_valid():
		form.save()
		return redirect('login')
	context = {'form': form, 'update': 'Update'}
	return render(request, 'login_register.html', context)

def home(request):
	return render(request, 'index.html', {})

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		return redirect('home')
	else:
		return redirect('login')

@login_required(login_url='/login')
def change_password(request):
	form = auth.forms.PasswordChangeForm(request.user, request.POST or None)
	context = {'form': form,}
	if form.is_valid():
		user = form.save()
		auth.update_session_auth_hash(request, user)  # Important!
		return redirect('home')
	return render(request, 'change_password.html', context)

