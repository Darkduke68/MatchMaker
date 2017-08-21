from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver


# ====================================
#   Question Model
# ====================================


class QuestionManager(models.Manager):
    """Provide method to retrieve unanswered question for requested user."""

    def unanswered(self, user):
        """Return unanswered questions query set."""
        q1 = Q(useranswer__user=user)
        qs = self.exclude(q1)
        return qs


class Question(models.Model):
    """The question model contains the question title."""

    text = models.TextField()
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    # answers = models.ManyToManyField('Answer')

    objects = QuestionManager()

    @property
    def title(self):
        return self.text

    def __str__(self):
        return self.text[:20]


class Answer(models.Model):
    """The answer model associates with a question."""

    question = models.ForeignKey(Question)
    text = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.text[:20]


# ====================================
#   Question Model
# ====================================


LEVELS = (
    ('Mandatory', 'Mandatory'),
    ('Very Important', 'Very Important'),
    ('Somewhat Important', 'Somewhat Important'),
    ('Not Important', 'Not Important'),
)


class UserAnswer(models.Model):
    """Model stores user's answer to a particular questions."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    question = models.ForeignKey(Question)
    my_answer = models.ForeignKey(Answer, related_name='user_answer')
    my_answer_importance = models.CharField(max_length=50, choices=LEVELS)
    my_points = models.IntegerField(default=-1)
    their_answer = models.ForeignKey(Answer, null=True, blank=True, related_name='match_answer')
    their_importance = models.CharField(max_length=50, choices=LEVELS)
    their_points = models.IntegerField(default=-1)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.my_answer.text[:20]


def score_importance(importance_level):
    if importance_level == "Mandatory":
        points = 300
    elif importance_level == "Very Important":
        points = 200
    elif importance_level == "Somewhat Important":
        points = 50
    else:
        points = 0
    return points


@receiver(pre_save, sender=UserAnswer)
def update_user_answer_score(sender, instance, *args, **kwargs):
    """Update scores in UserAnswer model before save."""
    my_points = score_importance(instance.my_answer_importance)
    instance.my_points = my_points
    their_points = score_importance(instance.their_importance)
    instance.their_points = their_points

















