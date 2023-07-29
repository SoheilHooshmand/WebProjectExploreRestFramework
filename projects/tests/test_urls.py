from django.test import SimpleTestCase
from django.urls import resolve, reverse
from projects.views import ProjectList, PorjectDetails, ReviewList, TagList

class TestUrl(SimpleTestCase):

    def test_projectlist_url_resolves(self):
        url = reverse('projectlist')
        self.assertEquals(resolve(url).func.view_class, ProjectList)

    def test_projectdetails_url_resolves(self):
        url = reverse('projectdetails', args=['some-str'])
        self.assertEquals(resolve(url).func.view_class, PorjectDetails)

    def test_reviewlist_url_resolves(self):
        url = reverse('reviewlist', args=['some-str'])
        self.assertEquals(resolve(url).func.view_class, ReviewList)

    def test_taglist_url_resolves(self):
        url = reverse('taglist')
        self.assertEquals(resolve(url).func.view_class, TagList)