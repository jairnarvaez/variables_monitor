from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def sign_in(request):
    titulo = "AgriTech"
    return(render(request, 'sign_in.html',  { 
                                            'width': 'w-20'     }))
