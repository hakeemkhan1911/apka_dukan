# Login views
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import LoginModel,OTP
from .forms import LoginForm
from shops.models import AddShopModel
from django.contrib.sessions.models import Session
from django.utils import timezone
from django import forms
from shoping.models import SellerByer,ImageModel,MessagesModel
from django.db.models import Min
from karigars.models import RegisterKarigarModel
from django.core.mail import send_mail
import smtplib
import socket

def logout_user(request):
    if request.method == 'POST':
        if request.POST.get('button')=='ہاں':
            logout(request)
        return redirect('home:home')
            
    else:
        return render(request,'warn.html',{'msg':'کیا آپ واقعی لاگ آؤٹ کرنا چاہتے ہیں؟'})

def register_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = f"{first_name} {last_name}"
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password_again = form.cleaned_data.get('password_again')

            if password != password_again:
                return render(request, 'message.html', {'msg': 'معاف کیجیے، پاس ورڈز مطابقت نہیں رکھتے!'})
            if LoginModel.objects.filter(full_name=username).exists() or User.objects.filter(username=username).exists():
                return render(request, 'message.html', {'msg': 'یہ صارف نام پہلے ہی استعمال ہو چکا ہے۔ براہ کرم کوئی اور استعمال کریں۔'})

            if LoginModel.objects.filter(email=email).exists():
                return render(request, 'message.html', {'msg': 'معاف کیجیے، یہ ای میل پہلے سے موجود ہے۔'})

            try:
                from decouple import config
                if username==config('SUPER_USER') and email==config('SUPER_USER_EMAIL'):
                    user = User.objects.create_superuser(username=username, password=password, email=email)
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    
                    login_model = form.save(commit=False)
                    login_model.fake_id = int(user.id)
                    login_model.full_name = username
                    login_model.status = 'shop_keeper'
                    if not 'image' in request.FILES:
                        login_model.image = 'default_user.jpg'
                    try:
                        login_model.save()
                    except:
                        login_model.image='default_user.jpg'
                        login_model.save()
                    return redirect('home:home')
                else:
                    return render(request,'message.html',{'msg':'Something bad happend'})
            except Exception as e:
                return render(request, 'message.html', {'msg': f'کچھ غلط ہو گیا {e} :'})
    else:
        form = LoginForm(initial={'email':'@gmail.com'})
        return render(request, 'submit.html', {'form': form, 'text': 'براہ کرم اپنی معلومات نیچے درج کریں۔'})

def get_one_image_per_product(objs):
    image_ids = objs.values('product_info').annotate(min_id=Min('id')).values_list('min_id', flat=True)
    images = ImageModel.objects.filter(id__in=image_ids)
    return images

def me(request):
    try:
        me = LoginModel.objects.get(fake_id=request.user.id)
    except LoginModel.DoesNotExist:
        me=RegisterKarigarModel.objects.get(fake_id=request.user.id)
    user=User.objects.get(id=request.user.id)
    my_products = get_one_image_per_product(ImageModel.objects.filter(product_info__owner=user))
    i_want_to_buy = SellerByer.objects.filter(byer=user).values_list('product_id', flat=True)
    product_ids = list(i_want_to_buy)
    i_want_to_buy=get_one_image_per_product(ImageModel.objects.filter(product_info__id__in=product_ids))
    def sort_it(to_sort,whome):
        li=[]
        if whome == 'sender':
            for a in to_sort:
                b = MessagesModel.objects.filter(message_header__seller__id=request.user.id, message_header__product=a.product_info,byer_read=False).count()
                li.append((b,a))
        else:
            for a in to_sort:
                b = MessagesModel.objects.filter(message_header__byer__id=request.user.id, message_header__product=a.product_info,seller_read=False).count()
                li.append((b,a))
        li = sorted(li, key=lambda x: x[0],reverse=True)
        return li
    i_want_to_buy=sort_it(i_want_to_buy,'byer')
    my_products = sort_it(my_products,'sender')
    total_new_msgs=sum([a[0] for a in my_products]+[a[0] for a in i_want_to_buy])
    shop_id = AddShopModel.objects.filter(shop_owner__fake_id=me.fake_id).first()
    return render(request,'me.html',{'me':me,'shop_id':shop_id,'my_products':my_products,'i_want_to_buy':i_want_to_buy,'total_new_msgs':total_new_msgs})


def update_user(request):
    try:
        user1 = LoginModel.objects.get(fake_id=request.user.id)
    except LoginModel.DoesNotExist:
        return redirect('karigars:update_karigar')
    if request.method == 'POST':
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        
        if password != password_again:
            return render(request, 'message.html', {'msg': 'معاف کیجیے، پاس ورڈز مطابقت نہیں رکھتے۔'})
        
        form = LoginForm(request.POST, instance=user1)
        
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            
            # Update the User model
            full_name = request.POST.get('first_name') + ' ' + request.POST.get('last_name')
            email=request.POST.get('email')

            if LoginModel.objects.filter(full_name=full_name).exclude(id=form.instance.id).exists():
                return render(request,'message.html',{'msg':'Sorry the username has already been used. Please try another one.'})
            if LoginModel.objects.filter(email=email).exclude(id=form.instance.id).exists():
                return render(request,'message.html',{'msg':'Sorry the Email has already been used. Please try another one.'})
            user.email=email
            user.username = full_name
            user.set_password(password)  # Update the password
            user.save()

            # Update the LoginModel instance
            form.instance.fake_id = user.id
            form.instance.full_name=full_name
            form.save()  # Save the updated instance

            # Authenticate and log in the user
            user = authenticate(request, username=user.username, password=password)  # Use updated username and password
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('login:me')
            else:
                return render(request, 'message.html', {'msg': 'لاگ ان کرنے میں ناکامی ہوئی۔ براہ کرم دوبارہ کوشش کریں۔'})
        else:
            return render(request, 'message.html', {'msg': 'غلط اسناد!'})
    
    else:
        form = LoginForm(instance=user1)
        return render(request, 'submit.html', {'form': form, 'text': 'اپنی معلومات اپ ڈیٹ کریں۔'})

def delete_user(request):
    try:
        user=LoginModel.objects.get(fake_id=request.user.id)
    except LoginModel.DoesNotExist:
        return redirect('karigars:delete_karigar')
        
    if request.POST.get('button')=='ہاں':
        shop=AddShopModel.objects.filter(id=user.id)
        if shop.count()==1:
            shop.first().delete()
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            if str(user.id) == session.get_decoded().get('_auth_user_id'):
                session.delete()
        
        User.objects.get(id=request.user.id).delete()
        logout(request)
        user.delete()
        return redirect('home:home')
    elif request.POST.get('button')=='نہیں':
        return redirect('login:me')
    return render(request, 'warn.html', {'msg': 'کیا آپ واقعی حذف کرنا چاہتے ہیں؟ یہ عمل واپس نہیں ہو سکتا۔'})

def login_user(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        to_login=LoginModel.objects.filter(full_name=username,email=email,password=password)
        if to_login.exists():
            user = authenticate(request,username=username,password=password,email=email)
            if user is not None:
                login(request,user)
                return redirect('home:home')
            else:
                return render(request, 'message.html', {'msg': 'غلط صارف نام یا پاس ورڈ!'})
        else:
            return render(request, 'message.html', {'msg': 'غلط صارف نام یا پاس ورڈ!','redirect_to':'login:login_user'})
    else:
        return render(request,'login_user.html')
  
def which_user(request):
    if request.method == 'POST':
        if request.POST.get('button') =='دکان دار':
            return redirect('login:login_user')
        elif request.POST.get('button') == 'کاریگر':
            return redirect('karigars:login_karigar')
        else:
            return render(request,'message.html',{'msg':'Sorry can\'t proceed'})
    else:
        return render(request,'which_user.html')

def register(request):
    if request.method == 'POST':
        if request.POST.get('button') == 'کاریگر':
            return redirect('karigars:register_karigar')
        else:
            return redirect('login:register_user')
    else:
        return render(request,'register.html')

def new_password(request):
    
    if request.method == 'POST':
        password=request.POST.get('password')
        re_enter=request.POST.get('renter_password')
        if password == re_enter:
            email=request.session.get('otp_email')
            user=User.objects.filter(email=email)
            username=user.first().username
            user_instance = user.first()
            user_instance.set_password(password)
            user_instance.email=email
            user_instance.save()
            user = authenticate(request,username=username,password=password,email=email)
            if user is not None:
                login(request,user)
                current_user = LoginModel.objects.filter(fake_id=user.id).first()
                if not current_user:
                    current_user = RegisterKarigarModel.objects.filter(fake_id=user.id).first()
                current_user.password=password
                current_user.save() 
                return redirect('home:home')
            return render(request, 'message.html', {'msg': f'کامیابی {user}'})
        else:
            return render(request, 'message.html', {'msg': 'دوبارہ کوشش کریں'})
    else:
        return render(request,'new_password.html')


def password_reset(request):
    if request.method == 'POST':
        if 'email' in request.POST:
            email=request.POST.get('email')
            if User.objects.filter(email=email).exists():
                import random
                otp_random = random.randint(100000,999999)
                request.session['otp_email']=email
                OTP.objects.filter(email=email).delete()
                OTP.objects.create(email=email,otp=otp_random)
                try:
                    send_mail(
                        subject='Password Reset',
                        message=f'''
                            محترم صارف،
                            آپ کی (اپکا دوکان) پر پاس ورڈ دوبارہ ترتیب دینے کی درخواست موصول ہوئی ہے۔
                            براہ کرم نیچے دیا گیا ایک دفعہ استعمال ہونے والا پاس کوڈ درج کریں:
                            🔐 پاس کوڈ: {otp_random}
                            
                            اگر آپ نے یہ درخواست نہیں دی تو براہ کرم اس پیغام کو نظر انداز کریں۔
                            آپ کی حفاظت ہمارے لیے بہت اہم ہے۔
                            
                            شکریہ،
                            ٹیم اپکا دوکان
                        ''',
                        from_email='apkadukan1911@gmail.com',  # Uses DEFAULT_FROM_EMAIL
                        recipient_list=[email],  # change to real recipient
                        fail_silently=False,)
                except socket.gaierror:
                    return render(request,'message.html',{'msg':"❌ انٹرنیٹ کنیکشن دستیاب نہیی ہے۔"})
                except smtplib.SMTPAuthenticationError as e:
                    return render(request,'message.html',{'msg':"❌ توثیق ناکام ہو گئی۔ براہ کرم جی میل کا ای میل یا پاس ورڈ چیک کریں۔"})
                except ConnectionRefusedError:
                    return render(request,'message.html',{'msg':"❌  کنیکشن رد کر دیا گیا۔ ہو سکتا ہے پورٹ بلاک ہو یا سرور تک رسائی نہ ہو۔"})
                except socket.timeout:
                    return render(request,'message.html',{'msg':"❌ کنیکشن کا وقت ختم ہو گیا (ٹائم آؤٹ)۔"})
                
                except smtplib.SMTPDataError as e:
                    if e.smtp_code == 421:
                        return render(request,'message.html',{'msg':"⚠️ جی میل کی حد سے تجاوز ہو گیا ہے، بعد میں دوبارہ کوشش کریں۔"})
                    else:
                        return render(request,'message.html',{'msg':"❌ ڈیٹا ایرر ہوا۔"})
                except smtplib.SMTPException as e:
                    return render(request,'message.html',{'msg':"❌ عمومی  ایرر ہوا۔"})
                except Exception as e:
                    return render(request,'message.html',{'msg':"❌ ایک غیر متوقع خرابی پیش آئی۔"})
                return render(request, 'type_password.html')
    
            else:
                return render(request, 'message.html', {'msg': 'ایسا ای میل موجود نہیں ہے۔'})
        elif 'otp' in request.POST:
            otp = request.POST.get('otp')
            try:
                otp_random=OTP.objects.get(email=request.session.get('otp_email'),otp=otp)
                if str(otp) == str(otp_random.otp):
                    if otp_random.is_expired():
                        otp_random.delete()
                        return render(request, 'message.html', {'msg': 'او ٹی پی کی مدت ختم ہو گئی ہے۔'})
                    if 'otp_email' in request.session:
                        email = request.session['otp_email']
                        otp_random.delete()
                        return redirect('login:new_password')
                else:
                    return render(request, 'message.html', {'msg': f'او ٹی پی غلط ہے۔ {otp} {otp_random}'})
            except OTP.DoesNotExist:
                return render(request, 'message.html', {'msg': 'او ٹی پی غلط ہے۔'})
    return render(request,'reset_password_form.html')


def profile_photo_update(request):
    if RegisterKarigarModel.objects.filter(fake_id=request.user.id).exists():
        user = RegisterKarigarModel.objects.get(fake_id=request.user.id)
    elif LoginModel.objects.filter(fake_id=request.user.id):
        user = LoginModel.objects.get(fake_id=request.user.id)
    
    if request.method=='POST' and 'button' not in request.POST:
        user.image = request.FILES['image']
        user.save()#update_fields=['image'])
    if request.POST.get('button') == 'Update':
        return render(request,'update.html')
    elif request.POST.get('button')=='Delete':
        user.image='default_user.jpg'
        user.save()
    return redirect('login:me')

def user_profile(request,user_id):
    try:
        user=LoginModel.objects.get(fake_id=user_id)
    except LoginModel.DoesNotExist:
        user=RegisterKarigarModel.objects.get(fake_id=user_id)
    return render(request,'user_profile.html',{'user_profile':user})
    
'''from django.core.cache import cache
from django.http import JsonResponse

def send_otp(request):
    user_phone = request.POST.get('phone')

    otp_attempts = cache.get(f'otp_attempts_{user_phone}', 0)
    if otp_attempts >= 3:
        return JsonResponse({"error": "Too many OTP requests. Try again later."}, status=429)

    otp = str(random.randint(100000, 999999))
    OTP.objects.filter(phone=user_phone).delete()
    otp_hashed = make_password(otp)
    OTP.objects.create(phone=user_phone, otp_hashed=otp_hashed)

    request.session['otp_phone'] = user_phone  # Store in session

    cache.set(f'otp_attempts_{user_phone}', otp_attempts + 1, timeout=3600)  # Reset after 1 hour

    return JsonResponse({"message": "OTP sent successfully"})'''