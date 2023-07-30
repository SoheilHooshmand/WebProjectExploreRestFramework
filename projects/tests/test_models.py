from django.test import TestCase
from projects.models import Project, Review, Tag
from profiles.models import Profile

class ProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.profile1 = Profile.objects.create(name = 'Ali', email = "ali@gmail.com")
        cls.profile2 = Profile.objects.create(name = 'Reza', email = 'reza@gmail.com')
        cls.tag = Tag.objects.create(name = "test tag")
        cls.project = Project.objects.create(
            name = 'project1',
            owner = cls.profile1,
            description = "about project1",
            demo_link = "demo_link",
            source_link = 'source_link'
        )
        cls.project.tags.add(cls.tag)
        cls.review = Review.objects.create(
            owner = cls.profile2,
            project = cls.project,
            body = "Greate",
            value = 'up'
        )



    def test_tag_creation(self):
        tag = Tag.objects.get(id = self.tag.id)

        self.assertEquals(tag.name, 'test tag')

    def test_review_creation(self):
        review = Review.objects.get(id = self.review.id)

        self.assertEquals(review.owner, self.profile2)
        self.assertEquals(review.project, self.project)
        self.assertEquals(review.body, 'Greate')
        self.assertEquals(review.value, 'up')

    def test_project_creation(self):
        project = Project.objects.get(id = self.project.id)

        self.assertEquals(project.name, 'project1')
        self.assertEquals(project.owner, self.profile1)
        self.assertEquals(project.description, 'about project1')
        self.assertEquals(project.demo_link, 'demo_link')
        self.assertEquals(project.source_link, 'source_link')

        tags = project.tags.all()
        self.assertEquals(tags.count(), 1)
        self.assertIn(self.tag, tags)

        reviews = project.review_set.all()
        self.assertEquals(reviews.count(), 1)
        self.assertIn(self.review, reviews)


    def test_string_representation(self):
        project = Project.objects.get(id = self.project.id)
        self.assertEquals(str(project), "project1")

    def test_reviewers_property(self):
        project = Project.objects.get(id = self.project.id)
        reviewers_id = project.reviewers
        self.assertListEqual(list(reviewers_id), [self.profile2.id])

    def test_getVoteCount_method(self):
        project = Project.objects.get(id = self.project.id)
        project.getVoteCount
        self.assertEquals(project.vote_total, 1)

    def test_review_unique_together_constraint(self):
        with self.assertRaises(Exception) as context:
            Review.objects.create(
                owner = self.profile2,
                project = self.project,
                body = "Not bad",
                value = 'up'
            )

        exception_message = str(context.exception)
        self.assertIn('Duplicate entry', exception_message)




