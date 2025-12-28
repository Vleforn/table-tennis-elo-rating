from .models import RatingRecords, Match

K_INDEX = 32
START_ELO = 1000

def update_rating(rating_A, score_A, rating_B, score_B):
    # Chess elo system
    K_factor = 32
    scale_factor = 400
    expected_score_A = 1 / (1 + 10 ** ((rating_B - rating_A) / scale_factor))
    expected_score_B = 1 - expected_score_A
    print(f"expected_score_A = {expected_score_A}")
    print(f"expected_score_B = {expected_score_B}")
    norm_score_A = score_A / (score_A + score_B)
    norm_score_B = 1 - score_A
    upd_rating_A = rating_A + K_factor * (norm_score_A - expected_score_A)
    upd_rating_B = rating_B + K_factor * (norm_score_B - expected_score_B)
    return upd_rating_A, upd_rating_B

def sync_rating_history():
    pass
    # clear rating history
    # getu unique id from match
    # delete everythin that not in the prev list from history

def add_new_player_records():
    pass


def recalculate_rating_history():
    RatingRecords.objects.all().delete()
    matches = Match.objects.order_by('created_at')
    players = {}
    for match in matches:
        if match.player_one.id not in players:
            players[match.player_one.id] = START_ELO
        if match.player_two.id not in players:
            players[match.player_two.id] = START_ELO

        curr_rating_one = players[match.player_one.id]
        score_one = match.score_one
        curr_rating_two = players[match.player_two.id]
        score_two = match.score_two

        upd_rating_one, upd_rating_two = update_rating(
            curr_rating_one, score_one,
            curr_rating_two, score_two
        )

        upd_rating_record_one = RatingRecords(
            player=match.player_one,
            rating=upd_rating_one,
            match=match
        )
        upd_rating_record_two = RatingRecords(
            player=match.player_two,
            rating=upd_rating_two,
            match=match
        )

        players[match.player_one.id] = upd_rating_one
        players[match.player_two.id] = upd_rating_two

        upd_rating_record_one.save()
        upd_rating_record_two.save()
