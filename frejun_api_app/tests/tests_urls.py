from django.test import SimpleTestCase
from django.urls import resolve, reverse
from frejun_api_app.views import *


class TestURLs(SimpleTestCase):
    def test_index_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_inbound_is_resolved(self):
        url = reverse('inbound')
        self.assertEquals(resolve(url).func, inbound)

    def test_outbound_is_resolved(self):
        url = reverse('outbound')
        self.assertEquals(resolve(url).func, outbound)
