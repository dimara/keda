#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import *
import datetime
from django import template
from django.utils import simplejson
from django.conf import settings
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import render_to_response
from reception.models import *
from reception import constants
from django.db.models import Q
from django.core.context_processors import csrf
from django import forms
from itertools import chain
from django.contrib.auth.decorators import login_required
from reception.constants import *
import os

import os, tempfile, zipfile
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper


@login_required(login_url='/accounts/login/')
def home(request):
    date = datetime.date.today()
    now = datetime.datetime.now()
    if request.user.is_authenticated():
      # Do something for authenticated users.
      username = request.user.username

    return render_to_response("welcome.html", {"now" : now,"date": date, "username": username}, context_instance=RequestContext(request))

def get_display(key, list):
    d = dict(list)
    try:
      key = int(key)
    except:
      pass
    if key in d:
        return d[key]
    return None

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


def check_availability(avail, check_in, check_out, include_pending=False, include_notleft=False):
    err = None
    ret = []
    excluded_statuses = [RS_PENDING, RS_CONFIRM, RS_UNKNOWN]
    if (check_out and check_out <= check_in):
            err = "ERROR: Check-out before Check-in!!!"
    else:
        for a in avail:
            ok = True
            res = []
            for r in a.reservations.filter(status__in=excluded_statuses):
                if r.inside(check_in, check_out):
                    if include_pending and r.status == RS_PENDING:
                      res.append(r)
                    else:
                      ok = False
                      break
                elif include_notleft and RE_NOTLEFT in r.notifications[0]:
                    res.append(r)
            if ok:
                ret.append((a, res))

    return (ret, err)

def get_ctx(period, start, end, area, category, damaged, rtype, status, agent):
    ctx = {
      "period": period,
      "start": start,
      "end": end,
      "periods": Period.objects.all(),
      "area": area,
      "areas": Appartment.AREAS,
      "category": category,
      "categories": Category.objects.values(),
      "damaged": damaged,
      "rtype": get_display(rtype, Reservation.RESERVATION_TYPES),
      "rtypes": Reservation.RESERVATION_TYPES,
      "status": get_display(status, Reservation.STATUSES),
      "statuses": Reservation.STATUSES,
      "agent": get_display(agent, Reservation.AGENTS),
      "agents": Reservation.AGENTS,
      }
    return ctx


@login_required(login_url='/accounts/login/')
def availability(request):
    period, start, end =  get_start_end(request)
    area = request.GET.get("area")
    category = id_from_request(request.GET, "category")
    damaged = request.GET.get("damaged", False)
    pending = request.GET.get("pending", False)
    notleft = request.GET.get("notleft", False)

    avail = Appartment.objects.all()
    if area:
        avail = avail.filter(area=area)

    if damaged:
        avail = avail.exclude(damages__fixed=False)

    if category:
        avail = avail.filter(category=category)

    errors = None
    avail, errors = check_availability(avail, start, end, pending, notleft)
    avail = sorted(avail, key=lambda (a, r): (a.area, int(a.no)))

    ctx = get_ctx(period, start, end, area, category, damaged, None, None, None)
    ctx.update({
      "avail": avail,
      "errors": errors,
      })
    return render_to_response("availability.html", ctx, context_instance=RequestContext(request))


@login_required(login_url='/accounts/login/')
def appartments(request):
    period, start, end =  get_start_end(request)
    area = request.GET.get("area")
    category = id_from_request(request.GET, "category")
    damaged = request.GET.get("damaged", False)

    appartments = Appartment.objects.all()
    if area:
        appartments = appartments.filter(area=area)

    if damaged:
        appartments = appartments.exclude(damages__fixed=False)

    if category:
        appartments = appartments.filter(category=category)

    appartments = sorted(appartments, key=lambda a: (a.area, int(a.no)))
    appres = []
    for a in appartments:
        reserved = False
        for r in a.reservations.all():
            if r.status in (RS_CONFIRM, RS_PENDING, RS_UNKNOWN) and r.inside(start, end):
                reserved = True
                appres.append((a, r))
        if not reserved:
          appres.append((a, None))

    ctx = get_ctx(period, start, end, area, category, damaged, None, None, None)
    ctx.update({
      "appartments": appartments,
      "appres": appres,
      })
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
    exact = request.GET.get("exact", None)
    if period:
        period = Period.objects.get(id=period)
        start = period.start
        end = period.end
    elif start and end:
        start = get_datetime(start)
        end = get_datetime(end)
    elif exact:
        if start:
          start = get_datetime(start)
        if end:
          end = get_datetime(end)
    else:
        start = get_datetime(start)
        end = start + datetime.timedelta(days=1)

    return period, start, end

@login_required(login_url='/accounts/login/')
def info(request):
    period, start, end = get_start_end(request)
    rtype = request.GET.get("rtype", None)
    status = request.GET.get("status", None)
    reservations = Reservation.objects.all()
    if rtype:
        reservations = reservations.filter(res_type=rtype)
    if status:
        reservations = reservations.filter(status=status)
    reservations = filter(lambda x: x.inside(start, end), reservations)
    reservations = Reservation.objects.filter(id__in=[r.id for r in reservations])
    reservations = reservations.all().prefetch_related(
                                         "owner__rank",
                                         "owner__relatives",
                                         "owner__contacts",
                                         "owner__vehicles",
                                         "appartment",
                                         "receipts")
    reservations = sorted(reservations, key=lambda x: x.owner.surname)
    ctx = get_ctx(period, start, end, None, None, None, rtype, status, None)
    ctx.update({
      "reservations": reservations,
      })
    return render_to_response("info.html", ctx, context_instance=RequestContext(request))


def get_cvs(ctx):
    reservations = ctx["reservations"]
    period = ctx["period"]
    p = period.name if period else None
    s = ctx["start"].isoformat()
    e = ctx["end"].isoformat()
    t = ctx["rtype"]
    a = ctx["agent"]
    st = ctx["status"]
    timestamp = datetime.datetime.now().isoformat()
    comments = """\
# Reservations
# period %s
# between %s and %s
# type %s
# agent %s
# status %s
# as generated @ %s
""" % (p, s, e, t, a, st, timestamp)
    header = u"Βαθμός|Επίθετο|Όνομα|Οίκημα|Status\n"
    data = ""
    for r in reservations:
       ap = r.appartment.appartment if r.appartment else None
       rank = r.owner.rank.short if r.owner.rank else None
       data += "%s|%s|%s|%s|%s\n" % \
               (rank, r.owner.surname, r.owner.name, ap, r.get_status_display())

    response = "%s%s%s" % (comments, header,  data)
    return response


@login_required(login_url='/accounts/login/')
def reservations(request):

    period, start, end = get_start_end(request)
    rtype = request.GET.get("rtype", None)
    status = request.GET.get("status", None)
    agent = request.GET.get("agent", None)
    order = request.GET.get("order", None)
    exact = request.GET.get("exact", None)
    txt = request.GET.get("file", None)
    cvs = request.GET.get("cvs", None)
    reservations = Reservation.objects.all()
    if rtype:
        reservations = reservations.filter(res_type=rtype)
    if status:
        reservations = reservations.filter(status=status)
    if agent:
        reservations = reservations.filter(agent=agent)

    if exact:
        reservations = filter(lambda x: x.on(start, end), reservations)
    else:
        reservations = filter(lambda x: x.inside(start, end), reservations)
    reservations = Reservation.objects.filter(id__in=[r.id for r in reservations])
    reservations = reservations.prefetch_related("owner", "appartment", "receipts")
    if order == "apartment":
      reservations = sorted(reservations, key=lambda r: (r.appartment.area, int(r.appartment.no)) if r.appartment else None)
    else:
      reservations = sorted(reservations, key=lambda r: r.owner.surname)

    ctx = get_ctx(period, start, end, None, None, None, rtype, status, agent)
    ctx.update({
      "reservations": reservations,
      })
    if cvs:
      data = get_cvs(ctx)
      return send_response(data, txt=txt)
    else:
      return render_to_response("reservations.html", ctx, context_instance=RequestContext(request))


def send_response(data, txt=True):
      if txt:
        content_type = "text/plain"
      else:
        data = """<html> <head> <meta charset="utf-8"> </head> <body>""" + data.replace("\n","<br>") + "<body>"
        content_type = "text/html"
      return HttpResponse(data, content_type=content_type)


@login_required(login_url='/accounts/login/')
def logistic(request):

    period, start, end = get_start_end(request)
    rtype = request.GET.get("rtype", None)
    status = request.GET.get("status", None)
    receipts = Receipt.objects.all()
    if rtype:
        receipts = receipts.filter(reservation__res_type=rtype)
    if status:
        receipts = receipts.filter(reservation__status=status)
    receipts = [r for r in receipts if r.inside(start, end)]
    receipts = sorted(receipts, key=lambda r: (r.date, int(r.no)))

    l = lambda x: [r.euro for r in x]
    ctx = get_ctx(period, start, end, None, None, None, rtype, status, None)
    ctx.update({
      "sum": sum(l(receipts)),
      "receipts": receipts,
      })
    return render_to_response("logistic.html", ctx, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login/')
def th(request):

    period, start, end = get_start_end(request)
    reservations = Reservation.objects.filter(telephone=True)
    reservations = [r for r in reservations if r.inside(start, end)]
    reservations = sorted(reservations, key=lambda r: (r.appartment.area, int(r.appartment.no)) if r.appartment else None)

    ctx = get_ctx(period, start, end, None, None, None, None, None, None)
    ctx.update({
      "reservations": reservations,
      "title": "Phone Activations",
      })
    return render_to_response("th.html", ctx, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login/')
def damages(request):

    date = datetime.date.today()
    damages = Damage.objects.filter(fixed=False).order_by("tag")

    ctx = {
      "damages": damages,
      "date":date,
      }
    return render_to_response("damages.html", ctx, context_instance=RequestContext(request))


@login_required(login_url='/accounts/login/')
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
      "RS_PENDING": RS_PENDING,
      "RS_CONFIRM": RS_CONFIRM,
      "RS_UNKNOWN": RS_UNKNOWN,
      }
    return render_to_response("map.html", ctx, context_instance=RequestContext(request))


@login_required(login_url='/accounts/login/')
def gmap_data(request):
    period, start, end = get_start_end(request)
    f = open("latlng.json")
    content = f.read()
    info = simplejson.loads(content)
    appartments = Appartment.objects.all()
    for a in appartments:
        fr = True
        try:
          info[a.area]["url"] = "/appartments/?period=&start=&end=&area=%s&category=" % a.area
          info[a.appartment]["url"] = "/admin/reception/appartment/%s/" % a.id
        except:
          msg = u"Cannot add url for " + a.appartment
          print msg.encode("utf-8")
        for r in a.reservations.all():
            if r.status in (RS_CONFIRM, RS_PENDING, RS_UNKNOWN) and r.inside(start, end):
              fr = False
              if info.get(a.appartment, None):
                info[a.appartment]["status"] = r.status
                info[a.appartment]["reservation"] = u"Όνομα: %s<br>Period: %s<br>Type:%s" % (r.owner, r.period, r.get_res_type_display())
              if info.get(a.area, None):
                info[a.area]["reserved"].append([a.appartment, r.status])
        if fr and info.get(a.area, None):
          info[a.area]["free"].append(a.appartment)
        if fr and info.get(a.appartment, None):
          info[a.appartment]["status"] = "FREE"
          info[a.appartment]["reservation"] = "Free!!"
    return HttpResponse(simplejson.dumps(info))

@login_required(login_url='/accounts/login/')
def persons(request):
    text = request.GET.get("text", None)
    inside = request.GET.get("inside", None)
    persons = []
    trunc = False
    if text:
      text = text.upper()
      persons = MilitaryPerson.objects.all()
      if inside == "vehicles":
        persons = persons.filter(vehicles__plate__contains=text)
      elif inside == "surnames":
        persons = persons.filter(surname__contains=text)
      if len(persons) > 20:
        persons = MilitaryPerson.objects.filter(id__in=[p.id for p in persons[:20]])
        trunc = True
      persons = persons.all().prefetch_related("reservations", "contacts", "vehicles", "rank")
      persons = sorted(persons, key=lambda p: p.surname)
    ctx = {
      "trunc": trunc,
      "text": text,
      "inside": inside,
      "persons": persons,
      }
    return render_to_response("persons.html", ctx, context_instance=RequestContext(request))


@login_required(login_url='/accounts/login/')
def stats(request):

    period, start, end = get_start_end(request)
    live = request.GET.get("live", False)
    show = request.GET.get("show", False)
    fast = request.GET.get("fast", False)
    cvs = request.GET.get("cvs", False)
    txt = request.GET.get("file", False)
    reservations = Reservation.objects.all()
    reservations = filter(lambda x: x.inside(start, end), reservations)
    if live:
      reservations = filter(lambda x: x.status == RS_CONFIRM, reservations)
    else:
      reservations = filter(lambda x: x.status != RS_CANCEL, reservations)
    rids = [r.id for r in reservations]
    errors = None
    if not fast and len(rids) < 900:
      persons = sum([r.persons for r in reservations if r.persons])
      receipts = Receipt.objects.filter(reservation__in=rids)
      euros = sum([r.euro for r in receipts])
    else:
      errors = "Too many reservations found! Cannot calculate persons and euros!"
      persons = 0
      euros = 0
    regular = filter(lambda x: x.res_type == RT_REGULAR, reservations)
    b3 = filter(lambda x: x.agent == RA_GEA, regular)
    ea = filter(lambda x: x.agent == RA_EA, regular)
    my = filter(lambda x: x.agent == RA_MY, regular)
    osseay = filter(lambda x: x.res_type == RT_OSSEAY, reservations)
    paratheristes = filter(lambda x: x.res_type == RT_DAILY, reservations)
    monada = filter(lambda x: x.res_type == RT_UNIT, reservations)

    ctx = get_ctx(period, start, end, None, None, None, None, None, None)
    ctx.update({
      "show": show,
      "live": live,
      "reservations": reservations,
      "total": len(reservations),
      "persons": persons,
      "euros": euros,
      "regular": len(regular),
      "b3": len(b3),
      "ea": len(ea),
      "my": len(my),
      "osseay": len(osseay),
      "paratheristes": len(paratheristes),
      "monada": len(monada),
      "errors": errors,
      })
    p = period.name if period else ""
    dates = u"%s περίοδος: %s..%s" % (p,  start.strftime("%d %b"), end.strftime("%d %b"))
    timestamp = datetime.datetime.now().isoformat()
    comments = u"""\
# Stats
# period %s
# between %s and %s
# as generated @ %s
""" % (p, start.isoformat(), end.isoformat(), timestamp)
    header = u"Ημ/νίες|ΤΑΚΤΙΚΟΙ|EURO|ΓΕΑ/Β3|Ε.Α.|Μ.Υ.|ΠΑΡ/ΣΤΕΣ|ΜΟΝΑΔΑ|ΟΣΣΕΑΥ\n"
    data = u"%s|%d|%.2f|%d|%d|%d|%d|%d|%d\n" % \
           (dates, len(reservations), euros,
            len(b3), len(ea), len(my),
            len(paratheristes), len(monada), len(osseay))
    graph = create_graph(comments, header, data)
    ctx.update({"graph": graph})
    if cvs:
        response = comments + "#" + header + data
        return send_response(response, txt=txt)
    else:
      return render_to_response("stats.html", ctx, context_instance=RequestContext(request))

def create_graph(comments, header, data):
   f = open("stats.dat", "w")
   contents = comments + header + data
   f.write(contents.encode("utf-8"))
   f.close()
   os.system("gnuplot stats.plt")
   return "stats.pdf"

@login_required(login_url='/accounts/login/')
def test(request):

    period, start, end = get_start_end(request)
    rtype = request.GET.get("rtype", None)
    status = request.GET.get("status", None)
    order = request.GET.get("order", None)

    reservations = Reservation.objects.all()

    if rtype:
        reservations = reservations.filter(res_type=rtype)
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
      "rtypes": Reservation.RESERVATION_TYPES,
      "statuses": Reservation.STATUSES,
      "periods": Period.objects.all(),
      "reservations": reservations,
      }
    return render_to_response("test.html", ctx, context_instance=RequestContext(request))



def send_file(request):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    filename=request.GET.get("filename", "stats.pdf")
    content_type=request.GET.get("content_type", "application/pdf")
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(filename)
    return response
