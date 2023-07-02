from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import UserManager


# Create your models here.

class Vendor(AbstractUser):
    name = models.CharField(verbose_name='company name',max_length=200)
    email = models.EmailField(verbose_name='email', unique=True, max_length=255)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()
 
    username = None

class Tool(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=20)
    date_version = models.DateField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    ready = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    topic = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self) -> str:
        return self.topic

class Tool_Category(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    value = models.IntegerField(choices=(
        (3, '+++'),
        (2, '++'),
        (1, '+'),
        (0, 'Not Supported')
    ))

    class Meta:
        unique_together = (('tool', 'category'),)

    def __str__(self) -> str:
        return self.tool.name + str(self.category) + str(self.value)

class Survey_user(models.Model):
    nickname = models.CharField(max_length=200)
    count = models.IntegerField()

class Question(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.text

class Category_Answer(models.Model):
    user = models.ForeignKey(Survey_user, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    priority = models.CharField(max_length=200)

class User_Answer(models.Model):
    user = models.ForeignKey(Survey_user, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    count = models.IntegerField()