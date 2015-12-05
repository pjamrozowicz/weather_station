from django.contrib import admin
from .forms import NewsletterForm
from .models import Newsletter

# Register your models here.


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["__str__", "name"]
    form = NewsletterForm


admin.site.register(Newsletter, NewsletterAdmin)