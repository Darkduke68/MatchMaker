from decimal import Decimal
from django.db.models import Q
from questions.models import UserAnswer, Question


def calculate_match(user_a, user_b):
    """Calculate match percentage for two users.

    Return: A tuple has match percentage and the total question answered
        by both users (percentage, questions_in_common).
    """
    question_set1 = Question.objects.filter(Q(useranswer__user=user_a))
    question_set2 = Question.objects.filter(Q(useranswer__user=user_b))
    # return 0 if no question is answered for either user
    if question_set1.count() == 0 or question_set2.count() == 0:
        return 0.0, 0
    question_set = (question_set1 | question_set2).distinct()
    a_points = 0
    b_points = 0
    a_total_points = 0.000001
    b_total_points = 0.000001
    questions_in_common = 0

    # cumulative points for user a and user b
    for question in question_set:
        try:
            a_answer = UserAnswer.objects.get(user=user_a, question=question)
        except:
            a_answer = None
        try:
            b_answer = UserAnswer.objects.get(user=user_b, question=question)
        except:
            b_answer = None
        if a_answer and b_answer:
            questions_in_common += 1
            if a_answer.their_answer == b_answer.my_answer:
                b_points += a_answer.their_points
            b_total_points += a_answer.their_points
            if b_answer.their_answer == a_answer.my_answer:
                a_points += b_answer.their_points
            a_total_points += b_answer.their_points

    # compute percentage using geometric mean
    if questions_in_common > 0:
        a_decimal = a_points / Decimal(a_total_points)
        b_decimal = b_points / Decimal(b_total_points)
        if a_decimal == 0:
            a_decimal = 0.000001
        if b_decimal == 0:
            b_decimal = 0.000001
        match_percentage = (Decimal(a_decimal) * Decimal(b_decimal)) ** (1/Decimal(questions_in_common))
        return match_percentage, questions_in_common
    else:
        return 0.0, 0












