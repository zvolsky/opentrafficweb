from django.db import models

# Create your models here.

class UserUpload(models.Model):
    file = models.FileField(upload_to='userupload/files/', max_length=500)
