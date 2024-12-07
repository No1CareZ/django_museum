from django.contrib import admin
from .models import Exposition, Exhibit


@admin.register(Exposition)
class ExpositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    pass
