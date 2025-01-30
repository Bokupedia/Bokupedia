from django.shortcuts import render
from django.db.models import Case, When
from discussion_forum.models import Category

def rules(request):
    return render(request, 'rules.html')  

def mission(request):
    return render(request, 'mission.html')  

def staff(request):
    return render(request, 'staff.html')

def contents(request):
    categories = Category.objects.annotate(
        custom_order=Case(
            When(name='Gündem', then=0),
            default=1,
        )
    ).order_by('custom_order', 'name')
    return render(request, 'contents.html', {'categories': categories})

def custom_403_view(request, exception):
    return render(request, 'errors/403.html', status=403)

def custom_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500_view(request):
    return render(request, 'errors/500.html', status=500)
