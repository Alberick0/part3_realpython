from django.test import TestCase, RequestFactory
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve

import django_ecommerce.settings as settings

from payments.models import User

from payments.forms import SigninForm
from payments.forms import UserForm, CardForm

from payments.views import sign_out, soon, register

import unittest
import mock


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # user
        cls.test_user = User(email='test@testing.com', name='test user')
        cls.test_user.save()

        # request
        cls.request = RequestFactory().get('/')

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


class FormTesterMixin:
    def assertFormError(self, form_cls, expected_error_name,
                        expected_error_msg, data):
        from pprint import pformat
        test_form = form_cls(data=data)

        # if we get an error then the form should not be valid
        self.assertFalse(test_form.is_valid())

        self.assertEquals(
            test_form.errors[expected_error_name],
            expected_error_msg,
            msg="Expected {} : Actual {}: using data {}".format(
                test_form.errors[expected_error_name], expected_error_msg,
                pformat(data))
        )


class FormTests(unittest.TestCase, FormTesterMixin):
    def test_signing_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': {'email': 'j@j.com'},
             'error': ('password', [u'This field is required.'])},
            {'data': {'password': '1234'},
             'error': ('email', [u'This field is required.'])}
        ]

        for invalid_data in invalid_data_list:
            self.assertFormError(SigninForm, invalid_data['error'][0],
                                 invalid_data['error'][1], invalid_data['data'])

    def test_user_form_passwords_match(self):
        form = UserForm(
            {
                'name': 'jj',
                'email': 'j@j.com',
                'password': '1234',
                'ver_password': '1234',
                'last_4_digitss': '1123',
                'stripe_token': '1'
            })

        # Is the data valid? -- If not print out the errors
        self.assertTrue(form.is_valid(), form.errors)

        # This will throw an error if the form doesn't clean
        self.assertIsNotNone(form.clean())

    def test_user_form_passwords_dont_match_throws_error(self):
        form = UserForm(
            {
                'name': 'jj',
                'email': 'j@j.com',
                'password': '234',  # bad pass
                'ver_password': '1234',
                'last_4_digitss': '1123',
                'stripe_token': '1'
            })

        # Is the data valid?
        self.assertFalse(form.is_valid())

        # self.assertRaisesMessage(forms.ValidationError, 'Passwords do not '
        #                                                 'match', form.clean)

    def test_card_form_data_validates_invalid_data(self):
        invalid_data_list = [
            {'data': {'last_4_digitss': '123'},
             'error': ('last_4_digitss', [u'Ensure this value has at least 4 '
                                         u'characters (it has 3).'])},
            {'data': {'last_4_digitss': '12345'},
             'error': ('last_4_digitss', [u'Ensure this value has at most 4 '
                                         u'characters (it has 5).'])}
        ]

        for invalid_data in invalid_data_list:
            self.assertFormError(CardForm, invalid_data['error'][0],
                                 invalid_data['error'][1], invalid_data['data'])


class RegisterPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/register'
        cls.request = RequestFactory().get(cls.url)

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

    def test_register_resolves_to_right_view(self):
        register_url = resolve(self.url)

        self.assertEquals(register_url.func, register)

    def test_register_returns_appropriate_response_code(self):
        register_code = self.client.get(self.url)

        self.assertEquals(register_code.status_code, 200)

    def test_register_returns_correct_html(self):
        register_html = register(self.request)

        self.assertEquals(self.html.content, register_html.content)

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

    def test_registering_new_user_returns_successfully(self):
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

        with mock.patch('stripe.Customer') as stripe_mock:
            config = {'create.return_value': mock.Mock()}
            stripe_mock.configure_mock(**config)

            resp = register(self.request)

            # self.assertEquals(resp.content, "")
            # self.assertEquals(resp.status_code, 302)
            # self.assertEquals(self.request.session['user'], 1)

            # verify the user was actually stored in the DB
            User.objects.get(email='python@rocks.com')
