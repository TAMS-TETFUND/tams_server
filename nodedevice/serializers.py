from rest_framework import serializers

from db.models import NodeDevice


class NodeDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeDevice
        fields = ["id", "name", "token"]
