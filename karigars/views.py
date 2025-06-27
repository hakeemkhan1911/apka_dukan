from django.shortcuts import render,redirect
from .models import RegisterKarigarModel
from .forms import RegisterKarigarForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from login.models import LoginModel

def register_karigar(request):
    if request.method != 'POST':
        form = RegisterKarigarForm(initial={'email':'@gmail.com'})
        return render(request, 'submit.html', {'form': form})

    password = request.POST.get('password')
    password_again = request.POST.get('password_again')
    email = request.POST.get('email')
    username = request.POST.get('full_name')

    if password != password_again:
        return render(request, 'message.html', {'msg': 'پاس ورڈ مماثل نہیں ہیں۔ دوبارہ کوشش کریں۔'})  # Translated

    # Check if username already exists
    if LoginModel.objects.filter(full_name=username).exists() or RegisterKarigarModel.objects.filter(full_name=username).exists():
        return render(request, 'message.html', {'msg': 'یہ صارف نام پہلے سے استعمال ہو چکا ہے۔ براہ کرم کوئی دوسرا نام استعمال کریں۔'})  # Translated

    # Validate the form first
    form = RegisterKarigarForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'message.html', {'msg': 'فارم کا ڈیٹا درست نہیں ہے۔ براہ کرم چیک کرکے دوبارہ کوشش کریں۔'})  # Translated

    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'message.html', {'msg': 'تصدیق ناکام ہوئی۔ براہ کرم دوبارہ کوشش کریں۔'})  # Translated

        login(request, user)
        if not 'image' in request.FILES:
            form.instance.image = 'default_user.jpg'
        form = form.save(commit=False)
        form.fake_id = user.id
        form.status = 'karigar'
        try:
            form.save()
        except:
            form.image='default_user.jpg'
            form.save()
        return redirect('home:home')

    except Exception as ex:
        return render(request, 'message.html', {'msg': f'خرابی: {str(ex)}'})  # Translated


def login_karigar(request):
    if request.method == 'POST':
        full_name=request.POST.get('full_name')
        password = request.POST.get('password')
        karigar = RegisterKarigarModel.objects.filter(
            full_name=full_name,
            password=password
            )
        if karigar.count()==1:
            user = authenticate(request,username=full_name,password=password)
            if user is not None:
                login(request,user)
                return redirect('home:home')
        else:
            return render(request,'message.html',{'msg':'معذرت، لاگ ان نہیں ہو سکا','redirect_to':'karigars:login_karigar'})  # Translated
    else:
        return render(request,'login_karigar.html')

def update_karigar(request):
    karigar = RegisterKarigarModel.objects.get(fake_id=request.user.id)
    if request.method == 'POST':
        shop = karigar.karigar_shop
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        if password != password_again:
            return render(request, 'message.html', {'msg': 'معذرت، پاس ورڈ مماثل نہیں ہیں۔','redirect_to':'home:home'})  # Translated
        form = RegisterKarigarForm(request.POST, instance=karigar)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            # Update the User model
            full_name = request.POST.get('full_name')
            user.username = full_name
            user.set_password(password)  # Update the password
            user.save()

            # Update the LoginModel instance
            form.instance.fake_id = user.id
            form.instance.full_name=full_name
            form.instance.karigar_shop=shop
            form.save()  # Save the updated instance

            # Authenticate and log in the user
            user = authenticate(request, username=user.username, password=password)  # Use updated username and password
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('home:home')
            else:
                return render(request, 'message.html', {'msg': 'لاگ ان کرنے میں ناکامی۔ براہ کرم دوبارہ کوشش کریں۔'})  # Translated
        else:
            return render(request, 'message.html', {'msg': 'غلط تصدیقی معلومات!'})  # Translated
    
    else:
        form = RegisterKarigarForm(instance=karigar)
        return render(request, 'submit.html', {'form': form, 'text': 'اپنی معلومات اپ ڈیٹ کریں۔'})  # Translated


def delete_karigar(request):
    if request.method=='POST':
        if request.POST.get('button')=='Yes':
            RegisterKarigarModel.objects.get(fake_id=request.user.id).delete()
            User.objects.get(id=request.user.id).delete()
            return redirect('home:home')
        else:
            return redirect('shops:karigar_info',request.user.id)
    else:
        return render(request,'warn.html',{'msg':'کیا آپ واقعی اپنا اکاؤنٹ حذف کرنا چاہتے ہیں؟'})  # Translated

def all_karigars(request):
    karigars=RegisterKarigarModel.objects.filter(karigar_shop=None)
    return render(request,'all_karigars.html',{'karigars':karigars})