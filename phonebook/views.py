import csv
import random
from django.shortcuts import render
from .models import Phonebook, Lead, Selection, CallDetailRecord

def index(request):
    
    # if CDR is empty, create phonebook and leads
    cdr_data = CallDetailRecord.objects.all()

    # temp manual upload phonebook
    upload = input("Upload Phonebook: ")
    
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
                    # create lead
                    lead = Lead()
                    lead.contact_name = row[name_index]
                    lead.contact_number = row[number_index]
                    lead.age = row[age_index]
                    lead.phonebook = phonebook
                    lead.save()
                    
                    # create selection 
                    mock_desription = ['Yes', 'No', 'Maybe', 'Call Me Later', 'Do Not Call']
                    selection = Selection()
                    selection.key = random.randrange(0, 5)
                    selection.description = mock_desription[selection.key]
                    selection.save()

                    # simulate CDR creation
                    record = CallDetailRecord()
                    record.lead = lead
                    record.selection = selection
                    record.save()
                    
        context = {
            'records': CallDetailRecord.objects.all()
        }
                    
        return render(request, 'phonebook/index.htm', context)
    
    elif len(cdr_data) > 0:
        # temp store phonebook numbers
        phonebook_numbers = dict()
        
        # extract numbers from phonebook
        with open(f'static/phonebooks/{upload}') as inFile:
            reader = csv.reader(inFile)
            
            line_count = 0
            for row in reader:
                if line_count == 0:
                    file_headers = [title.strip().lower() for title in row if len(title) > 0]
                    number_index = file_headers.index('contact number')                 
                    line_count += 1
                else:
                    # add number to storage
                    phonebook_numbers[row[number_index]] = phonebook_numbers.setdefault(row[number_index], row)
                    
        for record in cdr_data:
            for number in phonebook_numbers:
                # skip duplicates
                if number == record.lead.contact_number:
                    # continue
                    print("\n",number, '|', record.lead.contact_number,'\n')
                
                    
        return render(request, 'phonebook/index.htm')
      
    else:    
        context = {
            'records': CallDetailRecord.objects.all()
        }    
            
        return render(request, 'phonebook/index.htm', context)