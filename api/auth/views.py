from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from shshop.module.user.models import UserInfo
from .serializers import UserSerializer, UserSerializerupdata  # , CustomTokenObtainPairSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "uid": user.id})


# 在上面的代码中，我们继承了 ObtainAuthToken 视图，并重写了 post 方法。
# 在这个方法中，我们首先使用序列化器验证用户名和密码。
# 然后，我们使用 Token.objects.get_or_create 方法获取用户的 Token。
# 最后，我们将 Token 发送回前端。


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]





from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model

User = get_user_model()



from rest_framework import status
from rest_framework.response import Response

from .serializers import UserSerializerupdata


class UserAvatarUpdateView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        serializer = UserSerializerupdata(data=request.data)
        if serializer.is_valid():
            nickname = serializer.validated_data['nickname']
            user = UserInfo.objects.get(nickname=nickname)
            user.avatar = serializer.validated_data['avatar']
            user.save()
            return Response({"success": "Avatar updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

