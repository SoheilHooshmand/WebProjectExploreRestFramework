from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from profiles.models import Profile, Skill, Message
from django.contrib.auth.models import User


class ProfilelistTest(TestCase):

    def setUp(self):
        self.client = APIClient()


    def test_get_profiles(self):

        response = self.client.get('/profiles/')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_post_profiles(self):

        data = {
            'first_name' : 'Sohrab',
            'email' : 'Sohrab@gmail.com',
            'username' : 'Sohi',
            'password' : '1234'
        }

        response = self.client.post('/profiles/', data = data, format = 'json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class ProfileDetailsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(first_name = 'Ali', email = 'Ali@gmail.com', username = 'ali', password = '1234')
        self.client.force_authenticate(user = self.user)


    def test_get_profile(self):

        response = self.client.get(f'/profiles/profile/{self.user.profile.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_put_profile(self):

        data = {
            'name' : 'Soheil',
            'email' : 'Soheil@gmail.com'
        }

        response = self.client.put(f'/profiles/profile/{self.user.profile.id}/', data = data, format = 'json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_profile(self):

        response = self.client.delete(f'/profiles/profile/{self.user.profile.id}/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

class SkillListTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(first_name = 'Ali', email = 'ali@gamil.com', username = 'ali', password = '1234')
        self.client.force_authenticate(user = self.user)

    def test_post_skills(self):

        data = {
            'owner' : self.user.profile.id,
            'name' : 'Python',
            'description' : 'I love python'
        }

        response = self.client.post(f'/profiles/skills/', data = data, format = 'json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class SkillDetailsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(first_name = 'Ali', email = 'Ali@gmail.com', username = 'ali', password = '1234')
        self.client.force_authenticate(user = self.user)
        self.skill = Skill.objects.create(owner = self.user.profile, name = 'Python', description = 'I love python')

    def test_put_skill(self):

        data = {
            'name' : 'Java',
            'description' : 'I love java'
        }

        response = self.client.put(f'/profiles/skills/{self.skill.id}/', data = data, format = 'json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_skill(self):

        response = self.client.delete(f'/profiles/skills/{self.skill.id}/')

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class MessageListTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(first_name = 'Ali', email = 'Ali@gmail.com', username = 'ali', password = '1234')
        self.user1 = User.objects.create(first_name = 'Soheil', email = 'Soheil@gmail.com', username = 'soheil', password = '5676')
        self.message = Message.objects.create(sender = self.user.profile, recipient = self.user1.profile, name = 'a', subject = 'b', body = 'c')
        self.client.force_authenticate(user = self.user1)

    def test_get_messages(self):

        response = self.client.get('/profiles/messages/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_post_message(self):

        data = {
            'recipient' : self.user.profile.id,
            'name' : 'g',
            'subject' : 't',
            'body' : 'r'
        }

        response = self.client.post('/profiles/messages/', data = data, format = 'json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class MessageDetailsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(first_name = 'Ali', email = 'Ali@gmail.com', username = 'ali', password = '1234')
        self.user1 = User.objects.create(first_name = 'Soheil', email = 'Soheil@gmail.com', username = 'soheil', password = '5677')
        self.message = Message.objects.create(sender = self.user.profile, recipient = self.user1.profile, name = 'a', subject = 'b', body = 'c')
        self.client.force_authenticate(user = self.user1)

    def test_get_message(self):

        response = self.client.get(f'/profiles/messages/{self.message.id}/')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_message(self):

        response = self.client.delete(f'/profiles/messages/{self.message.id}/')

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

