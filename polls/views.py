import django
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers

from .models import Choice, Question

def to_json(model):    
    #import code; code.interact(local=locals())
    if (django.db.models.query.QuerySet == model.__class__):
      data = model
    else:
      data = [model]
    
    res = serializers.serialize('json', data)
    return res

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
      """
      Return the last five published questions (not including those set to be
      published in the future).
      """
      return Question.objects.filter(
          pub_date__lte=timezone.now()
      ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def json(request):
    q = get_object_or_404(Question, pk=1)
    q = Question.objects.all()
    res = to_json(q)
    return HttpResponse(res, content_type='application/json')

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
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