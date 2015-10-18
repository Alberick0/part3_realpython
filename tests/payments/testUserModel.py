from django.test import TestCase, RequestFactory
from django.db import IntegrityError

from payments.models import User
from payments.views import sign_out


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
        self.assertEqual(User.get_by_id(1), self.test_user)

    # -- Testing logout -- #
    def test_create_user_function_stores_in_database(self):
        """
        Tests User.create method
        """
        new_user = User.create('jean', 'jean_test@hotmail.com', 'password',
                               '1234', '1')
        test = User.objects.get(email='jean_test@hotmail.com')

        self.assertEquals(test, new_user)

    def test_create_user_already_exists_throws_IntegrityError(self):
        self.assertRaises(
            IntegrityError,
            User.create,
            "test user",
            "test@testing.com",
            "jj",
            "1234",
            89
        )

    def test_user_logout_functionality_works(self):
        """
        Test that logout clears the session
        """
        self.request.session = {'user': '1'}

        sign_out(self.request)
        self.assertEquals(self.request.session, {})

