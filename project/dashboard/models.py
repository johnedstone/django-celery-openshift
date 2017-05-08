from __future__ import unicode_literals

from django.db import models

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Language(models.Model):

    language = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)

    objects = models.Manager() # The default manager

    class Meta:
        ordering = ['language']

    def __str__(self):
        return self.language

@python_2_unicode_compatible
class Environment(models.Model):

    ENV_CHOICES = [(k, settings.OPENSHIFT_API[k]['display']) for k in settings.OPENSHIFT_API.keys()]

    environment = models.CharField(choices=ENV_CHOICES, max_length=20, unique=True)

    class Meta:
        ordering = ['environment']

    def __str__(self):
        return self.environment

class BuildConfigOrderedManager(models.Manager):
    def get_queryset(self):
        ordered_queryset = super(BuildConfigOrderedManager, self).get_queryset().order_by(
            'environment').order_by('namespace').order_by('name').order_by('last_seen')

        return ordered_queryset

@python_2_unicode_compatible
class BuildConfig(models.Model):
    """Daily Build Config."""

    environment = models.ForeignKey(Environment)
    name = models.CharField(max_length=100)
    namespace = models.CharField(max_length=100)
    last_seen = models.DateField(auto_now_add=True)
    build_config = JSONField(blank=True, default={})
    language = models.ForeignKey(Language, null=True, blank=True)

    objects = models.Manager() # The default manager
    bc_objects_ordered = BuildConfigOrderedManager()


    class Meta:
        unique_together = (
            ('environment', 'namespace', 'name', 'last_seen'),
        )
        # hold on ordering here, as it's expensive: ordering = together

    def __str__(self):
        return '{}:{}:{}:{}'.format(
            self.environment.get_environment_display(),
            self.namespace,
            self.name,
            self.last_seen,
        )

# vim: ai et ts=4 sw=4 sts=4 nu
