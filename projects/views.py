from .models import Project, Review
from .serializer import TagSerilaizer, ReviewSerilaizer, ProjectSerilaizer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from . import utils


class ProjectList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format = None) :
        projects = utils.search_project(request)
        done, result = utils.paginate(request, projects)
        if done == True:
            return result
        else:
            serializer = ProjectSerilaizer(projects, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, format = None) :
        profile = request.user.profile
        data = request.data
        project, created = Project.objects.get_or_create(
            owner = profile,
            name = data['name']
        )
        project.image = data['image']
        project.description = data['description']
        project.demo_link = data['demo_link']
        project.source_link = data['source_link']
       tags_data = data['tags']
        for tag_data in tags_data:
            tag_name = tag_data['name']
            tag_id = tag_data["id"]
            tag, created = Tag.objects.get_or_create(
                name = tag_name,
                id = tag_id
            )
            project.tags.add(tag)
            project.save()
        serializer = ProjectSerilaizer(project)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

class PorjectDetails(APIView):

    permission_classes = [IsAuthenticated]

    def get_project(self, pk):
        try:
            return Project.objects.get(id = pk)
        except Project.DoesNotExist:
            return Http404

    def get(self, request, pk, format = None):
        project = self.get_project(pk)
        serializer = ProjectSerilaizer(project, many = False)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request, pk, format = None):
       profile = request.user.profile
       project = self.get_project(pk)
       if profile == project.owner:
           serializer = ProjectSerilaizer(project, data = request.data)
           serializer.owner = project.owner
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status = status.HTTP_200_OK)
           return Response(status = status.HTTP_400_BAD_REQUEST)
       else:
           return Response(status = status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format = None):
        profile = request.user.profile
        project = self.get_project(pk)
        if profile == project.owner :
            project.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == "PUT":
            return [IsAuthenticated()]
        elif self.request.method == "DELETE":
            return [IsAuthenticated()]
        else:
            return [AllowAny()]


class ReviewList(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format = None):
        project = Project.objects.get(id = pk)
        profile = request.user.profile
        data = request.data
        if profile != project.owner :
            review, created = Review.objects.get_or_create(
                owner = profile,
                project = project
            )
            review.body = data['body']
            review.value = data['value']
            review.save()
            project.getVoteCount
            serializer = ReviewSerilaizer(review, many = False)
            if created == True:
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else :
            return Response(status = status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]




class TagList(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, format = None):
        serializer = TagSerilaizer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]

