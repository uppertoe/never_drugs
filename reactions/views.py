from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.html import escape
from itertools import chain

from .forms import TicketForm
from .models import Drug, Condition, Interaction


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
        # Include related interactions via
        # interactions.drugs related_name
        context['interactions'] = (
            self.object.interactions.all()
            .prefetch_related('conditions', 'secondary_conditions'))
        # Include related interactions via
        # interactions.secondary_drugs related_name
        context['secondary_interactions'] = (
            self.object.secondary_drug_interactions.all()
            .prefetch_related('conditions', 'secondary_conditions'))
        return context


class ConditionDetailView(DetailView):
    model = Condition
    context_object_name = 'condition'
    template_name = 'reactions/condition_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interactions'] = (
            self.object.interactions.all()
            .prefetch_related('drugs', 'secondary_drugs'))
        # Include related interactions via
        # interactions.secondary_conditions related_name
        context['secondary_interactions'] = (
            self.object.secondary_condition_interactions.all()
            .prefetch_related('drugs', 'secondary_drugs'))
        return context


class InteractionDetailView(DetailView):
    model = Interaction
    context_object_name = 'interaction'
    template_name = 'reactions/interaction_detail.html'
    queryset = Interaction.objects.all().prefetch_related(
        'drugs', 'secondary_drugs', 'conditions',
        'secondary_conditions', 'sources')


def search_view(request):
    query = request.GET.get('q')
    context = {}
    if query:
        drugs = (
            Drug.objects
            .filter(Q(name__icontains=query) | Q(aliases__icontains=query))
            .prefetch_related('interactions'))
        conditions = (
            Condition.objects
            .filter(Q(name__icontains=query) | Q(aliases__icontains=query))
            .exclude(ready_to_publish=False)
            .prefetch_related('interactions'))
        interactions = (
            Interaction.objects
            .filter(Q(name__icontains=query))
            .exclude(include_article=False)
            .prefetch_related(
                'conditions',
                'secondary_conditions',
                'drugs',
                'secondary_drugs'))

        # redirect straight to page if only 1 result
        drug_count = drugs.count()
        condition_count = conditions.count()
        interaction_count = interactions.count()
        if drug_count + condition_count + interaction_count == 1:
            if drug_count:
                return redirect(drugs.get())
            if condition_count:
                return redirect(conditions.get())
            if interaction_count:
                return redirect(interactions.get())

        form = TicketForm(initial={'name': query})
        context = {
            # combine querysets from both models
            'results': chain(drugs, conditions, interactions),
            'query': query,
            'offer_to_add':
            False if drugs.exists() | conditions.exists() | interactions.exists() else True,
            'ticket_form': form}
    return render(request, 'reactions/search.html', context)


def escape_model_fields(queryset, sep, *args):
    '''
    Takes a model, separator and fields to return as a list of escaped strings

    Arguments:
    model: Model on which to obtain .values_list
    sep: Separator to split the .values_list string on
    *args: Model fields to include
    '''
    output = []
    # Converts values_list tuple into list with empty strings removed
    for field_strings in list(filter(None, chain(
            *queryset.values_list(*args)))):
        # Splits on user-entered separators in model.field
        for split_string in field_strings.split(sep):
            output.append(escape(split_string))
    return output


def list_contents_view(request):
    # Provides a list of drug.name/alias and
    # condition.name/alias for autocomplete
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            drugs = escape_model_fields(
                Drug.objects.all(),
                ', ',
                'name',
                'aliases')
            conditions = escape_model_fields(
                Condition.objects.filter(ready_to_publish=True),
                ', ',
                'name',
                'aliases')
            interactions = escape_model_fields(
                # TODO: exclude include_article == False
                Interaction.objects.filter(include_article=True),
                ', ',
                'name'
            )
            # Remove duplicates
            context = list(set(drugs+conditions+interactions))
            return JsonResponse({'context': context})
        return JsonResponse({'status': 'Bad Request'}, status=400)
    else:
        return HttpResponseBadRequest('Bad Request')
