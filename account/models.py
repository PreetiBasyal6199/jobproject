
from .managers import UserManager

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
GENDER_CHOICES = (("male", "Male"), ("female", "Female"))
JOB_TYPE = (
    ("1", "Full time"),
    ("2", "Part time"),
    ("3", "Internship"),
)



class User(AbstractUser):
    username=None
    email = models.EmailField(unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    role=models.CharField(max_length=15)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




class JobDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type=models.CharField( choices=JOB_TYPE,max_length=10)
    position=models.CharField(max_length=20)
    description=models.TextField(max_length=100)
    salary=models.PositiveBigIntegerField()
    company_name=models.CharField(max_length=40)
    company_address=models.CharField(max_length=20)
    website=models.CharField(max_length=100)
    created_at=models.DateField(default=timezone.now)
    last_date=models.DateField()

    def __str__(self):
        return self.position

class Apply_Job(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    job=models.ForeignKey(JobDetails,on_delete=models.CASCADE)
    applied_date=models.DateField(default=timezone.now)

class Applicant(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='applicant')
    job=models.CharField(max_length=80)
    company=models.CharField(max_length=50)
    applied_date = models.DateField(default=timezone.now)
    resume=models.FileField()
    applied=models.BooleanField(default=False)