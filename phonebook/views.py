import csv
from django.shortcuts import render
from .models import Phonebook, Lead, Selection, CallDetailRecord

def index(request):
    # if there is no data in the CDR, populate relevant tables
    cdr_data = CallDetailRecord.objects.all()
    if len(cdr_data) <= 0:
        # with open('phonebooks/phonebook1.csv') as inFile:
        #     reader = csv.reader(inFile, delimeter=',')
        #     for row in reader:
        #         print(row)
        pass
        
    return render(request, 'phonebook/index.htm')