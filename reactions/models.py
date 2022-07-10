import uuid
from django.db import models
from django.urls import reverse


# Create your models here.
class LowercaseField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(LowercaseField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

class DrugClass(models.Model):
    name =LowercaseField(max_length=255)

    def __str__(self):
        return self.name

class Drug(models.Model):
    name = LowercaseField(max_length=255, unique=True)
    aliases = LowercaseField(max_length=1023, blank=True)
    drug_class = models.ManyToManyField(DrugClass, blank=True)
    slug = models.SlugField(null=False, unique=True)

    def get_absolute_url(self):
        return reverse('drug_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

class Condition(models.Model):
    name = LowercaseField(max_length=255, unique=True)
    aliases = LowercaseField(max_length=1023, blank=True)
    slug = models.SlugField(null=False, unique=True)

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
        (L3, 'Well-designed study without randomisation'),
        (L4, 'Well designed case-control or cohort studies'),
        (L5, 'Reviews of qualitative studies'),
        (L6, 'Single qualitative study'),
        (L7, 'Expert body opinion'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    condition = models.ForeignKey(Condition,on_delete=models.CASCADE)
    drugs = models.ManyToManyField(Drug)
    reaction_type = LowercaseField(max_length=255)
    description = models.TextField()
    severity = models.CharField(
        max_length=2,
        choices=severity_choices,
        default=NA)
    evidence = models.CharField(
        max_length=2,
        choices=evidence_choices,
        default=L7)

    def get_drug_names(self):
        return [drug.name for drug in self.drugs.all()]
    
    def __str__(self):
        drugs_string = ' ,'.join(self.get_drug_names())
        return f'{self.condition} and {drugs_string} interaction'

    def get_absolute_url(self):
        return reverse('interaction_detail', kwargs={'str': self.condition.slug, 'pk': str(self.id)})