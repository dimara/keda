#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
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
        return u"%s %s" % (self.surname, self.name)


class Vehicle(models.Model):
    plate = models.CharField("Plate", max_length=10, blank=True, null=True)
    color = models.CharField("Color", max_length=20, blank=True, null=True)
    brand = models.CharField("Brand", max_length=20, blank=True, null=True)
    model = models.CharField("Model", max_length=20, blank=True, null=True)
    owner = models.ForeignKey(Person, related_name="vehicles", null=True, blank=True)

    def __unicode__(self):
        return u"%s: %s %s (%s)" % (self.plate, self.brand, self.model, self.color)


class ContactInfo(models.Model):
    mobile = models.CharField("Mobile Phone", max_length=30, blank=True, null=True)
    telephone = models.CharField("Telephone", max_length=30, blank=True, null=True)
    address = models.CharField("Address", max_length=30, blank=True, null=True)
    person = models.ForeignKey(Person, related_name="contacts", null=True, blank=True)

    def __unicode__(self):
        return u"Address: %s, Tel: %s, Mobile: %s" % (self.address, self.telephone, self.mobile)


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
      )

    related = models.ForeignKey(Person, related_name="relatives", null=True, blank=True)
    relationship = models.CharField("Relationship", choices=RELATIONSHIPS, max_length=30, blank=True, null=True)


class MilitaryPerson(Person):
    rank = models.ForeignKey(Rank, related_name="military_persons", null=True, blank=True)
    active = models.BooleanField("Active", default=True)
    speciality = models.CharField("Speciality", max_length=20, null=True, blank=True)

    def info(self):
        ret = super(MilitaryPerson, self).__unicode__()
        if self.speciality:
            ret = u"(%s) %s" % (self.speciality, ret)
        if self.rank:
            ret = u"%s %s" % (self.rank, ret)
        return ret

class Visitor(MilitaryPerson):
    member = models.BooleanField("Member", default=False)

    def __unicode__(self):
        ret = super(Visitor, self).__unicode__()
        if self.member:
            ret += u" (ΜΕΛΟΣ)"
        return ret

class VisitorForm(ModelForm):
    class Meta:
            model = Visitor


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
      ("B", "B"),
      ("Z", "Z"),
      ("M1", "M1"),
      ("M2", "M2"),
      ("M3", "M3"),
      ("M4", "M4"),
      ("M5", "M5"),
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
      ("AC" , "AirCondition"),
      ("TV", "Television"),
      ("DIRTY", "Extremely Dirty, Needs cleaning, etc."),
      ("ELECTRICAL", "Lights, Sockets, etc."),
      ("HYDRAVLICS", "Water leak, toilet, boiler, etc."),
      ("DOORS", "Doors, Locks, Windows, etc."),
      ("EQUIPMENT", "Broken/Missing equipment, etc."),
      ("WALLS", "Needs painting, broken sealing, etc."),
      ("OTHER", "Other kind of damage"),
    )
    tag = models.CharField("Tag", choices=DAMAGES, max_length=30)
    appartment = models.ForeignKey(Appartment, related_name="damages", null=True, blank=True)
    info = models.TextField("Further Info", null=True, blank=True)
    notified = models.ForeignKey(Unit, null=True, blank=True)
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

    RESERVATION_TYPES = (
      (u"ΠΑΡ/ΣΤΗΣ (ΤΑΚΤ)", "ΠΑΡ/ΣΤΗΣ (ΤΑΚΤ)"),
      (u"ΠΑΡ/ΣΤΗΣ", "ΠΑΡ/ΣΤΗΣ"),
      (u"ΟΣΣΕΑΥ", "ΟΣΣΕΑΥ"),
      (u"ΜΟΝΑΔΑ", "ΜΟΝΑΔΑ"),
      (u"ΣΧΟΛΕΙΑ", "ΣΧΟΛΕΙΑ"),
      )

    STATUSES = (
      ("PENDING", "Pending Confirmation"),
      ("CONFIRMED", "Confirmed"),
      ("CANCELED", "Canceled"),
      )

    check_in = models.DateField("Check In", null=True, blank=True)
    check_out = models.DateField("Check Out", null=True, blank=True)
    info = models.TextField("Further Info", max_length=200, null=True, blank=True)
    owner = models.ForeignKey(Person, related_name="reservations")
    persons = models.IntegerField("Persons", choices=PERSONS, default=1,
                                  null=True, blank=True)
    appartment = models.ForeignKey(Appartment, related_name="reservations")
    status = models.CharField("Status", choices=STATUSES, max_length=20, null=True, blank=True)
    res_type = models.CharField("Type", choices=RESERVATION_TYPES, max_length=20,
                                null=True, blank=True)

    def __unicode__(self):
        return  u"Από %s έως %s -> %s" % (self.check_in, self.check_out, self.appartment)

    @property
    def info(self):
        return  u"Από %s έως %s, Όνομα: %s, Άτομα: %d, Δωμάτιο: %s" % \
                  (self.check_in, self.check_out, self.owner, self.persons, self.appartment)

    @property
    def period(self):
        return u"%s..%s" % (self.check_in, self.check_out)

    def active(self, date=None):
        if not date:
            date = datetime.date.today()
        return (self.status == "CONFIRMED" and
                self.check_in and self.check_in <= date and
                (not self.check_out or (self.check_out and self.check_out >= date)))

    def inside(self, start, end):
        return (
             (self.check_in >= start and self.check_in <= end) or
             (self.check_out >= start and self.check_out <= end) or
             (self.check_in >= start and self.check_out <= end) or
             (self.check_in <= start and self.check_out >= end)
           )


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


class Period(models.Model):
    start = models.DateField("Starting Date")
    end = models.DateField("Ending Date")

