from django.db import IntegrityError
from django.test import TestCase, RequestFactory

from payments.models import User
from payments.views import sign_out


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # user
        cls.test_user = User.create('test tester', 'test@testing.com', 'pass',
                                    '1234', 10)

        # request
        cls.request = RequestFactory().get('/')

    def test_user_to_string_print_email(self):
        self.assertEquals(str(self.test_user), 'test@testing.com')

    def test_get_by_id(self):
        self.assertEqual(User.get_by_id(self.test_user.id), self.test_user)

    # -- Testing logout -- #
    def test_create_user_function_stores_in_database(self):
        """
        Tests User.create method
        """
        user = User.objects.get(email='test@testing.com')

        self.assertEquals(user, self.test_user)

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

    def test_create_two_users_each_user_has_unique_bigCoID(self):
        user1 = User.create('tester test', 'testing@test.com', 'pass',
                            '1234', '11')

        user2 = User.create('tester testing', 'testing@tester.com', 'pass',
                            '1234', '12')

        self.assertNotEqual(user1.bigCoID, user2.bigCoID)
