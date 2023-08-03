from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from projects.models import Tag, Project
from datetime import datetime
from profiles.models import Profile


class TestProjectList(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username = 'username', password = "password")
        self.tag1 = Tag.objects.create(name = 'tag1')
        self.client.force_authenticate(user = self.user)


    def test_get_projects(self):
        response = self.client.get('/projects/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_post_projects(self):
        data = {
            'name' : 'project1',
            'image' : 'image1',
            'description' : "description1",
            'demo_link' : 'demo_link1',
            'source_link' : "source_link1",
            'tags' : [
                {
                    'name' : self.tag1.name,
                    'id' : str(self.tag1.id)
                }
            ]
        }

        response = self.client.post('/projects/', data = data, format = 'json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)



class TestProjectDetails(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.tag = Tag.objects.create(name = 'tag1')
        self.project = Project.objects.create(name='Test project', owner=self.user.profile)
        self.project.tags.add(self.tag)

    def test_get_project(self):
        response = self.client.get(f'/projects/project/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_put_project(self):

        data = {
            'name' : 'update project',
            'tags' : [
                {
                    'name' : 'tag1'
                }
            ]
        }

        response = self.client.put(f'/projects/project/{self.project.id}/', data = data, format = 'json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)


    def test_delete_project(self):

        response = self.client.delete(f'/projects/project/{self.project.id}/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class TestReviewList(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username = 'username', password = 'password')
        self.project = Project.objects.create(name = 'test project')
        self.tag = Tag.objects.create(name = 'tag')
        self.project.tags.add(self.tag)
        self.client.force_authenticate(user = self.user)


    def test_post_reviews(self):

       data = {
           'body' : 'good',
           'value' : 'up'
       }

       response = self.client.post(f'/projects/review/{self.project.id}/', data = data, format = 'json')
       self.assertEquals(response.status_code, status.HTTP_201_CREATED)


class TestTagList(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username = 'username', password = 'password', is_staff = True)
        self.client.force_authenticate(user = self.admin_user)



    def test_post_tags(self):

        data = {
            'name' : 'tag'
        }

        responses = self.client.post('/projects/tag/', data = data, format = 'json')
        self.assertEquals(responses.status_code, status.HTTP_201_CREATED)

