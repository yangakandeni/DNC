import csv
import random
from django.shortcuts import render
from .models import Phonebook, Lead, Selection, CallDetailRecord, DoNotCall
from django.http import HttpResponse
import json

def index(request):
    
    # upload phonebook
    # csv_file = upload_phonebook()
    csv_file = 'phonebook1.csv'

    # get all records in the CDR and covert to dict
    cdr_records = convert_to_dict()

    if len(cdr_records) <= 0:
        # generate leads using phonebook data
        create_leads(csv_file)

        # simulate CDR
        simulate_cdr()
    else:       
        # update DNCs 
        update_dnc('3')
        
        # convert phonebook data to dict
        phonebook_dict = convert_to_dict(csvfilepath=f'static/phonebooks/{csv_file}', contact_name='contact name', contact_number='contact number', age='age')
        
        # for num in phonebook_dict:
        #     if num in cdr_records:
        #         if cdr_records[num] == '3':
        #             # save to DNC table
        #             dnc = DoNotCall()
        #             dnc.lead = Lead.objects.filter(contact_number='3')
        #             dnc.save()
                    
        #         else:
        #             print(f'\n{num}')
        
        return HttpResponse(json.dumps(cdr_records))

    # parse mock CDR into template
    context = {
        'records': CallDetailRecord.objects.all()
    }
                
    return render(request, 'phonebook/index.htm', context)
    
    # # temp manual upload phonebook
    # upload = input("\nUpload Phonebook: \n")

    # # if CDR is empty, create phonebook and leads
    # records = CallDetailRecord.objects.all()
    
    # # instantiate phonebook
    # phonebook = Phonebook()
    # phonebook.name = upload.split('.')[0]
    
    # # save phonebook to database
    # phonebook.save()

    
    # if len(records) <= 0:
    #     print('\nGenerating CDR ...\n')
        
    #     # save leads to database
    #     with open(f'static/phonebooks/{upload}') as inFile:
    #         reader = csv.reader(inFile)
            
    #         line_count = 0
    #         for row in reader:
    #             if line_count == 0:
    #                 file_headers = [title.strip().lower() for title in row if len(title) > 0]
    #                 name_index = file_headers.index('contact name')
    #                 number_index = file_headers.index('contact number')
    #                 age_index = file_headers.index('age')                    
    #                 line_count += 1
    #             else:
    #                 # create lead
    #                 lead = Lead()
    #                 lead.contact_name = row[name_index]
    #                 lead.contact_number = row[number_index]
    #                 lead.age = row[age_index]
    #                 lead.phonebook = phonebook
    #                 lead.save()

    #         # create mock selection 
    #         mock_desription = ['Yes', 'No', 'Maybe', 'Call Me Later', 'Do Not Call']

    #         # create mock CDR
    #         for lead in Lead.objects.all():

    #             selection = Selection()
    #             selection.key = random.randrange(0, 5)
    #             selection.description = mock_desription[selection.key]
    #             selection.save()

    #             record = CallDetailRecord()
    #             record.lead = lead
    #             record.selection = selection
    #             record.save()
                    
    #     # parse mock CDR into template
    #     context = {
    #         'records': CallDetailRecord.objects.all()
    #     }
                    
    #     return render(request, 'phonebook/index.htm', context)
    
    # else:
    #     # print('\ntheres content\n')

    #     # temp store phonebook numbers and relative data
    #     phonebook_dict = dict()

    #     # extract numbers from phonebook
    #     with open(f'static/phonebooks/{upload}') as inFile:
    #         reader = csv.reader(inFile)
            
    #         line_count = 0
    #         for row in reader:
    #             if line_count == 0:
    #                 file_headers = [title.strip().lower() for title in row if len(title) > 0]
    #                 number_index = file_headers.index('contact number')
    #                 name_index = file_headers.index('contact name')
    #                 age_index = file_headers.index('age')               
    #                 line_count += 1
    #             else:
    #                 # add number to and relative data to storage
    #                 phonebook_dict[row[number_index]] = phonebook_dict.setdefault(row[number_index], {'number': row[number_index], 'name': row[name_index], 'age': row[age_index]})


    #     for record in records:
    #         if record.lead.contact_number in phonebook_dict:
    #             if record.selection.key == '4':
    #                 # print(record.lead.contact_number, record.selection.key)

    #                 # add to DNC table
    #                 DNC = DoNotCall()
    #                 DNC.lead = record.lead
    #                 print('\nUpdating DNC...', DNC.lead.contact_number, '\n')
    #                 DNC.save()

    #                 # remove from phonebook
    #                 phonebook_dict.pop(record.lead.contact_number)
    #             else:
    #                 # Update existing lead
    #                 record.lead.contact_name = phonebook_dict[record.lead.contact_number].get("name")
    #                 record.lead.contact_number = phonebook_dict[record.lead.contact_number].get("number")
    #                 record.lead.age = phonebook_dict[record.lead.contact_number].get("age")
    #                 record.lead.phonebook = phonebook
    #                 # lead.save()

    #                 print('\nUpdating record...', record.lead.contact_number, record.selection.key,'\n')
                    
    #                 # create mock selection 
    #                 mock_desription = ['Yes', 'No', 'Maybe', 'Call Me Later', 'Do Not Call']
    #                 selection = Selection()
    #                 selection.key = random.randrange(0, 5)
    #                 selection.description = mock_desription[selection.key]
    #                 selection.save()

    #                 # create mock CDR
    #                 CDR = CallDetailRecord()
    #                 CDR.lead = record.lead
    #                 CDR.selection = selection
    #                 CDR.save()
    #                 pass

    #     context = {
    #         'records': CallDetailRecord.objects.all()
    #     }
                    
    #     return render(request, 'phonebook/index.htm', context)

    #     #     if record.lead.contact_number in phonebook_dict:
    #     #         if record.selection.key == '4':

    #     #             # add to DNC table
    #     #             lead = Lead()
    #     #             lead.contact_name = phonebook_dict[record.lead.contact_number].get("name")
    #     #             lead.contact_number = phonebook_dict[record.lead.contact_number].get("number")
    #     #             lead.age = phonebook_dict[record.lead.contact_number].get("age")
    #     #             lead.phonebook = phonebook
    #     #             lead.save()

    #     #             DNC = DoNotCall()
    #     #             DNC.lead = lead
    #     #             print('\nUpdating DNC...', DNC.lead.contact_number, '\n')
    #     #             DNC.save()

    #     #         else:
    #     #             for dnc in DoNotCall.objects.all():
    #     #                 if not record.lead.contact_number == dnc.lead.contact_number:
    #     #                     print(f'\nSKIP: dnc lead number {dnc.lead.contact_number}\n')
    #     #                     continue

    #     #                 # Update existing lead
    #     #                 lead = Lead()
    #     #                 lead.contact_name = phonebook_dict[record.lead.contact_number].get("name")
    #     #                 lead.contact_number = phonebook_dict[record.lead.contact_number].get("number")
    #     #                 lead.age = phonebook_dict[record.lead.contact_number].get("age")
    #     #                 lead.phonebook = phonebook
    #     #                 lead.save()

    #     #                 print('\nUpdating record...', record.lead.contact_number, record.selection.key,'\n')
                        
    #     #                 # create mock selection 
    #     #                 mock_desription = ['Yes', 'No', 'Maybe', 'Call Me Later', 'Do Not Call']
    #     #                 selection = Selection()
    #     #                 selection.key = random.randrange(0, 5)
    #     #                 selection.description = mock_desription[selection.key]
    #     #                 selection.save()

    #     #                 # create mock CDR
    #     #                 record = CallDetailRecord()
    #     #                 record.lead = lead
    #     #                 record.selection = selection
    #     #                 record.save()

    #     #         # context = {
    #     #         #     'records': CallDetailRecord.objects.all()
    #     #         # }
                            
    #     #         # return render(request, 'phonebook/index.htm', context)

    #     #     else:
    #     #         # if record.selection.key == '4':
    #     #         #     continue

    #     #         print('\nCreating new record...', record.lead.contact_number, record.selection.key,'\n')
                
    #     #         # Create new lead
    #     #         with open(f'static/phonebooks/{upload}') as inFile:
    #     #             reader = csv.reader(inFile)
                
    #     #             line_count = 0
    #     #             for row in reader:
    #     #                 if line_count == 0:
    #     #                     file_headers = [title.strip().lower() for title in row if len(title) > 0]
    #     #                     name_index = file_headers.index('contact name')
    #     #                     number_index = file_headers.index('contact number')
    #     #                     age_index = file_headers.index('age')                    
    #     #                     line_count += 1
    #     #                 else:
    #     #                     # create lead
    #     #                     lead = Lead()
    #     #                     lead.contact_name = row[name_index]
    #     #                     lead.contact_number = row[number_index]
    #     #                     lead.age = row[age_index]
    #     #                     lead.phonebook = phonebook
    #     #                     lead.save()


    #     # context = {
    #     #     'records': CallDetailRecord.objects.all()
    #     # }
                    
    #     # return render(request, 'phonebook/index.htm', context)

    # #     # temp store phonebook numbers and relative data
    # #     phonebook_dict = dict()

    # #     # retrieve and save CDR data to dict
    # #     CDR_dict = dict()
    # #     for record in records:
    # #         CDR_dict[record.lead.contact_number] = CDR_dict.setdefault(record.lead.contact_number, record.selection.key)
        
    # #     # extract numbers from phonebook
    # #     with open(f'static/phonebooks/{upload}') as inFile:
    # #         reader = csv.reader(inFile)
            
    # #         line_count = 0
    # #         for row in reader:
    # #             if line_count == 0:
    # #                 file_headers = [title.strip().lower() for title in row if len(title) > 0]
    # #                 number_index = file_headers.index('contact number')
    # #                 name_index = file_headers.index('contact name')
    # #                 age_index = file_headers.index('age')               
    # #                 line_count += 1
    # #             else:
    # #                 # add number to and relative data to storage
    # #                 phonebook_dict[row[number_index]] = phonebook_dict.setdefault(row[number_index], {'number': row[number_index], 'name': row[name_index], 'age': row[age_index]})
        
    #     # print('\n phonebook dict', phonebook_dict, '\n')
    #     # print('\n CDR dict', CDR_dict, '\n')
        
    #     # DNC_list = list()
    #     # for num in phonebook_dict:
    #     #     # if num in DNC_list:
    #     #     #     # print('\nAdd NOT to db', phonebook_dict[record.lead.contact_number].get("number"))
                
    #     #     #     # print(DNC_list, '\n')
                
    #     #     if num in records:
    #     #         # if CDR_dict[num] == '4':
    #     #         print(f'\nNo add to db', num)
                    
    #                 # DNC_list.append(num)
    #                 # print(DNC_list, '\n')
                    
    #             # else:
    #             #     print('\nAdd to db', num)

    #             #     # create lead
    #             #     lead = Lead()
    #             #     lead.contact_name = phonebook_dict[num].get("name")
    #             #     lead.contact_number = phonebook_dict[num].get("number")
    #             #     lead.age = phonebook_dict[num].get("age")
    #             #     lead.phonebook = phonebook
    #             #     lead.save()
                
    #         # create mock selection 
    #         # mock_desription = ['Yes', 'No', 'Maybe', 'Call Me Later', 'Do Not Call']
    #         # selection = Selection()
    #         # selection.key = random.randrange(0, 5)
    #         # selection.description = mock_desription[selection.key]
    #         # selection.save()

    #         # # create mock CDR
    #         # record = CallDetailRecord()
    #         # record.lead = lead
    #         # record.selection = selection
    #         # record.save()
                
                
                
    #         # else:
    #         #     print('\nAdd to db', num)
                
    #         #     # print('add to db', phonebook_dict[record.lead.contact_number].get("number"), record.selection.key) 
    #         #     # create lead
    #         #     lead = Lead()
    #         #     lead.contact_name = phonebook_dict[num].get("name")
    #         #     lead.contact_number = num
    #         #     lead.age = phonebook_dict[num].get("age")
    #         #     lead.phonebook = phonebook
    #         #     lead.save()
    #     # parse mock CDR into template
    # #     context = {
    # #         'records': CallDetailRecord.objects.all()
    # #     }
        
    # #     return render(request, 'phonebook/index.htm', context)
      
    # # else:   
    # #     return render(request, 'phonebook/index.htm')


def convert_to_dict(csvfilepath=None, contact_name=None, contact_number=None, age=None):

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
        for record in CallDetailRecord.objects.all():
            dict_storage[record.lead.contact_number] = dict_storage.setdefault(record.lead.contact_number, {
                'name': record.lead.contact_name,
                'age' : record.lead.age,
                'selection': record.selection.key
            })


    return dict_storage

# print(convert_to_dict(csvfilepath='static/phonebooks/phonebook1.csv', contact_name='contact name', contact_number='contact number', age='age'))

def create_leads(csvfile):

    # make instance of Phonebook
    phonebook = Phonebook()
    phonebook.name = csvfile.split('.')[0]
    phonebook.save()

    # Create new lead
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

    return None

def upload_phonebook():

    try:
        phonebook  = input("Upload phonebook: ")
        return phonebook
    except:
        if not phonebook.split('.')[1] is 'csv':
            return 'Wrong Format'

def simulate_cdr():

    # create mock selection 
    mock_desription = ['Yes', 'No', 'Maybe', 'Call Me Later', 'Do Not Call']

    # create mock CDR
    for lead in Lead.objects.all():

        selection = Selection()
        selection.key = random.randrange(0, 5)
        selection.description = mock_desription[selection.key]
        selection.save()

        record = CallDetailRecord()
        record.lead = lead
        record.selection = selection
        record.save()
            
    return None

def update_dnc(dnc_key):
    
    dnc_records = CallDetailRecord.objects.filter(selection__key=dnc_key)
    
    for record in dnc_records:
        dnc_list = DoNotCall()
        dnc_list.lead = record.lead
        dnc_list.save()
        
    return None
