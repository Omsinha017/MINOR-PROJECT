from django.db import models
from django.utils.timezone import now

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=254)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return 'Message from ' + self.name
    