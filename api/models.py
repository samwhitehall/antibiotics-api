from django.db import models

#TODO: slugs should be unique

class Provider(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    description = models.TextField()

    @property
    def any_live(self):
        return any(dt.published 
            for dt in DecisionTree.objects.filter(provider=self))

    @property
    def test_slug(self):
        return '%s-test' % self.slug

    @property
    def test_name(self):
        return 'TEST: %s' % self.name

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
    created = models.DateTimeField(auto_now_add=True, unique=True)
    published = models.BooleanField(default=False)

    provider = models.ForeignKey(Provider, null=True)
    diagnosis = models.ForeignKey(Diagnosis, null=True)

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
