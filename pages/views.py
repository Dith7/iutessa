# pages/views.py
from django.shortcuts import render

def home_view(request):
    """Landing page simple"""
    return render(request, 'pages/home.html', {
        'title': 'IUTESSA Mokolo'
    })