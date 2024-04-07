# Custom Django Serializer
**Convert Django Instance and QuerySet into Python-Json Readable Format.**

**Features**
* Date: Default: 17 December, 1994
* Time: Default: 12:30:00 (24 Hour)
* DateTime: Default: 17 December, 1994 12:30 PM
* None: Default: ''
* Contact Number With Country Code: +91 9712397123
* Decrypt Data: User defined logic
* Add Path to Media Files
* Custom Functions:
* Django ORM Optimization

**Notes**

This is the base possible serializer example,   
it is programmed to take any custom logic and flexible to change as per varied requirements  

For Django ORM Optimization Follow These Rules:
1) For One level FK and M2M, care already taken by serializer
2) For deep level, set select_related and prefetch_related explicitly  
   Example: selected_related(company_branch_id__company_id), prefetch_related(team_members__designation_id)

For Custom Function Follow These Rules:
1) For Model Fields pass (obj, value) as arguments  
   where obj is model instance and value is resolved value  
   Example: lambda obj, value: obj.name + value

2) For FK and M2M pass (obj) as arguments  
   where obj is django instance of related model  
   Example: lambda obj: obj.get_full_name()
  
3) For Annotate keys pass (obj) as arguments  
   where obj is django instance of main model  
   Example: lambda obj: 'Hi ' + obj.name
