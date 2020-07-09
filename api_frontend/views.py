from django.shortcuts import render

# Create your views here.
def api_frontend(request):
    return render(request,'api_frontend/frontend.html')