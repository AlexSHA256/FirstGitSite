from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect

from .models import Question, Choice

from django.core.urlresolvers import reverse
from django.views import generic

from django.http import Http404

'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Leave the rest of the views (detail, results, vote) unchanged


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
'''


class IndexView(generic.ListView):  # коцепция отображение списка обьектов
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):  # коцепция отображение подробностей о конкретном обьекте
    model = Question  # указываем с какой моделью работать
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# https://djbook.ru/rel1.9/ref/class-based-views/base.html


def vote(request, question_id):  # принимает форму и обрабатывает
    question = get_object_or_404(Question, pk=question_id)

    try:
        print('request post: ', request.POST)
        selected_choice = question.choice_set.get(pk=request.POST['choice'])  # возвращает связанный с вопросом выбор

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))