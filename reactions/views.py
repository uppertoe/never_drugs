from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.html import escape
from itertools import chain

from .models import Drug, Condition, Interaction

# Create your views here.
class DrugListView(ListView):
    model = Drug
    context_object_name = 'drug_list'
    template_name = 'reactions/drug_list.html'

class ConditionListView(ListView):
    model = Condition
    context_object_name = 'condition_list'
    template_name = 'reactions/condition_list.html'

class DrugDetailView(DetailView):
    model = Drug
    context_object_name = 'drug'
    template_name = 'reactions/drug_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include related interactions via interactions.drugs related_name
        context['interactions'] = (self.object.interactions.all()
        .exclude(ready_to_publish=False)
        .prefetch_related('conditions',))
        # Include related interactions via interactions.secondary_drugs related_name
        context['secondary_interactions'] = (self.object.secondary_interactions.all()
        .exclude(ready_to_publish=False)
        .prefetch_related('conditions',))
        return context

class ConditionDetailView(DetailView):
    model = Condition
    context_object_name = 'condition'
    template_name = 'reactions/condition_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interactions'] = (self.object.interactions.all()
        .exclude(ready_to_publish=False)
        .prefetch_related('drugs', 'secondary_drugs'))
        return context

class InteractionDetailView(DetailView):
    model = Interaction
    context_object_name = 'interaction'
    template_name = 'reactions/interaction_detail.html'
    queryset = Interaction.objects.all().prefetch_related('drugs', 'secondary_drugs', 'conditions', 'sources')

def SearchView(request):
    query = request.GET.get('q')
    if query:
        drugs = (Drug.objects
        .filter(Q(name__icontains=query) | Q(aliases__icontains=query))
        .prefetch_related('interactions'))
        conditions = (Condition.objects
        .filter(Q(name__icontains=query) | Q(aliases__icontains=query))
        .exclude(ready_to_publish=False)
        .prefetch_related('interactions'))
        context = {
            'results': chain(drugs,conditions), #combine querysets from both models
            'query': query,
            'offer_to_add': False if drugs.exists() | conditions.exists() else True,}
        return render(request, 'reactions/search.html', context)
    return render(request, 'reactions/search.html') # template {% if %} to catch empty context

def escape_model_fields(model,sep, *args):
    '''
    Takes a model, separator and fields to return as a list of escaped strings

    Arguments:
    model: Model on which to obtain .values_list
    sep: Separator to split the .values_list string on
    *args: Model fields to include
    '''
    output = []
    #Converts values_list tuple into list with empty strings removed
    for i in list(filter(None, chain(*model.objects.values_list(*args)))):
        # Splits on user-entered separators in model.field
        for k in i.split(sep): output.append(escape(k))
    return output

def ListContentsView(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            drugs = escape_model_fields(Drug, ', ', 'name', 'aliases')
            conditions = escape_model_fields(Condition, ', ', 'name', 'aliases')
            return JsonResponse({'context': drugs + conditions})
        return JsonResponse({'status': 'Bad Request'}, status=400)
    else:
        return HttpResponseBadRequest('Bad Request')
