from django.test import TestCase
from django.contrib.auth.models import User
from nba.models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.email = 'user@testuser.com'
        self.location = 'Bielsko-Biala'

    def test_profile(self):
        user_obj = User.objects.create(username=self.username, email=self.email)
        profile_obj = Profile.objects.create(location=self.location, user=user_obj)

        self.assertEqual(profile_obj.location, self.location)
        self.assertEqual(profile_obj.user.username, self.username)
        self.assertEqual(profile_obj.user.email, self.email)
