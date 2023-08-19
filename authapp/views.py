from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from authapp.models import Contact , Enrollment, MembershipPlan,Trainer,Gallery,Attendance, Equipment, Video
from django.core.mail import send_mail
import uuid
import string
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
import io
from io import BytesIO
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Video
# from django.contrib import messages

# Create your views here.
def Home(request):
    return render(request,"index.html")

def show_quiz(request):
    return render(request, )

def gallery(request):
    posts=Gallery.objects.all()
    context={"posts":posts}
    return render(request,"gallery.html",context)

# ------------------------- Attendance -----------------------------#
def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    SelectTrainer=Trainer.objects.all()
    context={"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        phonenumber=request.POST.get('PhoneNumber')
        Login=request.POST.get('logintime')
        Logout=request.POST.get('loginout')
        SelectWorkout=request.POST.get('workout')
        TrainedBy=request.POST.get('trainer')
        query=Attendance(phonenumber=phonenumber,Login=Login,Logout=Logout,SelectWorkout=SelectWorkout,TrainedBy=TrainedBy)
        query.save()
        messages.warning(request,"Attendace Applied Success")
        return redirect('/attendance')
    return render(request,"attendance.html",context)

#  -------------------------------- profile -----------------------#
def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    user_phone=request.user
    posts=Enrollment.objects.filter(PhoneNumber=user_phone)
    attendance=Attendance.objects.filter(phonenumber=user_phone)
    print(posts)
    context={"posts":posts,"attendance":attendance}
    return render(request,"profile.html",context)

# def profile(request):
#     if not request.user.is_authenticated:
#          messages.warning(request,"Please Login and Try Again")
#          return redirect('/login')
#     user_phone = request.user
#     posts=Enrollment.objects.filter(PhoneNumber=user_phone)
#     attendance=Attendance.objects.filter(PhoneNumber=user_phone)
#     context = {"posts":posts}
#     return render(request,"profile.html", context)

# -------------------------------------- SignUp ---------------------------------#

def signup(request):
    if request.method=="POST":
        username=request.POST.get('usernumber')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
      
        # if len(username)>10 or len(username)<10:
        #     messages.info(request,"Phone Number Must be 10 Digits")
        #     return redirect('/signup')

        if pass1!=pass2:
            messages.info(request,"Password is not Matching")
            return redirect('/signup')
       
        try:
            if User.objects.get(username=username):
                messages.warning(request,"Phone Number is Taken")
                return redirect('/signup')  
        except Exception as identifier:
            pass
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email is Taken")
                return redirect('/signup')  
        except Exception as identifier:
            pass  
        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request,"User is Created Please Login")
        return redirect('/login')   
    return render(request,"signup.html")

# ----------------------- Login ----------------------------------#
def handlelogin(request):
    if request.method=="POST":        
        username=request.POST.get('usernumber')
        pass1=request.POST.get('pass1')
        myuser=authenticate(username=username,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Successful")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')
            
        
    return render(request,"handlelogin.html")

#  --------------------------- Logout ------------------------------#

def handleLogout(request):
    logout(request)
    messages.success(request,"Logout Success")    
    return redirect('/login')

# --------------------  Forget password -----------------------#

def ForgetPassword(request):
    
    try:
        if request.method == 'POST':
            username = request.POST['email']
           
            if not User.objects.filter(email=username).first():
                messages.success(
                    request, 'User does not exist with this UserName')
                return redirect('login')
            else:
                token = str(uuid.uuid4())
                user_obj = User.objects.get(email=username)
                uidb64 = user_obj.id
                subject = 'Forgot Password link'
                message = f'Click on the below link to reset your Password http://127.0.0.1:8000/change_password/{uidb64}/{token}/'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user_obj.email, ]
                send_mail(subject, message, email_from, recipient_list)
                print(send_mail)
                messages.success(request,'Email send succesfully.')
                return redirect('login')   
    except Exception as e:
        print(e)
    return render(request, 'forget_password.html')
    
# -------------------------------- change password ------------------------------------#

def ChangePassword(request, uid64, token):
    
    if request.method == "POST":
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        usr = User.objects.get(id = uid64)
        print(usr)

    try:
       
        if new_password != confirm_password:
            messages.success(
                request, 'Password and Confirm Password must be Same')
            return redirect(f'change_password.html/{uid64}/{token}')

        usr.set_password(new_password)
        usr.save()
        return redirect('password_confirmed')
    except Exception as e:
        print(e)
    return render(request, 'change_password.html')
    
#  ----------------------------- Contact -----------------------#
def contact(request):
    if request.method=="POST":
        name=request.POST.get('fullname')
        email=request.POST.get('email')
        number=request.POST.get('num')
        desc=request.POST.get('desc')
        myquery=Contact(name=name,email=email,phonenumber=number,description=desc)
        myquery.save() 
        user_obj = email
        subject = 'Contact message From  Client'
        message = f'User Name : {name}\n User Mail : {email}\n Phone Number : {number}\n Description : {desc}\n'
        email_from = user_obj
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, email_from, recipient_list)
        print(send_mail)     
        messages.info(request,"Thanks for Contacting us we will get back you soon")
        return redirect('/contact')
        
    return render(request,"contact.html")

# ------------------------------ Enroll ----------------------------#
def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')

    Membership=MembershipPlan.objects.all()
    SelectTrainer=Trainer.objects.all()
    context={"Membership":Membership,"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        FullName=request.POST.get('FullName')
        email=request.POST.get('email')
        gender=request.POST.get('gender')
        PhoneNumber=request.POST.get('PhoneNumber')
        DOB=request.POST.get('DOB')
        member=request.POST.get('member')
        trainer=request.POST.get('trainer')
        reference=request.POST.get('reference')
        address=request.POST.get('address')
        query=Enrollment(FullName=FullName,Email=email,Gender=gender,PhoneNumber=PhoneNumber,DOB=DOB,SelectMembershipplan=member,SelectTrainer=trainer,Reference=reference,Address=address)
        query.save()
        # send_confirmation_mail(request)
        messages.success(request,"Thanks For Enrollment")
        return redirect('/join')
    return render(request,"enroll.html",context)


def Videos(request):
    video=Video.objects.all()
    return render(request, "video.html",{"video": video})

# @login_required
# def upload_video(request):
#     if not request.user.is_staff:
#         messages.warning(request,"Only admin can upload videos.")
#         return redirect('videos')
    
#     if request.method == 'POST':
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Video uploaded successfully.')
#             return redirect('videos')
#     else:
#         form = VideoForm()
#     return render(request, 'upload_video.html', {'form': form})
# def Add_Equipment(request):
#     error = ""
#     if not request.user.is_authenticated:
#         messages.warning(request,"Please Login and Try Again")
#         return redirect('login')
#     if request.method == 'POST':
#         EquipmentName=request.POST.get('EquipmentName')
#         price=request.POST.get('price')
#         unit=request.POST.get('unit')
#         Date=request.POST.get('Date')
#         Description=request.POST.get('Description')
#         try:
#             Equipment.objects.create( name=EquipmentName, price=price, unit=unit, date=Date, description=Description)
#             error = "no"
#         except:
#             error = "yes"
#     Date = {'error': error}
#     return render(request, 'add_equipment.html', Date)


# def View_Equipment(request):
#     equ = Equipment.objects.all()
#     d = {'equ': equ}
#     return render(request, 'view_equipment.html', d)

# def Delete_Equipment(request,pid):
#     equipment = Equipment.objects.get(id=pid)
#     equipment.delete()
#     return redirect('view_equipment')


def Add_Equipment(request):
    error = ""
    # if not request.user.is_staff:
    #     return redirect('handlelogin')
    if request.method == 'POST':
        n = request.POST['name']
        p = request.POST['price']
        u = request.POST['unit']
        d = request.POST['date']
        desc = request.POST['desc']
        try:
            Equipment.objects.create( name=n, price=p, unit=u, date=d, description=desc)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_equipment.html', d)


def View_Equipment(request):
    equ = Equipment.objects.all()
    d = {'equ': equ}
    return render(request, 'view_equipment.html', d)

def Delete_Equipment(request,pid):
    equipment = Equipment.objects.get(id=pid)
    equipment.delete()
    return redirect('view_equipment')






# ------------------------------------- confirmation mail  ---------------------------#

# def send_confirmation_mail(request):
#     enroll_db = Enrollment.objects.filter(id=request.user.id).first()
#     print("--------------", enroll_db)
#     template = get_template('confirmation_mail.html')
#     data = {
#         'loan_id': enroll_db.id,
#         'user_email': enroll_db.Email,
#         'gender': enroll_db.Gender,
#         'PhoneNumber': enroll_db.PhoneNumber,
#         'DOB': enroll_db.DOB,
#         'member': enroll_db.SelectMembershipplan,
#         'trainer': enroll_db.SelectTrainer,
#         'reference': enroll_db.Reference,
#         'address': enroll_db.Address
    
#     }
#     html = template.render(data)
#     subject = 'Apply for Enrollment'
#     message = "PDF Attached Below"
#     email_from =  request.user.email
#     recipient_list = [settings.EMAIL_HOST_USER]
#     mail = EmailMultiAlternatives(subject, message, email_from, recipient_list)
#     mail.attach_alternative(html, "text/html")
#     mail.send()
#     return render(request, 'index.html')

