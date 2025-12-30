from django.db import models

# Create your models here.
class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #total_games
    #won_games
    #curr_rating
    #prev_rating

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Match(models.Model):
    player_one = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='as_player_one')
    score_one = models.IntegerField(null=False)
    player_two = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='as_player_two')
    score_two = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # order or id?

    def __str__(self):
        return f"Match: {self.player_one} vs. {self.player_two} ({self.score_one}:{self.score_two})"

class RatingRecords(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    rating = models.FloatField(null=False)
    match = models.ForeignKey(Match, on_delete=models.DO_NOTHING, null=True)
    #created_at

class EloParameter(models.Model):
    k_index = models.IntegerField(null=False)
    start_elo = models.IntegerField(null=False)

