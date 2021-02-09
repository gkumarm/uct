from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .forms import UserForm
from todo.forms import ResourceForm
from todo.models import Resource

# Create your views here.
def home(request):
	if request.user.is_authenticated:
		# do something if the user is authenticated
		return HttpResponseRedirect(reverse('todo_index'))
	else:
		return render(request, "uauth/login.html")

#		return render(request, "todo/todo_index.html")

# def index(request):
# 	return HttpResponseRedirect(reverse('todo_index'))

# @login_required
# def special(request):
# 	return HttpResponse("You are logged in !")

@login_required
def ulogout(request):
	logout(request)
	messages.success(request, 'You are logged out!')	
	return HttpResponseRedirect(reverse('uauth:home'))

def uregister(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = ResourceForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			if 'profile_pic' in request.FILES:
				print('found it')
				profile.profile_pic = request.FILES['profile_pic']
			profile.save()
			registered = True
		else:
			print(user_form.errors,profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = ResourceForm()
	
	return render(request,'uauth/registration.html',
					{
						'user_form':user_form,
						'profile_form':profile_form,
						'registered':registered
					}
				)

def ulogin(request):
	print ("Coming here....")
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		print("Authenticating user: {} and password: {}".format(username,password))		
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				res = Resource.objects.get (user__username = username)
				request.session ['can_edit_master_data'] = res.can_edit_master_data
				print ('Can edit flag: ', res.can_edit_master_data)
				return HttpResponseRedirect(reverse('todo_index'))
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: [{}] and password: [{}]".format(username,password))
			messages.error(request, 'Invalid login details given!')
			return render(request, 'uauth/login.html', {'errmsg':'Invalid login details given'})
	else:
		return render(request, 'uauth/login.html', {})

@login_required
def upassword(request):
	if request.method == 'POST':
		form = PasswordChangeForm (request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password updated successfully! Sign-in again with new credentials.')
			logout(request)
			return HttpResponseRedirect(reverse('uauth:home'))		
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)

	return render(request, 'uauth/password.html', {'form': form})

# def error_404 (request, exception):
# 	return render(request, 'uauth/404.html')

# def error_500 (request):
# 	return render(request, 'uauth/500.html')
