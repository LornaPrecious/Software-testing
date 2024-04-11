from django.shortcuts import render
from useraccounts.models import Contact
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request, "main/base.html")

def home(request):
    return render(request, "main/home.html")

# def aboutus(request):
#     return render(request, "main/aboutus.html")

def contactUs(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        contact_message = request.POST['message']


        if User.objects.filter(email=email):
            myCustomer = request.user.customer

            customer_contact = Contact(customer = myCustomer, fullname = fullname, email = email, contact_message = contact_message)
            customer_contact.save()
        
        else:
            customer_contact = Contact(fullname = fullname, email = email, contact_message = contact_message)
            customer_contact.save()

    return render(request, "main/contact.html")
      
