import secrets

from django.db import models
from django.db.models import Q, F


class NodeDevice(models.Model):
    """A model that keeps record of every legitimate node device
        to avoid processing data from unauthorized/unknown devices.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.id = self.next_valid_id()
        if self.name in (None, ''):
            self.name = self.next_device_name(self.next_valid_id())
        if self.token in (None, ''):
            self.token = secrets.token_urlsafe(32)
        super(NodeDevice, self).save(*args, **kwargs)
    
    @staticmethod
    def next_valid_id():
        next_id = NodeDevice.objects.filter(id__gt=0).order_by('id').last()
        next_id = 1 if next_id is None else (next_id.pk + 1)
        return next_id

    @staticmethod
    def next_device_name(next_valid_id):
        return f"TAMS {next_valid_id}"