from django.shortcuts import render

from discussion_forum.models import Category


def mission(request):
    return render(request, 'mission.html')  

def staff(request):
    return render(request, 'staff.html')

def contents(request):
    categories = Category.objects.all()
    return render(request, 'contents.html', {'categories': categories})

def custom_403_view(request, exception):
    return render(request, 'errors/403.html', status=403)

def custom_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500_view(request):
    return render(request, 'errors/500.html', status=500)
