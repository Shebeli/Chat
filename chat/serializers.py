from django.core.checks import messages
from rest_framework import serializers
from .models import ChatUser, Group, PrivateChat, PrivateChatMsg, GroupChatMsg
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['id','first_name','last_name','display_name','username','password','email','phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = ChatUser(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            display_name = validated_data['display_name'],
            username = validated_data['username'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    #No update for now. 

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name', 'creator', 'member', 'member_count']

class GCMSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatMsg
        fields = '__all__'

class PCMSerializer(serializers.ModelSerializer):
    PC = serializers.SerializerMethodField()

    class Meta:
        model = PrivateChatMsg
        fields = '__all__'

    #def create(self, validated_data):
        
    # def get_PC(self, obj):
    #     if obj.PC in ('',None):
            
    #     pc1 = PrivateChat.objects.get(Q(user1=self.initial_data['sender'])|Q(user2=self.initial_data['receiver']))
    #     pc2 = PrivateChat.objects.get(Q(user1=self.initial_data['receiver'])|Q(user2=self.initial_data['sender']))
    #     if pc1.exists():
    #         return pc1
    #     elif pc2.exists():
    #         return pc2
    #     else:
    #         new_pc = PrivateChat.objects.create(user1=self.initial_data['sender'], user2=self.initial_data['receiver'])
    #         return new_pc

class PCSerializer(serializers.ModelSerializer):
    #messages = PCMSerializer(many=True)

    class Meta:
        model = PrivateChat
        fields = ['id', 'user1', 'user2','blocked','date_created','msg']

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)