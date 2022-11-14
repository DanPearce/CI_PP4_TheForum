"""
Models for the contact app Structure
"""
from django.db import models


class Contact(models.Model):
    """
    This class is used to define the model parameters for the contact app,
    this will be used in the Contact Us Page / Form
    """
    first_name = models.CharField(
        max_length=50
        )
    last_name = models.CharField(
        max_length=50
        )
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(
        auto_now_add=True
        )

    def __str__(self):
        """
        Function to return some values as a string.
        """
        return f'{self.first_name} has left a message: {self.body}'
