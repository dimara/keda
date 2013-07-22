#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.forms import ChoiceField, ModelChoiceField
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from nested_inlines.forms import BaseNestedModelForm
import datetime

# Create your models here.
class Rank(models.Model):
    WEAPONS = (
      (u"ΕΣ", "ΕΣ"),
      (u"ΠΝ", "ΠΝ"),
      (u"ΠΑ", "ΠΑ"),
      )

    weapon = models.CharField("Force", choices=WEAPONS, max_length=5, default='ΠΑ')
    rank = models.CharField("Rank", max_length=20)
    short = models.CharField("Rank (abbreviation)", max_length=10)
    level = models.IntegerField("Level", default=0, null=True, blank=True)

    def __unicode__(self):
        return self.short

    @property
    def category(self):
        """ 4 categories used for staff.

        pol.pr., sminites, ypaks, aks
        """
        if self.level in (0, 1):
            return self.level
        if self.level in (2, 3, 4, 5):
            return 2
        return 3


class Person(models.Model):
    name = models.CharField("First Name", max_length=30, blank=True, null=True)
    surname = models.CharField("Last Name", max_length=30)

    def __unicode__(self):
        ret = u"%s " % (self.surname)
        if self.name:
          ret += self.name
        return ret

    class Meta:
        unique_together = ('name', 'surname',)

    def info(self):
        ret = u"%s" % self.surname
        if self.name:
          ret += u" %s" %self.name
        return ret

class Vehicle(models.Model):
    plate = models.CharField("Plate", max_length=10, blank=True, null=True)
    color = models.CharField("Color", max_length=20, blank=True, null=True)
    brand = models.CharField("Brand", max_length=20, blank=True, null=True)
    model = models.CharField("Model", max_length=20, blank=True, null=True)
    owner = models.ForeignKey(Person, related_name="vehicles", null=True, blank=True)

    def __unicode__(self):
        ret = u"%s" % self.plate
        if self.brand:
            ret += u",%s" % self.brand
        if self.model:
            ret += u",%s" % self.model
        if self.color:
            ret += u" (%s)" % self.color
        return ret


class ContactInfo(models.Model):
    mobile = models.CharField("Mobile Phone", max_length=30, blank=True, null=True)
    telephone = models.CharField("Telephone", max_length=30, blank=True, null=True)
    address = models.CharField("Address", max_length=30, blank=True, null=True)
    person = models.ForeignKey(Person, related_name="contacts", null=True, blank=True)

    def __unicode__(self):
        ret = u""
        if self.mobile:
          ret += u"Mobile: %s" % self.mobile
        if self.telephone:
          ret += u" Tel: %s, " % self.telephone
        if self.address:
          ret += u" Address: %s, " % self.address

        return ret


class Relative(Person):
    RELATIONSHIPS = (
      (u"ΥΙΟΣ", "ΥΙΟΣ"),
      (u"ΚΟΡΗ", "ΚΟΡΗ"),
      (u"ΠΑΤΕΡΑΣ", "ΠΑΤΕΡΑΣ"),
      (u"ΜΗΤΕΡΑ", "ΜΗΤΕΡΑ"),
      (u"ΣΥΖΥΓΟΣ", "ΣΥΖΥΓΟΣ"),
      (u"ΑΝΗΨΙΑ", "ΑΝΗΨΙΑ"),
      (u"ΑΔΕΡΦΙΑ", "ΑΔΕΡΦΙΑ"),
      (u"ΕΓΓΟΝΙΑ", "ΕΓΓΟΝΙΑ"),
      (u"ΝΥΦΗ", "ΝΥΦΗ"),
      (u"ΓΑΜΠΡΟΣ", "ΓΑΜΠΡΟΣ"),
      (u"ΠΕΘΕΡΟΣ", "ΠΕΘΕΡΟΣ"),
      (u"ΠΕΘΕΡΑ", "ΠΕΘΕΡΑ"),
      )

    related = models.ForeignKey(Person, related_name="relatives", null=True, blank=True)
    relationship = models.CharField("Relationship", choices=RELATIONSHIPS, max_length=30, blank=True, null=True)

    def __unicode__(self):
        ret = super(Relative, self).__unicode__()
        if self.relationship:
            ret += u" - %s" % self.relationship
        return ret


class MilitaryPerson(Person):
    rank = models.ForeignKey(Rank, related_name="military_persons", null=True, blank=True)
    active = models.BooleanField("Active", default=True)
    speciality = models.CharField("Speciality", max_length=20, null=True, blank=True)

    def info(self):
        ret = super(MilitaryPerson, self).info()
        if self.speciality:
            ret = u"(%s) %s" % (self.speciality, ret)
        if self.rank:
            ret = u"%s %s" % (self.rank.short, ret)
        if not self.active:
            ret += u" (ΕΑ)"
        return ret

class Visitor(MilitaryPerson):
    member = models.BooleanField("Member", default=False)

    def __unicode__(self):
        ret = super(Visitor, self).__unicode__()
        if self.member:
            ret += u" (ΜΕΛΟΣ)"
        return ret

    def info(self):
        ret = super(Visitor, self).info()
        if self.member:
            ret += u" (ΜΕΛΟΣ)"
        return ret


class Staff(MilitaryPerson):
    CATEGORIES = (
      (u"ΟΡΓ", "ΟΡΓΑΝΙΚΟΣ"),
      (u"ΑΠΟ", "ΑΠΟΣΠΑΣΜΕΝΟΣ"),
      )

    category = models.CharField("Category", max_length=20, choices=CATEGORIES, null=True, blank=True)
    extra = models.CharField("Extra Info", max_length=25, null=True, blank=True)


class Category(models.Model):
    desc = models.CharField("Description", max_length=20, blank=True, null=True)
    ranking = models.IntegerField("Ranking", blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.desc)


class Appartment(models.Model):
    AREAS = (
      (u"Α", "Α"),
      (u"Ι", "Ι"),
      (u"Β", "Β"),
      (u"Ζ", "Ζ"),
      (u"Μ1", "Μ1"),
      (u"Μ2", "Μ2"),
      (u"Μ3", "Μ3"),
      (u"Μ4", "Μ4"),
      (u"Μ5", "Μ5"),
    )
    BEDS = (
      (0, "None"),
      (1, "One"),
      (2, "Two"),
      (3, "Three"),
      (4, "Four"),
      (5, "Five"),
      (6, "Six"),
    )

    RANKINGS = (
      (1, "Low"),
      (3, "Medium"),
      (5, "High"),
      )

    area = models.CharField("Area", choices=AREAS, max_length=5)
    no = models.CharField("Number", max_length=5)
    rooms = models.IntegerField("Rooms", default=1, blank=True, null=True)
    double = models.IntegerField("Double Beds", default=0, choices=BEDS)
    single = models.IntegerField("Single Beds", default=2, choices=BEDS)
    bunk = models.IntegerField("Bunk Beds", default=0, choices=BEDS)
    category = models.ForeignKey(Category, related_name="appartments", default=None, blank=True, null=True)
    ranking = models.IntegerField("Quality Ranking", choices=RANKINGS, default=None, blank=True, null=True)

    @property
    def beds(self):
        return u"%dΔ+%dΜ+%dΚ" % (self.double, self.single, self.bunk)

    def __unicode__(self):
        return u"%s-%s" % (self.area, self.no)

    @property
    def info(self):
        return u"%s-%s, Δωμάτια: %d (%dΔ+%dΜ+%dΚ)" % \
                (self.area, self.no, self.rooms, self.double, self.single, self.bunk)

    @property
    def appartment(self):
        return u"%s-%s" % (self.area, self.no)

class Unit(models.Model):
    name = models.CharField("Name", max_length=20)
    internal = models.CharField("Internal Number", max_length=10, null=True, blank=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.internal)


class Damage(models.Model):
    DAMAGES = (
      ("AC" , "A/C"),
      ("TV", "TV"),
      ("DIRTY", "Πολύ βρώμικο, Θέλει καθάρισμα, κλπ."),
      ("ELECTRICAL", "Φώτα, Μπρίζες, κλπ."),
      ("HYDRAVLICS", "Διαρροές, τουαλέτες, Θερμοσίφωνες, κλπ."),
      ("DOORS", "Πόρτες, Κλειδαριές, Παράθυρα, κλπ."),
      ("EQUIPMENT", "Χαλασμένος/Ελλιπής εξοπλισμός, etc."),
      ("WALLS", "Θέλει βάψιμο, χαλασμένο ταβάνι/τοίχοι, etc."),
      ("OTHER", "Άλλου είδους βλάβη"),
    )
    tag = models.CharField("Tag", choices=DAMAGES, max_length=30)
    appartment = models.ForeignKey(Appartment, related_name="damages", null=True, blank=True)
    info = models.TextField("Further Info", null=True, blank=True)
    notified = models.ForeignKey(Unit, null=True, blank=True)
    date = models.DateField("Date", null=True, blank=True)
    fixed = models.BooleanField("Fixed", default=False)

    def __unicode__(self):
        r = u"%s -> %s: %s" % (self.appartment, self.tag, self.info)
        if self.fixed:
            r += " (FIXED)"

        return r


class Reservation(models.Model):
    PERSONS = (
      (1, "One"),
      (2, "Two"),
      (3, "Three"),
      (4, "Four"),
      (5, "Five"),
      (6, "Six"),
    )

    STATUSES = (
      ("PENDING", "Pending Confirmation"),
      ("CONFIRMED", "Confirmed"),
      ("CANCELED", "Canceled"),
      ("CHECKEDOUT", "Checked OUT"),
      ("UNKNOWN", "Unknown"),
      )

    check_in = models.DateField("Check In", null=True, blank=True)
    check_out = models.DateField("Check Out", null=True, blank=True)
    owner = models.ForeignKey(Person, related_name="reservations")
    persons = models.IntegerField("Persons", choices=PERSONS, default=1,
                                  null=True, blank=True)
    appartment = models.ForeignKey(Appartment, related_name="reservations", null=True, blank=True)
    status = models.CharField("Status", choices=STATUSES, max_length=20, null=True, blank=True)

    def __unicode__(self):
        return  u"Από %s έως %s, Όνομα: %s, Άτομα: %s, Δωμάτιο: %s, Status: %s" % \
                  (self.check_in, self.check_out, self.owner, self.persons, self.appartment, self.get_status_display())

    def owner_info(self):
        try:
          if self.owner.militaryperson:
            try:
              return ("visitor", self.owner.militaryperson.visitor.info())
            except:
              try:
                return ("staff", self.owner.militaryperson.staff.info())
              except:
                return ("militaryperson", self.owner.militaryperson.info())
        except:
          return ("person", self.owner.info())


    @property
    def info(self):
        return  u"Από %s έως %s, Όνομα: %s, Άτομα: %d, Δωμάτιο: %s, Status: %s" % \
                  (self.check_in, self.check_out, self.owner, self.persons, self.appartment, self.status)

    @property
    def period(self):
        ret = u"%s..." % self.check_in
        if self.check_out:
            ret += u"%s" % self.check_out
        return ret

    def active(self, start=None, include_all=True):
        if not start:
          start = datetime.date.today()
        end = start + datetime.timedelta(days=1)
        status = self.inside(start, end)
        if include_all:
            return status
        else:
            return self.status in ("CONFIRMED", "PENDING", "UNKNOWN") and status

    def inside(self, start, end):
        #TODO: please make it simpler
        # case that period or reservation are defined
        # reservation: [   ]
        # period:      {   }
        if self.check_in and start:
          # cases that reservation is fully defined
          # [   ]
          if self.check_out:
              return (
                # case of period start is between reservation dates
                # [ { ] (})
                (self.check_in <= start and self.check_out >= start) or
                  # {   }
                  (end and (
                    # case of period end is between reservation dates
                    # {  [  }  ]
                    (self.check_in <= end and self.check_out >= end) or
                    # case of reservation is between period dates
                    # { [   ] }
                    (self.check_in >= start and self.check_out <= end) or
                    # case of period is between reservation dates
                    # [ {  } ]
                    (self.check_in <= start and self.check_out >= end)
                    )
                  )
                )
          # case of partialy defined reservations
          # [
          else:
              # case of partialy defined period or case of end after check in
              # [ {
              # { [
              # { [ }
              return not end or self.check_in <= end

        return False

    def clean(self):
        super(Reservation, self).clean()
        if self.appartment:
            all_res = self.appartment.reservations.all()
            if self.id:
                all_res = all_res.exclude(id=self.id)
                res = Reservation.objects.get(id=self.id)
            messages = []
            errors = []
            conflicting_res_ids = []
            for r in all_res:
                if (r.status in ("PENDING", "CONFIRMED", "UNKNOWN") and
                    self.status in ("PENDING", "CONFIRMED", "UNKNOWN") and
                    r.inside(self.check_in, self.check_out)):
                    messages.append(u"\n%s" % r.info)
                    conflicting_res_ids.append(r.id)
            if conflicting_res_ids:
                err = ReservationConflictError(messages, conflicting_res_ids, self.id)
                raise err


    @property
    def receipt(self):
        if self.receipts.all():
            return self.receipts.all()[0]
        else:
            return None

class Period(models.Model):
    name = models.CharField("Period", max_length=10, null=True, blank=True)
    start = models.DateField("Starting Date")
    end = models.DateField("Ending Date")

    def __unicode__(self):
        r = u"%s" % (self.name)
        if self.start:
            r += " (%s .." % self.start
        if self.end:
            r += " %s)" % self.end

        return r

class ReservationConflictError(Exception):
    pass


class ReservationForm(BaseNestedModelForm):
    RESOLVE = (
      ("", "-------"),
      ("FORCE", "Force save"),
      ("SWAP", "Swap Appartments"),
      )

    resolve = ChoiceField(choices=RESOLVE, required=False, label="Resolve")
    period = ModelChoiceField(queryset=Period.objects.all(), required=False, label="Period")

    class Meta:
            model = Reservation
            fields = ["period", "check_in", "check_out", "owner", "appartment", "persons", "status", "resolve"]

    def resolve_conflict(self, e):
        resolve = self.cleaned_data.get("resolve", None)
        conflicting = Reservation.objects.get(id=e.args[1][0])
        print "resolving...."
        msgs = [u"Conflicting Reservations:", ]
        if not resolve:
          self._update_errors({
            "resolve": ["Choose a way to resolve conflict!"],
            NON_FIELD_ERRORS: msgs + e.args[0],
            })
        if resolve == "FORCE":
          pass
        if resolve == "SWAP":
          if len(e.args[1]) > 1:
            self._update_errors({
              "resolve": ["Swap is not supported for many conflicts!"],
              NON_FIELD_ERRORS: msgs + e.args[0],
              })
          else:
            # TODO: find first available appartment
            appartment = None
            if e.args[2]:
              existing = Reservation.objects.get(id=e.args[2])
              appartment = existing.appartment
            conflicting.appartment = appartment
            conflicting.save()
        print(u"%s\nRESOLVE: %s\nChanged: %s\nNew/Updated: %s" % (e.args[0][0], resolve, conflicting.info, self.instance.info))


    def clean(self):
        super(ReservationForm, self).clean()
        def get_datetime(value):
            if value:
              y, m, d = map(int, value.split("-"))
              return datetime.date(y, m, d)

        period = self.cleaned_data.get("period", None)
        check_in = self.cleaned_data.get("check_in", None)
        check_out = self.cleaned_data.get("check_out", None)
        if period and (check_in or check_out):
          self._update_errors({
            "period": ["You must provide either period or dates!"],
            })
        if period:
          self.cleaned_data["check_in"] = period.start
          self.cleaned_data["check_out"] = period.end
        return self.cleaned_data


    def full_clean(self):
        try:
          super(ReservationForm, self).full_clean()
        except Exception, e:
          self.resolve_conflict(e)


class InlineReservationForm(ReservationForm):
    pass

class Receipt(models.Model):
    RECEIPT_TYPES = (
      (u"ΤΑΚΤΙΚΟΣ", "ΤΑΚΤΙΚΟΣ"),
      (u"ΗΜ.ΑΠΟΖ", "ΗΜ.ΑΠΟΖ."),
      (u"ΟΣΣΕΑΥ", "ΟΣΣΕΑΥ"),
      )
    rtype = models.CharField("Type", choices=RECEIPT_TYPES, max_length=20,
                                null=True, blank=True)
    no = models.CharField("No", max_length=10)
    reservation = models.ForeignKey(Reservation, related_name="receipts")
    euro = models.DecimalField("Euro", decimal_places=2, max_digits=10 )

    def __unicode__(self):
        return u"Type: %s, No: %s, Euro: %0.2f, Name: %s, Reservation: %s" % \
                    (self.rtype, self.no, self.euro, self.reservation.owner, self.reservation)

    def inside(self, first, last):
       if first:
	 if last:
           return self.no >= first and self.no <= last
         else:
           return self.no >= first
       else:
         if last:
           return self.no <= last
         else:
           return True

class Keda(models.Model):
    RESERVATION_TYPES = (
      (u"ΤΑΚΤΙΚΟΣ", "ΤΑΚΤΙΚΟΣ"),
      (u"ΠΑΡ/ΣΤΗΣ", "ΠΑΡ/ΣΤΗΣ"),
      (u"ΟΣΣΕΑΥ", "ΟΣΣΕΑΥ"),
      (u"ΜΟΝΑΔΑ", "ΜΟΝΑΔΑ"),
      (u"ΣΧΟΛΕΙΑ", "ΣΧΟΛΕΙΑ"),
      )

    res_type = models.CharField("Type", choices=RESERVATION_TYPES, max_length=20,
                                null=True, blank=True)
    telephone = models.BooleanField("Telephone", default=False)
    book_ref = models.IntegerField("No", null=True, blank=True)
    reservation = models.OneToOneField(Reservation, related_name="keda")
    info = models.CharField("Further Info", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return u"Reservation: %s, Type: %s, Telephone: %s, No: %s, Info: %s" % \
               (self.reservation, self.res_type, self.telephone, self.book_ref, self.info)
