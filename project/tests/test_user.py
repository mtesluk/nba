from rest_framework.test import APIClient, APITestCase
from account.models import *
from django.contrib.auth.models import User


class UserTests(APITestCase):
    def setUp(self):
        client = APIClient()
        self.username = 'user1'
        self.password = 'pass1'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)

    def test_login(self):
        response = self.client.post('/api/v1/api-token-auth/', data={'username': 'user1', 'password': 'pass1'})
        data = response.json()

        self.assertTrue(data['token'])

    def test_get_user_data(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.get('/api/v1/auth-user')
        data = response.json()
        
        self.assertEqual(data['username'], self.username)
        self.assertFalse(data['is_superuser'])
        self.assertEqual(data['credits'], str(float(self.profile.credits)))

    def test_register_user(self):
        payload = {"username": "user2", "password": "pass2", "email": "m@m.pl", "first_name": "", "last_name": "", "site": "Wro"}
        response = self.client.post('/api/v1/auth-user', payload)
        data = response.json()
        
        self.assertEqual(data['username'], 'user2')
        self.assertEqual(data['username'], User.objects.get(username='user2').username)
