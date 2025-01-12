from django.shortcuts import render

from discussion_forum.models import Category


def mission(request):
    return render(request, 'mission.html')  

def staff(request):
    return render(request, 'staff.html')

def contents(request):
    categories = Category.objects.all()
    return render(request, 'contents.html', {'categories': categories})