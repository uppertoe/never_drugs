import uuid
from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils.text import slugify


# Create your models here.
class LowercaseField(models.CharField): # Override CharField to store lowercase strings
    def __init__(self, *args, **kwargs):
        super(LowercaseField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

class Source(models.Model):
    name = LowercaseField(max_length=255, blank=False, verbose_name='Article title')
    publication = LowercaseField(max_length=255, blank=False, verbose_name='Journal or publication name')
    reference = models.TextField(max_length=1023, blank=True, verbose_name='Full reference')
    url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.name[:30]} in {self.publication[:30]}'

class DrugClass(models.Model):
    name = LowercaseField(max_length=255)
    description = models.TextField(max_length=1023, blank=True)

    def __str__(self):
        return self.name

class Drug(models.Model):
    name = LowercaseField(max_length=255, unique=True)
    aliases = LowercaseField(max_length=1023, blank=True)
    slug = models.SlugField(null=False, unique=True, verbose_name='URL title')
    drug_class = models.ManyToManyField(DrugClass, blank=True, related_name='drugs')

    @admin.display(description='Classes')
    def get_drug_classes(self):
        return [drug_class for drug_class in self.drug_class.all()]

    def get_drug_class_string(self):
        return ', '.join([drug_class.name for drug_class in self.drug_class.all()])

    def get_absolute_url(self):
        return reverse('drug_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

class Condition(models.Model):
    name = LowercaseField(max_length=255, unique=True)
    aliases = LowercaseField(max_length=1023, blank=True)
    slug = models.SlugField(null=False, unique=True, verbose_name='URL title')
    description = models.TextField(max_length=1023, blank=True)
    ready_to_publish = models.BooleanField(default=False, verbose_name='Ready to publish?')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('condition_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

class Interaction(models.Model):
    # Severity level choices
    NA = 'NA'
    MILD = 'MI'
    MODERATE = 'MO'
    SEVERE = 'SE'
    severity_choices = [
        (NA, 'Not applicable'),
        (MILD, 'Mild'),
        (MODERATE, 'Moderate'),
        (SEVERE, 'Severe'),
    ]
    
    # Evidence level choices
    L1 = 'L1'
    L2 = 'L2'
    L3 = 'L3'
    L4 = 'L4'
    L5 = 'L5'
    L6 = 'L6'
    L7 = 'L7'

    evidence_choices = [
        (L1, 'Systematic review of RCTs'),
        (L2, 'Well-designed RCT'),
        (L3, 'Well-designed controlled study without randomisation'),
        (L4, 'Well designed case-control or cohort studies'),
        (L5, 'Reviews of qualitative studies'),
        (L6, 'Single qualitative study'),
        (L7, 'Expert body opinion'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = LowercaseField(max_length=255)
    conditions = models.ManyToManyField(Condition, related_name='interactions')
    drugs = models.ManyToManyField(Drug, related_name='interactions')
    description = models.TextField()
    severity = models.CharField(
        max_length=2,
        choices=severity_choices,
        default=NA)
    evidence = models.CharField(
        max_length=2,
        choices=evidence_choices,
        default=L7)
    sources = models.ManyToManyField(Source, related_name='sources')
    ready_to_publish = models.BooleanField(default=False, verbose_name='Ready to publish?')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_condition_string(self):
        return ', '.join([condition.name for condition in self.conditions.all()])
    
    @admin.display(description='Drugs')
    def get_drug_list(self): # Allow many-many relationship query
        return [drug for drug in self.drugs.all()]

    @admin.display(description='Conditions')
    def get_condition_list(self): # Allow many-many relationship query
        return [condition for condition in self.conditions.all()]

    def __str__(self):
        drugs_string = ', '.join([drug.name for drug in self.drugs.all()])
        conditions_string = ', '.join([condition.name for condition in self.conditions.all()])
        
        string_length = 30 # Insert '...' for long names
        if len(drugs_string) > string_length: drugs_string = drugs_string[:string_length] + '...'
        if len(conditions_string) > string_length: conditions_string = conditions_string[:string_length] + '...'
        return f'{self.name}: {conditions_string} with {drugs_string}'

    def get_absolute_url(self):
        return reverse('interaction_detail', kwargs={'str': slugify(self.name), 'pk': str(self.id)})