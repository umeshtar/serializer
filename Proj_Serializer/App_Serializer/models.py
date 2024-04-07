from django.db import models


# Create your models here.
class Model2(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=1000)
    alternate_email = models.EmailField()
    mobile_country_code = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=1000)
    alternate_mobile_country_code = models.CharField(max_length=100)
    alternate_mobile_number = models.CharField(max_length=100)
    emergency_number = models.CharField(max_length=100)
    blank_text = models.CharField(max_length=100, null=True, blank=True)
    blank_number = models.SmallIntegerField(null=True, blank=True)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    task_deadline = models.DateTimeField()
    sign_in_time = models.TimeField()
    model3_id = models.ManyToManyField('Model3', blank=True)
    models4_id = models.ForeignKey('Model4', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Model3(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Model4(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name














