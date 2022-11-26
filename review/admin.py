from django.contrib import admin

from .models import Review, ReviewSession


class ReviewAdmin(admin.ModelAdmin):
    pass


class ReviewSessionAdmin(admin.ModelAdmin):
    filter_horizontal = ('reviews', 'user_list')


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewSession, ReviewSessionAdmin)
