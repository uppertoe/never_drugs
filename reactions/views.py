from django.views.generic import ListView, DetailView

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

