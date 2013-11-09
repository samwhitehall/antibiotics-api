from django.db import models

class Provider(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    description = models.TextField()

    diagnosis = models.ManyToManyField('Diagnosis')

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.slug)

class Category(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class Diagnosis(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True)

    def __unicode__(self):
        return '%s/%s' % (self.category, self.name)

    class Meta:
        verbose_name_plural = "diagnoses"

class DecisionTree(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    version_number = models.PositiveIntegerField(unique=True)
    published = models.BooleanField(default=False)

    provider = models.ForeignKey(Provider, null=True)
    diagnosis = models.ForeignKey(Diagnosis, null=True)

    def __unicode__(self):
        return '%s (%s) v%d' % (
                self.diagnosis.name,
                self.diagnosis.provider.slug,
                self.version_number
            )

    class Meta:
        verbose_name = "decision tree"
