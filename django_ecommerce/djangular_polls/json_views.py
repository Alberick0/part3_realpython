from .serializers import PollSerializer, PollItemSerializer
from .models import Poll, PollItem

from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


class PollCollection(mixins.ListModelMixin, mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class PollMember(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PollItemCollection(mixins.ListModelMixin, mixins.CreateModelMixin,
                         generics.GenericAPIView):
    queryset = PollItem.objects.all()
    serializer_class = PollItemSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class PollItemMember(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
