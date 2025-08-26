from django.shortcuts import render

# Create your views here.
def notifications(request):
    titulo = "AgriTech"
    return(render(request, 'notifications.html',  { 
                                            'width': 'w-20',
     }))
