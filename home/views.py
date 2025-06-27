from django.shortcuts import render
from django.db.models import Count
from django.db.models import Q
from shops.models import AddShopModel
from .forms import FeedbackForm
from django.contrib.auth.models import User
from customers.models import Review
from payments.models import Transaction

def about_us(request):
    return render(request,'about_us.html')

def login_first(request):
    return render(request,'login_first.html')


def home(request):
    if request.method == 'POST':
        if request.POST.get('text'):
            text=request.POST.get('text')
            all_shops = AddShopModel.objects.filter(Q(shop_name__icontains=text)|Q(shop_address__icontains=text)|Q(shop_owner__full_name__icontains=text))
        
    else:
        all_shops = AddShopModel.objects.annotate(more_customers=Count('addcustomermodel')).order_by('-more_customers')
    all_ratings=Review.objects.all()
    rating_list=[]
    for shop in all_shops:
        each_shop_total_rating=[rate.rating for rate in all_ratings.filter(shop__id=shop.id)]
        rating_per_user=len(each_shop_total_rating)
        if rating_per_user==0:
            rating_per_user=1
        rating_sum_up=sum(each_shop_total_rating)
        rating_avg=round(rating_sum_up/rating_per_user,1)
        rating_list.append((shop,rating_avg))
    my_shop=AddShopModel.objects.filter(id=request.user.id).first()
    is_verified=None
    if request.user.is_authenticated:
        latest_transaction = Transaction.objects.filter(user__id=request.user.id).order_by('-created_at').first()
        is_verified = latest_transaction.is_verified if latest_transaction else False
    return render(request,'home.html',{'all_shops':all_shops,'my_shop':my_shop,'rating_list':rating_list,'is_verified':is_verified})


def feedback(request):
    
    if request.method == 'POST':
        from home.models import FeedbackModel
        rater=User.objects.get(id=request.user.id)
        rating=request.POST.get('rating_')
        comment=request.POST.get('comments')
        FeedbackModel.objects.create(
            rater=rater,
            rating=rating,
            comments=comment,
            )
        return render(request,'message.html',{'msg':'آپ کے فیڈ بیک کا شکریہ!','redirect_to':'home:home'})  # Translated
    form=FeedbackForm()
    return render(request, 'feedback.html',{'form':form})

def contact_us(request):
    from home.models import ContactUs
    if request.method == 'POST':
        user=User.objects.get(id=request.user.id)
        email=user.email
        message=request.POST.get('message')
        ContactUs.objects.create(
            user=user,
            email=email,
            message=message
            )
        return render(request,'message.html',{'msg':'Thank you','redirect_to':'home:home'})
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        name=user.username
        email=user.email
        return render(request,'contact_us.html',{'name':name,'email':email})
    return render(request,'contact_us.html')