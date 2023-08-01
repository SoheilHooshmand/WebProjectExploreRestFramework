from django.test import TestCase
from projects.models import Project, Review, Tag
from profiles.models import Profile
from projects.serializer import ProjectSerilaizer, ReviewSerilaizer, TagSerilaizer
from datetime import datetime
from collections import OrderedDict

class ProjectsSerializerClass(TestCase):

    def setUp(self):
        self.tag1 = Tag.objects.create(name = 'tag1')
        self.tag2 = Tag.objects.create(name = 'tag2')
        self.profile1 = Profile.objects.create(name = 'Soheil', email = "soheil@gmail.com")
        self.profile2 = Profile.objects.create(name = "Ali", email = "ali@gmail.com")
        self.project = Project.objects.create(
            name = 'project1',
            owner = self.profile1,
            description = 'description',
            demo_link = 'demo_link',
            source_link = 'source_link'
        )
        self.project.tags.add(self.tag1)
        self.review = Review.objects.create(
            owner = self.profile2,
            project = self.project,
            body = 'Greate',
            value = 'up'
        )

        self.validated_data = {
            'name' : 'project2',
            'owner' : self.profile1,
            'description' : "new description",
            'tags' : [
                {
                    'name' : self.tag2.name,
                    'id' : self.tag2.id
                }
            ],
            'demo_link' : 'new demo_link',
            'source_link' : 'new source_link'
        }


    def test_update_project_serilaizer(self):
        serializer = ProjectSerilaizer(instance = self.project)
        update_instance = serializer.update(self.project, self.validated_data)

        self.assertEquals(update_instance.name, 'project2')
        self.assertEquals(update_instance.owner, self.profile1)
        self.assertEquals(update_instance.description, 'new description')
        self.assertEquals(update_instance.demo_link, 'new demo_link')
        self.assertEquals(update_instance.source_link, 'new source_link')
        self.assertEquals(update_instance.tags.count(), 1)
        self.assertTrue(Tag.objects.filter(name = 'tag2').exists())

    def test_project_serializer(self):
        serializer = ProjectSerilaizer(instance = self.project)

        created_datetime = datetime.strptime(str(self.project.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime = created_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        created_datetime1 = datetime.strptime(str(self.tag1.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime1 = created_datetime1.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        created_datetime2 = datetime.strptime(str(self.profile2.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime2 = created_datetime2.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        created_datetime3 = datetime.strptime(str(self.review.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime3 = created_datetime3.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        created_datetime4 = datetime.strptime(str(self.profile1.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime4 = created_datetime4.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


        expected_data = {'id': str(self.project.id),
                         'owner': OrderedDict([('id', str(self.profile1.id)),
                                               ('name', 'Soheil'),
                                               ('email', 'soheil@gmail.com'),
                                               ('username', None),
                                               ('short_intro', None),
                                               ('bio', None),
                                               ('profile_image', None),
                                               ('social_github', None),
                                               ('social_linkedin', None),
                                               ('social_twitter', None),
                                               ('social_youtube', None),
                                               ('social_website', None),
                                               ('created', formatted_datatime4),
                                               ('user', None)]),
                         'tags': [OrderedDict([('id', str(self.tag1.id)),
                                               ('name', 'tag1'),
                                               ('created', formatted_datatime1)])],
                         'reviews': [OrderedDict([('id', str(self.review.id)),
                                                  ('owner', OrderedDict([('id', str(self.profile2.id)),
                                                                         ('name', 'Ali'),
                                                                         ('email', 'ali@gmail.com'),
                                                                         ('username', None),
                                                                         ('short_intro', None),
                                                                         ('bio', None),
                                                                         ('profile_image', None),
                                                                         ('social_github', None),
                                                                         ('social_linkedin', None),
                                                                         ('social_twitter', None),
                                                                         ('social_youtube', None),
                                                                         ('social_website', None),
                                                                         ('created', formatted_datatime2),
                                                                         ('user', None)])),
                                                  ('body', 'Greate'),
                                                  ('value', 'up'),
                                                  ('created', formatted_datatime3),
                                                  ('project', self.project.id)])],
                         'name': 'project1',
                         'image': None,
                         'description': 'description',
                         'demo_link': 'demo_link',
                         'source_link': 'source_link',
                         'vote_total': 0,
                         'vote_ratio': 0,
                         'created': formatted_datatime}

        self.assertDictEqual(serializer.data, expected_data)


    def test_review_serializer(self):
        serializer = ReviewSerilaizer(instance = self.review)

        created_datetime = datetime.strptime(str(self.review.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime = created_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        created_datetime1 = datetime.strptime(str(self.profile2.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime1 = created_datetime1.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        expected_data = {
            'id': str(self.review.id),
            'owner': OrderedDict(
                [('id', str(self.profile2.id)),
                 ('name', 'Ali'),
                 ('email', 'ali@gmail.com'),
                 ('username', None),
                 ('short_intro', None),
                 ('bio', None),
                 ('profile_image', None),
                 ('social_github', None),
                 ('social_linkedin', None),
                 ('social_twitter', None),
                 ('social_youtube', None),
                 ('social_website', None),
                 ('created', formatted_datatime1),
                 ('user', None)]),
            'body': 'Greate',
            'value': 'up',
            'created': formatted_datatime,
            'project': self.project.id
        }


        self.assertDictEqual(serializer.data, expected_data)


    def test_tag_serializer(self):
        seriaziler = TagSerilaizer(instance = self.tag1)

        created_datetime = datetime.strptime(str(self.tag1.created), '%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datatime = created_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        expected_data = {
            'id' : str(self.tag1.id),
            'name' : self.tag1.name,
            'created' : formatted_datatime,
        }

        self.assertDictEqual(seriaziler.data, expected_data)






