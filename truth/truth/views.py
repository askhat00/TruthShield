from django.shortcuts import render


def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def text_checker(request):
    return render(request, 'text_checker.html')

def file_checker(request):
    return render(request, 'file_checker.html')