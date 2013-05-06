#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Vehicle(models.Model):
    plate = models.CharField("Plate", max_length=10, blank=True, null=True)
    color = models.CharField("Color", max_length=20, blank=True, null=True)
    brand = models.CharField("Brand", max_length=20, blank=True, null=True)
    model = models.CharField("Model", max_length=20, blank=True, null=True)

    def __unicode__(self):
        return "%s: %s %s (%s)" % (self.plate, self.brand, self.model, self.color)

class ContactInfo(models.Model):
    mobile = models.CharField("Mobile Phone", max_length=30, blank=True, null=True)
    telephone = models.CharField("Telephone", max_length=30, blank=True, null=True)
    address = models.CharField("Address", max_length=30, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.mobile


class Person(models.Model):
    name = models.CharField("First Name", max_length=30, blank=True, null=True)
    surname = models.CharField("Last Name", max_length=30)

    def __unicode__(self):
        return u"%s %s" % (self.surname, self.name)


class Rank(models.Model):
    WEAPONS = (
      ("ΕΣ", "ΕΣ"),
      ("ΠΝ", "ΠΝ"),
      ("ΠΑ", "ΠΑ"),
      )
    weapon = models.CharField("Force", choices=WEAPONS, max_length=5, default='ΠΑ')
    rank = models.CharField("Rank", max_length=20)
    short = models.CharField("Rank (abbreviation)", max_length=10)

    def __unicode__(self):
        return self.short


class MilitaryPerson(Person):
    rank = models.ForeignKey(Rank, null=True, blank=True)
    active = models.BooleanField("Active")
    speciality = models.CharField("Speciality", max_length=20, null=True, blank=True)
    relatives = models.ManyToManyField(Person, related_name="related", null=True, blank=True)
    contacts = models.ManyToManyField(ContactInfo, related_name="person", null=True, blank=True)
    vehicles = models.ManyToManyField(Vehicle, related_name="owner", default=None, null=True, blank=True)

    @property
    def info(self):
        return u"%s (%s) %s %s" % (self.rank, self.speciality, self.name, self.surname)


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

    def __unicode__(self):
        return u"%s-%s" % (self.area, self.no)

    @property
    def info(self):
        return u"%s-%s (%dD+%dS+%dB)" % (self.area, self.no, self.double, self.single, self.bunk)

class Unit(models.Model):
    name = models.CharField("Name", max_length=20)
    internal = models.CharField("Internal Number", max_length=10, null=True, blank=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.internal)


class Damage(models.Model):
    DAMAGES = (
      ("AC" , "AirCondition"),
      ("TV", "Television"),
      ("ELECTRICAL", "Lights, etc."),
      ("DIRTY", "Extremely Dirty"),
      ("HYDRAVLICS", "Water leak, etc."),
    )
    tag = models.CharField("Tag", choices=DAMAGES, max_length=30)
    appartment = models.ForeignKey(Appartment, related_name="damages", null=True, blank=True)
    info = models.TextField("Further Info", null=True, blank=True)
    notified = models.ForeignKey(Unit, null=True, blank=True)
    fixed = models.BooleanField("Fixed", default=False)

    def __unicode__(self):
        r = u"%s -> %s" % (self.appartment, self.tag)
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
      ("V", "Vacation"),
      ("O", "Permanent"),
      ("U", "Unit"),
      ("S", "Schools"),
      )

    check_in = models.DateField("Check In", null=True, blank=True)
    check_out = models.DateField("Check Out", null=True, blank=True)
    info = models.TextField("Further Info", max_length=200, null=True, blank=True)
    owner = models.ForeignKey(MilitaryPerson, related_name="reservations")
    persons = models.IntegerField("Persons", choices=PERSONS, default=1,
                                  null=True, blank=True)
    appartment = models.ForeignKey(Appartment, related_name="reservations")
    cancel = models.BooleanField("Canceled", default=False)
    res_type = models.CharField("Type", choices=RESERVATION_TYPES, max_length=20,
                                null=True, blank=True, default=0)

    def __unicode__(self):
        return  u"%s ( %s - %s ) -> %s" % (self.owner.surname, self.check_in, self.check_out, self.appartment)


class Period(models.Model):
    start = models.DateField("Starting Date")
    end = models.DateField("Ending Date")

