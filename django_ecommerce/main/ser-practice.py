from datetime import datetime

from django.utils.six import BytesIO
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


# declaring the object
class Comment(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = datetime.now()


comment = Comment(email='test@test.com', content='foo bar')


# declaring the serializer
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


# serializing the object
serializer = CommentSerializer(comment)

# this is python native datatype
serializer.data

# render data to json
json = JSONRenderer().render(serializer.data)
json

# deserializing an object
stream = BytesIO(json)
data = JSONParser().parse(stream)

serializer = CommentSerializer(data=data)
serializer.is_valid()
serializer.validated_data


