from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, generics, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from .serializers import UserSerializer, GroupSerializer, GCMSerializer, PCMSerializer, PCSerializer, PasswordSerializer
from .models import ChatUser, Group, PrivateChat, PrivateChatMsg, GroupChatMsg


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = UserSerializer
    queryset = ChatUser.objects.all()

    @action(detail=True, methods=['post'])
    def chng_pass(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            print('serializerdata:',serializer.data)
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status':'password change succesfully'},status=status.HTTP_202_ACCEPTED)
        return Response( {'status':'password failed to change'},status=status.HTTP_400_BAD_REQUEST)


class PCViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = PCSerializer
    queryset = PrivateChat.objects.all()

    @action(detail=True, methods=['GET'])
    def associated_msgs(self, request, pk=None):
        pcm = PrivateChatMsg.objects.filter(PC=self.get_object())
        serializer = PCMSerializer(pcm, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=['GET'])
    def list_pc(self, request, pk=None):
        if request.user.is_anonymous:
            return Response({'status':'Login first'}, status=status.HTTP_401_UNAUTHORIZED)
        if pk is not None:
            pc = PrivateChat.objects.filter(pk=pk)
        else:
            pc = PrivateChat.objects.filter(Q(user1=request.user)| Q(user2=request.user))
        if pc.exists():
            serializer = PCSerializer(pc, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response({'status':'theres no data associated with requested user'}, status=status.HTTP_204_NO_CONTENT)

class PCMViewSet(viewsets.ModelViewSet):
    serializer_class = PCMSerializer
    queryset = PrivateChatMsg.objects.all()

    