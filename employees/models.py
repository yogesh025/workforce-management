from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)

# Company model
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Employee model
class Employee(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('not_started', 'Not Started'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees', null=True, 
    blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)
    training_completion_status = models.BooleanField(default=False)
    # New field
    training_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
