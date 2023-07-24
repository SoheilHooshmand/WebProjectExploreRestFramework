from .serializer import ProjectSerilaizer
from rest_framework.pagination import PageNumberPagination
from .models import Tag, Project
from django.db.models import Q

class MyPaginate(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100

def paginate(request, projects):
    pagination_class = MyPaginate()
    page = pagination_class.paginate_queryset(projects, request)
    done = False
    result = None
    if page is not None:
        done = True
        serliazer = ProjectSerilaizer(page, many = True)
        result =  pagination_class.get_paginated_response(serliazer.data)
    return done, result


def search_project(request):
    search_query = ""
    if request.GET.get("search_query") :
        search_query = request.GET.get("search_query")
    tags = Tag.objects.filter(name__icontains = search_query)
    projects = Project.objects.distinct().filter(Q(name__icontains = search_query) |
                                                 Q(description__icontains = search_query) |
                                                 Q(owner__name__icontains = search_query) |
                                                 Q(tags__in = tags))
    return projects



