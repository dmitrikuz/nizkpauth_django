from datetime import datetime, timezone

from django.conf import settings
from django.utils.functional import lazy
from django.utils.timezone import is_naive, make_aware



def make_utc(dt: datetime) -> datetime:
    if settings.USE_TZ and is_naive(dt):
        return make_aware(dt, timezone=timezone.utc)

    return dt


def datetime_from_epoch(ts: float) -> datetime:
    return make_utc(datetime.utcfromtimestamp(ts))
