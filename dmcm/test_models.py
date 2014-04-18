"""DMCM Models Unit Test."""

from django.test import TestCase

from .models import Page


class PageTest(TestCase):
    """
    Create and access Page.
    """
    def setUp(self):
        page = Page.objects.create(title='Test',
                                   slug='test',
                                   parent_id=1,
                                   content='# Test Content')
        sub_page = Page.objects.create(title='Test 2',
                                   slug='test-2',
                                   parent=page,
                                   content='# Test Content Two')

    def test_get_page(self):
        """Retrieve Page objects. Check their attributes."""
        pages = Page.objects.filter(slug='test')
        self.assertEqual(len(pages),
                         1,
                         'Wrong number of pages found: Got %s expected 1' % (len(pages)))
        page = pages[0]
        self.assertEqual(page.title,
                         'Test',
                         'Page: Unexpected title, got %s expected %s' % (page.title, 'Test'))
        absolute_url = page.get_absolute_url()
        self.assertEqual(absolute_url,
                         '/test/',
                         'Unexpected absolute url: Got %s expected "/test/"' % (absolute_url))

        subpage = Page.objects.get(slug='test-2')
        navigation_path = subpage.navigation_path()
        self.assertEqual(len(navigation_path),
                         2,
                         'Unexpected navigation path length: Got %s expected 2' % (len(navigation_path)))
        address = navigation_path[1]['address']
        self.assertEqual(address,
                         '/test/',
                         'Unexpected navigation path address: Got %s expected "/test/"' % (address))
