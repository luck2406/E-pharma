from django.contrib import admin
from .models import medicines,invoice,bill,profile,backup
# Register your models here.

admin.site.register(medicines)
admin.site.register(invoice)
admin.site.register(bill)
admin.site.register(profile)
admin.site.register(backup)