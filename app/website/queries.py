from .models import Player, RatingRecords
from django.db.models import Case, OuterRef, Subquery, When, DateTimeField, F


def get_curr_rating():
    subquery = RatingRecords.objects.filter(player=OuterRef('pk')).annotate(
        created_at=Case(
            When(match_id__isnull=True, then=F('player__created_at')),
            default=F('match__created_at'),
            output_field=DateTimeField()
            )
        ).order_by('-created_at')
    players = Player.objects.annotate(
        curr_rating=Subquery(subquery.values('rating')[:1]),
        latest_activity=Subquery(subquery.values('created_at')[:1]),
    )
    return players
