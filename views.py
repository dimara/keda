#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import *
import datetime
from django import template
import settings
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from reception.models import *
from django.db.models import Q
from django.core.context_processors import csrf
from django import forms


def home(request):
    now = datetime.datetime.now()
    return render_to_response("welcome.html", {"now": now}, context_instance=RequestContext(request))


def military_persons(request):
    military_persons = MilitaryPerson.objects.all()
    return render_to_response("military_persons.html", {"military_persons": military_persons}, context_instance=RequestContext(request))


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def value2id(value):
    if value:
        try:
            return int(value)
        except ValueError:
            pass

    return value


def id_from_request(qd, name):
    return value2id(qd.get(name))


def period_check(avail, check_in, chech_out):
    err = None
    if (check_in and check_out):
        if (check_out <= check_in):
            date_errors = "ERROR: Check-out before Check-in!!!"
        else:
            # check in not inside period
            avail = avail.exclude(reservations__check_in__lt=check_in, reservations__check_out__gt=check_in)
            # check out not inside period
            avail = avail.exclude(reservations__check_in__lt=check_out, reservations__check_out__gt=check_out)
            # period not between check in and check out
            avail = avail.exclude(reservations__check_in__gt=check_in, reservations__check_out__lt=check_out)

    return (avail, date_errors)


def availability(request):
    qd = request.GET
    check_in = qd.get("check_in")
    check_out = qd.get("check_out")
    area = qd.get("area")
    category = id_from_request(qd, "category")
    damaged = qd.get("damaged", False)

    avail = Appartment.objects.all()
    if area:
        avail = avail.filter(area=area)

    if not damaged:
        avail = avail.exclude(damages__fixed=False)

    if category:
        avail = avail.filter(category=category)

    date_errors = None
    if (check_in and check_out):
        date_errors, avail = check_period(avail, check_in, check_out)

    ctx =  {
      "check_in": check_in,
      "check_out": check_out,
      "date_errors": date_errors,
      "area": area,
      "areas": Appartment.AREAS + settings.USER_DEFINED_AREAS,
      "category": category,
      "categories": Category.objects.values(),
      "damaged": damaged,
      "avail": avail,
      }
    print ctx
    return render_to_response("availability.html", ctx, context_instance=RequestContext(request))


def parousiologio(request):
    staff = Staff.objects.all().order_by("rank__level").reverse()
    ctx = {
      "date": datetime.date.today(),
      "staff": staff,
      }
    return render_to_response("parousiologio.html", ctx, context_instance=RequestContext(request))


def appartments(request):
    appartments = Appartment.objects.all()

    ctx = {
        "appartments": appartments,
      }
    return render_to_response("appartments.html", ctx, context_instance=RequestContext(request))


def reservation(request):
    if request.method == 'GET':
        qd = request.GET
    elif request.method == 'POST':
        qd = request.POST
    check_in = qd.get("check_in")
    check_out = qd.get("check_out")
    aid = id_from_request(qd, "appartment")
    pid = id_from_request(qd, "person")
    print qd
    if request.method == 'GET':
        if aid:
            avail = Appartment.objects.filter(id=aid)
        else:
            avail = Appartment.objects.all()
        if pid:
            persons = MilitaryPerson.objects.filter(id=pid)
        else:
            persons = MilitaryPerson.objects.all()

        date_errors = None
        if (check_in and check_out):
            date_errors, avail = check_period(avail, check_in, check_out)

        ctx =  {
          "check_in": check_in,
          "check_out": check_out,
          "date_errors": date_errors,
          "aid": aid,
          "avail": avail,
          "pid": pid,
          "persons": persons,
          }
        ctx.update(csrf(request))
        return render_to_response("reservation.html", ctx, context_instance=RequestContext(request))

    elif request.method == 'POST':
        appartment = Appartment.objects.get(id=aid)
        person = MilitaryPerson.objects.get(id=pid)
        r = Reservation(owner=person, appartment=appartment, check_in=check_in, check_out=check_out, status="CONFIRMED")
        r.save()
        return HttpResponseRedirect('/reservations/')


def visitors(request):

    visitors = Visitor.objects.all()
    ctx = {
      "visitors": visitors,
      }
    return render_to_response("visitors.html", ctx, context_instance=RequestContext(request))


def test(request):
    return display_meta(request)
