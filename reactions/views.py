from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

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

class InteractionListView(ListView):
    model = Interaction
    context_object_name = 'interaction_list'
    template_name = 'reactions/interaction_list.html'
    queryset = Interaction.objects.all().prefetch_related('drugs', 'conditions')

class DrugDetailView(DetailView):
    model = Drug
    context_object_name = 'drug'
    template_name = 'reactions/drug_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interactions'] = self.object.interactions.all()
        return context

class ConditionDetailView(DetailView):
    model = Condition
    context_object_name = 'condition'
    template_name = 'reactions/condition_detail.html'

class InteractionDetailView(DetailView):
    model = Interaction
    context_object_name = 'interaction'
    template_name = 'reactions/interaction_detail.html'
    queryset = Interaction.objects.all().prefetch_related('drugs', 'conditions')

class InteractionSearchResultsListView(ListView):
    model = Interaction
    context_object_name = 'interaction_list'
    template_name = 'reactions/interaction_search_results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return (Interaction.objects
            .filter(Q(conditions__name__icontains=query))
            .prefetch_related('drugs', 'conditions'))

class SearchView(TemplateView):
    template_name = 'reactions/search.html'

def SearchResultsView(request):
    query = request.GET.get('q')
    drugs = Drug.objects.filter(Q(name__icontains=query) | Q(aliases__icontains=query)).prefetch_related('interactions')
    conditions = Condition.objects.filter(Q(name__icontains=query) | Q(aliases__icontains=query)).prefetch_related('interactions')
    context = {
        'drugs': drugs,
        'conditions': conditions,
        'query': query}
    return render(request, 'reactions/search_results.html', context)
