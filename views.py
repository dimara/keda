#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import *
import datetime
from django import template
from django.utils import simplejson
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
from itertools import chain


def home(request):
    date = datetime.date.today()
    now = datetime.datetime.now()
    return render_to_response("welcome.html", {"now" : now,"date": date}, context_instance=RequestContext(request))


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
    if (check_out and check_out <= check_in):
            err = "ERROR: Check-out before Check-in!!!"
    else:
        for a in avail:
            ok = True
            for r in a.reservations.all():
                if r.status in ("CONFIRMED", "PENDING") and r.inside(check_in, check_out):
                    ok = False
                    break
            if ok:
                ret.append(a)

    return (ret, err)


def availability(request):
    period, start, end =  get_start_end(request)
    area = request.GET.get("area")
    category = id_from_request(request.GET, "category")
    damaged = request.GET.get("damaged", True)

    avail = Appartment.objects.all()
    if area:
        avail = avail.filter(area=area)

    if not damaged:
        avail = avail.exclude(damages__fixed=False)

    if category:
        avail = avail.filter(category=category)

    date_errors = None
    avail, date_errors = check_period(avail, start, end)
    avail = sorted(avail, key=lambda a: (a.area, int(a.no)))

    ctx =  {
      "period": period,
      "start": start,
      "end": end,
      "periods": Period.objects.all(),
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
    period, start, end =  get_start_end(request)
    area = request.GET.get("area")
    category = id_from_request(request.GET, "category")
    damaged = request.GET.get("damaged", True)

    appartments = Appartment.objects.all()
    if area:
        appartments = appartments.filter(area=area)

    if not damaged:
        appartments = appartments.exclude(damages__fixed=False)

    if category:
        appartments = appartments.filter(category=category)

    appartments = sorted(appartments, key=lambda a: (a.area, int(a.no)))
    appres = []
    for a in appartments:
        reserved = False
        for r in a.reservations.all():
            if r.status in ("CONFIRMED", "PENDING") and r.inside(start, end):
                reserved = True
                appres.append((a, r))
        if not reserved:
          appres.append((a, None))

    ctx = {
      "period": period,
      "start": start,
      "end": end,
      "periods": Period.objects.all(),
      "areas": Appartment.AREAS,
      "categories": Category.objects.values(),
      "appartments": appartments,
      "appres": appres,
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

def get_start_end(request):
    period = id_from_request(request.GET, "period")
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    if period:
        period = Period.objects.get(id=period)
        start = period.start
        end = period.end
    elif start and end:
        start = get_datetime(start)
        end = get_datetime(end)
    else:
        start = get_datetime(start)
        end = start + datetime.timedelta(days=1)

    return period, start, end

def info(request):
    period, start, end = get_start_end(request)
    rtype = request.GET.get("rtype", None)
    status = request.GET.get("status", None)
    reservations = Reservation.objects.all()
    if rtype:
        reservations = reservations.filter(keda__res_type=rtype)
    if status:
        reservations = reservations.filter(status=status)
    mres = reservations.prefetch_related("owner__militaryperson__visitor__rank",
                                         "owner__militaryperson__staff__rank",
                                         "owner__militaryperson__rank",
                                         "owner__militaryperson",
                                         "owner__relatives",
                                         "owner__contacts",
                                         "owner__vehicles",
                                         "appartment",
                                         "receipts",
                                         "keda").filter(owner__militaryperson__isnull=False).all()
    pres = reservations.prefetch_related("owner__relatives",
                                         "owner__contacts",
                                         "owner__vehicles",
                                         "owner",
                                         "appartment",
                                         "receipts",
                                         "keda").filter(owner__militaryperson__isnull=True).all()

    reservations = list(chain(mres, pres))
    reservations = [r for r in reservations if r.inside(start, end)]
    reservations = sorted(reservations, key=lambda x: x.owner.surname)
    ctx = {
      "period": period,
      "start": start,
      "end": end,
      "rtype": rtype,
      "status": status,
      "rtypes": Keda.RESERVATION_TYPES,
      "statuses": Reservation.STATUSES,
      "periods": Period.objects.all(),
      "reservations": reservations,
      }
    return render_to_response("info.html", ctx, context_instance=RequestContext(request))

def reservations(request):

    period, start, end = get_start_end(request)
    rtype = request.GET.get("rtype", None)
    status = request.GET.get("status", None)
    reservations = Reservation.objects.all().prefetch_related("owner",
                                                              "appartment",
                                                              "receipts",
                                                              "keda")
    if rtype:
        reservations = reservations.filter(keda__res_type=rtype)
    if status:
        reservations = reservations.filter(status=status)

    reservations = [r for r in reservations if r.inside(start, end)]
    reservations = sorted(reservations, key=lambda x: x.owner.surname)
    ctx = {
      "period": period,
      "start": start,
      "end": end,
      "rtype": rtype,
      "status": status,
      "rtypes": Keda.RESERVATION_TYPES,
      "statuses": Reservation.STATUSES,
      "periods": Period.objects.all(),
      "reservations": reservations,
      }
    return render_to_response("reservations.html", ctx, context_instance=RequestContext(request))

def logistic(request):

    period, start, end = get_start_end(request)
    rtype = request.GET.get("rtype", None)
    status = request.GET.get("status", None)
    receipt_type = request.GET.get("receipt_type", None)
    first = request.GET.get("first", None)
    last = request.GET.get("last", None)
    receipts = Receipt.objects.all().order_by("no")
    if rtype:
        receipts = receipts.filter(reservation__keda__res_type=rtype)
    if receipt_type:
        receipts = receipts.filter(rtype=receipt_type)
    if status:
        receipts = receipts.filter(reservation__status=status)
    if first:
      receipts = [r for r in receipts if r.inside(first, last)]
    else:
      receipts = [r for r in receipts if r.reservation.inside(start, end)]

    l = lambda x: [r.euro for r in x]
    ctx = {
      "period": period,
      "start": start,
      "end": end,
      "rtype": rtype,
      "status": status,
      "sum": sum(l(receipts)),
      "periods": Period.objects.all(),
      "receipts": receipts,
      "rtypes": Keda.RESERVATION_TYPES,
      "statuses": Reservation.STATUSES,
      "receipt_types": Receipt.RECEIPT_TYPES,
      "receipt_type": receipt_type,
      }
    return render_to_response("logistic.html", ctx, context_instance=RequestContext(request))

def th(request):

    period, start, end = get_start_end(request)
    reservations = Reservation.objects.filter(status="CONFIRMED", keda__telephone=True)
    reservations = [r for r in reservations if r.inside(start, end)]
    reservations = sorted(reservations, key=lambda r: (r.appartment.area, int(r.appartment.no)) if r.appartment else None)

    ctx = {
      "period": period,
      "start": start,
      "end": end,
      "periods": Period.objects.all(),
      "reservations": reservations,
      }
    return render_to_response("th.html", ctx, context_instance=RequestContext(request))

def damages(request):

    date = datetime.date.today()
    damages = Damage.objects.filter(fixed=False).order_by("tag")

    ctx = {
      "damages": damages,
      "date":date,
      }
    return render_to_response("damages.html", ctx, context_instance=RequestContext(request))


def gmap(request):
    period, start, end = get_start_end(request)
    url = "/gmap_data/?period="
    if period:
      url += str(period.id)
    url += "&start="
    if start:
      url += start.isoformat()
    url += "&end="
    if end:
      url += end.isoformat()
    ctx = {
      "date": datetime.date.today(),
      "period": period,
      "start": start,
      "end": end,
      "url": url,
      "periods": Period.objects.all(),
      }
    return render_to_response("map.html", ctx, context_instance=RequestContext(request))


def gmap_data(request):
    period, start, end = get_start_end(request)
    f = open("latlng.json")
    content = f.read()
    info = simplejson.loads(content)
    appartments = Appartment.objects.all()
    for a in appartments:
        fr = True
        try:
          info[a.area]["url"] = "/appartments/?period=&start=&end=&area=%s&category=&damaged=on" % a.area
          info[a.appartment]["url"] = "/admin/reception/appartment/%s/" % a.id
        except:
          print "Cannot add url for " + a.appartment
        for r in a.reservations.all():
            if r.status in ("CONFIRMED", "PENDING") and r.inside(start, end):
              fr = False
              if info.get(a.appartment, None):
                info[a.appartment]["status"] = r.status
                try:
                  keda = r.keda.get_res_type_display()
                except:
                  keda = ""
                info[a.appartment]["reservation"] = u"Όνομα: %s<br>Period: %s<br>Type:%s" % (r.owner, r.period, keda)
              if info.get(a.area, None):
                info[a.area]["reserved"].append([a.appartment, r.status])
        if fr and info.get(a.area, None):
          info[a.area]["free"].append(a.appartment)
        if fr and info.get(a.appartment, None):
          info[a.appartment]["status"] = "FREE"
          info[a.appartment]["reservation"] = "Free!!"
    return HttpResponse(simplejson.dumps(info))

def test(request):

    period, start, end = get_start_end(request)
    rtype = request.GET.get("rtype", None)
    status = request.GET.get("status", None)
    order = request.GET.get("order", None)

    reservations = Reservation.objects.all()

    if rtype:
        reservations = reservations.filter(keda__res_type=rtype)
    if status:
        reservations = reservations.filter(status=status)

    reservations = [r for r in reservations if r.inside(start, end)]

    if order == "apartment":
      reservations = sorted(reservations, key=lambda r: (r.appartment.area, int(r.appartment.no)) if r.appartment else None)
    else:
      reservations = sorted(reservations, key=lambda r: r.owner.surname)

    #visitors = Visitor.objects.all()
    ctx = {
      "period": period,
      "start": start,
      "end": end,
      "rtype": rtype,
      "status": status,
      "rtypes": Keda.RESERVATION_TYPES,
      "statuses": Reservation.STATUSES,
      "periods": Period.objects.all(),
      "reservations": reservations,
      }
    return render_to_response("test.html", ctx, context_instance=RequestContext(request))
