from login.models import LoginModel
from karigars.models import RegisterKarigarModel
from shoping.models import MessagesModel
from django.contrib.auth.models import User

def user_status(request):
    if request.user.is_authenticated:
        current=User.objects.get(id=request.user.id)
        byer_unread = MessagesModel.objects.filter(message_header__byer=current,seller_read=False).count()
        seller_unread=MessagesModel.objects.filter(message_header__seller=current,byer_read=False).count()
        if byer_unread > 0 or seller_unread > 0:
            global_msg=byer_unread+seller_unread
        else :
            global_msg=False
        try:
            user = LoginModel.objects.get(fake_id=current.id)
        except LoginModel.DoesNotExist:
            user = RegisterKarigarModel.objects.get(fake_id=current.id)
        user_profile_url=user.image.url
        return {"global_status": user.status,'full_name':user.full_name,'global_msg':global_msg,'user_profile_url':user_profile_url}
    
    return {"global_status": "guest"}  # For non-logged-in users