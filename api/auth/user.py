from django.db.models import Sum
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from shshop.config.settings import ShSettings
from shshop.models import ShShopAddress, UserInfo, ShUserBalanceLog
from rest_framework.permissions import IsAuthenticated


class IsOwnerAuthenticated(IsAuthenticated):

    """仅拥有获取自己个人相关信息的权限"""

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.owner)


class ShShopAddressSerializer(serializers.ModelSerializer):
    """地址序列化"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShShopAddress
        fields = "__all__"


class ShShopAddressViewSet(viewsets.ModelViewSet):
    """地址增删改查"""

    serializer_class = ShShopAddressSerializer
    permission_classes = [
        IsOwnerAuthenticated,
    ]
    # authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get_queryset(self):
        return ShShopAddress.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        self.save_only_default(serializer)
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        self.save_only_default(serializer)
        return super().perform_update(serializer)

    def save_only_default(self, serializer):
        # 处理默认收货地址只能有一个
        if serializer.validated_data["is_default"]:
            self.get_queryset().filter(is_default=True).update(is_default=False)


class ShUserBalanceLogSerializer(serializers.ModelSerializer):
    """余额记录序列化"""

    change_status = serializers.SerializerMethodField()
    change_way = serializers.SerializerMethodField()

    class Meta:
        model = ShUserBalanceLog
        fields = "__all__"

    def get_change_status(self, obj):
        return obj.get_change_status_display()

    def get_change_way(self, obj):
        return obj.get_change_way_display()


class UserInfoSerializer(serializers.ModelSerializer):
    """扩展用户信息序列化"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    balance = serializers.ReadOnlyField()

    class Meta:
        model = UserInfo
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """用户序列化"""

    UserInfo = UserInfoSerializer(many=False)
    username = serializers.ReadOnlyField()
    ShUserBalanceLog_set = ShUserBalanceLogSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "UserInfo", "ShUserBalanceLog_set")

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        print(validated_data)
        try:
            UserInfo.objects.filter(owner=instance).update(**validated_data["UserInfo"])
        except KeyError:
            pass
        instance.save()
        return instance

    def validate_UserInfo(self, data):
        try:
            import re

            phone = data["phone"]
            reg = re.compile(ShSettings.REGEX_PHONE)
            if not reg.search(phone):
                raise serializers.ValidationError("手机号格式有误！")
        except KeyError:
            pass
        return data


class UserInfoMenmberViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    """用户中心"""

    serializer_class = UserSerializer
    # authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.id)

    @action(detail=True, methods=["get"])
    def balance(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data["addplus"] = (
            self.get_object()
            .ShUserBalanceLog_set.filter(change_status=1)
            .aggregate(Sum("amount"))["amount__sum"]
            or 0
        )
        response.data["minusplus"] = (
            self.get_object()
            .ShUserBalanceLog_set.filter(change_status=2)
            .aggregate(Sum("amount"))["amount__sum"]
            or 0
        )
        return response
