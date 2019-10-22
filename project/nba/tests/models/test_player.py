from django.test import TestCase
from nba.models import Player


class PlayerTestCase(TestCase):
    def setUp(self):
        self.name = 'LeBron James'
        self.age = 34
        self.position = 'SF'

    def test_player(self):
        player_obj = Player.objects.create(name=self.name, age=self.age, position=self.position)

        self.assertEqual(player_obj.name, self.name)
        self.assertEqual(player_obj.age, self.age)
        self.assertEqual(player_obj.position, self.position)
