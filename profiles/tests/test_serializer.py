from django.test import TestCase
from profiles.models import Profile, Skill, Message
from profiles.serializer import ProfileSerializer, SkillSerializer, MessageSerializer
from datetime import datetime
from collections import OrderedDict

class ProfileSerializerTest(TestCase):

    def setUp(self):

        self.profile = Profile.objects.create(name = 'Ali', email = 'Ali@gmail.com')
        self.profile1 = Profile.objects.create(name = 'Soheil', email = 'Soheil@gmail.com')
        self.skill = Skill.objects.create(owner = self.profile, name = 'Python')
        self.message = Message.objects.create(sender = self.profile, recipient = self.profile1, name = 'A', subject = 'B', body = 'C')

        self.validated_data = {
            'name' : 'Mamad',
            'email' : 'Mamad@gmail.com'
        }


    def test_update_profile_serializer(self):
        serializer = ProfileSerializer(instance = self.profile)
        update_instance = serializer.update(self.profile, self.validated_data)

        self.assertEquals(update_instance.name, 'Mamad')
        self.assertEquals(update_instance.email, "Mamad@gmail.com")

    def test_profile_serializer(self):
        serializer = ProfileSerializer(instance = self.profile)

        created_datetime = datetime.strptime(str(self.profile.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime = created_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        created_datetime1 = datetime.strptime(str(self.skill.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime1 = created_datetime1.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        expected_data = {
            'user' : None,
            'name' : 'Ali',
            'email' : 'Ali@gmail.com',
            'username' : None,
            'short_intro' : None,
            'bio' : None,
            'profile_image' : None,
            'social_github' : None,
            'social_linkedin' : None,
            'social_twitter' : None,
            'social_youtube' : None,
            'social_website' : None,
            'created' : formatted_datatime,
            'id' : str(self.profile.id),
            'skills' : [
                OrderedDict(
                    [
                        ('id', str(self.skill.id)),
                        ('name', self.skill.name),
                        ('description', self.skill.description),
                        ('created', formatted_datatime1),
                        ('owner', self.profile.id)
                    ]
                )
            ]
        }

        self.assertDictEqual(serializer.data, expected_data)

    def test_skill_serializer(self):
        serializer = SkillSerializer(instance = self.skill)

        created_datetime = datetime.strptime(str(self.skill.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime = created_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        expected_data = {
            'owner' : self.profile.id,
            'name' : self.skill.name,
            'description' : self.skill.description,
            'created' : formatted_datatime,
            'id' : str(self.skill.id)
        }

        self.assertDictEqual(serializer.data, expected_data)

    def test_message_serializer(self):

        serializer = MessageSerializer(instance = self.message)

        created_datetime = datetime.strptime(str(self.message.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime = created_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        expected_data = {
            'sender' : self.profile.id,
            'recipient' : self.profile1.id,
            'name' : self.message.name,
            'email' : self.message.email,
            'subject' : self.message.subject,
            'body' : self.message.body,
            'is_read' : self.message.is_read,
            'created' : formatted_datatime,
            'id' : str(self.message.id)
        }

        self.assertDictEqual(serializer.data, expected_data)