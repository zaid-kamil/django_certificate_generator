from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        group = request.POST.get('group') # customer
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, 'Invalid credentials')
                redirect('login')
            else:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Please fill all fields')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST['uname']
        fn = request.POST['firstName']
        ln = request.POST['lastName']
        email = request.POST['email']
        pwd1 = request.POST['password']
        pwd2 = request.POST['cpassword']
        if pwd1 == pwd2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=pwd1)
                user.is_active = False # disable the user until the admin activates the account
                user.save()
                # create profile
                profile = Profile(user=user, first_name=fn, last_name=ln)
                profile.save()
                messages.success(request, 'Account successfully created')
                # disable the user
                
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
    else:
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            form = ProfileForm(instance=profile)
        else:
            form = ProfileForm()
    return render(request, 'accounts/profile_create.html', {'form': form})

@login_required
def edit_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})


