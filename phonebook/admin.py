from django.contrib import admin
from .models import Lead, Selection, CallDetailRecord, Phonebook, DoNotCall

admin.site.register(Lead)
admin.site.register(Selection)
admin.site.register(CallDetailRecord)
admin.site.register(Phonebook)
admin.site.register(DoNotCall)
