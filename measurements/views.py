# measurement view
from django.shortcuts import render,redirect
from .models import AddMeasurementModel
from .forms import AddMeasurementForm 
from customers.models import AddCustomerModel

def add_measurement(request,customer_id):
    if request.method == 'POST':
        form = AddMeasurementForm(request.POST)
        customer = AddCustomerModel.objects.get(id=customer_id)
        
        if form.is_valid():
            form.instance.customer=customer
            form.save()
            return redirect('orders:add_order',customer_id)
    else:
        form=AddMeasurementForm()
    return render(request,'submit.html',{'form':form,'text':'Please add customer\'s measurements' })