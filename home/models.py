from django.db import models

class HeroSection(models.Model):
    heading = models.CharField(max_length=200, blank=True, null=True)  # Removed the trailing comma
    img = models.ImageField(blank=True, null=True)  # Corrected upload path
    description = models.TextField(blank=True, null=True)  # Fixed typo
    button_1 = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.heading or "Hero Section"  # In case heading is null


class HomeBanner(models.Model):
    img1 = models.ImageField(blank=True, null=True)
    img2 = models.ImageField(blank=True, null=True)
    img3 = models.ImageField(blank=True, null=True)
    

    def __str__(self):
        return "Home Banner"
class HomeBanner2(models.Model):
    img = models.ImageField(blank=True, null=True)
    link = models.URLField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.title)