from django import template
from garbageapp.models import *

register = template.Library()

@register.simple_tag()
def totalwork(request, did, d):
    fromdate = request.GET.get('fromdate')
    todate = request.GET.get('todate')
    driver = Driver.objects.get(id=did)
    complain = Complain.objects.filter(driver=driver, creationdate__date__gte=fromdate, creationdate__date__lte=todate)
    total = complain.count()
    complain = complain.filter(status='Completed')
    com_total = complain.count()
    remain_count = total - com_total
    if d == '0':
        return total
    if d == '1':
        return com_total
    if d == '2':
        return remain_count


@register.simple_tag()
def driver_totalwork(request, did, d):
    fromdate = request.GET.get('fromdate')
    todate = request.GET.get('todate')
    bin = Bin.objects.get(id=did)
    complain = Complain.objects.filter(bin=bin, creationdate__date__gte=fromdate, creationdate__date__lte=todate)
    total = complain.count()
    complain = complain.filter(status='Completed')
    com_total = complain.count()
    remain_count = total - com_total
    if d == '0':
        return total
    if d == '1':
        return com_total
    if d == '2':
        return remain_count
