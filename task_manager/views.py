from django.shortcuts import render

# Create your views here.
def task_manager(request):
    titulo = "AgriTech"
    return(render(request, 'task_manager.html',  { 
                                            'width': 'w-20'     }))
