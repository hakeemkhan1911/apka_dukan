from django.shortcuts import render,redirect
from .models import AddOrderModel
from .forms import AddOrderForm
from customers.models import AddCustomerModel
from datetime import datetime,timedelta

def add_order(request,customer_id):
    if request.method == 'POST':
        form=AddOrderForm(request.POST)
        if form.is_valid():
            customer = AddCustomerModel.objects.get(id=customer_id)
            form.instance.customer = customer
            form.save()
            return redirect('customers:customer_details',customer.id)
        else:
            return render(request,'message.html',{'msg':'Please try again!'})
    else:
        
        delivery_date=datetime.now()+timedelta(days=7)
        try:
            order=AddOrderModel.objects.get(customer__id=customer_id)
            remining=order.remining
            order.delete()
            form = AddOrderForm(initial={'previous':remining,'delivery_date':delivery_date})
        except AddOrderModel.DoesNotExist:
            form=AddOrderForm(initial={'delivery_date':delivery_date})
        return render(request,'submit.html',{'form':form,'text':'Add order details.'})
        
def order_details(request,customer_id):
    try:
        order=AddOrderModel.objects.get(customer__id=customer_id)
    except AddOrderModel.DoesNotExist:
        return redirect('orders:add_order',customer_id)
    
    return render(request,'order_details.html',{'order':order})
    
def delete_order(request,order_id):
    order=AddOrderModel.objects.get(id=order_id)
    if request.method == 'POST':
        customer_id = order.customer.id
        if request.POST.get('button') == 'Yes':
            order.delete()
            return redirect('customers:customer_details',customer_id)
        else:
            return redirect('orders:order_details',customer_id)
    else:
        return render(request,'warn.html',{'msg':'Are you sure to delete!'})
    
def update_order(request,order_id):
    order=AddOrderModel.objects.get(id=order_id)
    form=AddOrderForm(instance=order)
    if request.method == 'POST':
        form=AddOrderForm(request.POST,instance=order)
        if form.is_valid():
            form.instance.customer = order.customer
            form.save()
            return redirect('orders:order_details',form.instance.customer.id)
        else:
            return render(request,'message.html',{'msg':'Sorry somthing unexpected happend.'})
    return render(request,'submit.html',{'form':form,'text':'Update the order.'})
     
def new_order(request,order_id):
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders:order_details',form.instance.customer.id)
        else:
            return render(request,'message.html',{'msg':'Sorry could not save the order!'})
    else:
        try:
            remining=AddOrderModel.objects.get(id=order_id).remining
            form = AddOrderForm(initial={'remining':remining})
        except AddOrderModel.DoesNotExist:
            form=AddOrderForm()
        return render(request,'submit.html',{'form':form,'msg':'Add new order'})