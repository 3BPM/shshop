from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from shshop.models import UserInfo
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserInfo.objects.create(owner=user,nickname=validated_data['username'])#在这里可以改初始的昵称！！默认为用户输入的学号啦。
        return user
# 在这个例子中，我们定义了一个UserSerializer序列化器，使用serializers.ModelSerializer类来实现。我们还重写了create()方法来创建新用户。



class UserSerializerupdata(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['avatar','nickname']
