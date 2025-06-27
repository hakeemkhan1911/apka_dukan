from django.shortcuts import render,redirect
from .models import Transaction
from django.contrib.auth.models import User


def start_payment(request):
    if request.method=='POST':
        payment_app=request.POST.get('button')
        if payment_app=='easypaisa':
            return render(request,'pay_to.html',{'payment_method':'easypaisa','number':'03201809688'})
        elif payment_app =='jazzcash':
            return render(request,'pay_to.html',{'payment_method':'jazzcash','number':'03201809688'})
            
            
    return render(request,'start_payment.html')

def get_trnxn_id(request,payment_method):
    if payment_method=='easypaisa':
        pass
    elif payment_method=='jazzcash':
        pass
    if request.method == 'POST':
        tr_id=request.POST.get('transaction_id')
        user=User.objects.get(id=request.user.id)
        if Transaction.objects.filter(tid=tr_id).exists():
            return render(request,'message.html',{'msg':'The ID has already been used.'})
        Transaction.objects.create(
            
            user=user,
            tid=tr_id,
            plan='monthly',
            payment_method=payment_method,
            is_verified=False,
            
            )
        return render(request,'message.html',{'msg':'Thank you, we will notify you soon','redirect_to':'home:home'})
        
    return render(request,'get_trnxn_id.html',{'payment_method':payment_method})