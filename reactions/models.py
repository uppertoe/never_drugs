import uuid
from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils.text import slugify
from django.conf import settings

# Create your models here.
class Source(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Article title')
    publication = models.CharField(max_length=255, blank=False, verbose_name='Journal or publication name')
    reference = models.TextField(max_length=1023, blank=True, verbose_name='Full reference')
    year = models.IntegerField(blank=True, null=True, verbose_name='Year of publication')
    url = models.URLField(max_length=200, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'source_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'source_edited_by')

    def __str__(self):
        return f'{self.name} in {self.publication}'

class DrugClass(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1023, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'drug_class_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'drug_class_edited_by')

    def __str__(self):
        return self.name

class Drug(models.Model):
    name = models.CharField(max_length=255, unique=True)
    aliases = models.CharField(max_length=1023, blank=True)
    slug = models.SlugField(null=False, unique=True, verbose_name='URL title')
    drug_class = models.ManyToManyField(DrugClass, blank=True, related_name='drugs')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'drug_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'drug_edited_by')

    class Meta:
        ordering = ['name']

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
    name = models.CharField(max_length=255, unique=True)
    aliases = models.CharField(max_length=1023, blank=True)
    slug = models.SlugField(null=False, unique=True, verbose_name='URL title')
    description = models.TextField(max_length=1023, blank=True)
    sources = models.ManyToManyField(Source, related_name='condition_sources', blank=True)
    ready_to_publish = models.BooleanField(default=False, verbose_name='Ready to publish?') # False excludes from search
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'condition_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'condition_edited_by')

    class Meta:
        ordering = ['name']

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
        (SEVERE, 'Severe'),]
    
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
        (L7, 'Expert body opinion'),]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, blank=False)
    conditions = models.ManyToManyField(Condition, related_name='interactions', verbose_name="Conditions strongly linked with the interaction")
    secondary_conditions = models.ManyToManyField(Condition, related_name='secondary_condition_interactions', verbose_name='Conditions with a theoretical link to the interaction', blank=True)
    drugs = models.ManyToManyField(Drug, related_name='interactions', verbose_name='Contraindicated drugs', blank=True)
    secondary_drugs = models.ManyToManyField(Drug, related_name='secondary_drug_interactions', verbose_name='Drugs to use with caution', blank=True)
    description = models.TextField(blank=True)
    severity = models.CharField(
        max_length=2,
        choices=severity_choices,
        default=NA)
    evidence = models.CharField(
        max_length=2,
        choices=evidence_choices,
        default=L7)
    sources = models.ManyToManyField(Source, related_name='interaction_sources', blank=True)
    ready_to_publish = models.BooleanField(default=False, verbose_name='Ready to publish?') # False excludes from search
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'interaction_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'interaction_edited_by')

    def get_bootstrap_alert_colour(self): # chooses bootstrap alert colour based on interaction.severity
        severity_alert_dict = { 
            'NA': 'alert-secondary',
            'MI': 'alert-primary',
            'MO': 'alert-warning',
            'SE': 'alert-danger',}
        return severity_alert_dict.get(self.severity)

    def get_condition_string(self):
        return ', '.join([condition.name for condition in self.conditions.all()])

    def get_secondary_condition_string(self):
        return ', '.join([condition.name for condition in self.secondary_conditions.all()])
    
    @admin.display(description='Drugs')
    def get_drug_list(self): # Allow many-many relationship query for admin list_display
        return [drug for drug in self.drugs.all()]

    @admin.display(description='Conditions')
    def get_condition_list(self): # Allow many-many relationship query for admin list_display
        return [condition for condition in self.conditions.all()]

    def __str__(self):
        drugs_string = ', '.join([drug.name for drug in self.drugs.all()])
        conditions_string = ', '.join([condition.name for condition in self.conditions.all()])
        
        string_length = 30 # Insert '...' for long names
        if len(drugs_string) > string_length: drugs_string = drugs_string[:string_length] + '...'
        if len(conditions_string) > string_length: conditions_string = conditions_string[:string_length] + '...'
        return f'{self.name}: {conditions_string} with {drugs_string}'.capitalize()

    def get_absolute_url(self):
        return reverse('interaction_detail', kwargs={'str': slugify(self.name), 'pk': str(self.id)})

    def last_modified_string(self):
        return str(datetime.now() - self.date_modified.date)
