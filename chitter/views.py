from django.shortcuts import render,redirect
from .models import Profile, Meep
from django.contrib import messages
from .forms import MeepForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
#register auth form
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)#don't save form untill you sure the user is authenticated or logged in
                meep.user = request.user
                meep.save()
                messages.success(request, ("Your Meep Has Been Posted! .."))
                return redirect('home')

        meeps = Meep.objects.all().order_by("-created_at")#orders from the last entered meep
        return render(request, 'chitter\home.html', {"meeps" : meeps, "form":form})
    else:
        meeps = Meep.objects.all().order_by("-created_at")#shows meeps on site but not the form to enter meeps
        return render(request, 'chitter\home.html', {"meeps" : meeps})
    
def  profile_list(request):
    context = {
        "messages":messages
    }

    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)#this excludes the user logged in at the moment
        context = {
            "profiles":profiles
        }
        return render(request, 'chitter\profile_list.html', context)
    else:
        messages.success(request, ("You Must be Logged in to view this page..."))
        return redirect('home')
    
def profile_page(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(pk=pk)#this will get profiles of people you click on based on their id
        meeps = Meep.objects.filter(pk=pk)#meeps for user only, meeps can't be got cuz they are more than one most times so they are filtered
        #post form logic
        if request.method == 'POST':#this is for the follow form to follow and unfollow profiles
            #current user ID
            current_user_profile = request.user.profile
            action = request.POST['follow']#get form data
            #decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            #save the profile
            current_user_profile.save()
        context = {
            'profile':profile,
            'meeps':meeps
        }
        return render(request, 'chitter\profile_page.html', context)
    else:
        messages.success(request, ("You Must be Logged in to view this page..."))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']#this is the name of the field we getting the username from by using the field  name
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have been logged in successfully! "))
            return redirect('home')
        else:
            messages.success(request, ("Error logging in, try again with correct username or password "))
            return redirect('login')
    else:
        return render(request, 'chitter/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have Been Logged Out. please come back soon."))

def register_user(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #next we must clean out data  
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first name']
            last_name = form.cleaned_data['last name']
            email = form.cleaned_data['email']

            #login user
            user = authenticate(username=username, password=password)
            login(request, user)#will login us in if everything is alright
            messages.success(request, ("You have successfully registered!"))
            return redirect('home')
        
    else:
        return render(request, "chitter/register.html", {'form':form})
