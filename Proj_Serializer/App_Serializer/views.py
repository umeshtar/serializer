from django.shortcuts import render
from .models import *
from .my_serializer import TechnoSerializer, EncryptData


# Create your views here.
def my_view(request):
    inst = Model2.objects.all()

    # Normal Serializer
    ts = TechnoSerializer(request)
    data = ts.get_data(inst, fields=['name', 'alternate_email', 'emergency_number', 'blank_text', 'date_of_birth', 'task_deadline'],
                       fk=['models4_id'])
    print('=====================Normal Serializer============================')
    print(data)
    print('==================================================================')

    # Decrypt Data
    ts = TechnoSerializer(request)
    ts.set_decrypt('email', 'mobile_number')
    data = ts.get_data(inst, fields=['email', 'mobile_number'])
    print('=====================Decrypt Data============================')
    print(data)
    print('=============================================================')

    # Custom Date Format
    ts = TechnoSerializer(request)
    ts.set_datetime_format(date_of_joining='%d/%m/%Y', sign_in_time='%H:%M')
    data = ts.get_data(inst, fields=['date_of_joining', 'sign_in_time'])
    print('=====================Custom Date Format============================')
    print(data)
    print('===================================================================')

    # Custom Null Values
    ts = TechnoSerializer(request)
    ts.set_null(blank_number=0)
    data = ts.get_data(inst, fields=['blank_number'])
    print('=====================Custom Null Values============================')
    print(data)
    print('===================================================================')

    # Concat Number with Country Code
    ts = TechnoSerializer(request)
    ts.set_decrypt('mobile_number')
    ts.set_contact_detail(mobile_number='mobile_country_code', alternate_mobile_number='alternate_mobile_country_code')
    data = ts.get_data(inst, fields=['mobile_number', 'alternate_mobile_number'])
    print('=====================Concat Number with Country Code============================')
    print(data)
    print('================================================================================')

    # Annotate Fields or Extra Fields
    ts = TechnoSerializer(request)
    ts.set_func(hello=lambda obj: 'Hello ' + obj.name)
    data = ts.get_data(inst, ann=['hello'])
    print('=====================Annotate Fields or Extra Fields============================')
    print(data)
    print('================================================================================')

    # Nested Serializer
    ts2 = TechnoSerializer(request)
    ts2.fields.extend(['name', 'email'])

    ts = TechnoSerializer(request)
    ts.set_func(model3_id=lambda obj: ts2.get_data(obj))
    data = ts.get_data(inst, m2m=['model3_id'])
    print('=====================Nested Serializer============================')
    print(data)
    print('==================================================================')

    # All in One
    ts2 = TechnoSerializer(request, is_nested=True)
    ts2.fields.extend(['name', 'email'])

    ts = TechnoSerializer(request)
    ts.set_decrypt('email', 'mobile_number')
    ts.set_contact_detail(mobile_number='mobile_country_code', alternate_mobile_number='alternate_mobile_country_code')
    ts.set_null(blank_number=0)
    ts.set_datetime_format(date_of_joining='%d/%m/%Y', sign_in_time='%H:%M')
    ts.set_func(hello=lambda obj: 'Hello ' + obj.name, model3_id=lambda obj: ts2.get_data(obj))
    data = ts.get_data(inst, fields=['name', 'email', 'alternate_email', 'mobile_number', 'alternate_mobile_number', 'emergency_number',
                                     'blank_text', 'blank_number', 'date_of_birth', 'date_of_joining', 'task_deadline',
                                     'sign_in_time'], fk=['models4_id'], m2m=['model3_id'], ann=['hello'])
    print('=====================All in One============================')
    print(data)
    print('===========================================================')
    return render(request, 'index.html', {'data': data})






