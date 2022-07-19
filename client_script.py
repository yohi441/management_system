import csv
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from management_system.models import Client



with open('MOCK_DATA.csv', mode='r') as file:
    csvfile = csv.reader(file)
    next(csvfile)
    
    for i, lines in enumerate(csvfile):
        print(lines[0])
        client = Client.objects.create(first_name=lines[0], middle_name=lines[1],
                                       last_name=lines[2], email_address=lines[3],
                                       address=lines[4], contact_number=lines[5])
        
        if i == 10:
            break
        