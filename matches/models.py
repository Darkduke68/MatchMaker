import datetime
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# from jobs.models import Job, Employer, Location

from .signals import user_matches_update
from .utils import calculate_match


# ====================================
# Match Model
# ====================================


class MatchQuerySet(models.query.QuerySet):
    def all(self):
        return self.filter(active=True)

    def matches(self, user):
        q1 = self.filter(user_a=user).exclude(user_b=user)
        q2 = self.filter(user_b=user).exclude(user_a=user)
        return (q1 | q2).distinct()


class MatchManager(models.Manager):
    def get_queryset(self):
        return MatchQuerySet(self.model, using=self._db)

    def get_or_create_match(self, user_a=None, user_b=None):
        try:
            instance1 = self.get(user_a=user_a, user_b=user_b)
        except:
            instance1 = None
        try:
            instance2 = self.get(user_a=user_b, user_b=user_a)
        except:
            instance2 = None
        retrieved_instance = instance1 or instance2
        if retrieved_instance:
            retrieved_instance.check_update()
            return retrieved_instance, False
        else:
            new_instance = self.create(user_a=user_a, user_b=user_b)
            new_instance.do_match()
            return new_instance, True

    def update_for_user(self, user):
        qs = self.get_queryset().matches(user)
        for instance in qs:
            instance.do_match()

    def update_all(self):
        queryset = self.all()
        now = timezone.now()
        offset = now - datetime.timedelta(hours=12)
        offset2 = now - datetime.timedelta(hours=36)
        queryset.filter(modified__gt=offset2).filter(modified__lte=offset)
        for instance in queryset:
            instance.check_update()

    def get_matches(self, user):
        queryset = self.get_queryset().matches(user).order_by('-match_decimal')
        matches = []
        for match in queryset:
            if match.user_a == user:
                items_wanted = [match.user_b]
                matches.append(items_wanted)
            elif match.user_b == user:
                items_wanted = [match.user_a]
                matches.append(items_wanted)
        return matches

    def get_matches_with_percent(self, user):
        qs = self.get_queryset().matches(user).order_by('-match_decimal')
        matches = []
        for match in qs:
            if match.user_a == user:
                items_wanted = [match.user_b, match.percent]
                matches.append(items_wanted)
            elif match.user_b == user:
                items_wanted = [match.user_a, match.percent]
                matches.append(items_wanted)
            else:
                pass
        return matches


class Match(models.Model):
    """Model stores information of two users."""

    user_a = models.ForeignKey(User, related_name='user_a')
    user_b = models.ForeignKey(User, related_name='user_b')
    match_decimal = models.DecimalField(decimal_places=8, max_digits=16, default=0.00)
    questions_answered = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = MatchManager()

    def __str__(self):
        return '{.2f}'.format(self.match_decimal)

    @property
    def percent(self):
        return '{.2f%%}'.format(self.match_decimal * Decimal(100))

    def do_match(self):
        user_a = self.user_a
        user_b = self.user_b
        match_decimal, questions_answered = calculate_match(user_a, user_b)
        self.match_decimal = match_decimal
        self.questions_answered = questions_answered
        self.save()

    def check_update(self):
        now = timezone.now()
        offset = now - datetime.timedelta(hours=12)  # 12 hours ago
        if self.updated <= offset or self.match_decimal == 0.0:
            self.do_match()
            # PositionMatch.objects.update_top_suggestions(self.user_a, 6)
            # PositionMatch.objects.update_top_suggestions(self.user_b, 6)


def user_matches_update_receiver(sender, user, *args, **kwargs):
    Match.objects.update_for_user(user)
    # PositionMatch.objects.update_top_suggestions(user, 20)

# connect to signal
user_matches_update.connect(user_matches_update_receiver)
#
#
# class PositionMatchManager(models.Manager):
#     def update_top_suggestions(self, user, match_int):
#         matches = Match.objects.get_matches(user)[:match_int]
#         for match in matches:
#             job_set = match[0].userjob_set.all()
#             if job_set.count > 0:
#                 for job in job_set:
#                     try:
#                         the_job = Job.objects.get(text__iexact=job.position)
#                         jobmatch, created = self.get_or_create(user=user, job=the_job)
#                     except:
#                         pass
#                     try:
#                         the_loc = Location.objects.get(name__iexact=job.location)
#                         locmatch, created = LocationMatch.objects.get_or_create(user=user, location=the_loc)
#                     except:
#                         pass
#                     try:
#                         the_employer = Employer.objects.get(name__iexact=job.employer_name)
#                         empymatch, created = EmployerMatch.objects.get_or_create(user=user, employer=the_employer)
#                     except:
#                         pass
#
#
# class PositionMatch(models.Model):
#     user = models.ForeignKey(User)
#     job = models.ForeignKey(Job)
#     hidden = models.BooleanField(default=False)
#     liked = models.NullBooleanField()
#     updated = models.DateTimeField(auto_now=True, auto_now_add=False)
#
#     def __unicode__(self):  # __str__(self):
#         return self.job.text
#
#     objects = PositionMatchManager()
#
#     def check_update(self, match_int):
#         now = timezone.now()
#         offset = now - datetime.timedelta(seconds=12)  # 12 hours ago
#         if self.updated <= offset:
#             PositionMatch.objects.update_top_suggestions(self.user, match_int)
#
#     @property
#     def get_match_url(self):
#         return reverse("position_match_view_url", kwargs={"slug": self.job.slug})
#
#
# class EmployerMatch(models.Model):
#     user = models.ForeignKey(User)
#     employer = models.ForeignKey(Employer)
#     hidden = models.BooleanField(default=False)
#     liked = models.NullBooleanField()
#
#     def __unicode__(self):  # __str__(self):
#         return self.user.username
#
#     @property
#     def get_match_url(self):
#         return reverse("employer_match_view_url", kwargs={"slug": self.employer.slug})
#
#
# class LocationMatch(models.Model):
#     user = models.ForeignKey(User)
#     location = models.ForeignKey(Location)
#     hidden = models.BooleanField(default=False)
#     liked = models.NullBooleanField()
#
#     def __unicode__(self):  # __str__(self):
#         return self.user.username
#
#     @property
#     def get_match_url(self):
#         return reverse("location_match_view_url", kwargs={"slug": self.location.slug})








