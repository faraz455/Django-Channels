from django.shortcuts import render
from app.models import Chat, Group
# Create your views here.
def indexPage(request, group_name):
    print(group_name, 'group nameeeee')
    group = Group.objects.filter(name=group_name).first()
    chats= []
    if group:
        chats = Chat.objects.filter(groupName = group)
        print('in chatttttt---- ', chats)
    else:
        group = Group(name = group_name)
        group.save()
    print('group----------', group)
    

    return render(request, 'index.html', {'groupName': group_name, 'chats': chats})