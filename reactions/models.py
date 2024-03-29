import uuid
from datetime import datetime
from django.db import models
from django.db.models import Q
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
    description = MarkdownxField(
        blank=True,
        null=True,
        verbose_name='Description',
        help_text=(
            'Use this field to outline the '
            'drug\'s background and contraindications')
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
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

    def get_all_interactions(self):
        return self.interactions.all() | self.secondary_drug_interactions.all()

    def get_all_conditions(self):
        return (Condition.objects.filter(
            Q(interactions__drugs=self) | Q(secondary_condition_interactions__drugs=self) | Q(interactions__secondary_drugs=self) | Q(secondary_condition_interactions__secondary_drugs=self))
            .distinct())

    def get_condition_count(self):
        return self.get_all_conditions().count()

    def alias_list(self):
        return self.aliases.split(', ') + [self.name] if self.aliases else [self.name]

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

    # TL;DR box choices
    GREY = 'GY'
    BLUE = 'BL'
    YELLOW = 'YE'
    GREEN = 'GN'
    RED = 'RE'
    tldr_box_choices = [
        (GREY, 'Grey'),
        (BLUE, 'Blue'),
        (YELLOW, 'Yellow'),
        (GREEN, 'Green'),
        (RED, 'Red')]

    default_description = (
        '# Overview\n'
        '---\n'
        'Overview text here\n\n'
        '# Pathophysiology\n'
        '---\n'
        'Pathophysiology text here\n\n'
        '# Impacts on anaesthesia\n'
        '---\n'
        'Impacts text here \n\n'
        '### *Drug name here*\n'
        '`Expert opinion` Further detail here')

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
    tldr = MarkdownxField(
        blank=True,
        null=True,
        verbose_name='TL;DR',
        help_text=(
            'A brief description of the important anaesthetic concern '
            'to appear at the top of the article'))
    tldr_box = models.CharField(
        max_length=2,
        choices=tldr_box_choices,
        default=RED,
        verbose_name='TL;DR banner colour')
    see_also = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        verbose_name='See also',
        help_text='Link to related conditions here <br>')
    description = MarkdownxField(
        blank=True,
        null=True,
        default=default_description,
        verbose_name='Article body',
        help_text=format_html(
            '{}<a href="{}" target="_blank" rel="noopener noreferrer">{}</a><br>{}',
            markdown_field_helptext,
            markdown_link,
            markdown_link_text,
            markdown_field_post_helptext))
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
        return self.aliases.split(', ') + [self.name] if self.aliases else [self.name]

    def alias_dict(queryset):
        dict = {}

        def insert_non_duplicates(name, item):
            if name not in dict:
                dict[name] = item
            else:
                dict.pop(name)  # dict should be free of duplicates

        for item in queryset:
            for alias in item.alias_list():
                insert_non_duplicates(alias.lower(), item)
        return dict

    def description_markdown(self):
        # Replace NoneType with '' if empty
        return markdownify(self.description) if self.description else ''

    def tldr_markdown(self):
        # Replace NoneType with '' if empty
        return markdownify(self.tldr) if self.tldr else ''

    def get_tldr_box_colour(self):
        # chooses bootstrap alert colour based on interaction.severity
        alert_dict = {
            'GY': 'alert-secondary',
            'BL': 'alert-primary',
            'YE': 'alert-warning',
            'GN': 'alert-success',
            'RE': 'alert-danger'}
        return alert_dict.get(self.tldr_box) if self.tldr else ''

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
        return [self.name]  # Retain combatibility with Condition.alias_dict()

    def description_markdown(self):
        # Replace NoneType with '' if empty
        return markdownify(self.description) if self.description else ''

    def get_all_conditions(self):
        return self.conditions.all() | self.secondary_conditions.all()

    def get_all_drugs(self):
        return self.drugs.all() | self.secondary_drugs.all()

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
