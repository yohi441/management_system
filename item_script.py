import csv
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from management_system.models import Item, Category



with open('item_mock_date.csv', mode='r') as file:
    csvfile = csv.reader(file)
    next(csvfile)
    
    for i, lines in enumerate(csvfile):
        print(lines)
        item = Item.objects.create(item=lines[0], serial_number=lines[1],
                                       model=lines[2], appraise_value=lines[3],
                                       item_description=lines[4],
                                       remarks=lines[6])
        item.save()
        category = Category.objects.get(pk=lines[5])
        item.category.add(category)
        
        
        if i == 10:
            break