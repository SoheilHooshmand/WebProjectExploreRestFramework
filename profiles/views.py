from .models import Profile, Skill, Message
from .serializer import UserSerializer, ProfileSerializer, SkillSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import utils


class ProfileList(APIView):

    def get(self, request, format = None):
        profiles = utils.search_profiles(request)
        done, result = utils.ProfilePaginate(request, profiles)
        if done :
            return result
        else :
            serializer = ProfileSerializer(profiles, many = True)
            return Response(serializer.data)

    def post(self, request, format = None):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            hash_password = make_password(request.data['password'])
            data = serializer.validated_data
            data['password'] = hash_password
            #data['is_superuser'] = True
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)


class ProfileDetails(APIView):

    permission_classes([IsAuthenticated])

    def get_profile(self, pk):
        try:
            return Profile.objects.get(id = pk)
        except Profile.DoesNotExist:
            return Http404


    def get(self, request, pk, format = None):
        profile = self.get_profile(pk)
        serializer = ProfileSerializer(profile, many = False)
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        profile = self.get_profile(pk)
        serializer = ProfileSerializer(profile, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        profile = self.get_profile(pk)
        profile.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == "PUT" or self.request.method == "DELETE":
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

class SkillList(APIView):

   permission_classes([IsAuthenticated])

   def post(self, request, format = None):
       serializer = SkillSerializer(data = request.data)
       user = request.user.profile
       if serializer.is_valid():
           data = serializer.validated_data
           data['owner'] = user
           serializer.save()
           return Response(serializer.data, status = status.HTTP_201_CREATED)

   def get_permissions(self) :
       if self.request.method == "POST":
           return [IsAuthenticated()]


class SkillDetails(APIView):

    permission_classes([IsAuthenticated])

    def get_skill(self, pk):
        try:
            return Skill.objects.get(id = pk)
        except Skill.DoesNotExist:
            return Http404

    def put(self, request, pk, format = None):
        skill = self.get_skill(pk)
        profile = request.user.profile
        serializer = SkillSerializer(skill, data = request.data)
        if serializer.is_valid() and skill.owner == profile:
            serializer.save()
            return Response(serializer.data)
        return Response(status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        skill = self.get_skill(pk)
        profile = request.user.profile
        if skill.owner == profile:
            skill.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == "PUT" or self.request.method == "DELETE":
            return [IsAuthenticated()]
        else:
            return [AllowAny()]


class MessageList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        messages = profile.messages.all()
        done, result = utils.MessagePaginate(request, messages)
        if done :
            return result
        else :
            serializer = MessageSerializer(messages, many = True)
            return Response(serializer.data)

    def post(self, request):
        profile = request.user.profile
        serializer = MessageSerializer(data = request.data)
        if serializer.is_valid() :
            data = serializer.validated_data
            if data['recipient'] != profile:
                data['sender'] = profile
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(status = status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == "GET" and self.request.method == "POST":
            return [IsAuthenticated()]
        else :
            return [AllowAny()]


class MessageDetails(APIView):

    permission_classes = [IsAuthenticated]

    def get_message(self, pk):
        try:
            return Message.objects.get(id = pk)
        except Message.DoesNotExist:
            Http404

    def get(self, request, pk, format = None):
        profile = request.user.profile
        message = self.get_message(pk)
        if message.recipient == profile:
            if message.is_read == False:
                message.is_read = True
                message.save()
            serializer = MessageSerializer(message, many = False)
            return Response(serializer.data)

    def delete(self, request, pk, format = None):
        profile = request.user.profile
        message = self.get_message(pk)
        if profile == message.recipient:
            message.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == 'GET' and "DELETE" :
            return [IsAuthenticated()]
        else :
            return [AllowAny]









