
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import Profile
from feed.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import Profile, FriendRequest
from .forms import UserCreationForm, UserUpdateForm, ProfileUpdateForm, ContactForm
import random

User = get_user_model()
def register(request):

    if request.method =='POST':
        add= request.POST['add']
        email= request.POST['email']
        username= request.POST['username']
        pass1= request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1==pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Taken')
                return redirect('register')
            else:    
                 user=User.objects.create_user(first_name=add,email=email,username=username,password=pass1)
                 user.save();
                 messages.info(request,'User Created')
                 return redirect('login')
                 
        else:
             messages.info(request,'Password Not Matching')
        return redirect('/')   
    else:    
        return render(request,'users/register.html')  

@login_required
def users_list(request):
	users = Profile.objects.exclude(user=request.user)
	sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
	sent_to = []
	friends = []
	for user in users:
		friend = user.friends.all()
		for f in friend:
			if f in friends:
				friend = friend.exclude(user=f.user)
		friends+=friend
	my_friends = request.user.profile.friends.all()
	for i in my_friends:
		if i in friends:
			friends.remove(i)
	if request.user.profile in friends:
		friends.remove(request.user.profile)
	random_list = random.sample(list(users), min(len(list(users)), 10))
	for r in random_list:
		if r in friends:
			random_list.remove(r)
	friends+=random_list
	for i in my_friends:
		if i in friends:
			friends.remove(i)
	for se in sent_friend_requests:
		sent_to.append(se.to_user)
	context = {
		'users': friends,
		'sent': sent_to
	}
	return render(request, "users/users_list.html", context)

def friend_list(request):
	p = request.user.profile
	friends = p.friends.all()
	context={
	'friends': friends
	}
	return render(request, "users/friend_list.html", context)

@login_required
def send_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest, created = FriendRequest.objects.get_or_create(
			from_user=request.user,
			to_user=user)
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

@login_required
def cancel_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(
			from_user=request.user,
			to_user=user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

@login_required
def accept_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	if(FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
		request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
		request_rev.delete()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

@login_required
def delete_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

def delete_friend(request, id):
	user_profile = request.user.profile
	friend_profile = get_object_or_404(Profile, id=id)
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)
	return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))

@login_required
def profile_view(request, slug):
	p = Profile.objects.filter(slug=slug).first()
	u = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
	user_posts = Post.objects.filter(user_name=u)

	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user).filter(to_user=p.user)) == 1:
				button_status = 'friend_request_sent'

		# if we have recieved a friend request
		if len(FriendRequest.objects.filter(
			from_user=p.user).filter(to_user=request.user)) == 1:
				button_status = 'friend_request_received'

	context = {
		'u': u,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
		'post_count': user_posts.count
	}

	return render(request, "users/profile.html", context)

# def register(request):
# 	if request.method == 'POST':
# 		form = UserCreationForm(request.POST)
# 		if form.is_valid():
# 			f=form.save(commit=False)
# 			f.user=request.user
# 			f.save()
# 			username = form.cleaned_data.get('username')
# 			# address_1 = form.cleaned_data.get('address_1')
# 			# address_2 = form.cleaned_data.get('address_2')
# 			# city = form.cleaned_data.get('city')
			
# 			messages.success(request, f'Your account has been created! You can now login!')
# 			return redirect('login')
# 	else:
# 		form = UserCreationForm()
# 	return render(request, 'users/register.html', {'form':form})

@login_required
def edit_profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('my_profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context ={
		'u_form': u_form,
		'p_form': p_form,
	}
	return render(request, 'users/edit_profile.html', context)

@login_required
def my_profile(request):
	p = request.user.profile
	you = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=you)
	rec_friend_requests = FriendRequest.objects.filter(to_user=you)
	user_posts = Post.objects.filter(user_name=you)
	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user).filter(to_user=you)) == 1:
				button_status = 'friend_request_sent'

		if len(FriendRequest.objects.filter(
			from_user=p.user).filter(to_user=request.user)) == 1:
				button_status = 'friend_request_received'

	context = {
		'u': you,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
		'post_count': user_posts.count
	}

	return render(request, "users/profile.html", context)

@login_required
def search_users(request):
	query = request.GET.get('q')
	object_list = User.objects.filter(username__icontains=query)
	context ={
		'users': object_list
	}
	return render(request, "users/search_users.html", context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
          
        if form.is_valid():
            return HttpResponse("Yay! you are human.")
        else:
            return HttpResponse("OOPS! Bot suspected.")
            
    else:
        form = ContactForm()
          
    return render(request, 'login.html', {'form':form})