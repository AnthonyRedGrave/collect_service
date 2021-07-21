from django.db import models


class SoftDeleteObjectMixin(models.Model):
    def delete(object, *args, **kwargs):
        print(object)
        object.active = False
        object.save()
    
    class Meta:
        abstract = True