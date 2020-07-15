from django.contrib import admin
from .models import Lead, Selection, CallDetailRecord, Phonebook, DoNotCall

class LeadInLine(admin.StackedInline):
    model = Lead
    extra = 1

class PhonebookAdmin(admin.ModelAdmin):
    inlines = [LeadInLine]
    
admin.site.register(Lead)
admin.site.register(Selection)
admin.site.register(CallDetailRecord)
admin.site.register(Phonebook, PhonebookAdmin)
admin.site.register(DoNotCall)
