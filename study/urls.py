from django.urls import path
from .utils import random_text
from .views import upload, list_items, display, profile, myuploads, action, login, register, user_edit, home, logout, change_password

urlpatterns = [
	path('upload/<slug:typ>', upload, name='upload'),
	path('content/', list_items, name='items'),
	path('subjects_django_xyz=<int:sub_id>/', list_items, name='items'),
	path('notes_django_zyx=<int:note_id>', display, name='display'),
	path('profile', profile, name='profile'),
	path('myuploads', myuploads, name='myuploads'),
	path('action/<slug:typ>/<slug:topic>/<int:id>', action, name='action'),
	path('login', login, name='login'),
	path('register', register, name='register'),
	path('update/user_credentials', user_edit, name='user_edit'),
	path('', home, name='home'),
	path('logout', logout, name='logout'),
	path('change_password', change_password, name='change_password'),
]