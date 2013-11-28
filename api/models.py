from django.db import models

import jsonfield

class Provider(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField()

    @property
    def any_live(self):
        return any(dt.published 
            for dt in DecisionTree.objects.filter(provider=self))

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.slug)


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(unique=True, max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class Diagnosis(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(unique=True, max_length=100)
    category = models.ForeignKey(Category, null=False, blank=False)

    def __unicode__(self):
        return '%s/%s' % (self.category, self.name)

    class Meta:
        verbose_name_plural = "diagnoses"

class DecisionTree(models.Model):
    created = models.DateTimeField(auto_now_add=True, unique=True)
    published = models.BooleanField(default=False)

    provider = models.ForeignKey(Provider, null=False, blank=False)
    diagnosis = models.ForeignKey(Diagnosis, null=False, blank=False)

    decision_structure = jsonfield.JSONField(blank=True)

    @property
    def version(self):
        return DecisionTree.objects.filter(
            provider=self.provider,
            diagnosis=self.diagnosis,
            created__lt=self.created
        ).count() + 1

    def __unicode__(self):
        return '%s (%s) v%d %s' % (
                self.diagnosis.name,
                self.provider.slug,
                self.version,
                "(PUB)" if self.published else ""
            )

    class Meta:
        verbose_name = "decision tree"

class Question(models.Model):
    qid = models.CharField(unique=True, max_length=30)
    label = models.CharField(max_length=100, blank=True)
    information = models.TextField(blank=True)
    answers = jsonfield.JSONField(blank=True)

    @property
    def question_type(self):
        return "check" if len(self.answers) == 2 else "radio"

    def __unicode__(self):
        return '(%s) %s' % (self.qid, self.label)

class Treatment(models.Model):
    tid = models.CharField(unique=True, max_length=30)
    details = models.TextField(blank=True)

    def __unicode__(self):
        return '(%s) %s' % (self.tid, self.details[:30])
