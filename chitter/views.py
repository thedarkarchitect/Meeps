from django.shortcuts import render,redirect
from .models import Profile
from django.contrib import messages

# Create your views here.
def home(request):
    context ={
        
    }
    return render(request, 'chitter\home.html', context)

def  profile_list(request):
    context = {
        "messages":messages
    }

    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)#this excludes the user logged in at the moment
        return render(request, 'chitter\profile_list.html', {"profiles" : profiles})
    else:
        messages.success(request, ("You Must be Logged in to view this page..."))
        return redirect('home')
    
def profile_page(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(pk=pk)

        context = {
            'profile':profile
        }
        return render(request, 'chitter\profile_page.html', context)
    else:
        messages.success(request, ("You Must be Logged in to view this page..."))
        return redirect('home')
    