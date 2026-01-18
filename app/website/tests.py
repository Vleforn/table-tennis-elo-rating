from django.test import TestCase
from .elo_calc import update_rating

# Create your tests here.
class EloCalculatorTests(TestCase):
    def test_update_rating_zero_scores(self):
        p1_rating = 1000
        p1_score = 0
        p2_rating = 1200
        p2_score = 0
        self.assertRaises(ValueError, update_rating, p1_rating, p1_score, p2_rating, p2_score)

    def test_update_rating_negative_values(self):
        self.assertRaises(ValueError, update_rating, -1, -1, -1, -1)
        self.assertRaises(ValueError, update_rating, -1, 1, 1, 1)
        self.assertRaises(ValueError, update_rating, 1, -1, 1, 1)
        self.assertRaises(ValueError, update_rating, 1, 1, -1, -1)
        self.assertRaises(ValueError, update_rating, 1, 1, -1, 1)

    def test_update_rating(self):
        p1_rating = 1000
        p1_score = 1
        p2_rating = 1000
        p2_score = 1 
        upd_p1_rating, upd_p2_rating = update_rating(p1_rating, p1_score, p2_rating, p2_score)
        self.assertIs(1000, upd_p1_rating)
        self.assertIs(1000, upd_p2_rating)

