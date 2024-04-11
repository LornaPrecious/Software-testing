from django.test import TestCase
from django.contrib.auth.models import User

from useraccounts.models import Customer

class CustomerModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create a test customer
        self.customer = Customer.objects.create(
            user=self.user,
            customer_id=1,
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )

    def test_customer_str_method(self):
        """Test the __str__ method of Customer model"""
        self.assertEqual(str(self.customer), '1')  # Since __str__ returns customer_id

    def test_customer_fields(self):
        """Test the fields of Customer model"""
        self.assertEqual(self.customer.user, self.user)
        self.assertEqual(self.customer.customer_id, 1)
        self.assertEqual(self.customer.first_name, 'John')
        self.assertEqual(self.customer.last_name, 'Doe')
        self.assertEqual(self.customer.email, 'john@example.com')

    def test_customer_db_table(self):
        """Test the custom database table name"""
        self.assertEqual(Customer._meta.db_table, 'customer')

    def test_customer_instance(self):
        """Test instance creation"""
        self.assertIsInstance(self.customer, Customer)

    def test_customer_primary_key(self):
        """Test primary key"""
        self.assertTrue(self.customer.customer_id)

    def test_customer_blank_fields(self):
        """Test blank fields"""
        customer = Customer.objects.create(customer_id=2)  # Creating with required field only
        self.assertEqual(customer.first_name, None)
        self.assertEqual(customer.last_name, None)
        self.assertEqual(customer.email, None)

    def test_customer_null_fields(self):
        """Test null fields"""
        self.assertIsNone(self.customer.password)  # Password is nullable

    def test_customer_user_cascade_delete(self):
        """Test cascade delete of associated user"""
        user_id = self.user.id
        self.customer.delete()
        self.assertFalse(User.objects.filter(id=user_id).exists())

    def test_customer_str_with_null_customer_id(self):
        """Test __str__ method with null customer_id"""
        customer = Customer.objects.create(user=self.user)
        self.assertEqual(str(customer), 'None')  # __str__ returns 'None' if customer_id is None
