from django.test import SimpleTestCase
from django.urls import resolve, reverse
from profiles.views import ProfileList, ProfileDetails, SkillList, SkillDetails, MessageList, MessageDetails

class TestUrls(SimpleTestCase):

    def test_profilelist_url_resolves(self):
        url = reverse("profilelist")
        self.assertEquals(resolve(url).func.view_class, ProfileList)

    def test_profiledetails_url_resolves(self):
        url = reverse("profiledetails", args=['some-str'])
        self.assertEquals(resolve(url).func.view_class, ProfileDetails)

    def test_skilllist_url_resolves(self):
        url = reverse('skilllist')
        self.assertEquals(resolve(url).func.view_class, SkillList)

    def test_skilldetails_url_resolves(self):
        url = reverse("skilldetails", args=['some-str'])
        self.assertEquals(resolve(url).func.view_class, SkillDetails)

    def test_messagelist_url_resolves(self):
        url = reverse('messagelist')
        self.assertEquals(resolve(url).func.view_class, MessageList)

    def test_messagedetails_url_resolves(self):
        url = reverse('messagedetails', args=['some-str'])
        self.assertEquals(resolve(url).func.view_class, MessageDetails)
