from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import index
from django.shortcuts import render_to_response
from django.test import RequestFactory
from payments.models import User


class MainPageTests(TestCase):
    # -- Setup --#
    @classmethod  # Function decorator that runs once at class creation
    def setUpTestData(cls):
        """
        Mocks a request, sets an empty session. This code is ran at class
        creation

        This method is new in django 1.8 and provides faster performance
        """
        # mock a request object, so we can manipulate the session
        cls.request = RequestFactory().get('/')

        # create a session that appears to have a logged user
        cls.request.session = {}

    # -- Testing routes --#
    def test_root_resolves_to_main_view(self):
        """
        uses resolve to get the view function for a path
        """
        main_page = resolve('/')
        self.assertEquals(main_page.func, index)

    def test_returns_appropriate_html_response_code(self):
        """
        self.client is a dummy web browser
        """
        index = self.client.get('/')
        self.assertEquals(index.status_code, 200)

    # -- Testing templates and views --#
    def test_returns_exact_html(self):
        index = self.client.get('/')
        self.assertEquals(index.content, render_to_response(
            'index.html').content)

    def test_index_handles_logged_in_user(self):
        """                                                 payments_user
        Verifies the right template is used with a logged user
        """
        # create the user needed for user lookup from index page
        user = User(name='test', email='test@testing.com')

        # saves user on DB
        user.save()

        # sets session value equals to user ID on DB
        self.request.session = {'user': '1'}

        # request the index page
        resp = index(self.request)

        # verify it return the page for the logged in user
        self.assertEquals(resp.content, render_to_response(
            'user.html', {'user': user}).content)
