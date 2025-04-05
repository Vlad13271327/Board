from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    CAT=(('tanks','Танки'), 
         ('hralers','Хилы'),
         ('damage_dealers','ДД'),
         ('traders','торговецы'),
         ('gildmasters','гилдмастеры'),
         ('questgivers','квестгиверы'),
         ('blacksmiths','кузнецы'),
         ('tanners','кожевники'),
         ('potions_master','зельевар'),
         ('spellmaster','мастер заклинаний'),)
    category = models.CharField(max_length=25, choices=CAT, verbose_name='Категория')
    date_in= models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=250, verbose_name='Название')
    text=RichTextField(null=True)

class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    status = models.BooleanField(default=False)
    date_in = models.DateTimeField(auto_now_add=True)                
      
