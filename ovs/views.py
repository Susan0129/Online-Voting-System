from curses.ascii import HT
from http.client import ImproperConnectionState
from django.conf import settings
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth.models import User
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import random
from .models import *
from .forms import CreateUserForm, CreateAdminForm, ChangeForm
import os

# Create your views here.

def home(request):
    return render(request, 'ovs/Welcome.html')

def faq(request):
    return render(request, 'ovs/Faq.html')

def tutorial(request):
    return render(request, 'ovs/Tutorial.html')

def loginUser(request):
    if request.method == "POST":
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.success(request, 'Invalid username or password!')
            return render(request, "ovs/Login_User.html")
    else:
        return render(request, "ovs/Login_User.html")


def registerAdmin(request):
    form = CreateAdminForm()
    
    if request.method=="POST":
        form = CreateAdminForm(request.POST)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'ovs/Register_admin.html',context)

def registerUser(request):
    form = CreateUserForm()
    
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'ovs/Register_User.html',context)

@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    return render(request, "ovs/Dashboard.html")

@login_required
def positionView(request):
    obj = Position.objects.all()
    return render(request, "ovs/position.html", {'obj':obj})

@login_required
def resultView(request):
    obj = Candidate.objects.all().order_by('position','-total_vote')
    return render(request, "ovs/result.html", {'obj':obj})

@login_required
def userVerify(request):
    return render(request,'ovs/Dash.html')

@login_required
def editProfileView(request):
    if request.method == "POST":
        form = ChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/verifyUser')
    else:
        form = ChangeForm(instance=request.user)
    return render(request, "ovs/edit_profile.html", {'form':form})

@login_required
def changePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('/verifyUser')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "ovs/password.html", {'form':form})

@login_required
def candidateView(request, pos):
    obj = get_object_or_404(Position, pk = pos)
    if request.method == "POST":

        temp = ControlVote.objects.get_or_create(user=request.user, position=obj)[0]

        if temp.status == False:
            temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.save()
            temp.status = True
            temp.save()
            return HttpResponseRedirect('/position/')
        else:
            messages.success(request, 'you have already voted this position.')
            return render(request, 'ovs/candidate.html', {'obj':obj})
    else:
        return render(request, 'ovs/candidate.html', {'obj':obj})

@login_required
def candidateDetailView(request, id):
    obj = get_object_or_404(Candidate, pk=id)
    return render(request, "ovs/candidate_detail.html", {'obj':obj})



    
@login_required
def verify(request):
    html_content = '''
        <html>
            <body>
                <img src="cid:logo.png" />
            </body>
        </html>
    '''
    email = EmailMultiAlternatives(
        "User Verification - Share2",
        html_content,
        'susanpeteti@gmail.com',
        ['caspianfernsby@gmail.com']
    )

    email.mixed_subtype = 'related'
    email.attach_alternative(html_content,"text/html")

    img_path = os.path.join(settings.BASE_DIR, 'static/images/share2.png')
    with open(img_path, 'rb') as image:
        banner_image = MIMEImage(image.read())
        banner_image.add_header('Content-ID', '<share2.png>')
        email.attach(banner_image)

    email.send()

    if request.method == 'POST':
        if len(request.FILES) != 0:
            img = request.FILES['image']
        return redirect('dashboard')

    return render(request, 'ovs/Verify.html')
