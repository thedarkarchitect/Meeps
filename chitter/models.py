from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#meep model
class Meep(models.Model):
    user = models.ForeignKey(
        User, related_name="meeps", on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(
            f"{self.user} "
            f"({self.created_at: %Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#this means that a user has one profile and one user accout associated
    follows = models.ManyToManyField("self",
                                    related_name="followed_by",
                                    symmetrical=False,#this means that you can follow someone but they don't have to follow you back but they are you followers
                                    blank=True
                                    )
    date_modified = models.DateTimeField(User, auto_now=True)#gives current profile
    
    def __str__(self):
        return self.user.username
    
#create Profile When New User signs up
#@receiver(post_save, sender=User)#same as line 28
def created_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()#sves the profile 
        #have the user follow themselves by using the instance of the profile which has a relation to the User
        user_profile.follows.set([instance.profile.id])
        user_profile.save()#save instance of the user following the profile

post_save.connect(created_profile, sender=User)



