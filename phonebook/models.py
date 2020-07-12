from django.db import models

class Phonebook(models.Model):
    name = models.CharField(max_length=30)
    leads = models.ManyToManyField(Lead)
    date = models.DateField(auto_now=False, auto_now_add=False)

class Lead(models.Model):
    contact_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)
    age = models.CharField(max_length=3)

class CallDetailRecord(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE) 
    date = models.DateField(auto_now=False, auto_now_add=False)
    
class Selection(models.Model):
    key = models.CharField(max_length=2)
    description = models.CharField(max_length=30)

