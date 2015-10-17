import socket
import mock
import django_ecommerce.settings as settings

from django.test import TestCase, RequestFactory
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve

from payments.forms import UserForm
from payments.views import register, soon
from payments.models import User


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
        self.assertEquals(resp.content.decode('utf-8'), '')

        self.assertEquals(resp.status_code, 302)
        self.assertEquals(self.request.session['user'], new_user.pk)

        # verified the user was stored in the DB
        create_mock.assert_called_with('pyRock', 'python@rocks.com',
                                       'bad_password', '4242', new_cust.id)

    def test_registering_user_when_stripe_is_down(self):
        # request used to test the view
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
