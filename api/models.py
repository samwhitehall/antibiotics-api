from django.db import models

class Provider(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    description = models.TextField()

    diagnoses = models.ManyToManyField('Diagnosis')

    @property
    def any_live(self):
        return any(dt.published 
            for dt in DecisionTree.objects.filter(provider=self))

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
    version_number = models.PositiveIntegerField()
    published = models.BooleanField(default=False)

    provider = models.ForeignKey(Provider, null=True)
    diagnosis = models.ForeignKey(Diagnosis, null=True)

    def __unicode__(self):
        return '%s (%s) v%d %s' % (
                self.diagnosis.name,
                self.provider.slug,
                self.version_number,
                "(PUB)" if self.published else ""
            )

    class Meta:
        verbose_name = "decision tree"
