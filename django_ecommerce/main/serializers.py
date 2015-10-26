from rest_framework import serializers
from main.models import StatusReport


class StatusReportSerializer(serializers.Serializer):
    pk = serializers.Field()
    user = serializers.RelatedField(many=False, read_only=True)
    when = serializers.DateTimeField()
    status = serializers.CharField(max_length=200)

    @staticmethod
    def restore_object(self, attrs, instance=None):
        """
        This create or update a new StatusReport instance
        :param attrs:
        :param instance:
        :return:
        """

        if instance:
            instance.user = attrs.get('user', instance.user)
            instance.when = attrs.get('when', instance.when)
            instance.status = attrs.get('status', instance.status)
            return instance

        return StatusReport(**attrs)
