from django.db import models
from django.contrib.auth.models import User

from PIL import Image # pip install Pillow

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
	name = models.CharField(max_length=40, default='Anonymous')
	mobileNumber = models.CharField(max_length=16, null =True )

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save(self, *args, **kwargs) # calling the save method of parent class of Profile class
		
		img = Image.open(self.image.path) # opens image of the current Profile objects
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save()

