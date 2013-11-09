from django.db import models

class Provider(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    description = models.TextField()

class Category(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)

class Diagnosis(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
