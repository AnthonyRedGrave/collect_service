from django.db import models


class SoftDeleteMixin(models.Model):
    deleted = models.BooleanField("Удалено ли", default=False)

    def delete(object, *args, **kwargs):
        object.deleted = True
        object.save()

    class Meta:
        abstract = True