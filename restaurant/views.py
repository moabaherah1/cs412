# File: views.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 13 Feb 2025
# Description:has all the correct functions to correctly process requests

from django.shortcuts import render
import random
import time 

# Create your views here.
def home(request):
    #Define a view to show the 'home.html' template.

    template = 'restaurant/base.html'
    return render(request, template)

def order(request):
    #Define a view to show the order page
    specials = [
        "The Mike Burger",
        "The JP Burger",
        "The MA Burger",
        "The Richard Burger"
    ]

    template = 'restaurant/order.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        'specials': random.choice(specials)
    }

    return render(request, template, context)

def confirmation(request):
    #Define a view function to show the confirmation page
    if request.method == 'POST':
        # dictionary for prices 
        prices = {
            "Small_Burger": 400,
            "Medium_Burger": 500,
            "Big_Burger": 600,
            "Fries": 70,
            "extra_cheese": 50,
            "beef_bacon": 70,
            "egg": 80,
            "specials": 900,
        }

        # get list of ordered items
        ordered_items = []
        total_price = 0

        # loop through and add items
        for item, price in prices.items():
            if item in request.POST:
                ordered_items.append(item)
                total_price += price
        
        # Since our specials are different than our actual items, we want to check if someone chooses the specials
        #If they do, we want to append it to their order-- i was also having an issue with "None" being appended - 
        #So i do another if statement to check if someone chooses the specific special for that day- and then append - which fixed it
        if "specials" in request.POST:
            special_name = request.POST.get('special')   
            if special_name:     
                ordered_items.append(special_name)   
        
        #this creates a struct apparently so i cant add directly - instead use time.time
        #current_time = time.localtime()
        #random_time = random.randrange(30,60)
        #ready = current_time + random_time
        #readytime = time.strftime("%a %b %d %H:%M:%S %Y", ready)

        current_time = time.time()
        random_time = random.randrange(30,60) * 60 #must be added in seconds
        ready = current_time + random_time 
        final_time = time.localtime(ready)
        readytime = time.strftime("%a %b %d %H:%M:%S %Y", final_time)

        #getting user input stuffs
        name = request.POST.get('name', 'N/A')
        phone = request.POST.get('phone', 'N/A')
        email = request.POST.get('email', 'N/A')

        special_instructions = request.POST.get('special_instructions', 'N/A')

        context = {
            'ordered_items': ordered_items,
            'total_price': total_price,
            'readytime': readytime,
            'name': name,
            'phone':phone,
            'email':email,
            'special_instructions':special_instructions,
        }


        return render(request, 'restaurant/confirmation.html', context)


def main(request):
    #Define a view to show the 'home.html' template
    template = 'restaurant/main.html'
    return render(request, template)