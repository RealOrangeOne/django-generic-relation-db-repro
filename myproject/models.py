from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey


class MainModel(models.Model):
    text = models.CharField(blank=True, max_length=100)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="+"
    )
    object_id = models.CharField(
        max_length=255,
    )

    revisions = GenericForeignKey("content_type", "object_id", for_concrete_model=False)


class Revision(models.Model):
    mains = GenericRelation(MainModel)
