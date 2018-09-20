from django.shortcuts import render
from .models import Purchase
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
from decimal import Decimal

def prepare_total_spending():
    total_category_spending = {}

    purchase_category_list = Purchase.objects.order_by().values_list('type', flat=True).distinct()

    for purchase_type in purchase_category_list:
        purchase_type_total_spending = round(Purchase.objects.filter(type=purchase_type).aggregate(Sum('amount'))['amount__sum'], 2)
        total_category_spending[purchase_type] = purchase_type_total_spending

    return total_category_spending

def total_spending_all_categories():
    return round(Purchase.objects.aggregate(Sum('amount'))['amount__sum'], 2)

def index(request):
    try:
        purchases = Purchase.objects.all().order_by('-time')
        total_spending = round(Purchase.objects.aggregate(Sum('amount'))['amount__sum'], 2)
    except Purchase.DoesNotExist:
        raise Http404("Could not find any purchases.")

    context = {
        'purchases': purchases,
        'total_spending': total_spending,
        'spending_by_category': prepare_total_spending(),
        'total_spending_all_categories': total_spending_all_categories(),
    }

    return render(request, 'main/index.html', context)

def new(request):
    return render(request, 'main/new.html')

def create(request):
    place = request.POST['place']
    type = request.POST['type']
    time = request.POST['time']
    amount = request.POST['amount']

    new_purchase = Purchase(place=place, type=type, time=time, amount=amount, user=request.user)
    new_purchase.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('main:index'))
