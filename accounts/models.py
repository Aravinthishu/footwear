from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    pickup_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    delivery_address = models.TextField( null=True, blank=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar.jpg')
        return avatar
    
    @property
    def email(self): 
        email = self.user.email
        return  email

        
    
    def _str_(self):
        return str(self.user.username)