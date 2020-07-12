from django.contrib import admin
from .models import Lead, Selection, CallDetailRecord, Phonebook

admin.site.register(Lead)
admin.site.register(Selection)
admin.site.register(CallDetailRecord)
admin.site.register(Phonebook)
