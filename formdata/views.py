from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def show_form(request):
    '''Show the form to the user'''

    template_name = 'formdata/form.html'
    return render(request, template_name)

def submit(request): 
    '''Process the form and generate a result'''


    template_name = "formdata/confirmation.html"
    print(request.POST)

    if request.POST:
        
        #extract the fields into vars
        name = request.POST['name']
        fav_color = request.POST['fav_color']

        #create context variables so we can use them in the template!
        context = {
            'name' : name,
            'fav_color' : fav_color,
        }
    return render(request,template_name=template_name, context=context)