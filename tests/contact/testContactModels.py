from datetime import datetime, timedelta

from django.test import TestCase, RequestFactory, SimpleTestCase
from django.core.urlresolvers import resolve
from contact.views import contact
from contact.forms import ContactForm, ContactView


class ContactPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/contact/'
        cls.request = RequestFactory().get(cls.url)
        cls.request.session = 1
        cls.firstUser = ContactForm(
            email="first@first.com",
            name="first",
            timestamp=datetime.today() + timedelta(days=2)
        )
        cls.firstUser.save()

    def test_contact_page_resolves_to_right_view(self):
        contact_page = resolve(self.url)

        self.assertEquals(contact_page.func, contact)

    def test_contact_form_str_returns_email(self):
        self.assertEqual("first@first.com", str(self.firstUser))

    def test_ordering(self):
        contacts = ContactForm.objects.all()
        self.assertEqual(self.firstUser, contacts[0])


class ContactViewTests(SimpleTestCase):
    def test_displayed_fields(self):
        expected_fields = ['name', 'email', 'topic', 'message']
        self.assertEqual(ContactView.Meta.fields, expected_fields)
