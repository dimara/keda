from django.http import HttpResponse
import datetime
from django import template
import settings
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from reception.models import *
from django.db.models import Q


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


def id_from_request(request, name):
    return value2id(request.GET.get(name))


def search(request):
    check_in = request.GET.get("check_in")
    check_out = request.GET.get("check_out")
    area = request.GET.get("area")
    category = id_from_request(request, "category")
    damaged = request.GET.get("damaged", False)

    avail = Appartment.objects.all()
    date_errors = None
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

    if area:
        avail = avail.filter(area=area)

    if not damaged:
        avail = avail.exclude(damages__fixed=False)

    if category:
        avail = avail.filter(category=category)

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
    return render_to_response("search.html", ctx, context_instance=RequestContext(request))


def parousiologio(request):
    staff = Staff.objects.all().order_by("rank__level").reverse()
    ctx = {
      "date": datetime.date.today(),
      "staff": staff,
      }
    return render_to_response("parousiologio.html", ctx, context_instance=RequestContext(request))


def appartments(request, idx):
    appartments = Appartment.objects.filter(id=idx)
    damages = Damage.objects.filter(appartment=idx)
    reservations = Reservation.objects.filter(appartment=idx)

    ctx = {
        "appartments": appartments,
        "damages": damages,
        "reservations": reservations,
      }
    return render_to_response("appartments.html", ctx, context_instance=RequestContext(request))

def test(request):
    return display_meta(request)
