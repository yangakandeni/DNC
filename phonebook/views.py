import csv
import re
from django.shortcuts import render
from .models import Phonebook, Lead, Selection, CallDetailRecord

def index(request):
    # tem manual phonebook upload
    upload = input("Upload Phonebook: ")
    
    # if there is no data in the CDR, populate relevant tables
    cdr_data = CallDetailRecord.objects.all()
    if len(cdr_data) <= 0:
        # create phonebook
        phonebook = Phonebook()
        phonebook.name = upload.split('.')[0]
        phonebook.save()
        
        # create lead
        with open(f'static/phonebooks/{upload}') as inFile:
            reader = csv.reader(inFile)
            
            line_count = 0
            for row in reader:
                if line_count == 0:
                    file_headers = [title.strip().lower() for title in row if len(title) > 0]
                    name_index = file_headers.index('contact name')
                    number_index = file_headers.index('contact number')
                    age_index = file_headers.index('age')                    
                    line_count += 1
                else:
                    lead = Lead()
                    lead.contact_name = row[name_index]
                    lead.contact_number = row[number_index]
                    lead.age = row[age_index]
                    lead.phonebook = phonebook
                    lead.save()
                
    context = {
        # 'phonebook': new_phonebook
    }
    
        
    return render(request, 'phonebook/index.htm', context)