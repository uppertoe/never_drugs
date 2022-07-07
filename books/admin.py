from django.contrib import admin

from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price',)
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.
admin.site.register(Book, BookAdmin)