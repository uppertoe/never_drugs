import uuid
from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils.text import slugify
from django.conf import settings
from django.utils.html import format_html
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Link for Markdown field helptext
markdown_field_helptext = "Add basic formatting using "
markdown_link = "https://www.markdownguide.org/cheat-sheet/"
markdown_link_text = "Markdown (cheat sheet)"
markdown_field_post_helptext = "A live preview of formatted content \
    is shown next to the input field"


class Source(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Article title')
    publication = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Journal or publication name')
    reference = models.TextField(
        max_length=2055,
        blank=True,
        null=True,
        verbose_name='Full reference')
    year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Year of publication')
    url = models.URLField(
        max_length=255,
        blank=True,
        null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='source_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='source_edited_by')

    def __str__(self):
        return f'{self.name} in {self.publication}'


class DrugClass(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='drug_class_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='drug_class_edited_by')

    def __str__(self):
        return self.name


class Drug(models.Model):
    name = models.CharField(max_length=255, unique=True)
    aliases = models.CharField(
        max_length=1023,
        blank=True,
        null=True)
    slug = models.SlugField(
        null=False,
        unique=True,
        verbose_name='URL title')
    drug_class = models.ManyToManyField(
        DrugClass,
        blank=True,
        related_name='drugs')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='drug_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='drug_edited_by')

    class Meta:
        ordering = ['name']

    @admin.display(description='Classes')
    def get_drug_classes(self):
        return [drug_class for drug_class in self.drug_class.all()]

    def get_drug_class_string(self):
        return ', '.join(
            [drug_class.name for drug_class in self.drug_class.all()])

    def get_absolute_url(self):
        return reverse('drug_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Condition(models.Model):
    # Peer review choices
    DRAFT = 'DR'
    MODIFY = 'MO'
    MOD_THEN_ACCEPT = 'AM'
    ACCEPT = 'AC'
    peer_review_choices = [
        (DRAFT, 'Draft'),
        (MODIFY, 'Requires modifications, then re-review'),
        (MOD_THEN_ACCEPT, 'Accepted after minor changes'),
        (ACCEPT, 'Accepted'), ]

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
        (L7, 'Expert body opinion'), ]

    name = models.CharField(
        max_length=255,
        unique=True)
    aliases = models.CharField(
        max_length=1023,
        blank=True,
        null=True)
    slug = models.SlugField(
        null=False,
        unique=True,
        verbose_name='URL title')
    description = MarkdownxField(
        blank=True,
        null=True,
        verbose_name='Article body',
        help_text=format_html(
            '{}<a href="{}" target="_blank" rel="noopener noreferrer">{}</a><br>{}',
            markdown_field_helptext,
            markdown_link,
            markdown_link_text,
            markdown_field_post_helptext)
    )
    sources = models.ManyToManyField(
        Source,
        related_name='condition_sources',
        blank=True)
    evidence = models.CharField(
        max_length=2,
        choices=evidence_choices,
        default=L7)
    ready_for_peer_review = models.BooleanField(
        default=False,
        verbose_name='Ready for peer review?')
    peer_review_status = models.CharField(
        max_length=2,
        choices=peer_review_choices,
        default=DRAFT)
    ready_to_publish = models.BooleanField(
        default=False,
        verbose_name='Ready to publish?')  # False excludes from search
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='condition_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='condition_edited_by')

    class Meta:
        ordering = ['name']

    def alias_list(self):
        return [self.aliases.split(', ')] + [self.name]

    def alias_dict(self):
        dict = {}
        queryset = Condition.objects.all().exclude(ready_to_publish=False)
        for condition in queryset:
            for alias in condition.alias_list:
                if alias not in dict:
                    dict[alias] = condition
        return dict

    def description_markdown(self):
        # Replace NoneType with '' if empty
        return markdownify(self.description) if self.description else ''

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
        (SEVERE, 'Severe'), ]

    # Helptext
    include_article_helptext = "Include this article if many conditions \
        lead to the same endpoint (i.e. malignant hyperthermia)"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(
        verbose_name='URL title',
        null=True,
        blank=True)  # Make null=False, unique=True, once migrated
    conditions = models.ManyToManyField(
        Condition,
        related_name='interactions',
        verbose_name="Conditions strongly linked with the interaction",
        blank=True)
    secondary_conditions = models.ManyToManyField(
        Condition,
        related_name='secondary_condition_interactions',
        verbose_name='Conditions with a theoretical link to the interaction',
        blank=True)
    drugs = models.ManyToManyField(
        Drug,
        related_name='interactions',
        verbose_name='Contraindicated drugs',
        blank=True)
    secondary_drugs = models.ManyToManyField(
        Drug,
        related_name='secondary_drug_interactions',
        verbose_name='Drugs to use with caution',
        blank=True)
    description = MarkdownxField(
        blank=True,
        null=True,
        verbose_name='Article body - not displayed by default',
        help_text=format_html(
            '{}<a href="{}" target="_blank" rel="noopener noreferrer">{}</a><br>{}',
            markdown_field_helptext,
            markdown_link,
            markdown_link_text,
            markdown_field_post_helptext)
    )
    severity = models.CharField(
        max_length=2,
        choices=severity_choices,
        default=NA)
    sources = models.ManyToManyField(
        Source,
        related_name='interaction_sources',
        blank=True)
    include_article = models.BooleanField(   # False excludes from search
        default=False,
        verbose_name='Include this article on the website?',
        help_text=include_article_helptext)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='interaction_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='interaction_edited_by')

    def alias_list(self):
        return [self.aliases.split(', ')] + [self.name]

    def alias_dict(self, queryset):
        dict = {}
        for item in queryset:
            if queryset.model is (Condition | Interaction):
                for alias in item.alias_list:
                    if alias not in dict:
                        dict[alias] = item
                    else:
                        dict.pop(alias)
            else:  # Assume item is a Drug
                dict[item.name] = item
        return dict

    def description_markdown(self):
        # Replace NoneType with '' if empty
        return markdownify(self.description) if self.description else ''

    def get_bootstrap_alert_colour(self):
        # chooses bootstrap alert colour based on interaction.severity
        severity_alert_dict = {
            'NA': 'alert-secondary',
            'MI': 'alert-primary',
            'MO': 'alert-warning',
            'SE': 'alert-danger'}
        return severity_alert_dict.get(self.severity)

    def get_condition_string(self):
        return ', '.join(
            [condition.name for condition in self.conditions.all()])

    def get_secondary_condition_string(self):
        return ', '.join(
            [condition.name for condition in self.secondary_conditions.all()])

    @admin.display(description='Drugs')
    # Allow many-many relationship query for admin list_display
    def get_drug_list(self):
        return [drug for drug in self.drugs.all()]

    @admin.display(description='Conditions')
    # Allow many-many relationship query for admin list_display
    def get_condition_list(self):
        return [condition for condition in self.conditions.all()]

    def __str__(self):
        drugs_string = ', '.join([drug.name for drug in self.drugs.all()])
        conditions_string = ', '.join(
            [condition.name for condition in self.conditions.all()])

        string_length = 30  # Insert '...' for long names
        if len(drugs_string) > string_length:
            drugs_string = drugs_string[:string_length] + '...'
        if len(conditions_string) > string_length:
            conditions_string = conditions_string[:string_length] + '...'
        return f'{self.name}: {conditions_string}\
             with {drugs_string}'.capitalize()

    def get_absolute_url(self):
        return reverse(
            'interaction_detail',
            kwargs={'str': slugify(self.name), 'pk': str(self.id)})

    def last_modified_string(self):
        return str(datetime.now() - self.date_modified.date)
