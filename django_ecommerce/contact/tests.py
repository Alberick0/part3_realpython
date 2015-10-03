from django.shortcuts import render_to_response
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from .views import contact
from .forms import ContactForm


class ContactPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/contact/'
        cls.request = RequestFactory().get(cls.url)

    def test_returns_correct_html(self):
        resp = contact(self.request)
        self.request.session = {}
        html = render_to_response('contact.html', {'form': ContactForm()})
        self.assertEquals(resp.content, html.content)

    def test_contact_page_resolves_to_right_view(self):
        contact_page = resolve(self.url)

        self.assertEquals(contact_page.func, contact)

    def test_contact_page_returns_appropriate_status_code(self):
        contact_page = self.client.get(self.url)

        self.assertEquals(contact_page.status_code, 200)

