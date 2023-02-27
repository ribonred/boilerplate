from django.db import models
from django.utils import timezone
from django_extensions.db.fields import RandomCharField
from django_lifecycle import LifecycleModelMixin


class BaseTimeStampModel(models.Model, LifecycleModelMixin):
    """
    Base model for timestamp support
    """

    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()

        self.updated = timezone.now()
        return super(BaseTimeStampModel, self).save(*args, **kwargs)


class TimestampWithUid(BaseTimeStampModel):
    uid = RandomCharField(length=12, unique=True, primary_key=True, editable=False)  # type: ignore

    class Meta:
        abstract = True
