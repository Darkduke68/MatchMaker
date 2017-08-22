from django.contrib import messages
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from matches.signals import user_matches_update

from .forms import UserResponseForm
from .models import Question, Answer, UserAnswer


@login_required()
def question_single(request, pk):
    """Endpoint to present a single question."""

    instance = get_object_or_404(Question, id=pk)

    # get or create a UserAnswer instance for that question
    try:
        user_answer = UserAnswer.objects.get(user=request.user, question=instance)
        updated = True
    except UserAnswer.DoesNotExist:
        user_answer = UserAnswer()
        updated = False
    except UserAnswer.MultipleObjectsReturned:
        user_answer = UserAnswer.objects.filter(user=request.user, question=instance)[0]
        updated = True

    form = UserResponseForm(request.POST or None)
    if form.is_valid():
        question_id = form.cleaned_data.get('question_id')

        answer_id = form.cleaned_data.get('answer_id')
        importance_level = form.cleaned_data.get('importance_level')

        their_importance_level = form.cleaned_data.get('their_importance_level')
        their_answer_id = form.cleaned_data.get('their_answer_id')

        question_instance = Question.objects.get(id=question_id)
        answer_instance = Answer.objects.get(id=answer_id)

        user_answer.user = request.user
        user_answer.question = question_instance
        user_answer.my_answer = answer_instance
        user_answer.my_answer_importance = importance_level
        if their_answer_id != -1:
            their_answer_instance = Answer.objects.get(id=their_answer_id)
            user_answer.their_answer = their_answer_instance
            user_answer.their_importance = their_importance_level
        else:
            user_answer.their_answer = None
            user_answer.their_importance = "Not Important"

        user_answer.save()
        user_matches_update.send(user=request.user, sender=user_answer.__class__)

        if updated:
            messages.success(request, "Updated successfully.", extra_tags='safe updated')
            return redirect('questions-update')
        else:
            messages.success(request, "Saved successfully.")
            return redirect('questions')

    context = {
        "form": form,
        "instance": instance,
        "user_answer": user_answer,
        "updated": updated,
    }
    return render(request, "questions/single.html", context)


@login_required()
def questions(request):
    """Endpoint to handle user request to answer questions."""

    next_questions = Question.objects.unanswered(request.user).order_by("?")
    if next_questions.count() > 0:
        next_q_instance = next_questions.first()
        return redirect("question-single", pk=next_q_instance.id)
    else:
        return render(request, "questions/countdown.html", {})


@login_required()
def questions_update(request):
    """Endpoint to update multiple instances of user answers."""

    answered = Question.objects.answered(request.user)
    print(answered.count())
    return render(request, "questions/update.html", {'questions': answered})



