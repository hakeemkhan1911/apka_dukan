# Shop views.py 
from django.shortcuts import render,redirect
from .models import AddShopModel
from login.models import LoginModel
from .forms import AddShopForm
from customers.models import AddCustomerModel
from django.contrib.auth.models import User
from karigars.models import RegisterKarigarModel
from requests.models import AddRequest
from customers.models import Review

def add_shop(request):
    my_shop = AddShopModel.objects.filter(shop_owner__fake_id=request.user.id)
    if my_shop.count()>=1:
        if request.POST.get('button') == 'Search':
            searched_text = request.POST.get('searched_text', '').strip()
            if searched_text:
                if searched_text.isnumeric():
                    customers = AddCustomerModel.objects.filter(serial_number=searched_text, shop=my_shop.first())
                else:
                    customers = AddCustomerModel.objects.filter(customer_name__icontains=searched_text, shop=my_shop.first())
                if customers.count()==1:
                    return redirect('customers:customer_details',customers.first().id)
                elif customers.count() == 0:
                    return render(request,'message.html',{'msg':'No name found'})
            else:
                customers = []
            return render(request, 'my_shop.html', {'customers': customers, 'my_shop': my_shop.first()})
        else:
            all_customers = AddCustomerModel.objects.filter(shop__shop_owner__fake_id=request.user.id)
            customers_dic={customer.serial_number:customer for customer in all_customers }
            try:
                last_number=all_customers.latest('serial_number').serial_number
                customers=[
                    customers_dic.get(i,None) for i in range(1,last_number+1)]
            except:
                customers={}
            my_shop=AddShopModel.objects.get(id=my_shop.first().id)
            karigar_requests=AddRequest.objects.filter(shop=my_shop).exclude(status='accepted').exclude(requester='shop')
            
            return render(request,'my_shop.html',{'customers':customers,'my_shop':my_shop,'karigar_requests':karigar_requests})
 
    else:
        if request.method == 'POST':
            owner = LoginModel.objects.get(fake_id=request.user.id)
            form = AddShopForm(request.POST, request.FILES)
            if form.is_valid():
                shop = form.save(commit=False)
                shop.shop_owner = owner
                shop.save()
                return redirect('home:home')
        else:
            phone = LoginModel.objects.get(fake_id=request.user.id).phone
            form = AddShopForm(initial={'phone': phone})
            
        return render(request, 'submit.html', {'form': form, 'text': 'Please enter the information below!'})

def update_shop(request,shop_id):
    shop = AddShopModel.objects.get(shop_owner__fake_id=request.user.id)
    if request.method == 'POST':
        form = AddShopForm(request.POST,instance=shop)
        if form.is_valid():
            form.instance.shop_owner=LoginModel.objects.get(fake_id=request.user.id)
            form.save()
            return redirect('shops:add_shop')
    else:
        form=AddShopForm(instance=shop)
        return render(request,'submit.html',{'form':form,'text':'Update Shop info!'})

def delete_shop(request,shop_id):
    shop = AddShopModel.objects.get(id=shop_id)
    if request.POST.get('button')=='ہاں':
        shop.delete()
        return redirect('home:home')
    elif request.POST.get('button')=='نہیں':
        return redirect('shops:add_shop')
    return render(request,'warn.html',{'msg':f'Are you sure to delete the {shop.shop_name} shop.Every data related to the shop will also be erased.Note that the action is not reversable!'})

def booking(request,shop_id):
    if request.method=='POST':
        shop=AddShopModel.objects.get(id=shop_id)
        if ('On' in request.POST and 'Off' in request.POST) or ('On' not in request.POST and 'Off' not in request.POST):
            return render(request,'message.html',{'msg':'Please select one option.'})
        elif 'On' in request.POST:
            shop.booking=True
        elif 'Off' in request.POST:
            shop.booking=False
        shop.save()
        return redirect('shops:add_shop')
    else:  
        return render(request,'booking.html')

def google_map(request,shop_id):
    shop=AddShopModel.objects.get(id=shop_id)
    if request.method == 'POST':
        shop.map_link = request.POST.get('map_link')
        shop.save()
        return redirect('shops:add_shop')
    return render(request,'google_map.html')

def shop_details(request,shop_id):
    shop=AddShopModel.objects.get(id=shop_id)
    for a in AddRequest.objects.filter(karigar__id=request.user.id):
        a.delete()
    try:
        karigar=RegisterKarigarModel.objects.get(fake_id=request.user.id)
        request_obj = AddRequest.objects.filter(shop=shop,karigar=karigar)
        if request_obj.count() >= 1:
            req_obj = request_obj.first()
            status=req_obj.status
            return render(request ,'shop_details.html',{'shop':shop,'status':status,'karigar':karigar,'req_obj':req_obj})
        else:
            status='not_sent'
        
    except RegisterKarigarModel.DoesNotExist:
        status=None
        karigar=None
    return render(request ,'shop_details.html',{'shop':shop,'status':status,'karigar':karigar})
# request sent by karigar
def request_recived(request,shop_id):
    shop = AddShopModel.objects.get(id=shop_id)
    karigar = RegisterKarigarModel.objects.get(fake_id=request.user.id)
    try:
        request_obj=AddRequest.objects.get(shop=shop,karigar=karigar)
    except AddRequest.DoesNotExist:
        
        request_obj=AddRequest.objects.create(
                    shop=shop,
                    karigar=karigar,
                    status='not_sent',
                    requester='karigar',
                    )
        request_obj.save()
        status='not_sent'
    if request.method =='POST':
        request_obj.status='sent'
        request_obj.requester='karigar'
        request_obj.save()
        status='sent'
    else:
        status=request_obj.status
    return render(request,'shop_details.html',{'shop':shop,'status':status})


def delete_request(request,shop_id):
    shop=AddShopModel.objects.get(id=shop_id)
    try:
        request_obj=AddRequest.objects.get(karigar__fake_id=request.user.id,requester='karigar',shop=shop)
        if request.POST.get('button')=='منسوخ':
            request_obj.delete()
    except AddRequest.DoesNotExist:
        if request.method=='POST':
            if request.POST.get('button')=='قبول':
                karigar = RegisterKarigarModel.objects.get(fake_id=request.user.id)
                karigar.karigar_shop=AddShopModel.objects.get(id=shop_id)
                karigar.save()
            deleteing = [req.delete() for req in AddRequest.objects.filter(karigar__fake_id=request.user.id,shop=shop)]
    return redirect('shops:shop_details',shop_id)


def request_accept(request,r_id):
    request_obj=AddRequest.objects.get(id=r_id)
    karigar = RegisterKarigarModel.objects.get(id=request_obj.karigar.id)
    if request.POST.get('button') == 'قبول کریں':
        request_obj.status='accepted'
        shop=AddShopModel.objects.get(shop_owner__fake_id=request.user.id)
        karigar.karigar_shop=shop
        request_obj.save()
        karigar.save()
        AddRequest.objects.filter(karigar=karigar,shop=shop).delete()
        return redirect('shops:add_shop')
    elif request.POST.get('button') == 'منسوخ':
        request_obj.delete()
        if request_obj.requester=='shop':
            return redirect('shops:karigar_info',karigar.fake_id)
        else:
            return redirect('shops:add_shop')
    return render(request,'request_accept.html')

def my_karigar(request,shop_id):
    my_karigar=RegisterKarigarModel.objects.filter(karigar_shop__id=shop_id)
    return render(request,'my_karigar.html',{'my_karigar':my_karigar})

def karigar_info(request,k_id,shop_id=None):
    karigar = RegisterKarigarModel.objects.get(fake_id=k_id)
    karigar_current_shop=karigar.karigar_shop
    if request.method=='POST':
        if request.POST.get('searched_text'):
            searched_text = request.POST.get('searched_text', '').strip()
            customers=[]
            if searched_text.isnumeric():
                customers = AddCustomerModel.objects.filter(serial_number=searched_text,shop=karigar.karigar_shop)
            else:
                customers=AddCustomerModel.objects.filter(customer_name__icontains=searched_text,shop=karigar.karigar_shop)
            if customers.count()==1:
                return redirect('customers:customer_details',customers.first().id)
            elif customers.count() == 0:
                return render(request,'message.html',{'msg':'No name found','redirect_to':f'karigars:karigar_info {k_id}'})
    else:
        
        all_customers = AddCustomerModel.objects.filter(shop=karigar_current_shop)
        customers_dic={customer.serial_number:customer for customer in all_customers }
        try:
            last_number=all_customers.latest('serial_number').serial_number
            customers=[
                customers_dic.get(i,None) for i in range(1,last_number+1)]
        except:
            customers={}
        if shop_id:
            shop=AddShopModel.objects.get(id=shop_id)
        else:
            try:
                shop = AddShopModel.objects.get(shop_owner__fake_id=request.user.id)
            except AddShopModel.DoesNotExist:
                shop=None
        if shop:
            req=AddRequest.objects.filter(karigar=karigar,shop=shop).first()
            shop_reqs=AddRequest.objects.filter(karigar=karigar,status='sent',requester='shop')
            return render(request,'karigar_info.html',{'me':karigar,'req':req,'customers':customers,'shop_reqs':shop_reqs})
        else:
            shop_reqs=AddRequest.objects.filter(karigar=karigar,status='sent',requester='shop')
            return render(request,'karigar_info.html',{'me':karigar,'customers':customers,'shop_reqs':shop_reqs})
            
    return render(request,'karigar_info.html',{'me':karigar,'customers':customers})

def leave_shop(request,shop_id,krgr_id=None):
    if request.method == 'POST':
        if krgr_id == None:
                krgr_id=request.user.id
        if request.POST.get('button')=='ہاں':
            karigar=RegisterKarigarModel.objects.get(fake_id=krgr_id)
            deleting = [req.delete() for req in AddRequest.objects.filter(shop__id=shop_id,karigar=karigar)]
            karigar.karigar_shop=None
            karigar.save()
            return redirect('shops:shop_details',shop_id)
        else:
            return redirect('shops:karigar_info',krgr_id)
    else:
        return render(request,'warn.html',{'msg':'Are you sure want to leave the shop.'})
            
# Shop request to karigar
def request_karigar(request,karigar_id):
    karigar=RegisterKarigarModel.objects.get(fake_id=karigar_id)
    shop=AddShopModel.objects.get(shop_owner__fake_id=request.user.id)
    req_obj=AddRequest.objects.create(
        karigar=karigar,
        shop=shop,
        status='sent',
        requester='shop',
        )
    return redirect('shops:karigar_info',karigar.fake_id)

def delete_karigar_request(request,karigar_fake_id):
    
    return redirect('shops:karigar_info',karigar_fake_id)

def update_shop_photo(request,shop_id):
    shop = AddShopModel.objects.get(id=shop_id)
    if request.method == 'POST' and 'button' not in request.POST:
        image=request.FILES['image']
        shop.image = image
        shop.save()
        return redirect('shops:add_shop')
    if request.POST.get('button')=='Update' :
        return render(request,'update.html')
    elif request.POST.get('button') == 'Delete':
        shop.image='default_shop.jpeg'
        shop.save()
        return redirect('shops:add_shop')


def rate_shop(request,shop_id,customer_id):
    if request.method == 'POST':
        customer=AddCustomerModel.objects.get(id=customer_id)
        shop=AddShopModel.objects.get(id=shop_id)
        rating=int(request.POST.get('rating'))
        comment=request.POST.get('comment')
        alreay_exists = Review.objects.filter(shop__id=shop_id,customer__id=customer_id)
        if alreay_exists.exists():
            alreay_exists.delete()
        Review.objects.create(
            customer=customer,
            shop=shop,
            rating=rating,
            comment=comment
            )
        return render(request,'message.html',{'msg':'Thank you for the rating.'})
    return render(request,'rate_shop.html')