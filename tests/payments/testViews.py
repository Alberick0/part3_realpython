import socket

import mock
from django.test import TestCase, RequestFactory
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from django.db import IntegrityError, transaction, DatabaseError

import django_ecommerce.settings as settings
from payments.forms import UserForm, SigninForm
from payments.views import register, soon, sign_out, sign_in
from payments.models import User, UnPaidUsers


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
    def setUpClass(cls):
        super().setUpClass()
        html = render_to_response(
            'register.html',
            {
                'form': UserForm(),
                'months': list(range(1, 12)),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': list(range(2011, 2036)),
            })

        ViewTesterMixin.setupViewTester('/register', register, html.content)

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
            self.assertEquals(resp.content, self.expected_html)

            # make sure that we did indeed call our is_valid function
            self.assertEquals(user_mock.call_count, 1)

    def get_mock_cust():
        class mock_cust:
            @property
            def id(self):
                return 1234

        return mock_cust()

    @mock.patch('payments.views.Customer.create', return_value=get_mock_cust())
    def test_registering_new_user_returns_successfully(self, stripe_mock):
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'python@rocks.com',
            'name': 'pyRock',
            'stripe_token': '...',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password',
        }

        resp = register(self.request)

        # Added decode so it would return string instead of byte
        self.assertEqual(resp.content, b'')
        self.assertEqual(resp.status_code, 302)

        users = User.objects.filter(email='python@rocks.com')
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].stripe_id, '1234')

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
            'stripe_token': '...',
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
            unpaid = UnPaidUsers.objects.filter(email="python@rocks.com")

            self.assertEquals(len(unpaid), 1)
            # Makes sure there was a notification
            self.assertIsNotNone(unpaid[0].last_notification)

            self.assertEquals(len(users), 1)
            self.assertEquals(users[0].stripe_id, '')

    @mock.patch('payments.models.UnPaidUsers.save', side_effect=IntegrityError)
    def test_registering_user_when_stripe_is_down_all_or_nothing(self,
                                                                 save_mock):

        # create the request used to test the view
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'python@rocks.com',
            'name': 'pyRock',
            'stripe_token': '...',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password',
        }

        # mock out stripe to return a connection error
        with mock.patch('stripe.Customer.create', side_effect=socket.error(
                "can't connect to stripe")) as stripe_mock:
            # run the test
            resp = register(self.request)

            # assert there is no new record in the DB
            users = User.objects.filter(email='pyton@rocks.com')
            self.assertEquals(len(users), 0)

            # check the associated table has no updated data
            unpaid = UnPaidUsers.objects.filter(email='python@rocks.com')
            self.assertEquals(len(unpaid), 0)

    @transaction.atomic()
    def save_points(self, save=True):
        user = User.create('jj', 'inception', 'jj', '1234', '...')
        sp1 = transaction.savepoint()

        user.name = 'starting down the rabbit hole'
        user.save()

        user.stripe_id = 4
        user.save()

        if save:
            transaction.savepoint_commit(sp1)
        else:
            transaction.savepoint_rollback(sp1)

        try:
            with transaction.atomic():
                user.create('limbo', 'illbehere@forever', 'mind blown', '1111')

            if not save:
                raise DatabaseError

        except DatabaseError:
            pass

    def test_savepoint_roolbacks(self):
        self.save_points(False)

        # verify that everything was stored
        users = User.objects.filter(email='inception')
        self.assertEquals(len(users), 1)

    def test_savepoint_rollbacks(self):
        self.save_points(False)

        # verify that everything was stored
        users = User.objects.filter(email='inception')
        self.assertEquals(len(users), 1)

        # note the values here are from the original create call
        self.assertEquals(users[0].stripe_id, '')
        self.assertEquals(users[0].name, 'jj')

        # this save point was rolled back because of DatabaseError
        limbo = User.objects.filter(email='illbehere@forever')
        self.assertEquals(len(limbo), 0)

    def test_savepoint_commit(self):
        self.save_points(True)

        # verify that everything was stored
        users = User.objects.filter(email='inception')
        self.assertEquals(len(users), 1)

        # note the values here are from the update calls
        self.assertEquals(users[0].stripe_id, '4')
        self.assertEquals(users[0].name, 'staring down the rabbit hole')

        # save point was committed by exiting the context_manager without an
        # exception
        limbo = User.objects.filter(email='illbehere@forever')
        self.assertEquals(len(limbo), 1)
