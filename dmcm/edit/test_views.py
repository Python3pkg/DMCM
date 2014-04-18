"""DMCM Edit Views Unit Test."""

from __future__ import absolute_import

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.views.decorators.csrf import csrf_exempt

from ..models import Page


class PageCreateUpdateTest(TestCase):
    """Create and Update Page."""

    @csrf_exempt
    def test_create_and_update_page(self):
        """Make use of the Create and Update Page views"""
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
                                     'content': '# Test Content',
                                     })

        self.assertEqual(response.status_code,
                         302,
                         'Unexpected status code on add, got %s expected 302' %
                             (response.status_code))

        test_page = Page.objects.get(slug='test-page')

        # Update the test Page
        response = self.client.post('/dmcm/edit/test-page/',
                                    {'title': 'Test Page',
                                     'slug': 'test-page',
                                     'parent': '1',  # Homepage in initial_data
                                     'content': '# Test Content Updated',
                                     })

        self.assertEqual(response.status_code,
                         302,
                         'Unexpected status code on add, got %s expected 302' %
                             (response.status_code))
