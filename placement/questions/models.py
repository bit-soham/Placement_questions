from django.db import models #type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore


# Create your models here.
class User(AbstractUser):
    # User = AbstractUser
    id = models.AutoField(primary_key=True, unique=True)
    is_email_verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to="profile_pics/", default="profile_pics/default_image.png")
    # hash = models.CharField(primary_key=True, max_length=64)

class Companies(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="company_logos/", default="company_logos/default_image.png")
    description = models.TextField()
    email = models.EmailField()

class Tags(models.Model):
    name = models.CharField(max_length=100)

class Questions(models.Model):
    image = models.ImageField(upload_to="question_images/", default=None)
    tags = models.ManyToManyField(Tags, blank=True, related_name="tags") # this is simply creating a many to many table 
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    question = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()


