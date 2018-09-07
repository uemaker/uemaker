from django.db import models

class BaseModel(models.Model):

    class Meta:
        app_label = 'manage'
        abstract = True