from django.shortcuts import render,redirect
from .models import Profile, Meep
from django.contrib import messages

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        meeps = Meep.objects.all().order_by("-created_at")#orders from the last entered meep

    context ={
        "meeps" : meeps
    }
    return render(request, 'chitter\home.html', context)

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
    