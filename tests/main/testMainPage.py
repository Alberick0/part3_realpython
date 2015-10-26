import mock
from django.test import TestCase, override_settings
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from django.test import RequestFactory

from main.views import index
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
    @override_settings(DEBUG_TOOLBAR_CONFIG={'DEBUG_TOOLBAR_CONFIG': False})
    def test_returns_exact_html(self):
        index = self.client.get('/')
        html = render_to_response('main/index.html')
        self.assertEquals(index.content, html.content)

    def test_index_handles_logged_in_user(self):
        """
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
            'main/user.html', {'user': user}).content)

    def test_verifies_index_user_foreignkey_badge_is_stabilised(self):
        # create a session that appears to have a logged in user
        self.request.session = {'user': '1'}

        # setup dummy user
        # we need to save user so user -> badges relationship is created
        u = User(email='test@user.com')
        u.save()

        with mock.patch('main.views.User') as user_mock:
            # tell mock what to do when called
            config = {'get_by_id.return_value': u}
            user_mock.configure_mock(**config)

            # run the test
            resp = index(self.request)

            # ensure we return the state of the session back to normal
            self.request.session = {}
            u.delete()

            """
            We are now sending a lot of state for logged in users, rather
            than recreating that all here, let's just check for some text
            that should only be present when we are logged in
            """

            self.assertContains(resp, "Report back to base")
