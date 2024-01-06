from django.db import models

class Complaint(models.Model):
    name = models.TextField(max_length=256, null=False)
    phone = models.TextField(max_length=10, null=False)
    complaint = models.TextField(max_length=1024, null=False)
    ticket_id = models.TextField(max_length=10, null=False)
    ticket_status = models.BooleanField(default=False)
    complaint_date = models.DateField(auto_now_add=True)
