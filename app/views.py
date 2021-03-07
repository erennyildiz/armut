from django.shortcuts import render
from app.serializers import *
from app.models import *
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status,generics, permissions
from django.contrib.auth.models import User
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        if(serializer.is_valid()):
            try:
                new_log = Log(logging_user=serializer.validated_data['user'],log_detail="success")
                new_log.save()
            except:
                pass
            user = serializer.validated_data['user']
            login(request, user)
            return super(LoginAPI, self).post(request, format=None)
        else:
            try:
                user = User.objects.filter(username=serializer.data["username"]).first()
                new_log = Log(logging_user=user,log_detail="fail")
                new_log.save()
            except:
                pass
            serializer.is_valid(raise_exception=True)

class messages(views.APIView):
    def post(self, request, format=None):
        many = True if isinstance(request.data, list) else False        
        request.data["sender"] = User.objects.filter(username=request.data["sender_name"]).first().id
        request.data["receiver"] = User.objects.filter(username=request.data["receiver_name"]).first().id
        serializer = MessageSerializer(data=request.data, many=many)
        if serializer.is_valid():
            is_block = Block.objects.filter(blocker=serializer.validated_data["receiver"], blocked=serializer.validated_data["sender"])
            if is_block.exists():
                return Response("blocked user!", status=status.HTTP_201_CREATED)
            else:
                serializer.save() 
            return Response("message created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class blocks(views.APIView):
    def post(self, request, format=None):
        many = True if isinstance(request.data, list) else False
        request.data["blocker"] = User.objects.filter(username=request.data["blocker_name"]).first().id
        request.data["blocked"] = User.objects.filter(username=request.data["blocked_name"]).first().id
        serializer = BlockSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response("block created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        blocks = Block.objects.all()
        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data)