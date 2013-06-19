#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import *
import datetime
from django import template
import settings
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import render_to_response
from reception.models import *
from django.db.models import Q
from django.core.context_processors import csrf
from django import forms


def home(request):
    now = datetime.datetime.now()
    return render_to_response("welcome.html", {"now": now}, context_instance=RequestContext(request))


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


def check_period(avail, check_in, check_out):
    err = None
    if (check_in and check_out):
        if (check_out <= check_in):
            err = "ERROR: Check-out before Check-in!!!"
        else:
            # check in not inside period
            avail = avail.exclude(reservations__check_in__lt=check_in, reservations__check_out__gt=check_in)
            # check out not inside period
            avail = avail.exclude(reservations__check_in__lt=check_out, reservations__check_out__gt=check_out)
            # period not between check in and check out
            avail = avail.exclude(reservations__check_in__gt=check_in, reservations__check_out__lt=check_out)

    return (avail, err)


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
        avail, date_errors = check_period(avail, check_in, check_out)

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
    return render_to_response("availability.html", ctx, context_instance=RequestContext(request))


def appartments(request):
    appartments = Appartment.objects.all()

    ctx = {
        "appartments": appartments,
      }
    return render_to_response("appartments.html", ctx, context_instance=RequestContext(request))


def parousiologio(request):
    staff = Staff.objects.all().order_by("rank__level", "extra", "-surname").reverse()
    ctx = {
      "date": datetime.date.today(),
      "staff": staff,
      }
    return render_to_response("parousiologio.html", ctx, context_instance=RequestContext(request))


def visitors(request):

    date = request.GET.get("date", None)
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    period = id_from_request(request.GET, "period")
    p = None
    #reservations = Reservation.objects.all().order_by("owner__surname")
    reservations = Reservation.objects.all().order_by("owner__surname")
    if period:
        p = Period.objects.get(id=period)
        reservations = [r for r in reservations if r.inside(p.start, p.end)]
    elif start and end:
        y, m, d = map(int, start.split("-"))
        start = datetime.date(y, m, d)
        y, m, d = map(int, end.split("-"))
        end = datetime.date(y, m, d)
        reservations = [r for r in reservations if r.inside(start, end)]
    else:
        if date:
            y, m, d = map(int, date.split("-"))
            date = datetime.date(y, m, d)
        else:
            date = datetime.date.today()
        reservations = [r for r in reservations if r.active(date)]

    #visitors = Visitor.objects.all()
    ctx = {
      "date": date,
      "start": start,
      "end": end,
      "period": p,
      #"visitors": [v for v in visitors for r in v.reservations.all() if r.active(date)],
      "periods": Period.objects.all(),
      "reservations": reservations,
      }
    return render_to_response("visitors.html", ctx, context_instance=RequestContext(request))


def test(request):
    return display_meta(request)
