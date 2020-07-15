import csv
import random
from django.shortcuts import render
from .models import Phonebook, Lead, Selection, CallDetailRecord, DoNotCall

def index(request):
    
    # upload phonebook
    # csv_file = 'phonebook1.csv'
    csv_file = upload_phonebook()

    # get all records in the CDR and covert to dict
    cdr_dict = convert_to_dict(model=CallDetailRecord)

    if len(cdr_dict) <= 0:
        # generate leads using phonebook data
        create_lead(csv_file)

        # simulate CDR
        simulate_cdr()
        
        # update DNCs
        update_dnc()   
           
    else:       
        # get all records in the DNC and covert to dict 
        dnc_dict = convert_to_dict(model=DoNotCall)
        
        # convert phonebook data to dict
        phonebook_dict = convert_to_dict(csvfilepath=f'static/phonebooks/{csv_file}', contact_name='contact name', contact_number='contact number', age='age')
        
        for num in phonebook_dict:
            if not num in dnc_dict:
                # create lead 
                create_lead(csvfile=csv_file,_dict=phonebook_dict, key=num, subkey_age='age', subkey_contact_name='name', subkey_contact_number='number', type='dict')
                
                # update DNCs
                update_dnc()
            else:
                continue

    # parse mock CDR into template
    context = {
        'records': CallDetailRecord.objects.all()
    }
                
    return render(request, 'phonebook/index.htm', context)
    
def convert_to_dict(model=None, csvfilepath=None, contact_name=None, contact_number=None, age=None):

    # dict storage
    dict_storage = dict()

    if not csvfilepath is None:
        csvfile = csvfilepath.split('/')[-1]

        # convert phonebook entries to dictionary
        with open(f'static/phonebooks/{csvfile}') as inFile:
            reader = csv.reader(inFile)
            
            line_count = 0
            for row in reader:
                if line_count == 0:
                    file_headers = [title.strip().lower() for title in row if len(title) > 0]
                    number_index = file_headers.index(contact_number)
                    name_index = file_headers.index(contact_number)
                    age_index = file_headers.index(age)               
                    line_count += 1
                else:
                    # add number to and relative data to storage
                    dict_storage[row[number_index]] = dict_storage.setdefault(row[number_index], {'number': row[number_index], 'name': row[name_index], 'age': row[age_index]})
    
    else:
        # convert CDR entries to dictionary
        for record in model.objects.all():
            if model is CallDetailRecord:
                dict_storage[record.lead.contact_number] = dict_storage.setdefault(record.lead.contact_number, {
                    'name': record.lead.contact_name,
                    'age' : record.lead.age,
                    'selection': record.selection.key
                })
            elif model is DoNotCall:
                dict_storage[record.lead.contact_number] = dict_storage.setdefault(record.lead.contact_number, {
                    'name': record.lead.contact_name,
                    'age' : record.lead.age
                })

    return dict_storage

def create_lead(csvfile=None, _dict=None, key=None, subkey_age=None, subkey_contact_name=None, subkey_contact_number=None, type='csv'):

    # make instance of Phonebook
    phonebook = Phonebook()
    phonebook.name = csvfile.split('.')[0]
    phonebook.save()

    # Create new lead FROM CSVFILE
    if type is 'csv':
        with open(f'static/phonebooks/{csvfile}') as inFile:
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
    else:
        # create new lead FROM DICTIONARY
        lead = Lead()
        lead.age = _dict[key].get(subkey_age)
        lead.contact_name = _dict[key].get(subkey_contact_name)
        lead.contact_number = _dict[key].get(subkey_contact_number)
        lead.phonebook = phonebook
        lead.save()
        
        simulate_cdr(type='dict', alead=lead)
        
    return None

def upload_phonebook():

    try:
        phonebook  = input("Upload phonebook: ")
        return phonebook
    except:
        if not phonebook.split('.')[1] is 'csv':
            return 'Wrong Format'

def simulate_cdr(type='csv', alead=None):

    # create mock selection 
    mock_desription = ['Yes', 'No', 'Maybe', 'Call Me Later', 'Do Not Call']

    # create mock CDR FROM CSV FILE
    if type == 'csv':
        for lead in Lead.objects.all():

            selection = Selection()
            selection.key = random.randrange(0, 5)
            selection.description = mock_desription[selection.key]
            selection.save()

            record = CallDetailRecord()
            record.lead = lead
            record.selection = selection
            record.save()
    else:
        selection = Selection()
        selection.key = random.randrange(0, 5)
        selection.description = mock_desription[selection.key]
        selection.save()

        record = CallDetailRecord()
        record.lead = alead
        record.selection = selection
        record.save()   
            
    return None

def update_dnc(dnc_key='4'):
    
    # retrieve all cdr leads with selection key matching dnc key
    cdr_records = CallDetailRecord.objects.filter(selection__key=dnc_key)
    
    # convert DNC records into dict
    dnc_dict = convert_to_dict(DoNotCall)
    
    for record in cdr_records:
        if not record.lead.contact_number in dnc_dict:
            dnc_list = DoNotCall()
            dnc_list.lead = record.lead
            dnc_list.save()
        
    return None
