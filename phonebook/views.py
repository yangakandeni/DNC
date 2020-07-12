import csv
import random
from django.shortcuts import render
from .models import Phonebook, Lead, Selection, CallDetailRecord, DoNotCall

def index(request):
    
    # if CDR is empty, create phonebook and leads
    records = CallDetailRecord.objects.all()

    # temp manual upload phonebook
    upload = input("\nUpload Phonebook: \n")
    
    # instantiate phonebook
    phonebook = Phonebook()
    phonebook.name = upload.split('.')[0]
    
    if len(records) <= 0:
        # save phonebook to database
        phonebook.save()
        
        # save leads to database
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
                    
                    # create mock selection 
                    mock_desription = ['Yes', 'No', 'Maybe', 'Call Me Later', 'Do Not Call']
                    selection = Selection()
                    selection.key = random.randrange(0, 5)
                    selection.description = mock_desription[selection.key]
                    selection.save()

                    # create mock CDR
                    record = CallDetailRecord()
                    record.lead = lead
                    record.selection = selection
                    record.save()
                    
        # parse mock CDR into template
        context = {
            'records': CallDetailRecord.objects.all()
        }
                    
        return render(request, 'phonebook/index.htm', context)
    
    elif len(records) > 0:
        # temp store phonebook numbers and relative data
        phonebook_numbers = dict()
        
        # extract numbers from phonebook
        with open(f'static/phonebooks/{upload}') as inFile:
            reader = csv.reader(inFile)
            
            line_count = 0
            for row in reader:
                if line_count == 0:
                    file_headers = [title.strip().lower() for title in row if len(title) > 0]
                    number_index = file_headers.index('contact number')
                    name_index = file_headers.index('contact name')
                    age_index = file_headers.index('age')               
                    line_count += 1
                else:
                    # add number to and relative data to storage
                    phonebook_numbers[row[number_index]] = phonebook_numbers.setdefault(row[number_index], {'name': row[name_index], 'age': row[age_index]})
                    
        # check for duplicates   
        for number in phonebook_numbers:
            for record in records:
                # skip duplicates
                if number == record.lead.contact_number:
                    # save lead to DNC table if selection key same as DNC key
                    if record.selection.key == '4':
                        dnc_lead = DoNotCall()
                        # add to DNC table if not exist
                        dnc_lead.lead = record.lead
                        dnc_lead.save()
                else:
                    # save phonebook to db
                    phonebook.save()
                    
                    # save unique leads
                    lead = Lead()
                    lead.contact_name = phonebook_numbers[number].get('name')
                    lead.contact_number = number
                    lead.age = phonebook_numbers[number].get('age')
                    lead.phonebook = phonebook
                    lead.save()
                    
            # create mock selection 
            mock_desription = ['Yes', 'No', 'Maybe', 'Call Me Later', 'Do Not Call']
            selection = Selection()
            selection.key = random.randrange(0, 5)
            selection.description = mock_desription[selection.key]
            selection.save()

            # create mock CDR
            record = CallDetailRecord()
            record.lead = lead
            record.selection = selection
            record.save()
                                   
        # parse mock CDR into template
        context = {
            'records': CallDetailRecord.objects.all()
        }
        
        return render(request, 'phonebook/index.htm', context)
      
    else:   
        return render(request, 'phonebook/index.htm')