from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from chat.models import Thread


@login_required(login_url='signin')
def chat(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
    user_id = User.objects.get(pk=request.user.id)
    admin_id = User.objects.get(pk=1)
    thread = Thread.objects.filter(Q(first_person=user_id) | Q(second_person=user_id))
    if thread.count() < 1:
        Thread.objects.create(first_person=user_id, second_person=admin_id)
        return redirect('chat')
    return render(request, 'chat/chat.html',
                  {
                      'Threads': threads
                  })
