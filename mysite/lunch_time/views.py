from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from .models import Question, Choice, Vote

app_name = "lunch_time"
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "lunch_time/index.html", context)

def detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, "lunch_time/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "lunch_time/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    # Get the selected choice and the entered name from the form
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        entered_name = request.POST["name"]
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "lunch_time/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice or enter your name.",
            },
        )
    
    # Process and save the vote
    vote_instance = Vote.objects.create(
        question=question,
        choice=selected_choice,
        name_text=entered_name
    )

    # Update the selected choice's vote count
    selected_choice.votes += 1
    selected_choice.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse("lunch_time:results", args=(question.id,)))