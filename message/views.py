from rest_framework.viewsets import ModelViewSet
from message.models import Message
from message.serializers import MessageSerializers

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers
