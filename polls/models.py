from django.db import models

# Create your models here.
class Image(models.Model):
    test_img = models.FileField(upload_to='data/test/021')
