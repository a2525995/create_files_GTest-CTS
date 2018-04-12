from django.db import models

# Create your models here.
class Textblog(models.Model):
    message  = models.TextField()
    times    = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

class User(models.Model):
    username   = models.CharField(max_length=50,unique=True)
    password   = models.CharField(max_length=50)
    email      = models.CharField(max_length=50)
    permission = models.BooleanField(default=True)

    def __unicode__(self):
        return self.username

class Advise(models.Model):
    xname     = models.CharField(max_length=20)
    xemail    = models.EmailField(max_length=50)
    Message   = models.TextField()

class list_info(models.Model):
    username = models.OneToOneField("User",on_delete=models.CASCADE)
    name     = models.CharField(max_length=30)
    Area     = models.CharField(max_length=30,null=True,blank=True)
    Tel      = models.CharField(max_length=11)
    age      = models.IntegerField(blank=True)
    DATEBIRTH= models.DateField(blank=True)
    sex      = (('man','male'),('woman','female'))
    user_sex = models.CharField(max_length=5,choices=sex,default='')
    per_mess = models.TextField(blank=True)
    img      = models.ImageField(upload_to='img/%Y/%m',verbose_name='Narrow of img',default='img/retina_wood.png')