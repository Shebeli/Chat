from re import error
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
    #No update for now.z 

class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ['id','name', 'creator', 'member', 'member_count']
        # extra_kwargs = {'member':{'required':False}}

    def get_member_count(self, obj):
        return obj.member.count() + 1

    def validate(self, data):
        if data['creator'] in data['member']:
            raise serializers.ValidationError("You cannot assign your self as the member in member array.")
        return data

class GCMSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatMsg
        fields = '__all__'

    def validate(self, data):
        if data['sender'] not in (data['Group'].member, data['Group'].creator):
            raise serializers.ValidationError("The sender is not a member of given group.")
        return data

class PCMSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChatMsg
        fields = '__all__'
        read_only_fields = ('PC',)

    def create(self, validated_data):
        pc1 = PrivateChat.objects.filter(Q(user1=self.validated_data['sender'])& Q(user2=self.validated_data['receiver']))
        pc2 = PrivateChat.objects.filter(Q(user1=self.validated_data['receiver'])& Q(user2=self.validated_data['sender']))
        if pc1.exists():
            print("pc1 worked")
            validated_data['PC'] = pc1[0]
            return PrivateChatMsg.objects.create(**validated_data) 
        elif pc2.exists():
            print("pc2 worked")
            validated_data['PC'] = pc2[0]
            return PrivateChatMsg.objects.create(**validated_data) 
        else:
            print("pc creation worked")
            new_pc = PrivateChat.objects.create(user1=self.validated_data['sender'], user2=self.validated_data['receiver'])
            validated_data['PC'] = new_pc
            return PrivateChatMsg.objects.create(**validated_data) 


class PCSerializer(serializers.ModelSerializer):
    #messages = PCMSerializer(many=True)

    class Meta:
        model = PrivateChat
        fields = ['id', 'user1', 'user2','blocked','date_created','msg']

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)

