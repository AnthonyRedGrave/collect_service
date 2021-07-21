from django.db import models


class SoftDeleteObjectMixin(models.Model):
    def delete(object, *args, **kwargs):
        object.active = False
        object.save()
    
    class Meta:
        abstract = True