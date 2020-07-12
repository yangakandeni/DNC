from django.db import models

class Lead(models.Model):
    contact_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)
    age = models.CharField(max_length=3)
    
    def __str__(self):
        return f'{self.contact_name} | {self.contact_number}'
    

class Phonebook(models.Model):
    name = models.CharField(max_length=30)
    leads = models.ManyToManyField(Lead)
    csv_file = models.FileField( upload_to=None, max_length=100)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class Selection(models.Model):
    key = models.CharField(max_length=2)
    description = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.key} | {self.description}'
    

class CallDetailRecord(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE) 
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.date} | {self.lead.contact_name} | {self.lead.contact_number} | {self.selection.key}'
    

