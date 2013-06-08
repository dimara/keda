from django.contrib import admin
from keda.reception.models import *

class RelativeInline(admin.TabularInline):
    model = Relative
    fk_name = "related"
    extra = 0

class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    fk_name = "person"
    extra = 0

class VehicleInline(admin.TabularInline):
    model = Vehicle
    fk_name = "owner"
    extra = 0

class ReceiptInline(admin.TabularInline):
    model = Receipt
    fk_name = "reservation"
    extra = 0

class ReservationInline(admin.TabularInline):
    model = Reservation
    fk_name = "owner"
    extra = 0

class PersonAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name')
    search_fields = ('surname', )
    ordering = ('surname', )
    inlines = [
        RelativeInline,
        ContactInfoInline,
        VehicleInline,
        ReservationInline,
        ]

class DamageInline(admin.TabularInline):
    model = Damage
    fk_name = "appartment"
    extra = 0

class AppartmentAdmin(admin.ModelAdmin):
    list_display = ('appartment', 'rooms', 'beds', 'category', )
    ordering = ('category', )
    inlines = [
        DamageInline,
        ]

class MilitaryPersonAdmin(PersonAdmin):
    list_display = PersonAdmin.list_display + ('rank', 'speciality')
    list_filter = ('active', )
    ordering = ('rank', )


class StaffAdmin(MilitaryPersonAdmin):
    list_display = MilitaryPersonAdmin.list_display + ('category', 'extra')


class DamageAdmin(admin.ModelAdmin):
    list_filter = ('fixed', )
    ordering = ('tag', 'appartment', )
    list_display = ('appartment', 'tag', 'info')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'check_in', 'check_out', 'appartment', 'res_type', 'telephone')
    list_filter = ('telephone', )
    ordering = ('check_in', 'check_out', )
    search_fields = ('owner', 'appartment')
    inlines = [
        ReceiptInline,
        ]

class ReceiptAdmin(admin.ModelAdmin):
    ordering = ('no', 'reservation', 'euro', 'rtype' )
    list_display = ('no', 'reservation', 'euro', 'rtype')

admin.site.register(Rank)
admin.site.register(Vehicle)
admin.site.register(ContactInfo)
admin.site.register(Relative, PersonAdmin)
admin.site.register(Visitor, MilitaryPersonAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Category)
admin.site.register(Appartment, AppartmentAdmin)
admin.site.register(Unit)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Damage, DamageAdmin)
admin.site.register(Reservation, ReservationAdmin)
