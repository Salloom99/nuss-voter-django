from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from .models import Department, Nominee, Unit, Voter


class NomineeFilter(admin.SimpleListFilter):
    title = 'unit'
    parameter_name = 'unit'

    def lookups(self, request, model_admin):
        if 'unit__department__nickname__exact' in request.GET:
            id = request.GET['unit__department__nickname__exact']
            units = Unit.objects.filter(department=id)
            return [(unit.nickname, unit.name) for unit in units]
        else:
            return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(unit=self.value())
        else:
            return queryset



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'nickname', 'units_count']
    search_fields = ['name', 'nickname']

    def units_count(self, department):
        url = (
            reverse('admin:main_unit_changelist')
            + '?'
            + urlencode({'department__nickname': str(department.nickname)})
        )
        return format_html('<a href="{}">{}</a>', url, department.units_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(units_count=Count('units'))


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'nickname', 'nominees_count']
    search_fields = ['name', 'nickname']

    def nominees_count(self, unit):
        url = (
            reverse('admin:main_nominee_changelist')
            + '?'
            + urlencode({'unit__nickname': str(unit.nickname)})
        )
        return format_html('<a href="{}">{}</a>', url, unit.nominees_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(nominees_count=Count('nominees'))


@admin.register(Nominee)
class NomineeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'unit', 'votes_count']
    search_fields = ['name']
    list_filter = ['unit__department', NomineeFilter]
    autocomplete_fields = ['votes']

    @admin.display(ordering='votes_count')
    def votes_count(self, nominee):
        url = (
            reverse('admin:main_voter_changelist')
            + '?'
            + urlencode({'votes__id': str(nominee.id)})
        )
        return format_html('<a href="{}">{}</a>', url, nominee.votes_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(votes_count=Count('votes'))


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ['id', 'qr_id', 'unit', 'votes_count']
    search_fields = ['name']
    list_filter = ['unit']
    autocomplete_fields = ['unit', 'votes']

    @admin.display(ordering='votes_count')
    def votes_count(self, voter):
        url = (
            reverse('admin:main_nominee_changelist')
            + '?'
            + urlencode({'votes__id': str(voter.id)})
        )
        return format_html('<a href="{}">{}</a>', url, voter.votes_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(votes_count=Count('votes'))
