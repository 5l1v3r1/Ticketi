from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import json

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    post = models.CharField(max_length = 100)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @property
    def get_profile_pics(self, profile_pic):
        return profile_pic.pic_path

class ProfilePic(models.Model):
    pic = models.ImageField(upload_to='profile_pictures/', default = 'profile_pictures/None/no-image.jpg')
    pic_path =  json.dumps(unicode('pic'))
    user = models.OneToOneField(User, default=None, related_name='pic_user')
    def cache(self):
        result = urllib.urlretrieve(self.url)
        self.pic.save(
            os.path.basename(self.url),
            File(open(result[0]))
        )
        self.save()
