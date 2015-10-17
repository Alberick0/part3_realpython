import mock
import django_ecommerce.settings as settings

from django import forms
from django.test import TestCase, RequestFactory
from django.shortcuts import render_to_response
from django.db import IntegrityError

from payments.models import User
from payments.views import sign_out, register, soon


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # user
        cls.test_user = User(email='test@testing.com', name='test user')
        cls.test_user.save()

        # request
        cls.request = RequestFactory().get('/')

    def get_MockUserForm(self):
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

    def test_user_to_string_print_email(self):
        self.assertEquals(str(self.test_user), 'test@testing.com')

    def test_get_by_id(self):
        self.assertEquals(User.get_by_id(1), self.test_user)

    # -- Testing logout -- #
    def test_user_logout_functionality_works(self):
        """
        Test that logout clears the session
        """
        self.request.session = {'user': '1'}

        sign_out(self.request)
        self.assertEquals(self.request.session, {})

    def test_create_user_function_stores_in_database(self):
        """
        Tests User.create method
        """
        new_user = User.create('jean', 'jean_test@hotmail.com', 'password',
                               '1234', '1')
        test = User.objects.get(email='jean_test@hotmail.com')

        self.assertEquals(test, new_user)

    def test_try_creating_existing_user_throws_IntegrityError(self):
        self.assertRaises(IntegrityError,
                          User.create, 'Jean Guzman', 'jeanalberick@gmail.com',
                          'password', '1234', None)

    @mock.patch('payments.views.UserForm', get_MockUserForm)
    @mock.patch('payments.models.User.save', side_effect='IntegrityError')
    def test_registering_user_twice_cause_error_msg(self, save_mock):
        # request used to test the view
        my_request = RequestFactory()
        my_request.method = 'POST'
        my_request.POST = {}
        my_request.session = {}

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

        # mock out stripe to avoid their server
        with mock.patch('stripe.Customer') as stripe_mock:
            config = {'create.return_value': mock.Mock()}
            stripe_mock.configure_mock(**config)

            # run the test
            resp = register(my_request)

            # verify things are okay
            # self.assertEquals(resp.content, html.content)
            # self.assertEqual(resp.status_code, 200)
            # self.assertEqual(my_request.session, {})

            # assert there is no records in the DB
            users = User.objects.filter(email='jeanalberick@gmail.com')
            self.assertEqual(len(users), 0)
