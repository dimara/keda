from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from reception.models import *
import datetime

class RelativeInline(admin.TabularInline):
    model = Relative
    fk_name = "related"
    extra = 0
    inlines = []

class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    fk_name = "person"
    extra = 0
    inlines = []

class VehicleInline(admin.TabularInline):
    model = Vehicle
    fk_name = "owner"
    extra = 0
    inlines = []

class ReceiptInline(admin.TabularInline):
    model = Receipt
    fk_name = "reservation"
    extra = 0
    inlines = []


class ReservationFormSet(BaseInlineFormSet):
    def get_queryset(self) :
      qs = super(ReservationFormSet, self).get_queryset()
      if len(qs) > 5:
        since = datetime.date.today() - datetime.timedelta(days=30)
        qs = qs.filter(check_in__gte=since)

      return qs


class ReservationAppartmentInline(admin.TabularInline):
    model = Reservation
    fk_name = "appartment"
    form = InlineReservationForm
    formset = ReservationFormSet
    extra = 0
    inlines = []

class NestedReservationInline(NestedTabularInline):
    model = Reservation
    form = InlineReservationForm
    fk_name = "owner"
    extra = 0
    inlines = [
        ReceiptInline,
        ]

class ReservationInline(admin.TabularInline):
    model = Reservation
    form = InlineReservationForm
    fk_name = "owner"
    extra = 0
    inlines = []

class NestedPersonAdmin(NestedModelAdmin):
    list_display = ('surname', 'name', )
    search_fields = ('surname', 'name', )
    ordering = ('surname', )
    form = PersonForm
    inlines = [
        ContactInfoInline,
        VehicleInline,
        ]

class DamageInline(admin.TabularInline):
    model = Damage
    fk_name = "appartment"
    extra = 0
    inlines = []

class NestedReservationAppartmentInline(NestedTabularInline):
    model = Reservation
    form = InlineReservationForm
    fk_name = "appartment"
    extra = 0
    inlines = [
        ReceiptInline,
        ]

class AppartmentAdmin(admin.ModelAdmin):
    list_display = ('appartment', 'rooms', 'beds', 'category', )
    ordering = ('area', 'no', 'category', )
    list_filter = ('area', 'category', )
    search_fields = ('area', 'no', )
    inlines = [
        DamageInline,
        ReservationAppartmentInline,
        ]

class NestedMilitaryPersonAdmin(NestedPersonAdmin):
    list_display = NestedPersonAdmin.list_display + ('rank', 'speciality')
    list_filter = ('active', )
    ordering = ('rank', )
    inlines = NestedPersonAdmin.inlines + [
      NestedReservationInline,
      ]


class NestedStaffAdmin(NestedMilitaryPersonAdmin):
    list_display = NestedMilitaryPersonAdmin.list_display + ('category', 'extra', 'power')
    list_filter = ('extra', 'power' )


class DamageAdmin(admin.ModelAdmin):
    list_filter = ('fixed', )
    ordering = ('tag', 'appartment', )
    list_display = ('appartment', 'tag', 'info')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'check_in', 'check_out', 'appartment')
    ordering = ('check_in', 'check_out', )
    search_fields = ('owner', 'appartment')
    form = ReservationForm
    inlines = [
        ReceiptInline,
        ]

    #def save_model(self, request, obj, form, change):
        #obj.save()

class ReceiptAdmin(admin.ModelAdmin):
    ordering = ('date', )
    list_display = ('date', 'no', 'reservation', 'euro', )
    search_fields = ('no', )

class PeriodAdmin(admin.ModelAdmin):
    ordering = ('name', 'start', )
    list_display = ('name', 'start', 'end', )

class CategoryAdmin(admin.ModelAdmin):
    ordering = ('desc', 'ranking', )
    list_display = ('desc', 'ranking', )

class ContactInfoAdmin(admin.ModelAdmin):
    ordering = ('person', )
    list_display = ('mobile', 'telephone', 'address', 'person', )
    search_fields = ('mobile', 'telephone', 'person', )

class RankAdmin(admin.ModelAdmin):
    ordering = ('level', )
    list_display = ('rank', 'short', 'level', )

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate', 'owner', )
    search_fields = ('plate', )

admin.site.register(Period, PeriodAdmin)
admin.site.register(Person, NestedPersonAdmin)
admin.site.register(Rank, RankAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(Relative, NestedPersonAdmin)
admin.site.register(MilitaryPerson, NestedMilitaryPersonAdmin)
admin.site.register(Staff, NestedStaffAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Appartment, AppartmentAdmin)
admin.site.register(Unit)
#admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Damage, DamageAdmin)
admin.site.register(Reservation, ReservationAdmin)
