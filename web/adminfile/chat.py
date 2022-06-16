from django.shortcuts import render

class ChatAdmin:
    def chat(request):
        return render(request, 'admin/chat.html')