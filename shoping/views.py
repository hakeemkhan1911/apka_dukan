from django.shortcuts import render, redirect
from django.db.models import Count
from .models import SellProductModel,ImageModel,MessagesModel,SellerByer
from .forms import SellProductForm,ImageForm,MessagesForm
from django.contrib.auth.models import User
from karigars.models import RegisterKarigarModel
from login.models import LoginModel
from django.db.models import Q


def shoping_list(request):
    if request.method=='POST':
        searched_text=request.POST.get('searched_text')
        whole_list=SellProductModel.objects.filter(Q(category__icontains=searched_text)|Q(name__icontains=searched_text)|Q(location__icontains=searched_text))
    else:
        whole_list=SellProductModel.objects.all()
    ids = [a.id for a in whole_list]
    whole_list1 =[]
    for a in ids:
        obj=ImageModel.objects.filter(product_info_id=a).first()
        if obj is not None:
            whole_list1.append(obj)
    return render(request,'shoping_list.html',{'images':whole_list1})

def sell_product(request):
    if request.method == 'POST':
        form = SellProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.owner=User.objects.get(id=request.user.id)
            form.save()
            return redirect('shoping:upload_image',form.instance.id)
    else:
        form = SellProductForm()
    return render(request,'submit.html',{'form':form,'text':"براہ کرم اپنی پروڈکٹ کی تفصیلات شامل کریں۔"})

def product_details(request,product_info_id):
    product = SellProductModel.objects.get(id=product_info_id)
    product_images=ImageModel.objects.filter(product_info=product)
    message=SellerByer.objects.filter(seller__id=request.user.id,product=product)
    try:
        product_owner_phone=LoginModel.objects.get(fake_id=product.owner.id).phone
    except LoginModel.DoesNotExist:
        product_owner_phone=RegisterKarigarModel.objects.get(fake_id=product.owner.id).phone
    return render(request,'product_details.html',{'product':product,'product_images':product_images,'message':message,'product_owner_phone':product_owner_phone})
def upload_image(request,image_info_id):
    if request.method == 'POST':
        form=ImageForm(request.POST,request.FILES)
        image_info = SellProductModel.objects.get(id=image_info_id)
        if form.is_valid():
            form.instance.product_info=image_info
            form.save()
            return redirect('shoping:product_details',image_info_id)
    else:
        form=ImageForm()
        return render(request,'submit.html',{'form':form,'text':'Select image to upload'})
    
def my_list(request):
    my_list=SellProductModel.objects.filter(owner__id=request.user.id)
    ids=[obj.id for obj in my_list]
    products = []
    uncompleted=[]
    for obj_id in ids:
        obj = ImageModel.objects.filter(product_info__id=obj_id).first()
        if obj is not None:
            products.append(obj)
        else:
            uncompleted.append(obj_id)
    uncompleted=SellProductModel.objects.filter(id__in=uncompleted)
    return render(request,'my_list.html',{'products':products,'uncompleted':uncompleted})

def delete_product(request,product_id):
    if request.method=='POST':
        if request.POST.get('button')=='ہاں':
            SellProductModel.objects.get(id=product_id).delete()
            return redirect('shoping:my_list')
        elif request.POST.get('button')=='نہیں':
            return redirect('shoping:product_details',product_id)
    else:
        return render(request,'warn.html',{'msg':'Are you sure to delete?'})

def product_update(request,product_info_id):
    product=SellProductModel.objects.get(id=product_info_id)
    if request.method == 'POST':
        form=SellProductForm(request.POST,instance=product)
        if form.is_valid():
            form.instance.owner=User.objects.get(id=request.user.id)
            form.save()
        return redirect('shoping:product_details',product_info_id)
    else:
        form=SellProductForm(instance=product)
        return render(request,'submit.html',{'form':form})

def messaging(request,product_id,byer_id):
    product=SellProductModel.objects.get(id=product_id)
    byer = User.objects.get(id=byer_id)
    message_info = SellerByer.objects.filter(product=product,seller=product.owner,byer=byer)
    # Owner is the current user
    if message_info.count() >=1:
        message_update=MessagesModel.objects.filter(message_header__product=product,message_header__seller=product.owner,message_header__byer=byer)
        if request.user.id == byer.id:
            message_update.update(seller_read=True)
        else:
            message_update.update(byer_read=True)
        messages = MessagesModel.objects.filter(message_header=message_info.first())
        message_header=messages.first()
    else:
        message_info=SellerByer.objects.create(byer=byer,seller=product.owner,product=product)
        message_info.save()
        messages=[]
    if request.method == 'POST':
        form=MessagesForm(request.POST)
        if form.is_valid():
            form.instance.sender=User.objects.get(id=request.user.id)
            #Product owner is messaging
            if request.user.id == product.owner.id:
                form.instance.reciver=byer
                form.instance.byer_read=True
            else:# Byer is messaging
                form.instance.reciver=product.owner
                form.instance.seller_read=True
            form.instance.product=product
            form.instance.message_header=message_info.first()
            form.save()
            messages=MessagesModel.objects.filter(message_header__byer=byer,message_header__product=product)
            form=MessagesForm()
    else:
        form=MessagesForm()
    return render(request,'messaging.html',{'messages':messages,'form':form})
        
def recipients_list(request,product_id):
    product=SellProductModel.objects.get(id=product_id)
    recipients=SellerByer.objects.filter(seller__id=request.user.id,product=product)
    recipients = [(MessagesModel.objects.filter(message_header=msg_obj,byer_read=False).count(),MessagesModel.objects.filter(message_header=msg_obj).first()) for msg_obj in recipients]
    return render(request,'recipents_list.html',{'recipients_list':recipients})

def full_image(request,image_url,has_permission=None,user_id=None,user_type=None):
    return render(request,'full_image.html',{'image_url':image_url,'user_type':user_type,'has_permission':has_permission,'user_id':user_id})
    
def delete_product_image(request,image_id):
    image=ImageModel.objects.get(id=image_id)
    image_info_id = image.product_info.id
    image.delete()
    return redirect('shoping:product_details',image_info_id)
    
