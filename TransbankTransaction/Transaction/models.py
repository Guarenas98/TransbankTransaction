from django.db import models
import uuid

# Create your models here.
class Credicard(models.Model):
    card_number =  models.CharField(max_length = 16 ,help_text = "Number of Credicard")
    name = models.CharField(max_length = 24 ,help_text = "Name Credicard")
    cvv = models.CharField(max_length =  4, help_text = "Card Security Code")
    card_expiration = models.CharField(max_length = 5, help_text = "Expiration (AA/MM)")

    status = models.ForeignKey('StatusTrans', on_delete = models.SET_NULL,
    null=True, blank = True)
    status.short_description = "When it's tried in TB"
    def __str__(self):
        """for this model look in admin suite like you set"""
        return f"{self.name} {self.card_number}"

class StatusTrans(models.Model):
    status =  models.CharField(max_length = 10)
    def __str__(self):
        return self.status
