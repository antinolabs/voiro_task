from django.db import models


#Profile models
class Profile(models.Model):    

    position_choices    =   (
        ("developer","DEVELOPER"),
        ("team lead","TEAM LEAD"),
        ("manager","MANAGER"),
        ("other","OTHER")
        )
    
    user_id     =   models.PositiveIntegerField()
    firstname    =   models.CharField(max_length=100)
    lastname    =   models.CharField(max_length=100)
    dob         =   models.DateField(null=True,blank=True)
    role        =   models.CharField(choices=position_choices,max_length=30)
    created_at  =   models.DateTimeField(auto_now_add=True) 
    updated_at  =   models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.firstname+" "+self.lastname
    

