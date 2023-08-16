from django.test import TestCase
from profiles.models import Profile, Skill, Message

class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.profile = Profile.objects.create(name = 'Ali', email = 'Ali@gmail.com')
        cls.profile1 = Profile.objects.create(name = 'Soheil', email = "Soheil@gmail.com")
        cls.skill = Skill.objects.create(owner = cls.profile, name = 'Python')
        cls.message = Message.objects.create(sender = cls.profile, recipient = cls.profile1, name = 'A', subject = 'B', body = 'C')


    def test_profile_creation(self):
        pro = Profile.objects.get(id = self.profile.id)

        self.assertEquals(pro.name, self.profile.name)
        self.assertEquals(pro.email, self.profile.email)

    def test_skill_creation(self):

        sk = Skill.objects.get(id = self.skill.id)

        self.assertEquals(sk.owner, self.profile)
        self.assertEquals(sk.name, self.skill.name)

    def test_message_creation(self):

        mes = Message.objects.get(id = self.message.id)

        self.assertEquals(mes.sender, self.profile)
        self.assertEquals(mes.recipient, self.profile1)
        self.assertEquals(mes.name, "A")
        self.assertEquals(mes.subject, "B")
        self.assertEquals(mes.body, "C")

