from rest_framework import serializers
from main.models import StatusReport


class StatusReportSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    user = serializers.StringRelatedField()
    when = serializers.DateTimeField()
    status = serializers.CharField(max_length=200)
