# coding: utf-8

from __future__ import unicode_literals

from datetime import datetime

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

from voting.managers import VoteManager


# SCORES = (
#     (+1, '+1'),
#     (-1, '-1'),
# )

SCORES = (
    (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), (9, "9"), (10, "10"),
    (-1, "-1"), (-2, "-2"), (-3, "-3"), (-4, "-4"), (-5, "-5"), (-6, "-6"), (-7, "-7"), (-8, "-8"), (-9, "-9"), (-10, "-10")
)

# SCORES= [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]



@python_2_unicode_compatible
class Vote(models.Model):
    """
    A vote on an object by a User.
    """
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices=SCORES)
    time_stamp = models.DateTimeField(editable=False, default=now)

    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        # One vote per user per object
        unique_together = (('user', 'content_type', 'object_id'),)

    def __str__(self):
        return '%s: %s on %s' % (self.user, self.vote, self.object)

    def is_upvote(self):
        return self.vote >= 1

    def is_downvote(self):
        return self.vote <= -1
