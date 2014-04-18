"""DMCM Views Unit Test."""

from __future__ import absolute_import

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client

from .models import Page


class SearchViewTest(TestCase):
    """Search for Pages."""

    def test_search_view(self):
        """Use the search view"""
        self.user = get_user_model().objects.create_user('john',
                                                         'john@montypython.com',
                                                         'password')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client = Client()
        self.client.login(username='john', password='password')

        # Create a Page
        response = self.client.post('/dmcm/edit/page/add/',
                                    {'title': 'Test Page',
                                     'slug': 'test-page',
                                     'parent': '1',  # Homepage in initial_data
                                     'content': 'Test Content',
                                     })

        self.assertEqual(response.status_code,
                         302,
                         'Unexpected status code on add, got %s expected 302' %
                             (response.status_code))

        test_page = Page.objects.get(slug='test-page')

        # Search for the test Page
        response = self.client.get('/search/?search_string=Test+Content')

        self.assertEqual(response.status_code,
                         200,
                         'Unexpected status code on search, got %s expected 200' %
                             (response.status_code))

        self.assertContains(response,
                            'Search Results')
