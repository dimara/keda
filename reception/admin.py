from django.contrib import admin
from keda.reception.models import *

class MilitaryPersonAdmin(admin.ModelAdmin):
    list_display = ('rank', 'surname', 'name')
    search_fields = ('surname', )
    list_filter = ('active', )
    ordering = ('surname', )
    filter_horizontal = ('vehicles', 'contacts' )


class DamageAdmin(admin.ModelAdmin):
    list_filter = ('fixed', )


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'check_in', 'check_out', 'appartment')
    ordering = ('check_in', 'check_out', )
    search_fields = ('owner', 'appartment')


admin.site.register(Rank)
admin.site.register(Vehicle)
admin.site.register(ContactInfo)
admin.site.register(Person)
admin.site.register(Relative)
admin.site.register(MilitaryPerson, MilitaryPersonAdmin)
admin.site.register(Staff)
admin.site.register(Category)
admin.site.register(Appartment)
admin.site.register(Unit)
admin.site.register(Damage, DamageAdmin)
admin.site.register(Reservation, ReservationAdmin)
