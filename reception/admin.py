from django.contrib import admin
from keda.reception.models import *

class RelativeInline(admin.TabularInline):
    model = Relative
    fk_name = "related"
    extra = 1

class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    fk_name = "person"
    extra = 1

class VehicleInline(admin.TabularInline):
    model = Vehicle
    fk_name = "owner"
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name')
    search_fields = ('surname', )
    ordering = ('surname', )
    inlines = [
        RelativeInline,
        ContactInfoInline,
        VehicleInline,
        ]

class MilitaryPersonAdmin(PersonAdmin):
    list_display = ('rank', ) + PersonAdmin.list_display
    list_filter = ('active', )


class DamageAdmin(admin.ModelAdmin):
    list_filter = ('fixed', )
    ordering = ('tag', 'appartment', )
    list_display = ('appartment', 'tag', 'info')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'check_in', 'check_out', 'appartment')
    ordering = ('check_in', 'check_out', )
    search_fields = ('owner', 'appartment')



admin.site.register(Rank)
admin.site.register(Vehicle)
admin.site.register(ContactInfo)
admin.site.register(Relative, PersonAdmin)
admin.site.register(Visitor, MilitaryPersonAdmin)
admin.site.register(Staff, MilitaryPersonAdmin)
admin.site.register(Category)
admin.site.register(Appartment)
admin.site.register(Unit)
admin.site.register(Damage, DamageAdmin)
admin.site.register(Reservation, ReservationAdmin)
