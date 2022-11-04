from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, template_name='course/index.html')

def login(request):
    return render(request, template_name='course/form.html')