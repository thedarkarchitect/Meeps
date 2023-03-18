from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep

# Register your models here.
admin.site.unregister(Group)
admin.site.register(Meep)

#mix profile info into user info so they are the same 
class ProfileInline(admin.StackedInline):
    model = Profile

#remove excess user information
class UserAdmin(admin.ModelAdmin):
    model = User
    #display username fields on the admin page
    fields = ["username"]#so we onlly see user names
    inlines = [ProfileInline]

#Unregister current/Initial User
admin.site.unregister(User)
#Reregister User
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)//we don't need to register profile since we making it inline to UserAdmin viewed in USer model

