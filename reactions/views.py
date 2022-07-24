from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import render
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
        context['interactions'] = (self.object.interactions.all()
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
        .prefetch_related('drugs',))
        return context

class InteractionDetailView(DetailView):
    model = Interaction
    context_object_name = 'interaction'
    template_name = 'reactions/interaction_detail.html'
    queryset = Interaction.objects.all().prefetch_related('drugs', 'conditions')

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
            'query': query,}
        return render(request, 'reactions/search.html', context)
    return render(request, 'reactions/search.html') # template {% if %} to catch empty context
