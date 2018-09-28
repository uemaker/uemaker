from django.db import models


class BaseModel(models.Model):

    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

    class Meta:
        app_label = 'manage'
        abstract = True
