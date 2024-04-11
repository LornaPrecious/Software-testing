from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    
    customer_id = models.IntegerField(primary_key= True)
    first_name = models.CharField(max_length= 100, null=True, blank=True)
    last_name = models.CharField(max_length= 100, null=True, blank=True)
    password = models.CharField(max_length= 100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return str(self.customer_id)
    class Meta:
        db_table='customer'


class QuotationInfo(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,  null=True, blank=True)

    quotecode = models.IntegerField(primary_key=True, auto_created=True)
    nationalid = models.CharField(max_length = 10, null=True, blank= True)
    dob = models.CharField(max_length = 200, null=True, blank=True)
    date = models.DateField(auto_now = True, null=True, blank=True)
    phone_number = models.IntegerField(help_text='0712345678 or +254712345678', null=True, blank=True) #look for a validator, ie. regex 
    gender = models.CharField(max_length=10)
    occupation = models.CharField(max_length = 200, null=True, blank=True)
    contribution_amount = models.CharField(max_length = 100, null=True, blank=True)   
    def __str__(self):
        return str(self.quotecode)
    class Meta:
        db_table='quotationTable'


class Dependants(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    dependants_id = models.IntegerField(default = 0, primary_key= True,  unique=True, auto_created=True)
    full_name = models.CharField(max_length= 100, null=True, blank=True)
    dependants_dob = models.CharField(max_length = 200, null=True, blank=True)
    relationship = models.CharField(max_length = 200, null=True, blank=True)

    def __str__(self):
        return str(self.dependants_id)
    class Meta:
        db_table='dependants'


class Policy(models.Model):
    #customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)

    policy_number = models.CharField(max_length=50, primary_key=True)
    policy_name = models.CharField(max_length = 50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    upper_limit = models.IntegerField(null=True, blank=True) #how much a user contributes
    lower_limit = models.IntegerField(null=True, blank=True) #how much a user contributes
    policy_amount = models.IntegerField(null=True, blank = True) #Pay out from insurance/ policy

    def __str__(self):
        return str(self.policy_number)
    class Meta:
        db_table='policy'

class PolicyUser(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null = True, blank = True)

    
class MentalDiseases(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
  
    disease_code = models.IntegerField(primary_key = True, auto_created=True)
    specific_type = models.CharField(max_length = 250, null=True, blank=True) #specific disease type eg. stage 4 of lung cancer

    def __str__(self):
        return str(self.disease_code)
    class Meta:
        db_table='mental_diseases'


class HeartDisease(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,  null=True, blank=True)
    
    disease_code = models.IntegerField(primary_key = True, auto_created=True)
    specific_type = models.CharField(max_length = 250, null=True, blank=True) #specific disease type eg. stage 4 of lung cancer

    def __str__(self):
        return str(self.disease_code)
    class Meta:
        db_table='heart_disease'


class ChestDisease(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,  null=True, blank=True)
    
    disease_code = models.IntegerField(primary_key = True, auto_created=True)
    specific_type = models.CharField(max_length = 250, null=True, blank=True) #specific disease type eg. stage 4 of lung cancer

    def __str__(self):
        return str(self.disease_code)
    class Meta:
        db_table='chest_disease'


class GutDisease(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,  null=True, blank=True)
    
    disease_code = models.IntegerField(primary_key = True, auto_created=True)
    specific_type = models.CharField(max_length = 250, null=True, blank=True) #specific disease type eg. stage 4 of lung cancer

    def __str__(self):
        return str(self.disease_code)
    class Meta:
        db_table='gut_disease'



class Contact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,  null=True, blank=True)

    fullname = models.CharField(max_length = 200)
    email = models.CharField (max_length = 200)
    contact_message = models.CharField(max_length = 5000)