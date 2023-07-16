from rest_framework.pagination import PageNumberPagination
from .serializer import ProfileSerializer, MessageSerializer
from .models import Profile, Skill
from django.db.models import Q

class MyPaginate(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100

def ProfilePaginate(request, profiles):
    pagination_class = MyPaginate()
    page = pagination_class.paginate_queryset(profiles, request)
    done = False
    result = None
    if page is not None:
        done = True
        serializer = ProfileSerializer(page, many = True)
        result = pagination_class.get_paginated_response(serializer.data)
    return done, result

def MessagePaginate(request, messages):
    pagination_class = MyPaginate()
    page = pagination_class.paginate_queryset(messages, request)
    done = False
    result = None
    if page is not None:
        done = True
        serializer = MessageSerializer(page, many = True)
        result = pagination_class.get_paginated_response(serializer.data)
    return done, result

def search_profiles(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get('search_query')
    skills = Skill.objects.filter(name__icontains = search_query)
    profiles = Profile.objects.distinct().filter(Q(name__icontains = search_query) |
                                                 Q(short_intro__icontains = search_query) |
                                                 Q(skill__in = skills))
    return profiles