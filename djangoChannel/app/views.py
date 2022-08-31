from django.shortcuts import render

# Create your views here.
def indexPage(request, group_name):
    return render(request, 'index.html', {'groupName': group_name})