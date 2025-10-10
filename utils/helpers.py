import random
import string
from datetime import datetime

class TestDataGenerator:
    """Utility class to generate test data for employee forms"""
    
    FIRST_NAMES = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 'James', 'Maria']
    LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    @staticmethod
    def generate_employee_id():
        """Generate a random employee ID"""
        return f"EMP{random.randint(1000, 9999)}"
    
    @staticmethod
    def generate_first_name():
        """Generate a random first name"""
        return random.choice(TestDataGenerator.FIRST_NAMES)
    
    @staticmethod
    def generate_last_name():
        """Generate a random last name"""
        return random.choice(TestDataGenerator.LAST_NAMES)
    
    @staticmethod
    def generate_username():
        """Generate a random username"""
        timestamp = str(int(datetime.now().timestamp()))[-4:]
        username = ''.join(random.choices(string.ascii_lowercase, k=4))
        return f"user_{username}{timestamp}"
    
    @staticmethod
    def generate_password():
        """Generate a random password"""
        return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=12))
    
    @staticmethod
    def generate_random_string(length):
        """Generate a random string of specified length"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def generate_employee_data(self):
        """Generate complete employee data"""
        first_name = self.generate_first_name()
        last_name = self.generate_last_name()
        return {
            'employee_id': self.generate_employee_id(),
            'first_name': first_name,
            'last_name': last_name,
            'username': f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}",
            'password': self.generate_password()
        }
