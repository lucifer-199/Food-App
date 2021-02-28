from django.db import models

class Food(models.Model):
    userID= models.IntegerField(default=0)
    id= models.AutoField
    title = models.CharField(max_length=500,default="")
    body= models.CharField(max_length=500,default="")

    def __str__(self):
        return self.title

