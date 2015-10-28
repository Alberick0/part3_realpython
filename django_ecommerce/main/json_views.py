from rest_framework import mixins, generics, permissions
from main.serializers import StatusReportSerializer, BadgeSerializer
from main.models import StatusReport, Badge
from main.permissions import IsOwnerOrReadOnly


class StatusCollection(mixins.ListModelMixin,  # allows to serialize to JSON
                       mixins.CreateModelMixin,  # allows POST to create
                       generics.GenericAPIView):  # core func + Browseable API

    queryset = StatusReport.objects.all()  # required
    serializer_class = StatusReportSerializer  # required
    permission_classes = (permissions.IsAuthenticated,)  # has to be a tuple

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class StatusMember(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    queryset = StatusReport.objects.all()
    serializer_class = StatusReportSerializer

    permission_classes = (
        permissions.IsAuthenticated, IsOwnerOrReadOnly  # has to be a tuple
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BadgeCollection(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BadgeMember(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):

    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
