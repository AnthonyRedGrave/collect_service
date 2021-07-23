from django.db import models


class DeletedObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=True)


class SoftDeleteMixin(models.Model):
    deleted = models.BooleanField("Удалено ли", default=False)
    objects = models.Manager()
    deleted_objects = DeletedObjectsManager()

    def delete(object, hard=False, *args, **kwargs):
        if hard:
            super().delete()
        else:
            object.deleted = True
            object.save()

    class Meta:
        abstract = True

# file - test_soft_delete_mixin