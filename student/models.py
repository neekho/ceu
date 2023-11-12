from django.db import models

from django.utils import timezone


import random

class StudenId(models.CharField):


    # Creating Primary keys for our student models
    # ex: 2019-20944

    def __init__(self, *args, **kwargs): 
        kwargs['max_length'] = 10 # Adjust the length as needed 
        super().__init__(*args, **kwargs) 
    
    
    def pre_save(self, model_instance, add): 
        if add and not getattr(model_instance, self.attname): 


            current_year = str(timezone.now().year)[-2:]  #2019-xxxxx
            next_year = str(int(current_year) + 1) # 2019-20xxx generates the next year of the curren year
            random_digits = str(random.randint(100, 999)) # generate the last 3 random digits 2019-20944
            primary_key_value = f"{current_year}-{next_year}{random_digits}" 
            setattr(model_instance, self.attname, primary_key_value) 
            
        
        return super().pre_save(model_instance, add) 



# Create your models here.
class Student(models.Model):

    id = StudenId(primary_key=True, editable=False)

    creator = models.ForeignKey('auth.User', related_name='student', on_delete=models.CASCADE)

    first_name = models.CharField(max_length=15, blank=False, null=False)

    last_name = models.CharField(max_length=15, blank=False, null=False)

    age = models.PositiveIntegerField(default=0)

    email = models.EmailField(unique=True, blank=True)

    course = models.CharField(max_length=6, blank=False, null=False)


    def save(self, *args, **kwargs):
         # Generate email if not provided
        if not self.email:
            self.email = f"{self.first_name.lower()}.{self.last_name.lower()}@ceu.edu.com.ph"

        super().save(*args, **kwargs)








