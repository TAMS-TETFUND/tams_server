from django.shortcuts import render

# Create your views here.
def vue_mount(request):
    return render(request, 'index.html')