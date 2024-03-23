#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.forms import ChoiceField, ModelChoiceField, Field, HiddenInput, BooleanField
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from nested_inlines.forms import BaseNestedModelForm
from reception.constants import *
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
    ident = models.CharField("ID", max_length=30, blank=True, null=True)

    def __unicode__(self):
        ret = u"%s " % (self.surname)
        if self.name:
          ret += self.name
        return ret

    def info(self):
        ret = u"%s" % self.surname
        if self.name:
          ret += u" %s" %self.name
        if self.ident:
          ret += u" -%s-" % self.ident
        return ret

    def identify(self):
        mobiles = ",".join([c.mobile for c in self.contacts.all()])
        plates = ",".join([v.plate for v in self.vehicles.all()])
        return u"Mobiles: %s, Plates: %s" % (mobiles, plates)

    def person_info(self):
        try:
          if self.militaryperson:
            try:
              return ("visitor", self.militaryperson.visitor.info())
            except:
              try:
                return ("staff", self.militaryperson.staff.info())
              except:
                return ("militaryperson", self.militaryperson.info())
        except:
          return ("person", self.info())


class Vehicle(models.Model):
    plate = models.CharField("Plate", max_length=10, blank=True, null=True)
    color = models.CharField("Color", max_length=20, blank=True, null=True)
    brand = models.CharField("Brand", max_length=20, blank=True, null=True)
    model = models.CharField("Model", max_length=20, blank=True, null=True)
    owner = models.ForeignKey(Person, models.SET_NULL, related_name="vehicles", null=True, blank=True)

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
    person = models.ForeignKey(Person, models.CASCADE, related_name="contacts", null=True, blank=True)

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

    related = models.ForeignKey(Person, models.CASCADE, related_name="relatives", null=True, blank=True)
    relationship = models.CharField("Relationship", choices=RELATIONSHIPS, max_length=30, blank=True, null=True)

    def __unicode__(self):
        ret = super(Relative, self).__unicode__()
        if self.relationship:
            ret += u" - %s" % self.relationship
        return ret


class MilitaryPerson(Person):
    rank = models.ForeignKey(Rank, models.SET_NULL, related_name="military_persons", null=True, blank=True)
    active = models.BooleanField("Active", default=True)
    speciality = models.CharField("Speciality", max_length=20, null=True, blank=True)

    def info(self):
        ret = super(MilitaryPerson, self).info()
        if self.speciality:
            ret = u"(%s) %s" % (self.speciality, ret)
        if self.rank:
            ret = u"%s %s" % (self.rank.short, ret)
        if not self.active:
            ret += u" ε.α."
        return ret

    def person_info(self):
        try:
          return ("staff", self.staff.info())
        except:
          return ("militaryperson", self.info())

    def __unicode__(self):
        return self.info()


class Unit(models.Model):
    name = models.CharField("Name", max_length=20)
    internal = models.CharField("Internal Number", max_length=10, null=True, blank=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.internal)


class Staff(MilitaryPerson):
    CATEGORIES = (
      (u"ΟΡΓ", u"ΟΡΓΑΝΙΚΟΣ"),
      (u"ΑΠΟ", u"ΑΠΟΣΠΑΣΜΕΝΟΣ"),
      )

    category = models.CharField("Category", max_length=20, choices=CATEGORIES, null=True, blank=True)
    extra = models.CharField("Extra Info", max_length=25, null=True, blank=True)
    power = models.BooleanField("In Unit-Power", default=True)
    unit = models.ForeignKey(Unit, models.SET_NULL, related_name="staff", null=True, blank=True)

    def person_info(self):
              return ("staff", self.info())


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
      (u"Ε", "Ε"),
      (u"Μ1", "Μ1"),
      (u"Μ2", "Μ2"),
      (u"Μ3", "Μ3"),
      (u"Μ4", "Μ4"),
      (u"Μ5", "Μ5"),
      (u"Μ3Ε", "Μ3Ε")
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
    category = models.ForeignKey(Category, models.SET_NULL, related_name="appartments", default=None, blank=True, null=True)
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

    @property
    def rates(self):
        """ Return a list for regular/schools/unit """
        if self.area in (u"Μ1", u"Μ2", u"Μ3"):
             return [R_LOW, R_SCHOOL, R_UNIT]
        elif self.area in (u"Μ4", u"Μ5"):
             return [R_MED, R_NA, R_NA]
        elif self.area in (u"Α"):
             return [R_LUX, R_NA, R_NA]
        elif self.area in (u"Β", u"Ζ"):
            if self.rooms == 2:
                return [R_HIGH, R_NA, R_UNITB]
            else:
                return [R_HIGHB, R_NA, R_UNITB]
        return [R_NA, R_NA, R_NA]


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
    appartment = models.ForeignKey(Appartment, models.CASCADE, related_name="damages", null=True, blank=True)
    info = models.TextField("Further Info", null=True, blank=True)
    notified = models.ForeignKey(Unit, models.SET_NULL, null=True, blank=True)
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
      (7, "Seven"),
      (8, "Eight"),
      (9, "Nine"),
    )

    AGENTS = (
      (RA_GEA, u"ΓΕΑ/Β3"),
      (RA_EA, u"ΕΑ"),
      (RA_MY, u"Μ.Υ"),
      (RA_DKTS, u"ΔΚΤΗΣ"),
      (RA_YDKTS, u"ΥΔΚΤΗΣ"),
      (RA_ASF, u"ΑΣΦΑΛΕΙΑ"),
      (RA_REC, u"RECEPTION"),
      (RA_GEETHA, u"ΓΕΕΘΑ"),
      )

    STATUSES = (
      (RS_PENDING, "Pending"),
      (RS_CONFIRM, "Confirmed"),
      (RS_CANCEL, "Canceled"),
      (RS_CHECKOUT, "Checked OUT"),
      (RS_UNKNOWN, "Unknown"),
      )

    RESERVATION_TYPES = (
      (RT_REGULAR, u"ΤΑΚΤΙΚΟΣ"),
      (RT_DAILY, u"ΠΑΡ/ΣΤΗΣ"),
      (RT_OSSEAY, u"ΟΣΣΕΑΥ"),
      (RT_UNIT, u"ΜΟΝΑΔΑ"),
      (RT_SCHOOLS, u"ΣΧΟΛΕΙΑ"),
      (RT_CLIMS, u"CLIMS"),
      (RT_AGAMON, u"ΑΓΑΜΩΝ"),
      (RT_EXTUNIT, u"ΑΠΟΣ/ΝΟΙ"),
      (RT_OTHER, u"ΑΛΛΟ"),
      )

    check_in = models.DateField("Check In", null=True, blank=True)
    check_out = models.DateField("Check Out", null=True, blank=True)
    owner = models.ForeignKey(MilitaryPerson, models.CASCADE, related_name="reservations")
    agent = models.IntegerField("Agent", choices=AGENTS, null=True, blank=True)
    persons = models.IntegerField("Persons", choices=PERSONS, default=1,
                                  null=True, blank=True)
    appartment = models.ForeignKey(Appartment, models.SET_NULL, related_name="reservations", null=True, blank=True)
    status = models.IntegerField("Status", choices=STATUSES, null=True, blank=True)
    res_type = models.IntegerField("Type", choices=RESERVATION_TYPES,
                                null=True, blank=True)
    telephone = models.BooleanField("Telephone", default=False)
    book_ref = models.IntegerField("No", null=True, blank=True)
    notes = models.CharField("Notes", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return  u"Από %s έως %s, Όνομα: %s, Άτομα: %s, Δωμάτιο: %s, Status: %s" % \
                  (self.check_in, self.check_out, self.owner, self.persons, self.appartment, self.get_status_display())

    @property
    def info(self):
        return  u"Από %s έως %s, Όνομα: %s, Άτομα: %d, Δωμάτιο: %s, Status: %s" % \
                  (self.check_in, self.check_out, self.owner, self.persons, self.appartment, self.get_status_display())

    @property
    def details(self):
        return  u"Από %s έως %s, Δωμάτιο: %s, Status: %s" % \
                  (self.check_in, self.check_out, self.appartment, self.get_status_display())
    @property
    def period(self):
        ret = u"%s..." % self.check_in.strftime("%d %b")
        if self.check_out:
            ret += u"%s" % self.check_out.strftime("%d %b")
        return ret

    def active(self, start=None, include_all=True):
        if not start:
          start = datetime.date.today()
        end = start + datetime.timedelta(days=1)
        status = self.inside(start, end)
        if include_all:
            return status
        else:
            return self.status in (RS_CONFIRM, RS_PENDING, RS_UNKNOWN) and status

    @property
    def notifications(self):
      today = datetime.date.today()
      errors = []
      if self.check_in < today and self.status == RS_PENDING:
        errors.append(RE_NOTARRIVED)
      if self.check_out and self.check_out < today:
        if self.status == RS_CONFIRM:
          errors.append(RE_NOTLEFT)
        if self.status == RS_PENDING:
          errors.append(RE_NEVERCAME)
      if self.res_type == RT_REGULAR:
        if self.agent not in (RA_GEA, RA_MY, RA_EA):
          errors.append(RE_NOAGENT)
        if not self.book_ref and self.status != RS_CANCEL:
          errors.append(RE_NOBOOK)
      if self.res_type in (RT_REGULAR, RT_DAILY) and self.status == RS_CHECKOUT:
        if not self.receipt or self.receipt.pending:
          errors.append(RE_NOTPAYED)
      return (errors, sum(errors)>=10)

    def on(self, start, end):
      if start and end:
          return self.check_in == start and self.check_out == end
      if start:
          return self.check_in == start
      if end:
          return self.check_out == end
      return False

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
                  # case of period is open and start is before check out
                  # { ]
                  (self.check_out >= start and not end) or
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

    @property
    def receipt(self):
        receipts = self.receipts.order_by("-date")
        if receipts:
            return receipts[0]
        else:
            return None

class Period(models.Model):
    name = models.CharField("Period", max_length=10, null=True, blank=True)
    start = models.DateField("Starting Date")
    end = models.DateField("Ending Date")

    def __unicode__(self):
        r = u"%s" % (self.name)
        if self.start:
            r += " (%s .." % self.start.strftime("%d %b")
        if self.end:
            r += " %s)" % self.end.strftime("%d %b")

        return r

class PersonForm(BaseNestedModelForm):
    RESOLVE = (
      ("", "-------"),
      ("IGNORE", "Ignore"),
      ("USE", "Use Existing"),
      )

    check = BooleanField(required=False)
    resolve = Field(required=False, widget=HiddenInput())
    existing = Field(required=False, widget=HiddenInput())


    class Meta:
        model = Person
        fields = "__all__"

    def full_clean(self):
        self.cleaned_data = {}
        super(PersonForm, self).full_clean()
        check = self.cleaned_data.get("check", None)
        resolve = self.cleaned_data.get("resolve", None)
        existing = self.cleaned_data.get("existing", None)
        name = self.cleaned_data.get("name", None)
        surname = self.cleaned_data.get("surname", None)
        conflicting = Person.objects.filter(surname=surname).exclude(id=self.instance.id)
        if conflicting and (check or not self.instance.id):
          self.fields["resolve"] = ChoiceField(choices=PersonForm.RESOLVE, required=False, label="Resolve")
          self.fields["existing"] = ModelChoiceField(queryset=conflicting, required=False, label="Existing")
          msgs = [u"Conflicting Person:", ]
          for c in conflicting:
            msgs.append("%s %s" % (": ".join(c.person_info()), c.identify()))
          if not resolve:
            # modify
            self._update_errors({
              "resolve": ["Choose a way to resolve conflict!"],
              NON_FIELD_ERRORS: msgs,
              })
          elif resolve == "IGNORE":
            pass
          elif resolve == "USE":
            if not existing:
              self._update_errors({
                "existing": ["Choose an existing entry!"],
                NON_FIELD_ERRORS: msgs,
                })
            else:
              self.instance.id = existing


class ReservationForm(BaseNestedModelForm):
    RESOLVE = (
      ("", "-------"),
      ("FORCE", "Force save"),
      ("SWAP", "Swap Appartments"),
      )

    resolve = Field(label="Resolve", required=False, widget=HiddenInput())
    period = ModelChoiceField(queryset=Period.objects.all(), required=False, label="Period")

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields["owner"].queryset = MilitaryPerson.objects.prefetch_related("rank").all().order_by("surname", "name")

    class Meta:
            model = Reservation
            fields = ["res_type", "agent", "period", "check_in", "check_out", "owner", "appartment",
                      "status", "persons", "book_ref", "telephone"]


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
        self.cleaned_data = {}
        super(ReservationForm, self).full_clean()
        if self.instance.appartment:
            reservations = self.instance.appartment.reservations.filter(status__in=[RS_PENDING, RS_CONFIRM, RS_UNKNOWN]).exclude(id=self.instance.id)
            conflicting = []
            for r in reservations:
                if (self.instance.status in (RS_PENDING, RS_CONFIRM, RS_UNKNOWN) and
                    r.owner.id != self.instance.owner.id and
                    r.inside(self.instance.check_in, self.instance.check_out)):
                    conflicting.append(r)
            if conflicting:
                self.fields["resolve"] = ChoiceField(choices=ReservationForm.RESOLVE, required=False, label="Resolve")
                resolve = self.cleaned_data.get("resolve", None)
                print("resolving....")
                msgs = [u"Conflicting Reservations:", ]
                if not resolve:
                  self._update_errors({
                    "resolve": ["Choose a way to resolve conflict!"],
                    NON_FIELD_ERRORS: msgs + [r.info for r in conflicting],
                    })
                if resolve == "FORCE":
                  pass
                if resolve == "SWAP":
                  if len(conflicting) > 1:
                    self._update_errors({
                      "resolve": ["Swap is not supported for many conflicts!"],
                      NON_FIELD_ERRORS: msgs + [r.info for r in conflicting],
                      })
                  else:
                    # TODO: find first available appartment
                    appartment = None
                    if self.instance.id:
                      existing = Reservation.objects.get(id=self.instance.id)
                      appartment = existing.appartment
                    conflicting[0].appartment = appartment
                    conflicting[0].save()
                msg = (u"Conflicting Reservations:\n%s\nRESOLVE: %s\nChanged: %s\nNew/Updated: %s" %
                       ("\n".join([c.info for c in conflicting]), resolve, conflicting[0].info, self.instance.info))
                print(msg.encode("utf-8"))



class InlineReservationForm(ReservationForm):
    pass

class Receipt(models.Model):
    date = models.DateTimeField("Date")
    no = models.CharField("No", max_length=10)
    reservation = models.ForeignKey(Reservation, models.CASCADE, related_name="receipts")
    euro = models.DecimalField("Euro", decimal_places=2, max_digits=10 )
    pending = models.BooleanField("Pending", default=False)

    def __unicode__(self):
        return u"No: %s, Euro: %0.2f, Name: %s, Reservation: %s" % \
                    (self.no, self.euro, self.reservation.owner, self.reservation)

    def inside(self, start, end):
       if self.date:
           if start:
              if end:
                  return self.date.date() >= start and self.date.date() <= end
              else:
                  return self.date.date() > start
       return False
