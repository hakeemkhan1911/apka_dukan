# customer views
from django import forms
from django.shortcuts import render,redirect
from shops.models import AddShopModel
from .forms import AddCustomerForm
from .models import AddCustomerModel
from measurements.models import AddMeasurementModel
from measurements.forms import AddMeasurementForm
from orders.models import AddOrderModel

def add_customer(request,shop_id,deleted=False):
    try:
        last_number = AddCustomerModel.objects.filter(shop__shop_owner__fake_id=request.user.id).latest('serial_number').serial_number
    except:
        last_number=0
    if request.method == 'POST':
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            shop = AddShopModel.objects.get(id=shop_id)
            form.instance.shop=shop
            form.save()
            return redirect('measurements:add_measurement',form.instance.id)
    else:
        if deleted:
            form = AddCustomerForm(initial={'serial_number':deleted})
        else:
            form = AddCustomerForm(initial={'serial_number':last_number+1})
    return render(request,'submit.html',{'form':form,'text':'براہ کرم گاہک کی معلومات درج کریں!'})  # Translated

def customer_details(request,customer_id):
    from login.models import LoginModel
    from karigars.models import RegisterKarigarModel
    
    customer=AddCustomerModel.objects.get(id=customer_id)
    measurement=AddMeasurementModel.objects.filter(customer=customer)
    try:
        client=LoginModel.objects.get(fake_id=request.user.id)
    except LoginModel.DoesNotExist:
        client=RegisterKarigarModel.objects.get(fake_id=request.user.id)
    if measurement.exists():
        measurement=measurement.first()
    else:
        measurement=False
    try:
        order=AddOrderModel.objects.filter(customer__id=customer_id).first()
        return render(request,'customer_details.html',{'customer_details':customer,'measurement_added':measurement,'order':order,'client':client})
    except:
        return render(request,'customer_details.html',{'customer_details':customer,'measurement_added':measurement,'client':client})

def update_customer(request,customer_id):
    from orders.forms import AddOrderForm
    customer=AddCustomerModel.objects.get(id=customer_id)
    customer_shop = customer.shop
    measurement=AddMeasurementModel.objects.filter(customer=customer).first()
    order=AddOrderModel.objects.filter(customer=customer).first()
    if measurement is None:
        return redirect('measurements:add_measurement',customer_id)
    if order is None:
        return redirect('orders:add_order',customer_id)
    if request.method=='POST':
        measurement_form=AddMeasurementForm(request.POST,instance=measurement)
        customer_form=AddCustomerForm(request.POST,instance=customer)
        order_form=AddOrderForm(request.POST,instance=order)
        if customer_form.is_valid() and measurement_form.is_valid() and order_form.is_valid():
            customer_form.instance.shop=customer_shop
            customer_form.save()
            customer=AddCustomerModel.objects.get(id=customer_id)
            measurement_form.instance.customer=customer
            order_form.instance.customer=customer
            measurement_form.save()
            order_form.save()
            return redirect('customers:customer_details',customer.id)
        else:
            return render(request,'message.html',{'msg':'ڈیٹا درست نہیں ہے'})  # Translated
    else:
        customer_form = AddCustomerForm(instance=customer)
        measurement_form=AddMeasurementForm(instance=measurement)
        order_form=AddOrderForm(instance=order)
        return render(request,'customer_update.html',{'form':customer_form,'measurement_form':measurement_form,'order_form':order_form})

def delete_customer(request,customer_id):
    customer=AddCustomerModel.objects.get(id=customer_id)
    if request.POST.get('button')=='ہاں':
        shop_id=customer.shop.id
        customer.delete()
        return redirect('shops:add_shop')
    elif request.POST.get('button')=='نہیں':
        return redirect('customers:customer_details',customer_id)
    return render(request,'warn.html',{'msg':'کیا آپ واقعی حذف کرنا چاہتے ہیں؟'})  # Translated

def login_customer(request,shop_id):
    if request.method=='POST':
        name=request.POST.get('customer_name')
        password=request.POST.get('password')
        phone=request.POST.get('customer_phone')
        customer=AddCustomerModel.objects.filter(customer_name=name,password=password,customer_phone=phone)
        if customer.exists():
            if customer.filter(shop__id=shop_id).exists():
                customer = customer.first()
                measurement_added = AddMeasurementModel.objects.filter(customer__id=customer.id).first()
                order = AddOrderModel.objects.filter(customer__id=customer.id).first()
                return render(request,'customer_self_details.html',{'customer_details':customer,'success':True,'measurement_added':measurement_added,'order':order})
            else:
                return render(request,'message.html',{'msg':'You are not customer of the shop.'})
                
        else:
            return render(request,'message.html',{'msg':'غلط معلومات درج کی گئی ہے۔'})
    if request.GET.get('button') =='Yes':
        
        return redirect(f'shops:rate_shop',shop_id,request.GET.get('customer_id'))
        
    else:
        form=AddCustomerForm()
        form.fields['serial_number'].widget = forms.HiddenInput()
        form.fields['customer_address'].widget = forms.HiddenInput()
        return render(request,'submit.html',{'form':form,'text':'اپنی معلومات نیچے درج کریں'})  # Translated
def share_customer_details(request,customer_id):
    customer = AddCustomerModel.objects.get(id=customer_id)
    order=AddOrderModel.objects.filter(customer=customer).first()
    wa_link=f'https://wa.me/92{customer.customer_phone}'
    return render(request,'share_customer_details.html',{'customer':customer,'order':order,'wa_link':wa_link})

'''import imgkit
from django.template.loader import render_to_string
from django.http import FileResponse
import tempfile

def receipt_image_view(request):
    html = render_to_string('receipt.html', {
        'customer': {'name': 'Ali'},
        'amount': '500',
        'date': '2025-05-20'
    })

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as image_file:
        imgkit.from_string(html, image_file.name)
        return FileResponse(open(image_file.name, 'rb'), content_type='image/png')'''