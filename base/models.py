from django.db import models
# from django.utils.timezone import now

import uuid
# Create your models here.
class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta: 
        abstract=True