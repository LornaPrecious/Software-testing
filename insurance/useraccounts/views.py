from django.forms import ValidationError
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import *
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.encoding import force_bytes, force_str, force_text
from .tokens import generate_token
from insurance import settings
from useraccounts.utils import determine_policy_based_on_contribution
from formtools.preview import FormPreview


from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import (
    MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
)

# Create your views here.

def register (request):
      if request.method =="POST":
            username = request.POST['username'] 
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            email = request.POST['email']       
            password = request.POST['password']
            pass2 = request.POST['pass2']
     
          
            if User.objects.filter(username=username):
                  messages.error(request, "Username already exist! Please try again")
                  return redirect('register')
            
            if User.objects.filter(email=email):
                  messages.error(request,"Email address is already registered!")
                  return redirect('register')
            
            #validate_password(password)

            if not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password) or len(password)<8:
                  messages.error(request,"Password Error! Must have a digit, one uppercase, one lowercase letter and at least 8 digits")
                  return redirect('register')
            

            if password != pass2:
                  messages.error(request, "Passwords did not match!")        

            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.is_active = False
            user.save()
            
            mycustomer=Customer(user = user, first_name = firstname, last_name = lastname, email=email, password=password)                                
            mycustomer.save()

            messages.success(request, "Your account has been created successfully. Please check your email for email verification.")

            #Verification email
            current_site = get_current_site(request)    
            verification_message = render_to_string('email_verification.html',{
                  'user': user,
                  'domain': current_site.domain,
                  'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                  'token':generate_token.make_token(user),
            })
            subject="Verify your email"
            from_email=settings.EMAIL_HOST_USER
            to_list=[user.email]
            message = EmailMessage(subject, verification_message, from_email, to_list)            
            message.content_subtype="html"
            message.fail_silently = False
            message.send()

            return redirect('login')

      return render(request, "registration/register.html")

def custom_login(request):
      if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                  login(request, user)
                  username = user.username
                  return render(request, "main/home.html", {'username': username})

            else:
                  messages.error(request, "Wrong credentials")
                  return redirect('register')

      return render(request, "registration/login.html")

def signout(request):
      logout(request)
      messages.success(request, 'Logout successfully')
      return redirect('home')

def activate(request, uidb64, token):
      try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user= User.objects.get(pk=uid)
      except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

      if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
      else:
           return render(request, 'activation_failed.html')
      

# def validate_password(password, user = None):
#       validators = [MinimumLengthValidator(min_length=8), CommonPasswordValidator(), NumericPasswordValidator()]
#       errors = []

#       for validator in validators:
#         try:
#             validator.validate(password, user)

#         except ValidationError as e:
#             errors.extend(e.messages)

#       if errors:
#         raise ValidationError(errors)




      # if request.method == "POST":
      #       password = request.POST['password']
      # if not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password):
      #   raise ValidationError("The password must contain both uppercase and lowercase characters, and digits.")


def bradleyForm(request):      
      if request.method =="POST":    
            phone_number = request.POST['telephoneNo']
            idNo = request.POST['idNumber']   
            dob = request.POST['dob']
            gender = request.POST['gender']
            occupation = request.POST['occupation']
            #fetching gender from radio button!

            name = request.POST['dependentName']
            dependants_dob = request.POST['dependentDob']
            relationships = request.POST['dependentRelation']

            mentaldisease = request.POST['mentaldisease']
            heartdisease = request.POST['heartdisease']
            gutdisease = request.POST['gutdisease']
            chestdisease = request.POST['chestdisease']

            contribution = request.POST['contribution']

            myCustomer = request.user.customer
            
            myQuote = QuotationInfo(customer = myCustomer, phone_number = phone_number, nationalid = idNo, dob = dob, gender = gender, occupation = occupation, contribution_amount = contribution)
            myQuote.save()

            mydependants = Dependants(customer = myCustomer, full_name = name, dependants_dob = dependants_dob, relationship = relationships)
            mydependants.save()

            mymentaldisease = MentalDiseases(customer = myCustomer, specific_type = mentaldisease)
            mymentaldisease.save()
            

            myheartdisease = HeartDisease(customer = myCustomer, specific_type = heartdisease)
            myheartdisease.save()
          

            mygutdisease = GutDisease(customer = myCustomer, specific_type = gutdisease)
            mygutdisease.save()
            

            mychestdisease = ChestDisease(customer = myCustomer, specific_type = chestdisease)
            mychestdisease.save()

         


             # Call the function to determine the policy based on the contribution amount
            policy = determine_policy_based_on_contribution(contribution)
            #preview = get_preview_details(myCustomer)

            mypolicyuser = PolicyUser(customer = myCustomer, policy = policy)
            mypolicyuser.save()

            if policy:
            # # Do something with the determined policy
                  return render(request, 'registration/form.html', {'policy': policy, 'myQuote': myQuote, 
                                                                  'mydependants':mydependants, 
                                                                  'mymentaldisease':mymentaldisease, 
                                                                  'myheartdisease':myheartdisease,
                                                                  'mygutdisease': mygutdisease,
                                                                  'mychestdisease': mychestdisease})
            else:
            # # Handle the case where no policy matches the contribution amount
                  messages.error(request, "Failed to get your policy, please try again.")
                              
      
      return render(request, "registration/form.html")

# def add_preview(request):

#       myCustomer = request.user.customer

#       quote_detail = QuotationInfo.objects.filter(customer=myCustomer)
#       dependants_detail = Dependants.objects.filter(customer=myCustomer)
#       chestdisease_detail = ChestDisease.objects.filter(customer=myCustomer)
#       mentaldisease_detail = MentalDiseases.objects.filter(customer=myCustomer)
#       heartdisease_detail = HeartDisease.objects.filter(customer=myCustomer)
#       gutdisease_detail = GutDisease.objects.filter(customer=myCustomer)
               
#       # context = {
#       #       'quote_detail': quote_detail,
#       #       'dependants_detail': dependants_detail,
#       #       'chestdisease_detail': chestdisease_detail,
#       #       'mentaldisease_detail': mentaldisease_detail,
#       #       'heartdisease_detail': heartdisease_detail,
#       #       'gutdisease_detail' : gutdisease_detail,
#       # }


#       return render(request, "registration/form_preview.html", {'quote_detail': quote_detail,
#             'dependants_detail': dependants_detail,
#             'chestdisease_detail': chestdisease_detail,
#             'mentaldisease_detail': mentaldisease_detail,
#             'heartdisease_detail': heartdisease_detail,
#             'gutdisease_detail' : gutdisease_detail,})


# # class QuoteFormPreview(FormPreview):
# #       form_template = 'registration/form.html'


# #       def done(self, request, cleaned_data):
# #           QuotationInfo.objects.create(**cleaned_data)
# #           return HttpResponse('Form submitted')