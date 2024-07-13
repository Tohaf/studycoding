from django.shortcuts import render, redirect
from .models import Room, Topic, message
from .form import createform
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

"""

rooms = [
    {'id':1, 'name':'javascript learning'},
    {'id':2, 'name':'django password'},
    {'id':3, 'name':'glango password'}
]
"""

def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return HttpResponse('You are already login')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "user does not exist")
        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username or password does not exist")
    context = {
        'page':page
    }
    return render (request, 'djangoapp/login_reg.html', context)

def logoutpage(request):
    logout(request)
    return redirect('home')


def RegisterPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
    context = {'form':form}
    return render (request, 'djangoapp/login_reg.html', context)



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None  else ""
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q( name__icontains = q) |Q(decription__icontains = q))
    topic = Topic.objects.all()
    room_count = rooms.count()
    recent_message = message.objects.filter(Q(room__topic__name__icontains = q))
    context = {
        'topic':topic,
        'rooms':rooms,
        'room_count':room_count,
        'recent_message':recent_message
    }
    return render(request, 'djangoapp/home.html', context)


@login_required(login_url='login')
def Rooms(request, pk):
    """"
    room =None
    for i in rooms:
        if i['id'] == pk:
            room = i
    context = {'room':room}
    """
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participant = room.participant.all()
    if request.method == 'POST':
        body_message = message.objects.create(
            user = request.user,
            room = room,
            body=request.POST.get('body')
        )
        room.participant.add(request.user)
        return redirect('Rooms', pk=room.id)

    context = {'room':room, 'room_messages' :room_messages, 'participant':participant}
    return render(request, 'djangoapp/room.html', context)




def userprofile(request, pk):
    user = User.objects.get(id=pk)
    topic = Topic.objects.all()
    rooms = user.room_set.all()
    recent_message = user.message_set.all()
    context = {'user':user, 'topic':topic, 'rooms':rooms, 'recent_message':recent_message }
    return render(request, 'djangoapp/userprofile.html', context)







@login_required(login_url='login')
def createRoom(request):
    form= createform()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        Room.objects.create(
            name = request.POST.get('name'),
            decription = request.POST.get('decription'),
            host = request.user,
            topic = topic
    )
        return redirect('home')
    
    #if request.method == 'POST':
     #   form = createform(request.POST)
      #  if form.is_valid():
       #     form.save()
        #    return redirect('home')
    context = {   
        'form': form,
        'topic': topics
    }

    return render(request, 'djangoapp/form_room.html', context)



@login_required(login_url='login')
def updateroom(request, pk):
    form = Room.objects.get(id=pk)
    update = createform(instance=form)
    if request.method == 'POST':
        update = createform(request.POST, instance=form)
        if update.is_valid():
            update.save()
            return redirect('home')
    context = {'update': update}
    return render(request, 'djangoapp/form_room.html', context)


@login_required(login_url='login')
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'djangoapp/delete.html')


@login_required(login_url='login')
def deletemessage(request, pk):
    room = message.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'djangoapp/delete.html', {'room':room})


























































































