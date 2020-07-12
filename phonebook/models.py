from django.db import models

class Phonebook(models.Model):
    name = models.CharField(max_length=30)
    csv_file = models.FileField( upload_to='static/phonebooks', max_length=100)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} | created on {self.date}'

class Lead(models.Model):
    contact_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)
    age = models.CharField(max_length=3)
    phonebook = models.ForeignKey(Phonebook, on_delete=models.CASCADE, related_name='leads')
    
    def __str__(self):
        return f'{self.contact_name} | {self.contact_number}'
    
    
    
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
    

