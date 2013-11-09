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

    provider = models.ForeignKey(Provider)
    category = models.ForeignKey(Category)

class DecisionTree(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    version_number = models.PositiveIntegerField(unique=True)
    published = models.BooleanField(default=False)

    diagnosis = models.ForeignKey(Diagnosis)
