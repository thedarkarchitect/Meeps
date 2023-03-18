from django.contrib import admin
from django.contrib.auth.models import Group, User

# Register your models here.
admin.site.unregister(Group)

#remove excess user information
class UserAdmin(admin.ModelAdmin):
    model = User
    #display username fields on the admin page
    fields =["username"]#so we onlly see user names

#Unregister current/Initial User
admin.site.unregister(User)
#Reregister User
admin.site.register(User, UserAdmin)
