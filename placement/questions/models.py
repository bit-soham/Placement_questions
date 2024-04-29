from django.db import models #type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore


# Create your models here.

class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to="profile_pics/", default="profile_pics/default_image.png")

class Companies(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    logo = models.ImageField(upload_to="company_logo/", default="company_logos/default_image.png")
    description = models.TextField(default="")
    website = models.TextField(blank=True)
    email = models.EmailField()

class Tags(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Questions(models.Model):
    image = models.ImageField(upload_to="question_images/", default=None)
    tags = models.ManyToManyField(Tags, blank=True, related_name="related_questions")
    companies = models.ManyToManyField(Companies, blank=True, related_name="related_questions")
    question = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)