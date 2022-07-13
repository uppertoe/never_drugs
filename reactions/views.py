from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q

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
    queryset = Interaction.objects.all().prefetch_related('drugs', 'condition')

class DrugDetailView(DetailView):
    model = Drug
    context_object_name = 'drug'
    template_name = 'reactions/drug_detail.html'

class ConditionDetailView(DetailView):
    model = Condition
    context_object_name = 'condition'
    template_name = 'reactions/condition_detail.html'

class InteractionDetailView(DetailView):
    model = Interaction
    context_object_name = 'interaction'
    template_name = 'reactions/interaction_detail.html'
    queryset = Interaction.objects.all().prefetch_related('drugs', 'condition')

class InteractionSearchResultsListView(ListView):
    model = Interaction
    context_object_name = 'interaction_list'
    template_name = 'reactions/interaction_search_results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Interaction.objects.filter(
            Q(condition__name__icontains=query)
        ).prefetch_related('drugs', 'condition')

class SearchView(TemplateView):
    template_name = 'reactions/search.html'