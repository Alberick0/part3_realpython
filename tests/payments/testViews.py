import socket
import mock
import django_ecommerce.settings as settings

from django.test import TestCase, RequestFactory
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from django.db import IntegrityError

from payments.forms import UserForm, SigninForm
from payments.views import register, soon, sign_out, sign_in
from payments.models import User


class ViewTesterMixin(object):
    @classmethod
    def setupViewTester(cls, url, view_func, expected_html, status_code=200,
                        session={}):
        request_factory = RequestFactory()
        cls.request = request_factory.get(url)
        cls.request.session = session
        cls.status_code = status_code
        cls.url = url
        cls.view_func = staticmethod(view_func)
        cls.expected_html = expected_html

    def test_resolves_to_right_view(self):
        test_view = resolve(self.url)
        self.assertEqual(test_view.func, self.view_func)

    def test_returns_appropriate_response_code(self):
        resp = self.view_func(self.request)
        self.assertEqual(resp.status_code, self.status_code)

    def test_returns_correct_html(self):
        resp = self.view_func(self.request)
        self.assertEqual(resp.content, self.expected_html)


class SingOutPageTests(TestCase, ViewTesterMixin):
    @classmethod
    def setUpTestData(cls):
        ViewTesterMixin.setupViewTester('/sign_out', sign_out, b'',
                                        status_code=302,
                                        session={'user': 'dummy'})


class SignInPageTests(TestCase, ViewTesterMixin):
    @classmethod
    def setUpTestData(cls):
        cls.html = render_to_response('sign_in.html',
                                      {'form': SigninForm(),
                                       'user': None})

        ViewTesterMixin.setupViewTester('/sign_in', sign_in, cls.html.content)


class RegisterPageTests(TestCase, ViewTesterMixin):
    @classmethod
    def setUpTestData(cls):
        cls.html = render_to_response(
            'register.html',
            {
                'form': UserForm(),
                'months': range(1, 12),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': range(2011, 2036),
            }
        )

        ViewTesterMixin.setupViewTester('/register', register, cls.html.content)

    def setUp(self):
        request_factory = RequestFactory()
        self.request = request_factory.get(self.url)

    def test_invalid_form_returns_registration_page(self):
        """
        This is an invalid form because the POST is being submitted empty
        """
        with mock.patch('payments.forms.UserForm.is_valid') as user_mock:
            user_mock.return_value = False  # needs explanation

            self.request.method = 'POST'
            self.request.POST = None
            resp = register(self.request)
            self.assertEquals(resp.content, self.html.content)

            # make sure that we did indeed call our is_valid function
            self.assertEquals(user_mock.call_count, 1)

    @mock.patch('payments.views.Customer.create')
    @mock.patch.object(User, 'create')  # mocks the create method from User
    def test_registering_new_user_returns_successfully(self, create_mock,
                                                       stripe_mock):
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'python@rocks.com',
            'name': 'pyRock',
            'stripe_token': '4242424242424242',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password',
        }

        # get the return values of the mocks
        new_user = create_mock.return_value
        new_cust = stripe_mock.return_value

        resp = register(self.request)

        # Added decode so it would return string instead of byte
        self.assertEquals(resp.content, b'')

        self.assertEquals(resp.status_code, 302)
        self.assertEquals(self.request.session['user'], new_user.pk)

        # verified the user was stored in the DB
        create_mock.assert_called_with('pyRock', 'python@rocks.com',
                                       'bad_password', '4242', new_cust.id)

    def get_MockUserForm(self):
        from django import forms

        class MockUserForm(forms.Form):
            def is_valid(self):
                return True

            @property
            def cleaned_data(self):
                return {
                    'email': 'python@rocks.com',
                    'name': 'pyRock',
                    'stripe_token': '...',
                    'last_4_digits': '4242',
                    'password': 'bad_password',
                    'ver_password': 'bad_password',
                }

            def addError(self, error):
                pass

        return MockUserForm()

    @mock.patch('payments.views.UserForm', get_MockUserForm)
    @mock.patch('payments.models.User.save', side_effect=IntegrityError)
    def test_registering_user_twice_cause_error_msg(self, save_mock):
        # create a session to push the data
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {}

        # create the expected html
        html = render_to_response(
            'register.html',
            {
                'form': self.get_MockUserForm(),
                'months': list(range(1, 12)),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': list(range(2011, 2036)),
            }
        )

        # mock stripe to avoid their server
        with mock.patch('payments.views.Customer') as stripe_mock:
            config = {'create.return_value': mock.Mock()}
            stripe_mock.configure_mock(**config)

            # run the test
            resp = register(self.request)

            # verify that we did things correctly
            self.assertEqual(resp.content, html.content)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.request.session, {})

            # assert there is no record in the db
            users = User.objects.filter(email='python@rocks.com')
            self.assertEqual(len(users), 0)

    def test_registering_user_when_stripe_is_down(self):
        # request used to test the view
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'python@rocks.com',
            'name': 'pyRock',
            'stripe_token': '',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password',
        }

        # mocking stripe and asking to threw an error
        with mock.patch('stripe.Customer.create',
                        side_effect=socket.error("Can't connect to Stripe")
                        ) as stripe_mock:

            # run test
            register(self.request)

            # assert there is a record in the db without Stripe id
            users = User.objects.filter(email='python@rocks.com')

            self.assertEquals(len(users), 1)
            self.assertEquals(users[0].stripe_id, '')