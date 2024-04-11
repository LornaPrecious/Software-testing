from django.test import TestCase, Client
from django.contrib.auth.models import User
from useraccounts.models import Customer
from .models import QuotationInfo

from django.urls import reverse


class QuotationInfoModelTestCase(TestCase): #TESTS DONE TO THE QUOTATIONINFOR MODEL
    def setUp(self):
        #Creation of a test user (testuser) using create_user method from Django's User model.
        self.user = User.objects.create_user(username='testuser', password='password123')
        #Creation of a test customer (John Doe) associated with the test user, utilizing the Customer model.
        self.customer = Customer.objects.create(
            user=self.user,
            customer_id=1,
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        #Creation of a test quotation info (quotation_info) associated with the test customer, utilizing the QuotationInfo model.
        self.quotation_info = QuotationInfo.objects.create(
            customer=self.customer,
            nationalid='1234567890',
            dob='1980-01-01',
            phone_number='0712345678',
            gender='Male',
            occupation='Engineer',
            contribution_amount='1000'
        )

    def test_quotation_info_str_method(self):
        #Tests the __str__ method of the QuotationInfo model.
        self.assertEqual(str(self.quotation_info), str(self.quotation_info.quotecode))

    def test_quotation_info_fields(self):
        #Tests various fields of the QuotationInfo model.
        self.assertEqual(self.quotation_info.customer, self.customer)
        self.assertEqual(self.quotation_info.nationalid, '1234567890')
        self.assertEqual(self.quotation_info.dob, '1980-01-01')
        self.assertIsNotNone(self.quotation_info.date)
        self.assertEqual(self.quotation_info.phone_number, '0712345678')
        self.assertEqual(self.quotation_info.gender, 'Male')
        self.assertEqual(self.quotation_info.occupation, 'Engineer')
        self.assertEqual(self.quotation_info.contribution_amount, '1000')

    def test_quotation_info_db_table(self):
        #Tests the custom database table name for the QuotationInfo model.
        self.assertEqual(QuotationInfo._meta.db_table, 'quotationTable')

    def test_quotation_info_instance(self):
        self.assertIsInstance(self.quotation_info, QuotationInfo)

    def test_quotation_info_blank_fields(self):
        #Tests the handling of blank fields in the QuotationInfo model.
        quotation_info = QuotationInfo.objects.create(quotecode=2)
        self.assertIsNone(quotation_info.nationalid)
        self.assertIsNone(quotation_info.dob)
        self.assertIsNone(quotation_info.phone_number)
        self.assertIsNone(quotation_info.occupation)
        self.assertIsNone(quotation_info.contribution_amount)



class ViewsTestCase(TestCase): #TESTS THE REGISTER AND LOGIN VIEWS 
    def setUp(self):
        #Client is used to simulate HTTP requests
        self.client = Client()

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

        # Test POST request to register a new user
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'password123',
            'pass2': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to login page after successful registration

    def test_custom_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # Test login with correct credentials
        user = User.objects.create_user(username='testuser', password='password123')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)  # Assuming login fails and redirects back to login page


class ModalTestCase(TestCase): #UI TESTS FOR THE MODAL DISPLAY OF USER INFORMATION 
    def setUp(self):
        self.client = Client()

    def test_modal_display(self):
        # Create a user for authentication
        user = User.objects.create_user(username='testuser', password='password123')

        # Log the user in
        self.client.login(username='testuser', password='password123')

        # Make a GET request to the form page
        response = self.client.get(reverse('quote'))

        # Check if the response contains the modal content
        self.assertContains(response, '<div id="myModal" class="modal">')

        # Check if the response contains the button that triggers the modal
        self.assertContains(response, '<button id="myBtn"> Preview </a></button>')

        # Check if the response contains the modal content (body)
        self.assertContains(response, '<div class="modal-content">')

        # Check if the response contains the modal content (footer)
        self.assertContains(response, '<div class="modal-footer">')

        # Check if the response contains the JavaScript code for modal functionality
        self.assertContains(response, 'var modal = document.getElementById("myModal");')

        # Check if the response contains the script to handle modal events (opening and closing)
        self.assertContains(response, 'modal.style.display = "block";')
        self.assertContains(response, 'modal.style.display = "none";')
