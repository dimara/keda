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
    ret = []
    if (check_in and check_out):
        if (check_out <= check_in):
            err = "ERROR: Check-out before Check-in!!!"
        else:
            for a in avail:
                ok = True
                for r in a.reservations.all():
                    if r.status in ("CONFIRMED") and r.inside(check_in, check_out):
                        ok = False
                        break
                if ok:
                    ret.append(a)

    ret = sorted(ret, key=lambda a: a.appartment)

    return (ret, err)


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
        avail, date_errors = check_period(avail, get_datetime(check_in), get_datetime(check_out))

    ctx =  {
      "check_in": check_in,
      "check_out": check_out,
      "date_errors": date_errors,
      "area": area,
      "areas": Appartment.AREAS,
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


def get_datetime(value):
    if value:
      y, m, d = map(int, value.split("-"))
      return datetime.date(y, m, d)
    else:
      return datetime.date.today()

def visitors(request):

    date = request.GET.get("date", None)
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    rtype = request.GET.get("rtype", None)
    status = request.GET.get("status", None)
    period = id_from_request(request.GET, "period")
    p = None
    #reservations = Reservation.objects.all().order_by("owner__surname")
    reservations = Reservation.objects.all().order_by("owner__surname")
    if rtype:
        reservations = reservations.filter(res_type=rtype)
    if status:
        reservations = reservations.filter(status=status)
    p = None
    if period:
        p = Period.objects.get(id=period)
        reservations = [r for r in reservations if r.inside(p.start, p.end)]
    elif start and end:
        start = get_datetime(start)
        end = get_datetime(end)
        reservations = [r for r in reservations if r.inside(start, end)]
    else:
        date = get_datetime(date)
        reservations = [r for r in reservations if r.active(date)]

    #visitors = Visitor.objects.all()
    ctx = {
      "date": date,
      "start": start,
      "end": end,
      "period": p,
      #"visitors": [v for v in visitors for r in v.reservations.all() if r.active(date)],
      "rtype": rtype,
      "status": status,
      "rtypes": Reservation.RESERVATION_TYPES,
      "statuses": Reservation.STATUSES,
      "periods": Period.objects.all(),
      "reservations": reservations,
      }
    return render_to_response("visitors.html", ctx, context_instance=RequestContext(request))


def test(request):

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
        start = get_datetime(start)
        end = get_datetime(end)
        reservations = [r for r in reservations if r.inside(start, end)]
    else:
        date = get_datetime(date)
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
    return render_to_response("test.html", ctx, context_instance=RequestContext(request))
