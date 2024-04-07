from django.shortcuts import render
from .models import *
from .my_serializer import DjangoSerializer


# Create your views here.
def my_view(request):
    inst = Model2.objects.all()

    # Normal Serializer
    ds = DjangoSerializer(request)
    data = ds.get_data(inst, fields=['name', 'alternate_email', 'emergency_number', 'blank_text', 'date_of_birth', 'task_deadline'],
                       fk=['models4_id'])
    print('=====================Normal Serializer============================')
    print(data)
    print('==================================================================')

    # Decrypt Data
    ds = DjangoSerializer(request)
    ds.set_decrypt('email', 'mobile_number')
    data = ds.get_data(inst, fields=['email', 'mobile_number'])
    print('=====================Decrypt Data============================')
    print(data)
    print('=============================================================')

    # Custom Date Format
    ds = DjangoSerializer(request)
    ds.set_datetime_format(date_of_joining='%d/%m/%Y', sign_in_time='%H:%M')
    data = ds.get_data(inst, fields=['date_of_joining', 'sign_in_time'])
    print('=====================Custom Date Format============================')
    print(data)
    print('===================================================================')

    # Custom Null Values
    ds = DjangoSerializer(request)
    ds.set_null(blank_number=0)
    data = ds.get_data(inst, fields=['blank_number'])
    print('=====================Custom Null Values============================')
    print(data)
    print('===================================================================')

    # Concat Number with Country Code
    ds = DjangoSerializer(request)
    ds.set_decrypt('mobile_number')
    ds.set_contact_detail(mobile_number='mobile_country_code', alternate_mobile_number='alternate_mobile_country_code')
    data = ds.get_data(inst, fields=['mobile_number', 'alternate_mobile_number'])
    print('=====================Concat Number with Country Code============================')
    print(data)
    print('================================================================================')

    # Annotate Fields or Extra Fields
    ds = DjangoSerializer(request)
    ds.set_func(hello=lambda obj: 'Hello ' + obj.name)
    data = ds.get_data(inst, ann=['hello'])
    print('=====================Annotate Fields or Extra Fields============================')
    print(data)
    print('================================================================================')

    # Nested Serializer
    ds2 = DjangoSerializer(request)
    ds2.fields.extend(['name', 'email'])

    ds = DjangoSerializer(request)
    ds.set_func(model3_id=lambda obj: ds2.get_data(obj))
    data = ds.get_data(inst, m2m=['model3_id'])
    print('=====================Nested Serializer============================')
    print(data)
    print('==================================================================')

    # All in One
    ds2 = DjangoSerializer(request, is_nested=True)
    ds2.fields.extend(['name', 'email'])

    ds = DjangoSerializer(request)
    ds.set_decrypt('email', 'mobile_number')
    ds.set_contact_detail(mobile_number='mobile_country_code', alternate_mobile_number='alternate_mobile_country_code')
    ds.set_null(blank_number=0)
    ds.set_datetime_format(date_of_joining='%d/%m/%Y', sign_in_time='%H:%M')
    ds.set_func(hello=lambda obj: 'Hello ' + obj.name, model3_id=lambda obj: ds2.get_data(obj))
    data = ds.get_data(inst, fields=['name', 'email', 'alternate_email', 'mobile_number', 'alternate_mobile_number', 'emergency_number',
                                     'blank_text', 'blank_number', 'date_of_birth', 'date_of_joining', 'task_deadline',
                                     'sign_in_time'], fk=['models4_id'], m2m=['model3_id'], ann=['hello'])
    print('=====================All in One============================')
    print(data)
    print('===========================================================')
    return render(request, 'index.html', {'data': data})






